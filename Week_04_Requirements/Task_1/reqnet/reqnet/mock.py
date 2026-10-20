"""Offline stand-in for the LLMs (`--mock`).

It is NOT meant to produce a good specification. It returns schema-valid,
input-dependent outputs (keyword heuristics) so that the whole LangGraph
network - fan-out, reducers, the review/revise feedback loop, ID handling,
rendering - can be debugged without network access or API cost. It also
deliberately leaves gaps (skipped assignments, an uncovered candidate per
area) so that the deterministic fallbacks and the feedback loop are exercised.
"""
from __future__ import annotations

import json
import re

from .llm import BaseBackend, extract_payload
from .schemas import (AreaConsolidation, AssignmentResult, ExtractionResult, Review,
                      Revision, Taxonomy)
from .textutil import tokens

KEY = re.compile(r"\b(need|needs|must|shall|should|want|would like|require|ability|able to|"
                 r"report|track|allow|filter|export|count|list of)\b", re.I)
OFFTOPIC = re.compile(r"\b(cat|dog|fence|ladder|weather|birthday|vacation|garden|recipe|socks)\b", re.I)

AREAS = [
    ("REP", "Report Creation and Scheduling", "report template output schedul format query filter"),
    ("INV", "Inventory and Item Management", "item inventory shelf transfer missing transit purge weed collection material volume"),
    ("PAT", "Patron Records", "patron borrower demographic inactive account card"),
    ("TRX", "Transactions and Circulation", "transaction circulation checkout checkin hold renewal"),
    ("FIN", "Financial Records", "fine fee payment financial money budget"),
    ("NFR", "Platform, Security and Constraints", "database html server role permission security login performance opac environment"),
    ("DOC", "Documentation and Help", "documentation help training manual error data dictionary"),
]


def _area_for(text: str) -> str:
    t = tokens(text)
    best, score = "REP", 0
    for code, _, kw in AREAS:
        s = len(t & tokens(kw))
        if s > score:
            best, score = code, s
    return best


class MockBackend(BaseBackend):
    def _complete(self, model, messages, schema):
        p = extract_payload(messages[1]["content"])
        fn = {ExtractionResult: self._extract, Taxonomy: self._taxonomy,
              AssignmentResult: self._assign, AreaConsolidation: self._consolidate,
              Review: self._review, Revision: self._revise}[schema]
        out = fn(p)
        return json.dumps(out), len(messages[1]["content"]) // 4, len(json.dumps(out)) // 4

    # ------------------------------------------------------------------
    def _extract(self, p):
        cands = []
        lines = re.split(r"(?<=[.!?])\s+|\n\s*[-*\d.)]+\s+|\n{2,}", p["text"])
        for ln in lines:
            ln = " ".join(ln.split())
            if len(ln) < 30 or len(ln) > 400 or not KEY.search(ln) or re.match(r"(From|To|Date|Subject):", ln):
                continue
            words = re.findall(r"[A-Za-z0-9']+", ln)
            cands.append({
                "title": " ".join(words[:7]).title(),
                "statement": "The system shall support the following need: " + ln,
                "type": "constraint" if re.search(r"must|database|server|html", ln, re.I) else "functional",
                "source_quote": ln[:150],
                "priority_signals": "[*] marker" if "[*]" in ln else "",
                "status": "rejected" if re.search(r"\breject", ln, re.I) else "proposed",
                "suspicious": bool(OFFTOPIC.search(ln)),
                "suspicious_reason": "personal chatter" if OFFTOPIC.search(ln) else "",
            })
        return {"candidates": cands[:40]}

    def _taxonomy(self, p):
        return {"system_name": "Integrated Library System – Management Reporting (mock)",
                "areas": [{"code": c, "name": n, "description": "Covers: " + kw} for c, n, kw in AREAS]}

    def _assign(self, p):
        out = []
        for i, c in enumerate(p["candidates"]):
            if i % 37 == 5:      # deliberately skip some -> exercises deterministic fallback
                continue
            out.append({"candidate_id": c["id"], "area_code": _area_for(c["title"] + " " + c["statement"])})
        return {"assignments": out}

    def _consolidate(self, p):
        groups: dict[str, list] = {}
        items = p["candidates"]
        if len(items) > 5:
            items = items[:-1]   # deliberately leave one uncovered -> exercises coverage loop
        reqs, discs = [], []
        for c in items:
            if c["suspicious"] or c["status"] == "rejected":
                discs.append({"name": c["title"], "candidate_ids": [c["id"]],
                              "category": "nonsensical" if c["suspicious"] else "out-of-scope",
                              "reason": c["suspicious_reason"] or "Rejected in the source discussion."})
                continue
            key = " ".join(sorted(tokens(c["title"]))[:3])
            groups.setdefault(key, []).append(c)
        for key, cs in groups.items():
            text = " ".join(c["statement"].replace("The system shall support the following need: ", "")
                            for c in cs[:3])
            reqs.append({
                "name": cs[0]["title"][:60],
                "description": "The system shall provide this capability. " + text[:600],
                "type": cs[0]["type"],
                "priority": "P1" if any("[*]" in c["priority_signals"] for c in cs) else
                            ("P2" if len(cs) > 1 else "P3"),
                "priority_rationale": f"{len(cs)} supporting candidate(s).",
                "candidate_ids": [c["id"] for c in cs],
            })
        return {"requirements": reqs, "discarded": discs}

    def _review(self, p):
        f = p["automatic_findings"]
        issues = []
        for u in f["uncovered_candidates"]:
            issues.append({"kind": "coverage", "candidate_ids": [u["id"]],
                           "description": f"Candidate {u['id']} is not covered.", "suggested_fix": "attach or add"})
        for d in f["near_duplicate_pairs"][:3]:
            issues.append({"kind": "duplicate", "requirement_ids": [d["a"], d["b"]],
                           "description": f"{d['a']} and {d['b']} look like duplicates."})
        for r in f["too_short_descriptions"][:5]:
            issues.append({"kind": "quality", "severity": "minor", "requirement_ids": [r],
                           "description": "Description too short."})
        blocking = [i for i in issues if i.get("severity", "blocking") == "blocking"]
        return {"approved": not blocking, "summary": f"mock review: {len(issues)} issues",
                "issues": issues,
                "glossary": [{"term": "patron", "definition": "A registered library user.",
                              "avoid": ["borrower"]},
                             {"term": "item", "definition": "A physical copy of a title.",
                              "avoid": ["copy"]}]}

    def _revise(self, p):
        ops, merged = [], set()
        index = [r["id"] for r in p["requirement_index"]]
        for i in p["issues"]:
            if i["kind"] == "duplicate" and len(i["requirement_ids"]) == 2:
                a, b = i["requirement_ids"]
                if a in merged or b in merged:
                    continue
                merged |= {a, b}
                ops.append({"op": "merge", "target_id": a, "merge_ids": [b]})
            elif i["kind"] == "quality" and i["requirement_ids"]:
                ops.append({"op": "update", "target_id": i["requirement_ids"][0],
                            "description": "The system shall provide this capability to authorized staff "
                                           "so that they can perform the described task efficiently and "
                                           "consistently across all branches, with results that can be "
                                           "viewed on screen and exported for further processing."})
        for c in p["candidates_to_place"]:
            same = [r for r in index if r.startswith(f"REQ-{c['area']}-") and r not in merged]
            if same:
                ops.append({"op": "attach", "target_id": same[0], "candidate_ids": [c["id"]]})
            else:
                ops.append({"op": "add", "area_code": c["area"], "candidate_ids": [c["id"]],
                            "name": c["title"][:60], "description": c["statement"], "priority": "P3"})
        ops.append({"op": "update", "target_id": "REQ-NOPE-999", "name": "x"})  # exercises rejection path
        return {"operations": ops, "notes": "mock revision"}
