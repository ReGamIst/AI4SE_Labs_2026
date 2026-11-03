# A pipeline for repository-aware code generation

## Is embedding matching the best strategy?
**No, not as the primary strategy for this task.** Each task already names its file, class and method, so similarity search is trying to rediscover something the code's structure states exactly.

I hand-picked 27 facts that the 10 tasks need, such as `InventoryLedger.available` for `Warehouse.stock_report`, and checked which ones reached the context:

| Context method | Facts found (of 27) | Tasks with every fact (of 10) | Average tokens per task |
|---|---:|---:|---:|
| Current hybrid search, top 5 | 24 | 8 | 1,528 |
| Structural lookup | 26 | 9 | 1,099 |

The structural lookup took the target class, the signatures of project classes it mentions, and test methods whose names contain the method name. It found `available` by following `Warehouse` to `InventoryLedger`, a link that similarity search has no direct way to see. It missed one fact because `test_discount_uses_floor_division` doesn't contain the word "price", so test lookup needs better rules than name matching.

Published evidence points the same way, with an important limit on repository size:

- **Search method may matter less than expected.** In a study of chunking for code completion, changing the retriever moved exact match by [at most 1.11 points on RepoEval](https://arxiv.org/pdf/2605.04763). An engineer formerly at Augment reported that [grep and find were sufficient](https://jxnl.co/writing/2025/09/11/why-grep-beat-embeddings-in-our-swe-bench-agent-lessons-from-augment/) for its agent on SWE-bench, while noting that the benchmark's repositories are smaller than real-world codebases.
- **Embeddings still help at scale.** Cursor reports [12.5% higher offline accuracy](https://cursor.com/blog/semsearch) with semantic search added to grep. Its online code retention rose 0.3% overall, but 2.6% on codebases with at least 1,000 files. These are the vendor's own figures, and it says the combination works best.
- **For this repository, retrieval may not be needed at all.** The source is about 14,000 tokens and the tests about 39,000. At `gpt-6-luna`'s [$0.10 per million input tokens](https://developers.openai.com/api/docs/pricing), sending everything costs about half a cent per call. This should be the baseline that any retrieval method has to beat, although irrelevant context could still reduce quality.

## Would a different number of chunks work better?
**A fixed number is the wrong setting.** A token budget, divided by purpose, is better. Here is what changing `k` did to the current search:

| Chunks | 1 | 3 | 5 | 8 | 10 | 15 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Facts found (of 27) | 13 | 22 | 24 | 24 | 25 | 25 | 25 |
| Average tokens per task | 312 | 978 | 1,528 | 2,376 | 2,900 | 4,431 | 5,917 |

Five is a reasonable value for this search: fewer loses facts quickly, while 20 costs almost four times the tokens for one more fact and still misses two. More chunks can't fix what the ranking doesn't surface.

A controlled study supports budgeting: context length was its [dominant parameter](https://arxiv.org/pdf/2605.04763), with diminishing returns beyond 4,096 tokens, though it tested only small models. I'd start with 2,000–4,000 tokens and let the model request more. Larger models may need less help choosing, so this is worth testing.

## Should chunking be more sophisticated?
**Not as the next improvement.** The evidence is mixed: [cAST reports gains](https://arxiv.org/pdf/2506.15655v2) over fixed-size chunking, but the [controlled study](https://arxiv.org/pdf/2605.04763) found that structure-aware methods didn't beat sliding windows, and that function-level chunking did worst. My own chunking choice kept functions whole, which is tidy, but I never showed that it produces better code.

The bigger change is to stop treating chunks as the main unit and use a **symbol index**. A single method can then appear in different forms as needed: its signature, full body, callers or tests. Chunks would remain useful only for the optional search tool, where an existing method such as cAST is good enough.

## Proposed pipeline
| Stage | What happens | Why |
|---|---|---|
| **1. Index** | Parse the repository into symbols, references, types and links from tests to code, preferably using coverage data. Update incrementally per commit. Embeddings are optional. | Gives exact answers to "what does this use?" and "what tests this?" |
| **2. Plan** | Resolve the target. Implement methods in dependency order, foundations first. | `Order.advance` depends on `transition`, so its tests can't pass until `transition` exists. |
| **3. Assemble context** | Within a token budget, add the target class and imports, signatures of the types it uses, its tests, its callers, and similar methods elsewhere. Rank by graph distance, as [aider's repository map](https://aider.chat/docs/repomap.html) does with file dependencies. | Predictable, explainable and small. |
| **4. Generate** | Start with an inexpensive model and request a patch to that symbol. Escalate to a stronger model after repeated failure. | Most of these methods are simple, so cost follows difficulty. |
| **5. Verify** | In a sandbox with no network or secrets, run syntax checks, type checks, targeted tests and then the full suite, with time limits. Tests are read-only. | Generated code is untrusted, and tests are the most reliable feedback. |
| **6. Repair** | Feed failures back to the model and offer tools: `find_symbol`, `find_references`, `read`, `grep` and `semantic_search`. Limit the rounds. | Fills gaps from real evidence. [RepoCoder](https://deepai.org/publication/repocoder-repository-level-code-completion-through-iterative-retrieval-and-generation) also uses earlier output to guide later retrieval. |
| **7. Report** | Present the diff, test results and any unresolved problems for human review. Never merge automatically. | Keeps a person responsible for the result. |

**Conflicts between sources need their own handling.** The `InventoryLedger.__contains__` task says "positive on-hand stock", but its test requires `True` at zero stock. The current script silently favours the test. A better pipeline would detect the mismatch and report it, because either the task or the test may be wrong.

## What changes from the current pipeline
| Area | Current | Proposed |
|---|---|---|
| Finding context | Hybrid search only | Structural lookup first, with search as a tool |
| Amount of context | Always 5 chunks | Token budget, with requests for more |
| Order of work | As listed in the JSON | Dependency order |
| Tests run | Full suite after all tasks | Targeted tests after each task, then the full suite |
| Execution safety | Runs on your computer | Isolated sandbox |
| Specification conflicts | Follows the test | Reports the conflict |

## How to evaluate it
Run these variants on the same tasks and several repositories of different sizes: whole repository, current top-5 search, structural lookup, and the full pipeline.

- **Measure:** tests passed on the first attempt and after repair, repair rounds, tokens, cost and time.
- **Hold back some tests:** if the model sees all the tests, passing them proves less. Keep some hidden from the model, and add mutation testing or human review.
- **Repeat runs:** models vary between runs, so one pass per variant isn't enough.

I would build the structural lookup and the sandbox first. They should bring the largest gains for the least work. Add embeddings only when a measured failure shows that they're needed, which is more likely in large repositories or when tasks are vaguely described.
