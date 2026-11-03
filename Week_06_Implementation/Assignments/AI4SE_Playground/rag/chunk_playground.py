#!/usr/bin/env python3
"""Split the files in ../playground into chunks for a RAG tool.

Python files are split along syntax boundaries (functions, classes, methods),
and other text files along blank lines. Source files are only parsed, never
imported or run. See chunking_design.md for the reasoning.

Usage, from anywhere (standard library only, Python 3.8+):

    python chunk_playground.py

Reads:  <repository>/playground/
Writes: <repository>/rag/playground_chunks.json
"""

from __future__ import annotations

import argparse
import ast
import json
import statistics
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

MAX_CHARS = 1200

RAG_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = RAG_DIR.parent / "playground"
DEFAULT_OUTPUT = RAG_DIR / "playground_chunks.json"

# Generated folders that can appear after running tests or creating a venv.
SKIP_DIRS = {
    ".git", ".idea", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    ".venv", ".vscode", "__pycache__", "build", "dist", "node_modules", "venv",
}


@dataclass
class Chunk:
    """One retrievable piece of a file. Line numbers are 1-based and inclusive."""

    id: str  # "<path>:<start_line>-<end_line>"
    path: str  # repository-relative, always with forward slashes
    start_line: int
    end_line: int
    kind: str  # module | function | function_part | class | class_part | text
    role: str  # source | test
    symbols: List[str]  # definitions in this chunk, e.g. ["Warehouse.add"]
    context: str  # location header to prepend when embedding or prompting
    text: str  # the exact source lines


@dataclass
class Span:
    """A range of lines that is a candidate for (part of) a chunk."""

    start: int
    end: int
    kind: str
    symbols: List[str]
    context: str = ""


def slice_text(lines: Sequence[str], start: int, end: int) -> str:
    return "\n".join(lines[start - 1:end])


def fits(lines: Sequence[str], start: int, end: int, max_chars: int) -> bool:
    return len(slice_text(lines, start, end)) <= max_chars


def node_start(node: ast.AST, lines: Sequence[str]) -> int:
    """Return a node's first line, including decorators and comments above it."""
    decorators = getattr(node, "decorator_list", [])
    start = min([node.lineno] + [d.lineno for d in decorators])
    indent = " " * node.col_offset
    while start > 1:
        previous = lines[start - 2]
        if previous.startswith(indent + "#"):
            start -= 1
        else:
            break
    return start


def partition(
    nodes: Sequence[ast.AST], lines: Sequence[str], first: int, last: int
) -> List[Tuple[int, int, ast.AST]]:
    """Divide lines first..last among nodes, so that no line is left out."""
    starts: List[Tuple[int, ast.AST]] = []
    for node in nodes:
        start = first if not starts else node_start(node, lines)
        if not starts or start > starts[-1][0]:  # skips "a = 1; b = 2" siblings
            starts.append((start, node))
    result = []
    for index, (start, node) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else last
        result.append((start, end, node))
    return result


def pack(spans: Sequence[Span], lines: Sequence[str], max_chars: int) -> List[Span]:
    """Greedily merge adjacent spans for as long as the result fits the limit."""
    packed: List[Span] = []
    for span in spans:
        if packed and fits(lines, packed[-1].start, span.end, max_chars):
            packed[-1].end = span.end
            packed[-1].symbols.extend(
                s for s in span.symbols if s not in packed[-1].symbols
            )
        else:
            packed.append(
                Span(span.start, span.end, span.kind, list(span.symbols), span.context)
            )
    return packed


def line_spans(
    lines: Sequence[str],
    first: int,
    last: int,
    max_chars: int,
    kind: str,
    symbols: Sequence[str],
    context: str,
) -> List[Span]:
    """Split at blank lines, and between single lines only where necessary."""
    spans: List[Span] = []
    number = first
    while number <= last:
        if not lines[number - 1].strip():
            number += 1
            continue
        end = number
        while end < last and lines[end].strip():
            end += 1
        if fits(lines, number, end, max_chars):
            spans.append(Span(number, end, kind, list(symbols), context))
        else:
            spans.extend(
                Span(n, n, kind, list(symbols), context) for n in range(number, end + 1)
            )
        number = end + 1
    return pack(spans, lines, max_chars)


def function_spans(
    node: ast.AST,
    start: int,
    end: int,
    lines: Sequence[str],
    max_chars: int,
    qualified_name: str,
    context: str,
) -> List[Span]:
    """Keep a function whole if it fits, otherwise split between statements."""
    if fits(lines, start, end, max_chars):
        return [Span(start, end, "function", [qualified_name], context)]
    pieces: List[Span] = []
    for s_start, s_end, _ in partition(node.body, lines, start, end):
        if fits(lines, s_start, s_end, max_chars):
            pieces.append(
                Span(s_start, s_end, "function_part", [qualified_name], context)
            )
        else:
            pieces.extend(
                line_spans(
                    lines, s_start, s_end, max_chars,
                    "function_part", [qualified_name], context,
                )
            )
    return pack(pieces, lines, max_chars)


def class_spans(
    node: ast.ClassDef,
    start: int,
    end: int,
    lines: Sequence[str],
    max_chars: int,
    file_context: str,
    prefix: str = "",
) -> List[Span]:
    """Keep a class whole if it fits, otherwise group its members up to the limit.

    Each part carries the class signature in its context, so a method retrieved
    on its own can still be traced to its class. Oversized members are not
    merged with their neighbours, which keeps every part's kind accurate.
    """
    name = prefix + node.name
    if fits(lines, start, end, max_chars):
        return [Span(start, end, "class", [name], file_context)]

    signature = lines[node.lineno - 1].strip().rstrip(":")
    context = f"{file_context} | {signature}"
    result: List[Span] = []
    pending: List[Span] = []

    def flush() -> None:
        result.extend(pack(pending, lines, max_chars))
        pending.clear()

    for m_start, m_end, member in partition(node.body, lines, start, end):
        if isinstance(member, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols = [f"{name}.{member.name}"]
        else:
            symbols = [name] if m_start == start else []

        if fits(lines, m_start, m_end, max_chars):
            pending.append(Span(m_start, m_end, "class_part", symbols, context))
            continue
        flush()
        if isinstance(member, ast.ClassDef):
            result.extend(
                class_spans(
                    member, m_start, m_end, lines, max_chars,
                    file_context, prefix=f"{name}.",
                )
            )
        elif isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result.extend(
                function_spans(
                    member, m_start, m_end, lines, max_chars, symbols[0], context
                )
            )
        else:
            result.extend(
                line_spans(
                    lines, m_start, m_end, max_chars, "class_part", symbols, context
                )
            )
    flush()
    return result


def python_spans(
    source: str, lines: Sequence[str], max_chars: int, context: str
) -> Optional[List[Span]]:
    """Return syntax-based spans, or None if the file cannot be parsed."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return None
    if not tree.body:
        return None

    spans: List[Span] = []
    module_code: List[Span] = []

    def flush() -> None:
        spans.extend(pack(module_code, lines, max_chars))
        module_code.clear()

    for start, end, node in partition(tree.body, lines, 1, len(lines)):
        if isinstance(node, ast.ClassDef):
            flush()
            spans.extend(class_spans(node, start, end, lines, max_chars, context))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            flush()
            spans.extend(
                function_spans(node, start, end, lines, max_chars, node.name, context)
            )
        elif fits(lines, start, end, max_chars):
            module_code.append(Span(start, end, "module", [], context))
        else:
            module_code.extend(
                line_spans(lines, start, end, max_chars, "module", [], context)
            )
    flush()
    return spans


def trim(span: Span, lines: Sequence[str]) -> Optional[Span]:
    """Remove blank lines from both ends; return None if nothing is left."""
    while span.start <= span.end and not lines[span.start - 1].strip():
        span.start += 1
    while span.end >= span.start and not lines[span.end - 1].strip():
        span.end -= 1
    return span if span.start <= span.end else None


def role_of(relative_path: str) -> str:
    parts = relative_path.split("/")
    is_test = "tests" in parts[:-1] or parts[-1].startswith("test_")
    return "test" if is_test else "source"


def chunk_source(relative_path: str, source: str, max_chars: int) -> List[Chunk]:
    """Split one file's text into chunks."""
    lines = source.split("\n")
    context = f"File: {relative_path}"
    spans = None
    if relative_path.endswith(".py"):
        spans = python_spans(source, lines, max_chars, context)
    if spans is None:
        spans = line_spans(lines, 1, len(lines), max_chars, "text", [], context)

    chunks = []
    for span in spans:
        trimmed = trim(span, lines)
        if trimmed is None:
            continue
        chunks.append(
            Chunk(
                id=f"{relative_path}:{trimmed.start}-{trimmed.end}",
                path=relative_path,
                start_line=trimmed.start,
                end_line=trimmed.end,
                kind=trimmed.kind,
                role=role_of(relative_path),
                symbols=trimmed.symbols,
                context=trimmed.context,
                text=slice_text(lines, trimmed.start, trimmed.end),
            )
        )
    verify(relative_path, lines, chunks)
    return chunks


def verify(relative_path: str, lines: Sequence[str], chunks: Sequence[Chunk]) -> None:
    """Stop if any non-blank line is lost, duplicated, or out of order."""
    expected = [n for n, line in enumerate(lines, 1) if line.strip()]
    covered = [
        n
        for chunk in chunks
        for n in range(chunk.start_line, chunk.end_line + 1)
        if lines[n - 1].strip()
    ]
    if covered != expected:
        raise RuntimeError(f"Chunks do not cover {relative_path} exactly once")


def read_text(path: Path) -> Optional[str]:
    """Read a text file with LF line endings, or return None if it is binary.

    Python's newline translation turns CRLF into LF, so a Windows checkout gives
    the same chunks as a Linux one. utf-8-sig also drops a byte order mark.
    """
    try:
        with open(path, encoding="utf-8-sig") as handle:
            text = handle.read()
    except UnicodeDecodeError:
        return None
    return None if "\x00" in text else text


def chunk_folder(
    input_dir: Path, max_chars: int
) -> Tuple[List[Chunk], Dict[str, str]]:
    """Chunk every text file under input_dir, in a fixed order."""
    files = [
        p
        for p in input_dir.rglob("*")
        if p.is_file() and not SKIP_DIRS.intersection(p.relative_to(input_dir).parts)
    ]
    chunks: List[Chunk] = []
    skipped: Dict[str, str] = {}
    base = input_dir.parent
    for path in sorted(files, key=lambda p: p.relative_to(base).as_posix()):
        relative_path = path.relative_to(base).as_posix()
        text = read_text(path)
        if text is None:
            skipped[relative_path] = "binary or not UTF-8"
        elif not text.strip():
            skipped[relative_path] = "empty"
        else:
            chunks.extend(chunk_source(relative_path, text, max_chars))
    return chunks, skipped


def build_metadata(
    input_dir: Path, max_chars: int, chunks: Sequence[Chunk], skipped: Dict[str, str]
) -> dict:
    sizes = [len(chunk.text) for chunk in chunks]
    return {
        "source_folder": input_dir.name,
        "max_chars": max_chars,
        "files_chunked": len({chunk.path for chunk in chunks}),
        "files_skipped": skipped,
        "chunk_count": len(chunks),
        "chars_median": statistics.median(sizes) if sizes else 0,
        "chars_max": max(sizes, default=0),
        "over_limit": sum(size > max_chars for size in sizes),
        "by_kind": dict(sorted(Counter(chunk.kind for chunk in chunks).items())),
        "by_role": dict(sorted(Counter(chunk.role for chunk in chunks).items())),
    }


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-chars", type=int, default=MAX_CHARS)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if args.max_chars <= 0:
        print("--max-chars must be greater than 0", file=sys.stderr)
        return 2
    input_dir = args.input.resolve()
    if not input_dir.is_dir():
        print(f"Folder not found: {input_dir}", file=sys.stderr)
        return 1

    chunks, skipped = chunk_folder(input_dir, args.max_chars)
    if not chunks:
        print(f"No text files found in: {input_dir}", file=sys.stderr)
        return 1

    metadata = build_metadata(input_dir, args.max_chars, chunks, skipped)
    payload = {"meta": metadata, "chunks": [asdict(chunk) for chunk in chunks]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(
        f"{metadata['chunk_count']} chunks from {metadata['files_chunked']} files "
        f"(median {metadata['chars_median']:g} chars, max {metadata['chars_max']})"
    )
    for path, reason in skipped.items():
        print(f"Skipped {path}: {reason}")
    if metadata["over_limit"]:
        print(f"Warning: {metadata['over_limit']} chunks exceed the limit")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
