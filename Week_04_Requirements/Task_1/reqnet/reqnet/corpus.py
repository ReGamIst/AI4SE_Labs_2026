"""Deterministic corpus loading and chunking (no AI)."""
from __future__ import annotations

import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

TEXT_SUFFIXES = {".txt", ".md", ".eml", ".text", ".rst", ".csv", ".json", ".html", ".htm", ""}

KIND_RULES = [
    (r"minutes", "meeting minutes"),
    (r"meeting", "meeting notes"),
    (r"interview", "stakeholder interview"),
    (r"survey", "survey results"),
    (r"srs|specification|requirements", "draft specification"),
    (r"reference|manual|guide", "reference document"),
]

DATE_PATTERNS = [
    (r"(\d{4})-(\d{2})-(\d{2})", lambda m: datetime(int(m[1]), int(m[2]), int(m[3]))),
    (r"(January|February|March|April|May|June|July|August|September|October|November|December)"
     r"\s+(\d{1,2}),\s+(\d{4})", lambda m: datetime.strptime(f"{m[1]} {m[2]} {m[3]}", "%B %d %Y")),
]


def _read(path: Path) -> str:
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def _guess_kind(rel: str, text: str) -> str:
    if rel.lower().endswith(".eml") or re.match(r"(from|to|subject):", text[:200], re.I):
        return "email thread"
    for probe in (rel.lower(), text[:400].lower()):   # file name is the stronger signal
        for pattern, kind in KIND_RULES:
            if re.search(pattern, probe, re.M):
                return kind
    return "document"


def _guess_date(rel: str, text: str) -> str:
    m = re.search(r"^Date:\s*(.+)$", text, re.M)
    if m:
        try:
            return parsedate_to_datetime(m.group(1).strip()).date().isoformat()
        except (TypeError, ValueError):
            pass
    for source in (rel, text[:3000]):
        for pat, conv in DATE_PATTERNS:
            mm = re.search(pat, source)
            if mm:
                try:
                    return conv(mm).date().isoformat()
                except ValueError:
                    continue
    return "unknown"


def _guess_title(rel: str, text: str) -> str:
    m = re.search(r"^Subject:\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    for line in text.splitlines()[:15]:
        s = line.strip(" =-#*\t")
        if len(s) > 8 and not re.match(r"^(from|to|date|cc):", s, re.I):
            return s[:120]
    return Path(rel).stem


def load_corpus(input_dir: str) -> list[dict]:
    root = Path(input_dir)
    if not root.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")
    files = sorted(p for p in root.rglob("*")
                   if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and not p.name.startswith("."))
    docs = []
    for i, p in enumerate(files, 1):
        text = _read(p).replace("\r\n", "\n").strip()
        if not text:
            continue
        rel = p.relative_to(root).as_posix()
        docs.append({
            "doc_id": f"DOC-{i:02d}",
            "path": rel,
            "title": _guess_title(rel, text),
            "kind": _guess_kind(rel, text),
            "date": _guess_date(rel, text),
            "chars": len(text),
            "text": text,
        })
    if not docs:
        raise SystemExit(f"No text documents found in {input_dir}")
    return docs


def chunk_document(doc: dict, max_chars: int = 9000, overlap_paras: int = 1) -> list[dict]:
    """Split on paragraph boundaries; consecutive chunks share `overlap_paras` paragraphs."""
    paras = [p for p in re.split(r"\n\s*\n", doc["text"]) if p.strip()]
    chunks, cur, size = [], [], 0
    for para in paras:
        if cur and size + len(para) > max_chars:
            chunks.append(cur)
            cur = cur[-overlap_paras:] if overlap_paras else []
            size = sum(len(x) for x in cur)
        cur.append(para)
        size += len(para) + 2
    if cur:
        chunks.append(cur)
    n = len(chunks)
    return [{
        "chunk_id": f"{doc['doc_id']}#{k + 1}",
        "doc_id": doc["doc_id"],
        "part": f"{k + 1}/{n}",
        "text": "\n\n".join(c),
    } for k, c in enumerate(chunks)]
