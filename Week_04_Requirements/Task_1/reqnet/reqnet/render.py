"""Deterministic rendering of the final specification (Markdown + JSON)."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from . import prompts as P

PRIO_ORDER = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}
CAT_LABEL = {
    "conflict": "Conflict", "superseded": "Superseded", "nonsensical": "Nonsensical / off-topic",
    "out-of-scope": "Out of scope", "not-a-requirement": "Not a requirement", "infeasible": "Infeasible",
}


def _sources(req, cands):
    out = []
    for cid in req["candidate_ids"]:
        c = cands.get(cid)
        if c:
            for d in [c["doc_id"], *c["also_in"]]:
                if d not in out:
                    out.append(d)
    return sorted(out)


def _cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render(state: dict, settings, backend, output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    cands, docs = state["candidates"], {d["doc_id"]: d for d in state["docs"]}
    areas = state["areas"]
    area_name = {a["code"]: a["name"] for a in areas}

    # ---- final, gap-free IDs (REQ-<AREA>-<nnn>, ordered by priority then name) [OS2]
    reqs, idmap = [], {}
    for a in areas:
        group = sorted((r for r in state["requirements"] if r["area"] == a["code"]),
                       key=lambda r: (PRIO_ORDER[r["priority"]], r["name"].lower()))
        for n, r in enumerate(group, 1):
            new = f"REQ-{a['code']}-{n:03d}"
            idmap[r["id"]] = new
            reqs.append({**r, "id": new, "sources": _sources(r, cands)})
    discs = []
    for n, d in enumerate(state["discarded"], 1):
        new = f"DIS-{n:03d}"
        idmap[d["id"]] = new
        discs.append({**d, "id": new, "sources": _sources(d, cands)})

    id_re = re.compile(r"\b(?:REQ-[A-Z]+-\d{3}|DIS-\d{3})\b")

    def remap(text):
        return id_re.sub(lambda m: idmap.get(m.group(0), m.group(0)), text or "")

    for x in reqs + discs:
        for k in ("description", "priority_rationale", "reason"):
            if k in x:
                x[k] = remap(x[k])
        if "conflicts_with" in x:
            x["conflicts_with"] = [remap(c) for c in x["conflicts_with"]]

    rev = state.get("review") or {}
    open_issues = [i for i in rev.get("issues", [])]
    for i in open_issues:
        i["requirement_ids"] = [idmap.get(r, r) for r in i["requirement_ids"]]
        i["description"] = remap(i["description"])
    approved = rev.get("approved") and not any(i["severity"] == "blocking" for i in open_issues)
    findings = state["findings"]
    covered = findings["stats"]["covered_candidates"]
    total_c = len(cands)

    L: list[str] = []
    w = L.append
    title = state.get("system_name") or "Software System"
    w(f"# Software Requirements Specification — {title}\n")
    w(f"*Generated {date.today().isoformat()} by the ReqNet agentic network from "
      f"{len(docs)} source documents. Status: "
      f"{'approved by the reviewer agent' if approved else 'not fully approved — see §8'}.*\n")

    w("## Contents\n")
    for t in ["1. Introduction", "2. Priority Scale", "3. Source Documents", "4. Glossary",
              "5. Requirements", "6. Discarded Requirements (Blacklist)", "7. Traceability Matrix",
              "8. Quality Assurance Record"]:
        w(f"- {t}")
    w("")

    w("## 1. Introduction\n")
    w(f"This document consolidates the requirements for **{title}** stated across a corpus of "
      f"heterogeneous sources (emails, meeting minutes, interviews, surveys, draft specifications). "
      f"{total_c} candidate statements were extracted; they were deduplicated, checked for conflicts and "
      f"consolidated into **{len(reqs)} requirements** in {len(areas)} functional areas. "
      f"Discarded candidates ({len(discs)}) are recorded with a justification in §6.\n")
    w("Each requirement has a unique identifier `REQ-<AREA>-<NNN>`, a short name, a descriptive "
      "paragraph, a type, a priority (§2) and the list of source documents it was derived from "
      "(§3, §7). Requirements are ordered by priority within each area. The key word *shall* "
      "denotes a mandatory capability.\n")
    w("| Area | Name | Requirements |\n|---|---|---|")
    for a in areas:
        w(f"| {a['code']} | {_cell(a['name'])} | {sum(1 for r in reqs if r['area'] == a['code'])} |")
    w("")

    w("## 2. Priority Scale\n")
    w("| Priority | Meaning | Criteria |\n|---|---|---|")
    for code, name, desc in P.PRIORITY_SCALE:
        w(f"| **{code}** | {name} | {desc} |")
    counts = {p: sum(1 for r in reqs if r["priority"] == p) for p in PRIO_ORDER}
    w("\nDistribution: " + ", ".join(f"{p}: {n}" for p, n in counts.items()) + ".\n")

    w("## 3. Source Documents\n")
    w("| ID | File | Type | Date | Title |\n|---|---|---|---|---|")
    for d in docs.values():
        w(f"| {d['doc_id']} | `{d['path']}` | {d['kind']} | {d['date']} | {_cell(d['title'])} |")
    w("")

    w("## 4. Glossary\n")
    gl = state.get("glossary") or []
    if gl:
        w("Preferred terms used consistently throughout this document.\n")
        w("| Term | Definition | Avoid |\n|---|---|---|")
        for g in sorted(gl, key=lambda g: g["term"].lower()):
            w(f"| **{_cell(g['term'])}** | {_cell(g['definition'])} | {_cell(', '.join(g.get('avoid', [])))} |")
    else:
        w("_No glossary was produced._")
    w("")

    w("## 5. Requirements\n")
    for si, a in enumerate(areas, 1):
        group = [r for r in reqs if r["area"] == a["code"]]
        w(f"### 5.{si} {a['name']} ({a['code']})\n")
        if a.get("description"):
            w(f"_{a['description']}_\n")
        for r in group:
            w(f"#### {r['id']} — {r['name']}\n")
            src = ", ".join(f"{s} (`{docs[s]['path']}`)" for s in r["sources"]) or "—"
            w(f"- **Priority:** {r['priority']}  ·  **Type:** {r['type']}")
            w(f"- **Derived from:** {src}")
            if r.get("priority_rationale"):
                w(f"- **Priority rationale:** {r['priority_rationale']}")
            w("")
            w(r["description"].strip() + "\n")

    w("## 6. Discarded Requirements (Blacklist)\n")
    if discs:
        w("Candidate requirements identified in the sources but **not** included in the specification.\n")
        w("| ID | Candidate | Category | Reason | Conflicts with / superseded by | Sources |\n"
          "|---|---|---|---|---|---|")
        for d in discs:
            w(f"| {d['id']} | {_cell(d['name'])} | {CAT_LABEL.get(d['category'], d['category'])} | "
              f"{_cell(d['reason'])} | {_cell(', '.join(d.get('conflicts_with', [])) or '—')} | "
              f"{', '.join(d['sources']) or '—'} |")
    else:
        w("_No candidates were discarded._")
    w("")

    w("## 7. Traceability Matrix\n")
    w("Which requirements were derived from each source document.\n")
    w("| Document | Requirements | Discarded |\n|---|---|---|")
    for did, d in docs.items():
        rr = [r["id"] for r in reqs if did in r["sources"]]
        dd = [x["id"] for x in discs if did in x["sources"]]
        w(f"| {did} `{d['path']}` | {', '.join(rr) or '—'} | {', '.join(dd) or '—'} |")
    w("")

    w("## 8. Quality Assurance Record\n")
    reviews = [h for h in state["history"] if h["step"] == "review"]
    w(f"- Candidate coverage: {covered}/{total_c} extracted candidates are linked to a requirement or a discard.")
    w(f"- Review rounds: {len(reviews)} (maximum {settings.max_review_rounds}).")
    for h in reviews:
        w(f"  - Round {h['round']}: approved={h['approved']}, {h['issues']} issues "
          f"({h['blocking']} blocking) — {h.get('summary', '')}")
    if open_issues:
        w("\nIssues reported in the final review round (not all may have been resolved):\n")
        for i in open_issues:
            w(f"- [{i['severity']}/{i['kind']}] {', '.join(i['requirement_ids'])}: {i['description']}")
    unc = findings["uncovered_candidates"]
    if unc:
        w(f"\nCandidates still not linked to any requirement ({len(unc)}):\n")
        for u in unc:
            w(f"- {u['id']} ({u['source_doc']}): {u['statement']}")
    w("")

    (out / "requirements.md").write_text("\n".join(L), encoding="utf-8")
    (out / "requirements.json").write_text(json.dumps({
        "system_name": title, "generated": date.today().isoformat(),
        "priority_scale": [{"code": c, "name": n, "criteria": d} for c, n, d in P.PRIORITY_SCALE],
        "documents": [{k: d[k] for k in ("doc_id", "path", "kind", "date", "title")} for d in docs.values()],
        "areas": areas, "glossary": gl,
        "requirements": [{k: r.get(k) for k in ("id", "area", "name", "type", "priority", "priority_rationale",
                                                 "description", "sources", "candidate_ids")} for r in reqs],
        "discarded": [{k: d.get(k) for k in ("id", "name", "category", "reason", "conflicts_with",
                                              "sources", "candidate_ids")} for d in discs],
        "candidates": list(cands.values()),
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / "run_log.json").write_text(json.dumps({
        "models": settings.models, "max_review_rounds": settings.max_review_rounds,
        "usage": backend.usage.by_model, "history": state["history"],
        "final_review": rev, "final_findings": {k: v for k, v in findings.items()},
    }, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
