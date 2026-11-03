# Chunking design

**Decision:** split along Python syntax boundaries, with a limit of **1,200 characters per chunk** and no overlap.

**Result:** 228 chunks from 26 files, with a median of 784 characters and a maximum of 1,190. The only file skipped is the empty `playground/tests/__init__.py`.

## Splitting method
The `playground` folder contains only Python: about 159,000 characters across 698 functions and methods and 103 classes. Code questions are usually about one function or class, so the splitter parses each file with `ast` and keeps those units intact where it can:

1. **Functions and classes that fit** become one chunk, along with their decorators and the comments directly above them.
2. **Larger classes** are split into groups of neighbouring methods, up to the limit.
3. **Larger functions** are split between statements, and between lines only if a single statement is too long.
4. **Other module code**, such as imports and constants, is grouped when adjacent.
5. **Other text files and Python that won't parse** are split at blank lines.

**Why not fixed-size windows:** I compared this method with fixed windows of up to 1,200 characters, cut at line ends. The windows split **87 of the 698 functions and methods (12.5%)**, while this method splits **one**: `Simulation.step`, which at 1,887 characters is too long to fit.

**Why no overlap:** overlap is mainly a way to soften arbitrary cuts, and these cuts fall between code units. Overlap would also put duplicate text into the retrieved results. Instead, each chunk has a `context` field with its file path and, for part of a split class, the class signature, so a method retrieved alone can be traced to its class.

## Chunk size
| Limit (chars) | Chunks | Median size (chars) | Functions split | Classes kept whole (of 103) | Largest chunk (est. tokens) |
|---:|---:|---:|---:|---:|---:|
| 500 | 471 | 365 | 27 | 23 | 168 |
| 800 | 315 | 583 | 3 | 34 | 279 |
| 1,000 | 261 | 700 | 1 | 44 | 336 |
| **1,200** | **228** | **784** | **1** | **51** | **413** |
| 1,500 | 204 | 805 | 1 | 63 | 464 |
| 2,000 | 178 | 796 | 0 | 78 | 607 |
| 3,000 | 158 | 733 | 0 | 94 | 943 |

The number of functions split stops improving at 1,000 characters, and only `Simulation.step` is split until the limit reaches 2,000. Going that high to protect one function would make the largest chunk about 47% bigger, and bigger chunks are less focused.

Within the 1,000–1,500 range, the choice is a judgement call between focused chunks and keeping more classes whole. I chose 1,200 as a middle value, not a proven best one.

## Data structure
`rag/playground_chunks.json` holds a `meta` summary and a `chunks` list. This is easy to inspect and load in the next step. Each chunk has these fields:

| Field | Purpose |
|---|---|
| `id` | Unique reference in the form `path:start-end` |
| `path`, `start_line`, `end_line` | Where to find and cite the source |
| `kind` | `module`, `function`, `function_part`, `class`, `class_part` or `text` |
| `role` | `source` or `test` |
| `symbols` | Definitions in the chunk, such as `Simulation.step` |
| `context` | File path, plus the class signature for part of a split class |
| `text` | The exact source lines |

