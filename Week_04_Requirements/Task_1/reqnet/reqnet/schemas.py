"""Pydantic schemas for every structured LLM output in the network.

Each agentic node must return JSON that validates against one of these models.
Validation failures are fed back to the model (see llm.py) - a small,
per-call self-correction loop in addition to the graph-level review loop.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

ReqType = Literal["functional", "non-functional", "constraint", "documentation", "data"]
Priority = Literal["P1", "P2", "P3", "P4"]
DiscardCategory = Literal[
    "conflict",          # contradicts another (kept) requirement / later decision
    "superseded",        # replaced by a later decision
    "nonsensical",       # not meaningful for the software / off-topic chatter
    "out-of-scope",      # explicitly declared out of scope in the corpus
    "not-a-requirement", # a fact, opinion or question, not a need
    "infeasible",        # declared impossible / unacceptable by stakeholders
]


# ---------------------------------------------------------------- extraction
class Candidate(BaseModel):
    title: str = Field(description="Short descriptive name, max ~10 words")
    statement: str = Field(description="Normalized requirement: 'The system shall ...'")
    type: ReqType = "functional"
    source_quote: str = Field("", description="Short verbatim evidence from the text")
    stakeholder: str = ""
    priority_signals: str = Field("", description="Evidence of importance in the text, if any")
    status: Literal["proposed", "agreed", "rejected", "questioned"] = "proposed"
    suspicious: bool = False
    suspicious_reason: str = ""


class ExtractionResult(BaseModel):
    candidates: list[Candidate] = Field(default_factory=list)


# ------------------------------------------------------------------ taxonomy
class Area(BaseModel):
    code: str = Field(description="2-5 uppercase letters, e.g. INV")
    name: str
    description: str = ""


class Taxonomy(BaseModel):
    system_name: str = Field("", description="Short name of the software system described")
    areas: list[Area]


class Assignment(BaseModel):
    candidate_id: str
    area_code: str


class AssignmentResult(BaseModel):
    assignments: list[Assignment]


# ------------------------------------------------------------- consolidation
class DraftRequirement(BaseModel):
    name: str
    description: str = Field(description="One paragraph (3-6 sentences)")
    type: ReqType = "functional"
    priority: Priority
    priority_rationale: str = ""
    candidate_ids: list[str]


class Discard(BaseModel):
    name: str
    candidate_ids: list[str]
    category: DiscardCategory
    reason: str
    conflicts_with: list[str] = Field(default_factory=list,
        description="Names/IDs of requirements it conflicts with or is superseded by")


class AreaConsolidation(BaseModel):
    requirements: list[DraftRequirement] = Field(default_factory=list)
    discarded: list[Discard] = Field(default_factory=list)


# -------------------------------------------------------------------- review
class Issue(BaseModel):
    kind: Literal["duplicate", "conflict", "terminology", "coverage",
                  "quality", "priority", "blacklist", "traceability"]
    severity: Literal["blocking", "minor"] = "blocking"
    requirement_ids: list[str] = Field(default_factory=list)
    candidate_ids: list[str] = Field(default_factory=list)
    description: str
    suggested_fix: str = ""


class GlossaryTerm(BaseModel):
    term: str
    definition: str
    avoid: list[str] = Field(default_factory=list, description="Synonyms to replace")


class Review(BaseModel):
    approved: bool
    summary: str = ""
    issues: list[Issue] = Field(default_factory=list)
    glossary: list[GlossaryTerm] = Field(default_factory=list)


# ------------------------------------------------------------------ revision
class Operation(BaseModel):
    op: Literal["update", "merge", "discard", "add", "attach", "restore"]
    # update/discard/attach target; merge: kept requirement
    target_id: Optional[str] = None
    # merge: requirements absorbed into target_id
    merge_ids: list[str] = Field(default_factory=list)
    # attach/add: candidates to link; restore: discarded entries to bring back
    candidate_ids: list[str] = Field(default_factory=list)
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ReqType] = None
    priority: Optional[Priority] = None
    priority_rationale: Optional[str] = None
    area_code: Optional[str] = None
    category: Optional[DiscardCategory] = None
    reason: Optional[str] = None
    conflicts_with: list[str] = Field(default_factory=list)


class Revision(BaseModel):
    operations: list[Operation] = Field(default_factory=list)
    notes: str = ""
