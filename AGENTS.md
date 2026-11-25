# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Codex, Cursor, etc.) when working with code in this repository.

## What this repo is

A student's submissions for the AI4SE (AI for Software Engineering) lab course, forked from the course repo (`Neltharion59/main` is merged in periodically). It is not one application. Each `Week_XX_*` folder holds that week's assignments, and each `Task_N/Task_N.md` is the assignment brief from the lecturer. Every other file in a task folder is the student's deliverable. Read the `Task_N.md` before working on a task: it states the required OUTPUT and the points.

- `Assessments/`: grading feedback (human and LLM-generated) on past weeks.
- `.claude/commands/task-summary.md`: `/task-summary N` summarizes a Week 08 task.
- `.claude/output-styles/ai4se.md`: keep explanations short and always list the files you changed.

There is no top-level build, lint or test setup. Each project below is self-contained; run its commands from its own directory. Code is Python (3.10–3.13), and several scripts call the OpenAI API through `OPENAI_API_KEY`.

## Projects with runnable code

**Week 03 Task 2: text-to-SQL evaluation** (`Week_03_Prompting/Assignments/Task_2/data/`)
`evaluate_retrieval_predictions.py` builds an in-memory SQLite DB from `restaurants-schema.csv` and `restaurants-db.txt`, runs each predicted SQL query and compares the result to `restaurants_dataset.csv`. It reads `restaurants_dataset_predictions.csv` (hardcoded `PREDICTIONS_PATH`), so to score a variant (`_ICIO`, `_ReAct`, `_TRACE`), copy or rename it to that name first.

**Week 04 Task 1: ReqNet** (`Week_04_Requirements/Task_1/reqnet/`)
A LangGraph pipeline that turns the stakeholder corpus in `../data/corpus` into a requirements spec. Its nodes are extractor → organizer → consolidator → reviewer/reviser loop, with a separate model per role. `REPORT.md` has the design and `README.md` has the options.
```
pip install -r requirements.txt
python run.py --input ../data/corpus --output output          # needs OPENAI_API_KEY
python run.py --input ../data/corpus --output output --mock   # offline, no key
```
LLM answers are cached in `.llm_cache/` keyed by request hash. Delete that folder to force fresh calls.

**Week 06: playground + RAG codegen** (`Week_06_Implementation/Assignments/AI4SE_Playground/`)
- `playground/` is a small order/inventory/pricing package that serves as the codegen target. Its tests use `unittest`:
  ```
  cd playground
  python -m unittest discover -s tests                 # all tests
  python -m unittest tests.test_pricing                # one module
  python -m unittest tests.test_pricing.SomeTestCase.test_x   # one test
  ```
- `rag/` is the pipeline: `chunk_playground.py` (AST chunking → `playground_chunks.json`) → `embed_chunks.py` (wordllama embeddings → `playground_index.npz`) → `solve_tasks.py` (retrieves the top 5 chunks for each task in `missing_code.json`, asks an OpenAI model for the code, writes it into `playground/`, runs the tests and retries failures). `solve_tasks.py --dry-run` needs no key and changes no files.
- `Week_06_Implementation/Assignments/Task_2..5/` contain copies of these same rag scripts and artifacts, submitted per task. `AI4SE_Playground/rag/` is the working copy that runs against the playground. If you change a script, keep the task copy in sync when it is a deliverable.

**Week 08: dissecting the coding assistant** (`Week_08_Dissecting/Assignments/`)
These tasks configure Claude Code itself (settings, skills, output styles, MCP, etc.). Per `readme.md`, the configuration changes must be kept until the end of the assignment, because a redacted config is submitted. Do not revert or clean up `.claude/` settings. The lecturer also asks students to do these tasks partly by hand, so prefer explaining and scaffolding over silently completing them.
