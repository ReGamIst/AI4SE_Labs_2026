#!/usr/bin/env python3
"""Turn chunks into embeddings, store them, and retrieve them by question.

Each chunk gets two vectors, which capture different things:

- dense:  a pretrained 256-dimensional WordLlama vector of the chunk's
          description (file, symbols, definition names, docstrings)
- sparse: a TF-IDF vector of the chunk's code, with identifiers split into words

A search ranks all chunks by each vector, then combines the two rankings with
reciprocal rank fusion. See embedding_design.md for the reasoning.

Setup (Python 3.10-3.13; no API key, and the model ships inside the package):

    python -m pip install wordllama==0.4.0.post1

Usage, from anywhere:

    python chunk_playground.py                 # creates playground_chunks.json
    python embed_chunks.py                     # creates playground_index.npz
    python embed_chunks.py search "How is tax added to an order total?"
    python embed_chunks.py search "can_afford behaviour" --k 8 --role test --full

From other Python code:

    from embed_chunks import load_store
    results = load_store().search("How is tax added to an order total?", k=5)
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
import sys
import textwrap
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np

RAG_DIR = Path(__file__).resolve().parent
DEFAULT_CHUNKS = RAG_DIR / "playground_chunks.json"
DEFAULT_INDEX = RAG_DIR / "playground_index.npz"

MODEL_NAME = "wordllama-l2_supercat-256"
RRF_K = 60  # The conventional reciprocal rank fusion constant.
FORMAT_VERSION = 1

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_WORD_PART = re.compile(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+")
_DEFINITIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


# Chunk representations -------------------------------------------------------


def describe_chunk(chunk: dict) -> str:
    """Return the text used for the dense vector.

    Averaged word vectors blur over long code, so chunks with definitions are
    described by their location, names and docstrings. Chunks without a complete
    definition have little else to describe them, so they keep their full text.
    """
    if chunk["kind"] in ("module", "text", "function_part"):
        return chunk["context"] + "\n" + chunk["text"]
    parts = [chunk["context"]] + chunk["symbols"]
    try:
        tree = ast.parse(textwrap.dedent(chunk["text"]))
    except SyntaxError:
        return "\n".join(parts + [chunk["text"]])
    for node in ast.walk(tree):
        if isinstance(node, _DEFINITIONS):
            parts.append(node.name)
            docstring = ast.get_docstring(node)
            if docstring:
                parts.append(docstring)
    return "\n".join(parts)


def tokenize(text: str) -> List[str]:
    """Split text into lowercase tokens, keeping identifiers and their words.

    "can_afford" gives can_afford, can, afford. "OutOfStockError" gives
    outofstockerror, out, of, stock, error.
    """
    tokens: List[str] = []
    for identifier in _IDENTIFIER.findall(text):
        tokens.append(identifier.lower())
        words = [word.lower() for word in _WORD_PART.findall(identifier)]
        if len(words) > 1:
            tokens.extend(words)
    return tokens


# Embedding -------------------------------------------------------------------


def load_model():
    """Load the WordLlama model from the files bundled with the package."""
    try:
        import wordllama
    except ImportError:
        raise SystemExit(
            "The wordllama package is missing. Install it with:\n"
            "    python -m pip install wordllama==0.4.0.post1"
        ) from None
    # Version 0.4.0.post1 looks for its bundled tokenizer in the wrong folder and
    # tries to download it. Pointing cache_dir at the package finds the local copy.
    package_dir = Path(wordllama.__file__).parent
    return wordllama.WordLlama.load(cache_dir=package_dir, disable_download=True)


class TfidfVectorizer:
    """Minimal TF-IDF: sublinear term frequency, smoothed IDF, unit length."""

    def __init__(self, vocabulary: Sequence[str], idf: np.ndarray) -> None:
        self.vocabulary = list(vocabulary)
        self.idf = idf
        self._positions = {term: i for i, term in enumerate(self.vocabulary)}

    @classmethod
    def fit(cls, texts: Sequence[str]) -> "TfidfVectorizer":
        document_frequency: Counter = Counter()
        for text in texts:
            document_frequency.update(set(tokenize(text)))
        vocabulary = sorted(document_frequency)
        count = len(texts)
        idf = np.array(
            [
                math.log((1 + count) / (1 + document_frequency[term])) + 1
                for term in vocabulary
            ],
            dtype=np.float32,
        )
        return cls(vocabulary, idf)

    def transform(self, text: str) -> np.ndarray:
        vector = np.zeros(len(self.vocabulary), dtype=np.float32)
        for term, count in Counter(tokenize(text)).items():
            position = self._positions.get(term)
            if position is not None:
                vector[position] = (1 + math.log(count)) * self.idf[position]
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector


@dataclass
class ChunkEmbedding:
    """The two unit-length vectors that represent one chunk."""

    dense: np.ndarray
    sparse: np.ndarray


def embed_chunk(chunk: dict, model, vectorizer: TfidfVectorizer) -> ChunkEmbedding:
    """Turn one chunk into its embedding."""
    dense = model.embed([describe_chunk(chunk)], norm=True)[0]
    return ChunkEmbedding(
        dense=np.asarray(dense, dtype=np.float32),
        sparse=vectorizer.transform(chunk["text"]),
    )


# Storage and retrieval -------------------------------------------------------


@dataclass
class SearchResult:
    """One retrieved chunk. A lower rank in either list means a closer match."""

    chunk: dict
    score: float  # fused score, only meaningful for ordering within one search
    dense_rank: int
    sparse_rank: int


class VectorStore:
    """Chunks with their vectors in memory, searched exactly."""

    def __init__(
        self,
        chunks: Sequence[dict],
        dense: np.ndarray,
        sparse: np.ndarray,
        vectorizer: TfidfVectorizer,
        chunks_hash: str,
        model=None,
    ) -> None:
        self.chunks = list(chunks)
        self.dense = dense
        self.sparse = sparse
        self.vectorizer = vectorizer
        self.chunks_hash = chunks_hash
        self._model = model

    @property
    def model(self):
        if self._model is None:
            self._model = load_model()
        return self._model

    def search(
        self, question: str, k: int = 5, role: Optional[str] = None
    ) -> List[SearchResult]:
        """Return the k best chunks, optionally only those with the given role."""
        if not question.strip():
            raise ValueError("The question is empty")
        if k <= 0:
            raise ValueError("k must be greater than 0")
        allowed = np.array(
            [role is None or chunk["role"] == role for chunk in self.chunks]
        )
        candidates = np.flatnonzero(allowed)
        if candidates.size == 0:
            return []

        query_dense = np.asarray(
            self.model.embed([question], norm=True)[0], dtype=np.float32
        )
        query_sparse = self.vectorizer.transform(question)
        dense_ranks = _ranks(self.dense[candidates] @ query_dense)
        sparse_ranks = _ranks(self.sparse[candidates] @ query_sparse)
        scores = 1 / (RRF_K + dense_ranks) + 1 / (RRF_K + sparse_ranks)

        best = np.argsort(-scores, kind="stable")[:k]
        return [
            SearchResult(
                chunk=self.chunks[candidates[i]],
                score=float(scores[i]),
                dense_rank=int(dense_ranks[i]),
                sparse_rank=int(sparse_ranks[i]),
            )
            for i in best
        ]

    def save(self, path: Path) -> None:
        """Write all vectors to one .npz file. Chunk text stays in the chunk file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        with open(temporary, "wb") as handle:
            np.savez_compressed(
                handle,
                format_version=np.array(FORMAT_VERSION),
                model_name=np.array(MODEL_NAME),
                chunks_hash=np.array(self.chunks_hash),
                chunk_ids=np.array([chunk["id"] for chunk in self.chunks]),
                dense=self.dense,
                sparse=self.sparse,
                vocabulary=np.array(self.vectorizer.vocabulary),
                idf=self.vectorizer.idf,
            )
        os.replace(temporary, path)


def _ranks(similarities: np.ndarray) -> np.ndarray:
    """Convert similarities into 1-based ranks; ties keep chunk order."""
    order = np.argsort(-similarities, kind="stable")
    ranks = np.empty(len(order), dtype=np.int64)
    ranks[order] = np.arange(1, len(order) + 1)
    return ranks


def read_chunks(chunks_path: Path) -> tuple:
    """Return the chunks and a hash of the chunk file's contents."""
    if not chunks_path.is_file():
        raise SystemExit(
            f"Chunk file not found: {chunks_path}\nRun chunk_playground.py first."
        )
    raw = chunks_path.read_bytes()
    chunks = json.loads(raw.decode("utf-8"))["chunks"]
    if not chunks:
        raise SystemExit(f"No chunks in: {chunks_path}")
    return chunks, hashlib.sha256(raw).hexdigest()


def build_store(chunks_path: Path = DEFAULT_CHUNKS) -> VectorStore:
    """Embed every chunk in the chunk file."""
    chunks, chunks_hash = read_chunks(chunks_path)
    model = load_model()
    vectorizer = TfidfVectorizer.fit([chunk["text"] for chunk in chunks])
    embeddings = [embed_chunk(chunk, model, vectorizer) for chunk in chunks]
    return VectorStore(
        chunks,
        dense=np.stack([e.dense for e in embeddings]),
        sparse=np.stack([e.sparse for e in embeddings]),
        vectorizer=vectorizer,
        chunks_hash=chunks_hash,
        model=model,
    )


def load_store(
    index_path: Path = DEFAULT_INDEX, chunks_path: Path = DEFAULT_CHUNKS
) -> VectorStore:
    """Load a saved store, refusing one that no longer matches its chunk file."""
    if not index_path.is_file():
        raise SystemExit(
            f"Index not found: {index_path}\nRun embed_chunks.py to build it."
        )
    chunks, chunks_hash = read_chunks(chunks_path)
    with np.load(index_path, allow_pickle=False) as data:
        if (
            int(data["format_version"]) != FORMAT_VERSION
            or str(data["model_name"]) != MODEL_NAME
            or str(data["chunks_hash"]) != chunks_hash
        ):
            raise SystemExit(
                "The index is out of date because the chunks or the embedding "
                "method changed.\nRun embed_chunks.py to rebuild it."
            )
        vectorizer = TfidfVectorizer(
            [str(term) for term in data["vocabulary"]], data["idf"]
        )
        return VectorStore(chunks, data["dense"], data["sparse"], vectorizer, chunks_hash)


# Command line ----------------------------------------------------------------


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("build", help="embed all chunks and save the index (default)")
    search = commands.add_parser("search", help="find the chunks that best match a question")
    search.add_argument("question")
    search.add_argument("--k", type=int, default=5, help="number of results (default 5)")
    search.add_argument("--role", choices=["source", "test"], help="limit results to one role")
    search.add_argument("--full", action="store_true", help="print each chunk's full text")
    return parser.parse_args(argv)


def print_results(results: Sequence[SearchResult], full: bool) -> None:
    if not results:
        print("No chunks match that role.")
    for number, result in enumerate(results, 1):
        symbols = ", ".join(result.chunk["symbols"][:4]) or "-"
        print(
            f"{number}. {result.chunk['id']}  [{result.chunk['kind']}, "
            f"{result.chunk['role']}]  dense #{result.dense_rank}, "
            f"sparse #{result.sparse_rank}"
        )
        print(f"   {symbols}")
        if full:
            print(textwrap.indent(result.chunk["text"], "   | "))


def main(argv: Optional[Sequence[str]] = None) -> int:
    # A Windows console may not support every character found in source code.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if args.command == "search":
        try:
            store = load_store(args.index, args.chunks)
            print_results(store.search(args.question, args.k, args.role), args.full)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        return 0

    store = build_store(args.chunks)
    store.save(args.index)
    print(
        f"Embedded {len(store.chunks)} chunks: {store.dense.shape[1]}-dimensional "
        f"dense vectors, {store.sparse.shape[1]}-term sparse vectors"
    )
    print(f"Wrote {args.index}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
