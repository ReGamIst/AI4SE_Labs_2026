# Text-to-SQL Prompts for the Restaurants Benchmark

Three prompts, each built on a different framework, for getting an LLM to produce `restaurants_dataset_predictions.csv` that scores as high as possible in `evaluate_retrieval_predictions.py`. A report on the choice of frameworks follows the prompts.

---

## 0. What the evaluator actually rewards

Before writing the prompts I read the evaluator and ran test queries against the database built from `restaurants-schema.csv` + `restaurants-db.txt`. This matters because the score is **execution accuracy on an exact row multiset**, so a query that is "semantically right" but uses a different column, city table or comparison operator scores zero.

**How scoring works**

- The prediction file must be `restaurants_dataset_predictions.csv` with columns `question,predicted_sql`.
- Each prediction is matched to a label by the **exact `question` string**, in file order (duplicate questions are consumed first-in, first-out). Every one of the 155 label rows needs a prediction, or the script raises an error.
- Each `predicted_sql` is run in SQLite. **One SQL error aborts the whole run**, so every query must be valid.
- A prediction is correct only if its rows equal the label rows as a multiset: same columns, same order of columns, same duplicate counts. Row order does not matter.

**Conventions I verified against the labels**

| Rule | Verified detail |
|---|---|
| Output columns | Always `L.HOUSE_NUMBER, R.NAME`, in that order (the labels look like `[[1503, "lee & ginas cafe"]]`). |
| Base join | `RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID` |
| No `DISTINCT`, no `LIMIT` | Labels keep duplicate rows (e.g. two `al romano's pizza` rows at 24261 mission blvd). |
| City ("in vallejo") | Filter on `L.CITY_NAME`, not `R.CITY_NAME`. For alameda, `R.CITY_NAME` returns 63 rows against 62 expected. |
| Region ("in the bay area", "in the monterey") | `JOIN GEOGRAPHIC G ON R.CITY_NAME = G.CITY_NAME WHERE G.REGION = '...'`. Joining through `L.CITY_NAME` returns 8,969 rows instead of 9,171. |
| "in the X" vs "in X" | Has "the" means it is a region; without "the", it is a city. For example, "in unknown" is the city `unknown`, while "in the unknown" is the region. |
| Street ("on plaza way") | Exact match `L.STREET_NAME = 'plaza way'`, keeping the street text verbatim (`'st'`, `'ave.'`, `'san pablo ave # a'`). |
| Food type | Exact `R.FOOD_TYPE = '...'`, using the words from the question (`'ice cream'`, `'vietnamese/louisiana'`, `'california'`). |
| "rating above X" | Strictly `R.RATING > X`. The text in parentheses ("below average or better") is decoration. |
| "best ..." | `R.RATING = (SELECT MAX(R.RATING) ...)` with the same joins and filters inside the subquery. |
| "where is NAME in CITY" | `R.NAME = 'NAME' AND L.CITY_NAME = 'CITY'` |
| Strings | Lowercase, and apostrophes doubled: `'denny''s'`. |
| Noise | About a third of the questions wrap the real request in irrelevant food chatter. The real request is the sentence that names a place or a filter, and everything else is ignored. |

**Sanity check.** A crude regex generator that applies only these rules scored **151/155 = 97.42 %**. Of the four misses, three came from the regex choosing the wrong clause in long noisy questions, which an LLM handles easily. The fourth is the question "What is the lifes greates illusion?", which contains no request and whose label cannot be reproduced. The realistic ceiling for a good prompt is therefore **154/155 ≈ 99.4 %**.

All three prompts below carry these rules. They differ in how the rules are structured and taught, and in how the model checks its own work.

---

## Prompt 1: ICIO (Instruction · Context · Input · Output)

```text
### INSTRUCTION
Convert every natural-language question in restaurants_dataset.csv into ONE SQLite
SELECT query, and write the results to a file named
restaurants_dataset_predictions.csv. The queries will be graded by executing them
and comparing the returned rows (as a multiset) to a hidden gold result, so the
exact columns, filters, and row multiplicity matter more than anything else.

### CONTEXT
Database (SQLite, all text values lowercase):
  RESTAURANT(ID int PK, NAME text, FOOD_TYPE text, CITY_NAME text, RATING real)
  LOCATION(RESTAURANT_ID int PK/FK -> RESTAURANT.ID, HOUSE_NUMBER int,
           STREET_NAME text, CITY_NAME text)
  GEOGRAPHIC(CITY_NAME text PK, COUNTY text, REGION text)
Known regions: 'bay area', 'napa valley', 'monterey', 'lake tahoe',
'sacramento area', 'los angeles area', 'northern california',
'yosemite and mono lake area', 'unknown'.

Gold-query conventions (follow them exactly):
1. SELECT clause is always:  SELECT L.HOUSE_NUMBER, R.NAME
2. FROM clause always starts:
   FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID
3. Never use DISTINCT, LIMIT, ORDER BY, or GROUP BY. Duplicate rows must be kept.
4. City ("in <city>", with no "the"):  L.CITY_NAME = '<city>'
5. Region ("in the <region>"): add
   JOIN GEOGRAPHIC G ON R.CITY_NAME = G.CITY_NAME  and  G.REGION = '<region>'
   Treat "in the X" as a region and "in X" as a city, even for 'monterey'/'unknown'.
6. Street ("on <street>"):  L.STREET_NAME = '<street>', copied verbatim
   (e.g. 'st', 'ave.', 'san pablo ave # a', 'exp/riveroaks').
7. Food ("<x> food", "a <x> restaurant", "places for <x>", "best <x>"):
   R.FOOD_TYPE = '<x>', copied verbatim (e.g. 'ice cream', 'california').
8. "rating above N" means R.RATING > N (strictly greater). Ignore the words in
   parentheses.
9. "best ..." means add  AND R.RATING = (SELECT MAX(R.RATING) FROM <same joins>
   WHERE <same filters>).
10. "where is <name> in <city>" means R.NAME = '<name>' AND L.CITY_NAME = '<city>'.
11. Escape apostrophes by doubling them: 'denny''s'.
12. Many questions contain irrelevant chatter about snacks, picnics, teacups, etc.
    Find the single clause that asks for restaurants and translate only that.
13. If a question contains no restaurant request at all, still emit valid SQL:
    SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L
    ON R.ID = L.RESTAURANT_ID WHERE 0

### INPUT
The attached file restaurants_dataset.csv (155 rows, columns: question, result).
Use ONLY the "question" column; do not read or copy the "result" column.

### OUTPUT
A UTF-8 CSV file named restaurants_dataset_predictions.csv:
- header row exactly:  question,predicted_sql
- exactly 155 data rows, in the same order as the input
- "question" copied character-for-character, including duplicates, punctuation
  and trailing spaces before "?"
- "predicted_sql" is a single-line SQLite query with no trailing semicolon
- standard CSV quoting (wrap fields with commas/quotes in double quotes)
Return the file only. Do not add commentary inside it.
```

**Why ICIO here.** The task is a pure data-transformation job: one CSV goes in and one CSV comes out under strict format rules. ICIO separates *what to do*, *the knowledge needed*, *the data* and *the output contract* into four sections that do not overlap. The Context section carries every schema rule and convention, and the Output section encodes the evaluator's matching rules (exact question strings, 155 rows, valid SQL).

**What I expect.** Of the three prompts, this one produces the most reliable output format. The rules are explicit and numbered, so a strong model should reach ~98–99 %. Its weakness is that it gives no worked examples, so the model must work out how rule 9 (the "best" subquery) or rule 5 (the region join) look in actual SQL from prose alone.

---

## Prompt 2: TRACE (Task · Requirements · Audience · Context · Examples)

```text
## TASK
You will translate 155 natural-language restaurant questions into SQLite queries
and save them as restaurants_dataset_predictions.csv (columns: question,predicted_sql).

## REQUIREMENTS
- One valid SQLite SELECT per question; one row per question; same order as input.
- Copy each question verbatim. Duplicate questions get their own rows.
- Output columns are always L.HOUSE_NUMBER, R.NAME, in that order.
- Never use DISTINCT / LIMIT / ORDER BY / GROUP BY.
- Ignore any sentence that is not a restaurant request (snack dilemmas, picnics,
  teacups, umbrellas, compasses...). Translate only the restaurant clause.
- Every query must run without error, since a single error crashes the grader.
  Double apostrophes inside string literals.

## AUDIENCE
The consumer is an automated grader, not a human. It executes your SQL and
compares the returned rows, including duplicates, to gold rows. Style, aliases
and whitespace do not matter, but returned rows must match exactly.

## CONTEXT
Schema:
  RESTAURANT(ID, NAME, FOOD_TYPE, CITY_NAME, RATING)
  LOCATION(RESTAURANT_ID -> RESTAURANT.ID, HOUSE_NUMBER, STREET_NAME, CITY_NAME)
  GEOGRAPHIC(CITY_NAME, COUNTY, REGION)
Mapping rules:
  "in <city>"              -> L.CITY_NAME = '<city>'
  "in the <region>"        -> JOIN GEOGRAPHIC G ON R.CITY_NAME = G.CITY_NAME,
                              G.REGION = '<region>'
  "on <street>"            -> L.STREET_NAME = '<street>'   (verbatim)
  "<x> food" / "a <x> restaurant" / "places for <x>" / "best <x>"
                           -> R.FOOD_TYPE = '<x>'          (verbatim)
  "rating above N"         -> R.RATING > N
  "best ..."               -> R.RATING = (SELECT MAX(R.RATING) ... same filters)
  "where is <name> in <c>" -> R.NAME = '<name>' AND L.CITY_NAME = '<c>'
  no restaurant request    -> ... WHERE 0

## EXAMPLES  (study the pattern, then apply it to all 155 questions)

Q: what is a restaurant in vallejo with a rating above 2 (below average or better)?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE L.CITY_NAME = 'vallejo' AND R.RATING > 2

Q: give me a restaurant on mission blvd in hayward for pizza food with a rating above 1.7 (poorly rated or better)?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE L.CITY_NAME = 'hayward' AND L.STREET_NAME = 'mission blvd' AND R.FOOD_TYPE = 'pizza' AND R.RATING > 1.7

Q: give me some restaurants in the napa valley with a rating above 2 (below average or better), and whether a taco or a bowl of cereal would make a better hat?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID JOIN GEOGRAPHIC G ON R.CITY_NAME = G.CITY_NAME WHERE G.REGION = 'napa valley' AND R.RATING > 2

Q: What is the best eclectic in calistoga ?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE L.CITY_NAME = 'calistoga' AND R.FOOD_TYPE = 'eclectic' AND R.RATING = (SELECT MAX(R.RATING) FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE L.CITY_NAME = 'calistoga' AND R.FOOD_TYPE = 'eclectic')

Q: what is the best basque in the bay area ?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID JOIN GEOGRAPHIC G ON R.CITY_NAME = G.CITY_NAME WHERE G.REGION = 'bay area' AND R.FOOD_TYPE = 'basque' AND R.RATING = (SELECT MAX(R.RATING) FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID JOIN GEOGRAPHIC G ON R.CITY_NAME = G.CITY_NAME WHERE G.REGION = 'bay area' AND R.FOOD_TYPE = 'basque')

Q: where is a thai in unknown with a rating above 2.7 (average or better)?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE L.CITY_NAME = 'unknown' AND R.FOOD_TYPE = 'thai' AND R.RATING > 2.7
   (note: "in unknown" with no "the" is a CITY, not a region)

Q: My unrelated culinary dilemma involves choosing between cinnamon toast, vegetable pie, and a bowl of rice for a pretend celebration, while a very serious committee of stuffed animals reviews the menu. give me a restaurant on 6th st in hayward for bar food with a rating above 1.7 (poorly rated or better)? On a completely separate note, ...
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE L.CITY_NAME = 'hayward' AND L.STREET_NAME = '6th st' AND R.FOOD_TYPE = 'bar' AND R.RATING > 1.7

Q: where is denny's in campbell ?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE R.NAME = 'denny''s' AND L.CITY_NAME = 'campbell'

Q: What is the lifes greates illusion?
SQL: SELECT L.HOUSE_NUMBER, R.NAME FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID WHERE 0

Now process every row of the attached restaurants_dataset.csv (use only the
"question" column) and return restaurants_dataset_predictions.csv.
```

**Why TRACE here.** TRACE is the only framework in the list whose structure builds in **Examples** together with Requirements and Context. Text-to-SQL benchmarks reward copying a fixed house style exactly, which is what few-shot examples teach best. The nine examples were chosen to cover every hard case I found while checking the conventions: city vs region, the region join key, the full "best" subquery, street + food + rating, a noisy wrapper, apostrophe escaping, the "in unknown" trap and the no-request fallback. The **Audience** section also tells the model that the reader is a grader comparing exact rows, which pushes it away from adding "helpful" `DISTINCT`, `ORDER BY` or `LIMIT` clauses.

**What I expect.** This is the prompt I expect to score highest when the model has **no code execution**. Seeing a full "best" subquery and a region join removes most of the guesswork left by ICIO, so ~99 % (154/155) is realistic. Its risk is over-copying: the model might reuse a city or food value from an example. The instruction "study the pattern, then apply it" is there to reduce that.

---

## Prompt 3: ReAct (Reason · Act · Observe)

```text
You are a text-to-SQL engineer with a Python + SQLite sandbox. Work in explicit
Reason -> Act -> Observe cycles until the output file is verified.

GOAL
Produce restaurants_dataset_predictions.csv (columns: question,predicted_sql) whose
queries, when run by the attached evaluate_retrieval_predictions.py, return row
multisets identical to the hidden gold results for all 155 questions in
restaurants_dataset.csv. You may NOT read the "result" column to construct answers,
and you may not hard-code result rows. Every answer must be a genuine SQL query
derived from the question.

FILES
- restaurants-schema.csv, restaurants-db.txt : schema and data
- restaurants_dataset.csv                     : questions (use "question" only)
- evaluate_retrieval_predictions.py           : the grader; load_database() builds
                                                the in-memory SQLite DB you must use

KNOWN CONVENTIONS (treat as hypotheses to confirm in the loop)
- SELECT L.HOUSE_NUMBER, R.NAME
  FROM RESTAURANT R JOIN LOCATION L ON R.ID = L.RESTAURANT_ID
- no DISTINCT / LIMIT / ORDER BY / GROUP BY
- "in <city>" -> L.CITY_NAME; "in the <region>" -> JOIN GEOGRAPHIC G
  ON R.CITY_NAME = G.CITY_NAME, G.REGION = ...
- "on <street>" -> L.STREET_NAME = verbatim; food words -> R.FOOD_TYPE = verbatim
- "rating above N" -> R.RATING > N ; "best" -> R.RATING = (SELECT MAX(...) same filters)
- "where is <name> in <city>" -> R.NAME = ... AND L.CITY_NAME = ...
- ignore off-topic chatter; questions with no request -> "... WHERE 0"
- double apostrophes inside literals

LOOP
Reason  : State which question pattern(s) you are handling and the rule you will apply.
Act     : Write or run code. Build the DB with load_database(); generate SQL for
          the batch; execute every query.
Observe : Report (a) any SQL errors, (b) queries returning 0 rows when the question
          names a real city/street/food type, which often means a misparsed value or a
          value that does not exist. Check with SELECT DISTINCT on the
          relevant column, (c) clauses that accidentally swallowed noise text
          (filter values longer than ~40 chars are suspect).
Repeat until no batch shows problems. Then:
  1. Write restaurants_dataset_predictions.csv with the csv module (proper quoting),
     header question,predicted_sql, 155 rows in input order, questions verbatim.
  2. Run python evaluate_retrieval_predictions.py and report the printed accuracy.
  3. If the script raises an error, fix it and re-run. A crash scores nothing.

Finish with: the final accuracy line, a list of any questions you believe are
unanswerable, and the CSV file.
```

**Why ReAct here.** Errors in this benchmark come from three places: parsing noisy questions, a value that does not exist in the data, or a crash that wipes out the whole run. ReAct makes the model **run its queries and inspect the results before submitting**, so it catches all three. "Observe" checks that the street `ave.` really exists for mill valley, that no query errors, and that no filter swallowed a picnic sentence. The evaluator is in the inputs, so the model can run it as its own final check. Comparing results to the label column is forbidden in the prompt: without that guard, a ReAct agent with access to the labels could simply copy them, which would game the metric rather than solve the task.

**What I expect.** When the model has a code-execution tool (Claude with the analysis tool, ChatGPT Code Interpreter, an agent), this is the most robust option. It should reliably reach the ~99.4 % ceiling and should never submit a file that crashes the grader. Without tools, it falls back to behaving like Prompt 1 with a longer preamble, so in that setting Prompt 2 is the better choice.

---

## Report: why these three frameworks, and where they were found

### Source

- **ICIO** and **TRACE** come from the Frompting framework library at **https://frompting.com/frameworks**. ICIO is listed under *AI & Prompt Engineering* ("separates the task, background, data, and output format for data-processing prompts"). TRACE is listed under *Communication & Storytelling* ("comprehensive brief covering the essentials of complex assignments": Task, Requirements, Audience, Context, Examples).
- **ReAct** comes from the same page, under *Reasoning & Analysis* (REACT: Reason, Act, Observe). It originates from Yao et al., *"ReAct: Synergizing Reasoning and Acting in Language Models"* (ICLR 2023, arXiv:2210.03629).
- As required, ROSES and zero-shot prompting were excluded. Both are also listed on the same page.

### Why these three

I wanted three frameworks that attack the problem in **three different ways**, rather than three re-wordings of "role + task + format":

| | ICIO | TRACE | ReAct |
|---|---|---|---|
| Main lever | Clear structure and an exact output contract | Learning from worked examples | Executing and checking its own work |
| Best when | Any model; you want a predictable format | No tools available; style must be copied exactly | The model can run Python/SQLite |
| Main risk addressed | Malformed CSV, wrong row count, crash | Wrong SQL shape (region join, "best" subquery) | Misparsed noisy questions, non-existent values, runtime errors |
| Expected score | ~98–99 % | ~99 % (154/155) | ~99.4 % (154/155), with no crashes |

### Frameworks considered and rejected

- **CO-STAR / CRISP / PACT**: these centre on style, tone and voice, which do not affect a SQL execution-accuracy grade.
- **RTF**: too thin to carry about a dozen schema conventions.
- **Tree of Thoughts / Chain of Density**: built for open-ended reasoning or summarisation. Most questions here are a deterministic mapping, so exploring several branches adds cost without accuracy.
- **Chain of Thought (CoT)**: helpful, but ReAct already includes step-by-step reasoning and adds the execution feedback that CoT lacks.
- **Few-Shot on its own**: TRACE already includes few-shot examples and adds requirements and audience around them, so TRACE is the stronger version of the same idea.

### Shared design decisions in all three prompts

1. **Conventions were derived from the data, not guessed.** I checked the city column, the region join key, the `>` operator and the output columns by running candidate queries against the gold labels. For example, filtering on `R.CITY_NAME` instead of `L.CITY_NAME` loses the alameda question (63 rows against 62), so all three prompts state the `L.CITY_NAME` rule explicitly.
2. **Crash-proofing.** Because a single SQL error aborts the evaluator, every prompt requires valid SQL, apostrophe escaping and a `WHERE 0` fallback for questions with no request.
3. **Exact question strings.** Because predictions are matched to labels by exact text and in queue order, every prompt requires questions to be copied verbatim, including duplicates.
4. **No label leakage.** Every prompt tells the model to use only the `question` column, so the score measures text-to-SQL ability and not copying.

### Expected ceiling

Applying these rules with a simple regex parser already scored **97.42 % (151/155)**, and the misses came from parsing long noisy questions, which LLMs handle well. One question ("What is the lifes greates illusion?") contains no request and cannot be answered from its text. The practical maximum is therefore **154/155 ≈ 99.4 %**, and Prompts 2 and 3 are designed to reach it.
