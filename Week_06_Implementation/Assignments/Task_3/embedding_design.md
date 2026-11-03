# Embedding and retrieval design

**Decision:** give each chunk two vectors, and combine their rankings at search time:

| Vector | Method | What it represents |
|---|---|---|
| Dense (256 dimensions) | Pretrained WordLlama model | The chunk's description: file, symbols, definition names and docstrings |
| Sparse (1,581 terms) | TF-IDF, with identifiers split into words | The chunk's code |

Vectors are stored in one NumPy file and searched exactly, with no separate vector database.

**Result:** across 60 test questions, the correct chunk was in the top 5 results for 80% of them. It ranked first for 38%, so later steps should retrieve at least 5 chunks rather than rely on the top result.

## Embedding method
| Option | Outcome |
|---|---|
| **WordLlama** (chosen for dense vectors) | Runs on CPU with no API key. The weights ship inside the package, so it works offline and all results here are measured. |
| **TF-IDF** (chosen for sparse vectors) | Finds exact identifiers such as `can_afford`, which general-purpose word embeddings handle poorly. |
| **Latent semantic analysis (LSA)** | Tested at 64 and 128 dimensions on the development questions. At 128, it was about level with plain TF-IDF on code text (hit@5 0.72 vs 0.70, MRR 0.50 vs 0.54), which didn't justify the extra step. |

## What gets embedded
WordLlama averages its word vectors, so a long code body blurs into its mix of common words. The tests supported this: description-only embedding clearly beat embedding the code on hit@5 and MRR. Chunks without a complete definition (`module`, `text`, `function_part`) keep their full text, because they have little else to describe them.

Descriptions have a clear weakness: the tests have no docstrings, so test chunks are poorly described. The sparse vector covers this because it reads the code itself, which is why it uses the raw chunk text.

## Retrieval
### How a question is matched to chunks
1. **Filter:** if a `role` is given, only chunks with that role are considered.
2. **Embed the question:** it gets the same two kinds of vector as the chunks, using the same model and the stored TF-IDF vocabulary. Question words that aren't in the vocabulary are ignored.
3. **Measure similarity:** each question vector is compared with every chunk's matching vector using cosine similarity. All vectors have unit length, so this is a plain dot product, computed for all chunks with one matrix multiplication.
4. **Rank separately:** the chunks are ranked once by dense similarity and once by sparse similarity.
5. **Combine the ranks:** each chunk's final score uses reciprocal rank fusion:
   `score = 1 / (60 + dense_rank) + 1 / (60 + sparse_rank)`
6. **Return the top `k`:** the highest-scoring chunks are returned, along with both of their ranks.
**Why ranks and not raw scores:** the two kinds of similarity aren't on comparable scales, so averaging them would favour whichever runs higher. Using ranks also avoids a tuned weight, which 60 questions couldn't justify. `k = 60` is the conventional constant, and it keeps a single first place from outweighing good ranks in both lists.
 
**Example:** these are the top results for "How is tax added to an order total?"
 
| Result | Chunk | Dense similarity (rank) | Sparse similarity (rank) | Final score |
|---:|---|---:|---:|---:|
| 1 | `pricing.py:12-34` (`FlatPricing`) | 0.419 (3) | 0.185 (1) | 0.03227 |
| 2 | `orders.py:76-101` (`Order.items`, `Order.total`) | 0.456 (1) | 0.154 (6) | 0.03154 |
| 3 | `enums.py:37-47` (`OrderStatus`) | 0.276 (9) | 0.157 (5) | 0.02988 |
| 4 | `base.py:34-55` (`PricingStrategy`) | 0.266 (13) | 0.182 (2) | 0.02983 |
 
`FlatPricing` contains the tax calculation. It wins despite not being first in the dense ranking, because it ranks well in both lists. This is the benefit of fusion.
 
### Comparison of configurations
 
I compared six configurations on 40 development questions, fixed the choice, then ran 20 new held-out questions:
 
| Configuration | Development (hit@1 / hit@5 / MRR) | Held-out (hit@1 / hit@5 / MRR) |
|---|---:|---:|
| Dense: description | 0.35 / 0.75 / 0.53 | 0.35 / 0.75 / 0.50 |
| Dense: context + code | 0.30 / 0.60 / 0.43 | 0.25 / 0.55 / 0.40 |
| Sparse: code | 0.40 / 0.70 / 0.54 | 0.15 / 0.75 / 0.42 |
| **Fusion: dense description + sparse code (chosen)** | **0.42 / 0.80 / 0.59** | **0.30 / 0.80 / 0.52** |
| Fusion: dense context + code, sparse code | 0.33 / 0.72 / 0.52 | 0.30 / 0.70 / 0.46 |
| Dense: best of description or context + code | 0.40 / 0.75 / 0.56 | 0.40 / 0.85 / 0.57 |
 
For the chosen configuration, hit@5 across all 60 questions was 73% for paraphrased questions, 87% for questions naming an identifier, and 87% for questions about expected behaviour from the tests. Hit@10 was 88% overall.
 
**How strong this evidence is:** the choice is reasonable but not proven. The bootstrap 95% interval for the MRR gain over dense description alone includes zero on both question sets (-0.05 to +0.17 and -0.14 to +0.17). The last row scored higher on the held-out set, but it did worse on behaviour questions in development, and switching after seeing held-out results would have defeated their purpose.

## Storage
`rag/playground_index.npz` is 280 KB and holds both matrices as 32-bit floats, along with the chunk IDs, TF-IDF vocabulary and weights. Chunk text stays in `playground_chunks.json`, so there is one source for it.

- **Why exact search:** one search over 228 chunks takes about 0.4 ms once the model is loaded. A separate test scanned 100,000 random 256-dimensional vectors in 18 ms. An approximate index such as FAISS, or a database, would add a dependency and could miss results, with no practical speed gain at this size.
- **Staying in sync:** the index stores a hash of the chunk file and refuses to load if that file changed. Rebuilding takes about 0.6 s.
- **No incremental updates:** TF-IDF weights depend on all chunks, so changes need a full rebuild, which is fine at this speed.

## Setup
```
python -m pip install wordllama==0.4.0.post1
python chunk_playground.py
python embed_chunks.py
python embed_chunks.py search "How is tax added to an order total?"
```
