# ReqNet — requirements refinement network (LangGraph + OpenAI)

## Setup
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...                            # Windows: set OPENAI_API_KEY=sk-...
```

## Run on the lab corpus
```bash
git clone https://github.com/ReGamIst/AI4SE_Labs_2026.git
python run.py --input AI4SE_Labs_2026/Week_04_Requirements/Task_1/data/corpus --output output
```
Outputs in `output/`:
- `requirements.md` — the requirements specification (deliverable)
- `requirements.json` — same content, machine-readable, incl. all extracted candidates
- `run_log.json` — models used, token usage per model, per-node history, final review
- `graph.mmd` — Mermaid diagram of the compiled LangGraph

Answers are cached in `.llm_cache/`; if a run is interrupted, rerun the same command and
finished calls are reused. Delete the folder for a fresh run.

## Options
```
--max-review-rounds N      review/revise iterations (default 3)
--concurrency N            parallel LLM calls in fan-out steps (default 8; lower it on rate limits)
--reasoning-effort LEVEL   minimal|low|medium|high, passed to the models if supported
--model-extractor / --model-organizer / --model-consolidator / --model-reviewer / --model-reviser
--mock                     offline dry run with a heuristic LLM stand-in (no key needed)
-v                         debug logging
```

Default models: extractor `gpt-5-mini`, organizer `gpt-5.4-nano`, consolidator and reviser
`gpt-6-luna`, reviewer `gpt-5.6-luna`. See `REPORT.md` for the design.
