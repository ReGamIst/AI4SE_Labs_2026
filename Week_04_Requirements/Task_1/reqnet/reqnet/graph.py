"""LangGraph agentic network for requirements refinement.

    load_corpus ─▶ extract (×chunks, LLM A) ─▶ normalize ─▶ organize (LLM B)
        ─▶ consolidate (×areas, LLM C) ─▶ integrate ─▶ check ─▶ review (LLM D)
                                                        ▲           │
                                                        │      approved / max rounds?
                                         apply_revision ◀─ revise (LLM C)   │ yes
                                                                            ▼
                                                                         render
Deterministic nodes: load_corpus, normalize, integrate, check, apply_revision, render.
Agentic nodes:       extract, organize, consolidate, review, revise.
"""
from __future__ import annotations

import logging
import operator
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Annotated, Any, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from . import prompts as P
from .corpus import chunk_document, load_corpus
from .llm import BaseBackend, make_user_message
from .schemas import (AreaConsolidation, AssignmentResult, ExtractionResult, Review,
                      Revision, Taxonomy)
from .textutil import jaccard, norm_key, tokens, word_count

log = logging.getLogger("reqnet")


# =============================================================== configuration
@dataclass
class Settings:
    models: dict[str, str] = field(default_factory=lambda: {
        "extractor": "gpt-5-mini",       # many parallel calls -> cheap, solid model
        "organizer": "gpt-5.4-nano",     # simple classification -> smallest model
        "consolidator": "gpt-6-luna",    # hardest reasoning: dedup + conflicts + writing
        "reviewer": "gpt-5.6-luna",      # independent model family member as critic
        "reviser": "gpt-6-luna",
    })
    max_review_rounds: int = 3
    chunk_chars: int = 9000
    min_areas: int = 6
    max_areas: int = 14
    assign_batch: int = 120
    max_area_candidates: int = 70
    near_dup_threshold: float = 0.5
    min_description_words: int = 30


def _rt(config: RunnableConfig) -> tuple[BaseBackend, Settings]:
    c = config["configurable"]
    return c["backend"], c["settings"]


# ======================================================================= state
class State(TypedDict, total=False):
    input_dir: str
    docs: list[dict]
    chunks: list[dict]
    raw_candidates: Annotated[list[dict], operator.add]
    candidates: dict[str, dict]
    system_name: str
    areas: list[dict]
    assignment: dict[str, str]
    area_results: Annotated[list[dict], operator.add]
    requirements: list[dict]
    discarded: list[dict]
    findings: dict
    review: dict
    glossary: list[dict]
    round: int
    history: Annotated[list[dict], operator.add]


def _doc_meta(doc: dict) -> dict:
    return {k: doc[k] for k in ("doc_id", "path", "title", "kind", "date")}


# ============================================================ 1. load (determ.)
def load_node(state: State, config: RunnableConfig) -> dict:
    _, s = _rt(config)
    docs = load_corpus(state["input_dir"])
    chunks = [c for d in docs for c in chunk_document(d, s.chunk_chars)]
    log.info("loaded %d documents -> %d chunks", len(docs), len(chunks))
    return {"docs": docs, "chunks": chunks, "round": 0,
            "history": [{"step": "load", "documents": len(docs), "chunks": len(chunks)}]}


def fan_out_extract(state: State) -> list[Send]:
    meta = {d["doc_id"]: _doc_meta(d) for d in state["docs"]}
    return [Send("extract", {"chunk": c, "doc": meta[c["doc_id"]]}) for c in state["chunks"]]


# ========================================================== 2. extract (LLM A)
def extract_node(payload: dict, config: RunnableConfig) -> dict:
    backend, s = _rt(config)
    chunk, doc = payload["chunk"], payload["doc"]
    user = make_user_message(P.EXTRACTOR_TASK, {
        "document": doc, "chunk_part": chunk["part"], "text": chunk["text"]})
    res = backend.call_json(s.models["extractor"], P.EXTRACTOR_SYSTEM, user,
                            ExtractionResult, tag=f"extract {chunk['chunk_id']}")
    out = []
    for c in res.candidates:
        d = c.model_dump()
        d.update(doc_id=doc["doc_id"], chunk_id=chunk["chunk_id"])
        out.append(d)
    log.info("extract %s -> %d candidates", chunk["chunk_id"], len(out))
    return {"raw_candidates": out}


# ===================================================== 3. normalize (determ.)
def normalize_node(state: State) -> dict:
    """Assign stable candidate ids and fold verbatim/near-verbatim duplicates
    (typically produced by overlapping chunks). Folded duplicates keep their
    document reference in `also_in`, so tracing is not lost [OS4]."""
    raw = sorted(state["raw_candidates"], key=lambda c: (c["chunk_id"], c["title"]))
    cands: dict[str, dict] = {}
    keys: list[tuple[str, set, str]] = []  # (key, tokens, cid)
    folded = 0
    for c in raw:
        if not c.get("statement", "").strip():
            continue
        toks = tokens(c["statement"] + " " + c["title"])
        k = norm_key(c["statement"])
        hit = None
        for k2, t2, cid2 in keys:
            if k == k2 or jaccard(toks, t2) >= 0.9:
                hit = cid2
                break
        if hit:
            folded += 1
            tgt = cands[hit]
            if c["doc_id"] != tgt["doc_id"] and c["doc_id"] not in tgt["also_in"]:
                tgt["also_in"].append(c["doc_id"])
            if c.get("priority_signals") and c["priority_signals"] not in tgt["priority_signals"]:
                tgt["priority_signals"] = (tgt["priority_signals"] + "; " + c["priority_signals"]).strip("; ")
            continue
        cid = f"C-{len(cands) + 1:03d}"
        cands[cid] = {**c, "id": cid, "also_in": []}
        keys.append((k, toks, cid))
    log.info("normalize: %d raw -> %d candidates (%d folded)", len(raw), len(cands), folded)
    return {"candidates": cands,
            "history": [{"step": "normalize", "raw": len(raw), "candidates": len(cands), "folded": folded}]}


# ========================================================= 4. organize (LLM B)
def organize_node(state: State, config: RunnableConfig) -> dict:
    backend, s = _rt(config)
    cands = state["candidates"]
    titles = [{"id": cid, "title": c["title"], "type": c["type"]} for cid, c in cands.items()]
    # scale the number of areas with the backlog size (small corpora -> few areas)
    min_a = max(1, min(s.min_areas, len(cands) // 10))
    max_a = max(min_a, min(s.max_areas, max(1, len(cands) // 4)))
    system = P.TAXONOMY_SYSTEM.format(min_areas=min_a, max_areas=max_a)
    tax = backend.call_json(s.models["organizer"], system,
                            make_user_message(P.TAXONOMY_TASK, {"candidates": titles}),
                            Taxonomy, tag="taxonomy")
    areas, seen = [], set()
    for a in tax.areas:
        code = re.sub(r"[^A-Z]", "", a.code.upper())[:5] or "GEN"
        while code in seen:
            code += "X"
        seen.add(code)
        areas.append({"code": code, "name": a.name, "description": a.description})
    codes = {a["code"] for a in areas}
    area_brief = [{"code": a["code"], "name": a["name"], "description": a["description"]} for a in areas]

    batches = [titles[i:i + s.assign_batch] for i in range(0, len(titles), s.assign_batch)]

    def assign(batch):
        items = [{"id": t["id"], "title": t["title"], "statement": cands[t["id"]]["statement"]} for t in batch]
        return backend.call_json(s.models["organizer"], P.ASSIGN_SYSTEM,
                                 make_user_message(P.ASSIGN_TASK, {"areas": area_brief, "candidates": items}),
                                 AssignmentResult, tag="assign")

    assignment: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        for res in ex.map(assign, batches):
            for a in res.assignments:
                code = a.area_code.strip().upper()
                if a.candidate_id in cands and code in codes:
                    assignment[a.candidate_id] = code

    # deterministic fallback for anything the small model skipped/hallucinated
    area_tok = {a["code"]: tokens(a["name"] + " " + a["description"]) for a in areas}
    fallback = 0
    for cid, c in cands.items():
        if cid not in assignment:
            ct = tokens(c["title"] + " " + c["statement"])
            assignment[cid] = max(area_tok, key=lambda k: len(ct & area_tok[k]))
            fallback += 1
    sizes = {a["code"]: sum(1 for v in assignment.values() if v == a["code"]) for a in areas}
    areas = [a for a in areas if sizes[a["code"]]]
    log.info("organize: %d areas %s (fallback assignments: %d)", len(areas), sizes, fallback)
    return {"areas": areas, "assignment": assignment, "system_name": tax.system_name,
            "history": [{"step": "organize", "areas": sizes, "fallback_assignments": fallback}]}


def fan_out_consolidate(state: State, config: RunnableConfig) -> list[Send]:
    _, s = _rt(config)
    docs = {d["doc_id"]: d for d in state["docs"]}
    sends = []
    for area in state["areas"]:
        ids = sorted((cid for cid, a in state["assignment"].items() if a == area["code"]),
                     key=lambda cid: state["candidates"][cid]["title"].lower())
        parts = [ids[i:i + s.max_area_candidates] for i in range(0, len(ids), s.max_area_candidates)]
        for pi, part in enumerate(parts):
            items = []
            for cid in part:
                c = state["candidates"][cid]
                d = docs[c["doc_id"]]
                items.append({
                    "id": cid, "title": c["title"], "statement": c["statement"], "type": c["type"],
                    "source_doc": c["doc_id"], "source_kind": d["kind"], "source_date": d["date"],
                    "also_in": c["also_in"], "quote": c.get("source_quote", ""),
                    "stakeholder": c.get("stakeholder", ""),
                    "priority_signals": c.get("priority_signals", ""), "status": c["status"],
                    "suspicious": c["suspicious"], "suspicious_reason": c.get("suspicious_reason", ""),
                })
            sends.append(Send("consolidate", {"area": area, "part": f"{pi + 1}/{len(parts)}",
                                              "candidates": items}))
    return sends


# ====================================================== 5. consolidate (LLM C)
def consolidate_node(payload: dict, config: RunnableConfig) -> dict:
    backend, s = _rt(config)
    area = payload["area"]
    system = P.CONSOLIDATOR_SYSTEM.format(priority_scale=P.PRIORITY_TEXT)
    user = make_user_message(P.CONSOLIDATOR_TASK.format(area_code=area["code"], area_name=area["name"]),
                             {"area": area, "candidates": payload["candidates"]})
    res = backend.call_json(s.models["consolidator"], system, user, AreaConsolidation,
                            tag=f"consolidate {area['code']} {payload['part']}")
    valid = {c["id"] for c in payload["candidates"]}
    reqs = []
    for r in res.requirements:
        d = r.model_dump()
        d["candidate_ids"] = [c for c in d["candidate_ids"] if c in valid]
        reqs.append(d)
    discs = []
    for x in res.discarded:
        d = x.model_dump()
        d["candidate_ids"] = [c for c in d["candidate_ids"] if c in valid]
        discs.append(d)
    log.info("consolidate %s %s: %d candidates -> %d requirements, %d discarded",
             area["code"], payload["part"], len(valid), len(reqs), len(discs))
    return {"area_results": [{"area": area["code"], "requirements": reqs, "discarded": discs}]}


# ===================================================== 6. integrate (determ.)
def _next_req_id(reqs: list[dict], area: str) -> str:
    nums = [int(r["id"].rsplit("-", 1)[1]) for r in reqs if r["area"] == area]
    return f"REQ-{area}-{(max(nums) if nums else 0) + 1:03d}"


def _next_disc_id(discs: list[dict]) -> str:
    nums = [int(d["id"].rsplit("-", 1)[1]) for d in discs]
    return f"DIS-{(max(nums) if nums else 0) + 1:03d}"


def integrate_node(state: State) -> dict:
    reqs, discs = [], []
    for res in sorted(state["area_results"], key=lambda r: r["area"]):
        for r in res["requirements"]:
            reqs.append({**r, "id": _next_req_id(reqs, res["area"]), "area": res["area"]})
        for x in res["discarded"]:
            discs.append({**x, "id": _next_disc_id(discs), "area": res["area"]})
    log.info("integrate: %d requirements, %d discarded", len(reqs), len(discs))
    return {"requirements": reqs, "discarded": discs,
            "history": [{"step": "integrate", "requirements": len(reqs), "discarded": len(discs)}]}


# ========================================================= 7. check (determ.)
def check_node(state: State, config: RunnableConfig) -> dict:
    """Deterministic quality gate: coverage, traceability, near-duplicates,
    description length, glossary violations. Feeds the reviewer."""
    _, s = _rt(config)
    reqs, discs, cands = state["requirements"], state["discarded"], state["candidates"]
    used: dict[str, list[str]] = {}
    for r in reqs:
        for c in r["candidate_ids"]:
            used.setdefault(c, []).append(r["id"])
    for d in discs:
        for c in d["candidate_ids"]:
            used.setdefault(c, []).append(d["id"])

    uncovered = [{"id": cid, "title": c["title"], "statement": c["statement"],
                  "area": state["assignment"].get(cid), "source_doc": c["doc_id"]}
                 for cid, c in cands.items() if cid not in used]
    untraced = [r["id"] for r in reqs if not r["candidate_ids"]]
    short = [r["id"] for r in reqs if word_count(r["description"]) < s.min_description_words]
    long_names = [r["id"] for r in reqs if word_count(r["name"]) > 10]

    toks = {r["id"]: tokens(r["name"] + " " + r["description"]) for r in reqs}
    pairs = []
    for i, a in enumerate(reqs):
        for b in reqs[i + 1:]:
            j = jaccard(toks[a["id"]], toks[b["id"]])
            if j >= s.near_dup_threshold:
                pairs.append((round(j, 2), a["id"], b["id"]))
    pairs.sort(reverse=True)

    term_violations = []
    for g in state.get("glossary") or []:
        for bad in g.get("avoid", []):
            pat = re.compile(rf"\b{re.escape(bad)}\b", re.I)
            hits = [r["id"] for r in reqs if pat.search(r["name"] + " " + r["description"])]
            if hits:
                term_violations.append({"use": g["term"], "instead_of": bad, "requirements": hits[:20]})

    findings = {
        "uncovered_candidates": uncovered,
        "requirements_without_sources": untraced,
        "near_duplicate_pairs": [{"similarity": j, "a": a, "b": b} for j, a, b in pairs[:25]],
        "too_short_descriptions": short,
        "too_long_names": long_names,
        "terminology_violations": term_violations,
        "stats": {"requirements": len(reqs), "discarded": len(discs), "candidates": len(cands),
                  "covered_candidates": len(cands) - len(uncovered)},
    }
    log.info("check: %d uncovered, %d untraced, %d near-dup pairs, %d short, %d term violations",
             len(uncovered), len(untraced), len(pairs), len(short), len(term_violations))
    return {"findings": findings,
            "history": [{"step": "check", "round": state.get("round", 0), **findings["stats"],
                         "uncovered": len(uncovered), "near_dups": len(pairs)}]}


# ========================================================== 8. review (LLM D)
def review_node(state: State, config: RunnableConfig) -> dict:
    backend, s = _rt(config)
    rnd = state.get("round", 0) + 1
    docs = {d["doc_id"]: d for d in state["docs"]}
    reqs = [{"id": r["id"], "area": r["area"], "name": r["name"], "type": r["type"],
             "priority": r["priority"], "description": r["description"],
             "sources": _sources(r, state["candidates"])} for r in state["requirements"]]
    discs = [{"id": d["id"], "name": d["name"], "category": d["category"], "reason": d["reason"],
              "candidates": d["candidate_ids"]} for d in state["discarded"]]
    payload = {
        "priority_scale": P.PRIORITY_TEXT,
        "documents": [{k: d[k] for k in ("doc_id", "kind", "date", "title")} for d in docs.values()],
        "requirements": reqs, "discarded": discs,
        "automatic_findings": {k: v for k, v in state["findings"].items() if k != "stats"},
        "previous_glossary": state.get("glossary") or [],
    }
    rev = backend.call_json(s.models["reviewer"], P.REVIEWER_SYSTEM,
                            make_user_message(P.REVIEWER_TASK.format(round=rnd), payload),
                            Review, tag=f"review {rnd}")
    blocking = sum(1 for i in rev.issues if i.severity == "blocking")
    log.info("review %d: approved=%s, %d issues (%d blocking)", rnd, rev.approved, len(rev.issues), blocking)
    glossary = [g.model_dump() for g in rev.glossary] or state.get("glossary") or []
    return {"review": rev.model_dump(), "glossary": glossary, "round": rnd,
            "history": [{"step": "review", "round": rnd, "approved": rev.approved,
                         "issues": len(rev.issues), "blocking": blocking,
                         "kinds": sorted({i.kind for i in rev.issues}), "summary": rev.summary}]}


def route_after_review(state: State, config: RunnableConfig) -> str:
    _, s = _rt(config)
    rev = state["review"]
    blocking = [i for i in rev["issues"] if i["severity"] == "blocking"]
    uncovered = state["findings"]["uncovered_candidates"]
    if (rev["approved"] and not blocking and not uncovered) or state["round"] >= s.max_review_rounds:
        return "render"
    return "revise"


# ========================================================== 9. revise (LLM C)
def revise_node(state: State, config: RunnableConfig) -> dict:
    backend, s = _rt(config)
    rev = state["review"]
    reqs = {r["id"]: r for r in state["requirements"]}
    discs = {d["id"]: d for d in state["discarded"]}
    ref_ids = {x for i in rev["issues"] for x in i["requirement_ids"]}
    # include near-duplicate partners and requirements in conflict so the reviser has context
    for p in state["findings"]["near_duplicate_pairs"]:
        if p["a"] in ref_ids or p["b"] in ref_ids:
            ref_ids |= {p["a"], p["b"]}
    affected = [{k: reqs[i][k] for k in ("id", "area", "name", "type", "priority", "priority_rationale",
                                          "description", "candidate_ids")} for i in sorted(ref_ids) if i in reqs]
    affected_discards = [discs[i] for i in sorted(ref_ids) if i in discs]
    ref_cands = {c for i in rev["issues"] for c in i["candidate_ids"]}
    ref_cands |= {u["id"] for u in state["findings"]["uncovered_candidates"]}
    cands = [{"id": c, "title": state["candidates"][c]["title"], "statement": state["candidates"][c]["statement"],
              "source_doc": state["candidates"][c]["doc_id"], "area": state["assignment"].get(c),
              "priority_signals": state["candidates"][c].get("priority_signals", "")}
             for c in sorted(ref_cands) if c in state["candidates"]]
    payload = {
        "issues": [i for i in rev["issues"]],
        "glossary": state.get("glossary") or [],
        "areas": [{"code": a["code"], "name": a["name"]} for a in state["areas"]],
        "affected_requirements": affected,
        "affected_discards": affected_discards,
        "candidates_to_place": cands,
        "requirement_index": [{"id": r["id"], "name": r["name"]} for r in state["requirements"]],
    }
    system = P.REVISER_SYSTEM.format(priority_scale=P.PRIORITY_TEXT)
    res = backend.call_json(s.models["reviser"], system,
                            make_user_message(P.REVISER_TASK.format(round=state["round"]), payload),
                            Revision, tag=f"revise {state['round']}")
    log.info("revise %d: %d operations", state["round"], len(res.operations))
    return {"review": {**rev, "operations": [o.model_dump() for o in res.operations]}}


# =============================================== 10. apply revision (determ.)
def apply_revision_node(state: State) -> dict:
    reqs = [dict(r) for r in state["requirements"]]
    discs = [dict(d) for d in state["discarded"]]
    area_codes = {a["code"] for a in state["areas"]}
    cand_ids = set(state["candidates"])
    byid = lambda rid: next((r for r in reqs if r["id"] == rid), None)  # noqa: E731
    applied, rejected = [], []

    for o in state["review"].get("operations", []):
        op = o["op"]
        try:
            if op == "update":
                r = byid(o["target_id"])
                assert r, f"unknown requirement {o['target_id']}"
                for k in ("name", "description", "type", "priority", "priority_rationale"):
                    if o.get(k):
                        r[k] = o[k]
            elif op == "merge":
                r = byid(o["target_id"])
                assert r, f"unknown requirement {o['target_id']}"
                for mid in o["merge_ids"]:
                    m = byid(mid)
                    if m and m is not r:
                        r["candidate_ids"] = sorted(set(r["candidate_ids"]) | set(m["candidate_ids"]))
                        r.setdefault("merged_ids", []).append(mid)
                        reqs.remove(m)
                for k in ("name", "description", "priority", "priority_rationale", "type"):
                    if o.get(k):
                        r[k] = o[k]
            elif op == "discard":
                r = byid(o["target_id"])
                assert r, f"unknown requirement {o['target_id']}"
                reqs.remove(r)
                discs.append({"id": _next_disc_id(discs), "area": r["area"], "name": r["name"],
                              "candidate_ids": r["candidate_ids"], "category": o.get("category") or "conflict",
                              "reason": o.get("reason") or "Discarded during review.",
                              "conflicts_with": o.get("conflicts_with", []), "former_id": r["id"]})
            elif op == "add":
                area = o.get("area_code") if o.get("area_code") in area_codes else \
                    state["assignment"].get(next(iter(o["candidate_ids"]), ""), sorted(area_codes)[0])
                assert o.get("name") and o.get("description") and o.get("priority"), "add needs name/description/priority"
                reqs.append({"id": _next_req_id(reqs, area), "area": area, "name": o["name"],
                             "description": o["description"], "type": o.get("type") or "functional",
                             "priority": o["priority"], "priority_rationale": o.get("priority_rationale") or "",
                             "candidate_ids": [c for c in o["candidate_ids"] if c in cand_ids]})
            elif op == "attach":
                r = byid(o["target_id"])
                assert r, f"unknown requirement {o['target_id']}"
                r["candidate_ids"] = sorted(set(r["candidate_ids"]) | {c for c in o["candidate_ids"] if c in cand_ids})
            elif op == "restore":
                d = next((x for x in discs if x["id"] == o["target_id"]), None)
                assert d, f"unknown discard {o['target_id']}"
                discs.remove(d)
                area = o.get("area_code") if o.get("area_code") in area_codes else d["area"]
                reqs.append({"id": _next_req_id(reqs, area), "area": area, "name": o.get("name") or d["name"],
                             "description": o.get("description") or d["reason"], "type": o.get("type") or "functional",
                             "priority": o.get("priority") or "P3", "priority_rationale": o.get("priority_rationale") or "",
                             "candidate_ids": d["candidate_ids"]})
            applied.append(op)
        except (AssertionError, KeyError, StopIteration) as e:
            rejected.append({"op": op, "target": o.get("target_id"), "error": str(e)})
    reqs.sort(key=lambda r: (r["area"], int(r["id"].rsplit("-", 1)[1])))
    log.info("apply_revision: %d applied, %d rejected", len(applied), len(rejected))
    return {"requirements": reqs, "discarded": discs,
            "history": [{"step": "apply_revision", "round": state["round"], "applied": len(applied),
                         "by_op": {k: applied.count(k) for k in sorted(set(applied))}, "rejected": rejected}]}


# ============================================================ helpers/render
def _sources(req: dict, cands: dict) -> list[str]:
    out = []
    for cid in req["candidate_ids"]:
        c = cands.get(cid)
        if not c:
            continue
        for d in [c["doc_id"], *c["also_in"]]:
            if d not in out:
                out.append(d)
    return sorted(out)


def render_node(state: State, config: RunnableConfig) -> dict:
    from .render import render
    c = config["configurable"]
    render(state, c["settings"], c["backend"], c["output_dir"])
    return {"history": [{"step": "render"}]}


# ================================================================ graph build
def build_graph(settings: Settings):
    g = StateGraph(State)
    g.add_node("load_corpus", load_node)
    g.add_node("extract", extract_node)
    g.add_node("normalize", normalize_node)
    g.add_node("organize", organize_node)
    g.add_node("consolidate", consolidate_node)
    g.add_node("integrate", integrate_node)
    g.add_node("check", check_node)
    g.add_node("review", review_node)
    g.add_node("revise", revise_node)
    g.add_node("apply_revision", apply_revision_node)
    g.add_node("render", render_node)

    g.add_edge(START, "load_corpus")
    g.add_conditional_edges("load_corpus", fan_out_extract, ["extract"])
    g.add_edge("extract", "normalize")
    g.add_edge("normalize", "organize")
    g.add_conditional_edges("organize", fan_out_consolidate, ["consolidate"])
    g.add_edge("consolidate", "integrate")
    g.add_edge("integrate", "check")
    g.add_edge("check", "review")
    g.add_conditional_edges("review", route_after_review, {"revise": "revise", "render": "render"})
    g.add_edge("revise", "apply_revision")
    g.add_edge("apply_revision", "check")
    g.add_edge("render", END)
    return g.compile()


def run(input_dir: str, output_dir: str, backend: BaseBackend, settings: Settings,
        max_concurrency: int = 8) -> dict[str, Any]:
    graph = build_graph(settings)
    return graph.invoke({"input_dir": input_dir},
                        config={"configurable": {"backend": backend, "settings": settings,
                                                 "output_dir": output_dir},
                                "max_concurrency": max_concurrency, "recursion_limit": 100})
