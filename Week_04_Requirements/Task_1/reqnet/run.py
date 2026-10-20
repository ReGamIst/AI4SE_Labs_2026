#!/usr/bin/env python3
"""ReqNet - agentic requirements refinement network (LangGraph + OpenAI).

Usage:
    export OPENAI_API_KEY=sk-...
    python run.py --input path/to/corpus_dir --output out/

    python run.py --input path/to/corpus_dir --output out_mock/ --mock   # offline dry run

Outputs in --output: requirements.md (the specification), requirements.json
(machine-readable, incl. all candidates), run_log.json (models, token usage,
per-node history), graph.mmd (Mermaid diagram of the network).
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reqnet.graph import Settings, build_graph, run  # noqa: E402
from reqnet.llm import build_backend  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="directory with the input corpus (searched recursively)")
    ap.add_argument("--output", default="output", help="output directory")
    ap.add_argument("--mock", action="store_true", help="use the offline heuristic LLM stand-in")
    ap.add_argument("--max-review-rounds", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=8, help="max parallel LLM calls in fan-out steps")
    ap.add_argument("--reasoning-effort", choices=["minimal", "low", "medium", "high"], default=None,
                    help="optional reasoning_effort passed to the models")
    ap.add_argument("--cache-dir", default=".llm_cache", help="disk cache of LLM answers ('' to disable)")
    for role, default in Settings().models.items():
        ap.add_argument(f"--model-{role}", default=default, help=f"model for the {role} node(s)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s", datefmt="%H:%M:%S")
    for noisy in ("httpx", "openai", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    settings = Settings(max_review_rounds=args.max_review_rounds)
    settings.models = {role: getattr(args, f"model_{role}") for role in settings.models}
    if len(set(settings.models.values())) < 3:
        logging.warning("fewer than 3 distinct models configured (spec ANS4 requires 3)")

    backend = build_backend(args.mock, Path(args.cache_dir) if args.cache_dir else None, args.reasoning_effort)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "graph.mmd").write_text(build_graph(settings).get_graph().draw_mermaid(), encoding="utf-8")

    t0 = time.time()
    state = run(args.input, str(out), backend, settings, max_concurrency=args.concurrency)
    dt = time.time() - t0
    print(f"\nDone in {dt:.0f}s: {len(state['requirements'])} requirements, "
          f"{len(state['discarded'])} discarded, review rounds: {state['round']}")
    print("Token usage:", json.dumps(backend.usage.by_model, indent=1))
    print(f"Specification: {out / 'requirements.md'}")


if __name__ == "__main__":
    main()
