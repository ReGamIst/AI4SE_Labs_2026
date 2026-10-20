"""Small deterministic text helpers (no AI)."""
from __future__ import annotations

import re

STOP = set("""a an the and or of to for in on at by with from as is are be been being this that these
those it its shall should must will would can could may might system user users staff ability able allow
allows allowing provide provides providing support supports via per each all any into than then also
such other more most not no only so we our they their there which who what when where how has have had
do does need needs needed want wants report reports""".split())


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    out = set()
    for w in words:
        if w in STOP or len(w) < 3:
            continue
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.add(w)
    return out


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def norm_key(text: str) -> str:
    return " ".join(sorted(tokens(text)))


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text or ""))
