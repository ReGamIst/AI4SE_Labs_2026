---
name: architecture-options
description: Turn a system brief (feature list + user stories) into a shared domain model, three contrasting architecture proposals, a comparison and recommendation, running conversation notes, and an ADR once the user picks one.
---

# Architecture options from a system brief

Use this skill when the user shares a product/system description (features, user stories, roles) and asks how it could be built, which architecture to use, or to compare implementation approaches. It also covers the follow-ups that usually come next: deep dives into one option, A-vs-B explanations, and recording the decision as an ADR.

## Outputs

1. **Conversation Notes** document (always) — living record of the analysis and every later message.
2. **ADR-NNN** document (only once the user chooses an option) — separate file, linked from the notes.
3. Chat replies for explanations and deep dives; the notes get a one-row summary of each.

Write notes and ADRs as Markdown documents (or the session's document type). Title them `<Project> – Conversation Notes` and `ADR-001: <Decision> for <Project>`. Date + author line under the title: `Mon DD, YYYY · @<user>`.

## Workflow

### 1. Read the brief and map the stories

- List every user story with its number. Group by role (e.g. customer, worker, admin).
- Build a **role table**: Role | Stories (ranges, e.g. `1–13, 32, 35`) | Key capabilities.
- Count stories per role and check the counts sum to the total. Stories in a brief are often out of order (e.g. admin stories appear in two blocks) — use the numbers, not the position.
- Note features in the description that aren't covered by any story (e.g. "search by skill and location" may only appear in the feature list) and carry them into the design anyway.

### 2. Derive the domain model (shared by all options)

- One table: Entity | Main fields | Relations. Keep it to the entities the stories actually need; say "N entities cover every story".
- Include status enums where a lifecycle exists (e.g. request: pending / accepted / rejected / cancelled).
- Map stories to entities mentally; every story must touch at least one entity.
- Record **open questions** the brief leaves unanswered (e.g. "can a customer review a worker without an accepted request?"). Propose a sensible default, but flag it — don't silently decide.

### 3. Propose three genuinely different architectures

Default trio (adapt if the brief clearly calls for something else, e.g. serverless or mobile-first):

| Option | Shape | Fits |
| --- | --- | --- |
| A: Layered monolith (server-rendered MVC) | One app, one DB, HTML rendered server-side | Course project, MVP, solo dev |
| B: REST API + SPA | Stateless JSON API + separate frontend | Web + mobile, split frontend/backend work |
| C: Microservices, event-driven | Service per capability, DB per service, gateway, broker | Large scale, many teams |

For **each** option, give the same sections so they compare cleanly:

- One-paragraph summary + who it's for.
- **Stack** (2–3 concrete choices, e.g. Django / Spring Boot / Laravel).
- **Structure**: modules or services named after the brief's bounded areas (accounts, catalogue, requests, Q&A, reviews, admin…).
- **Auth**: sessions vs JWT vs OIDC; where role checks are enforced (always server-side).
- **How admin stories are covered** (e.g. Django admin covers most for free in A; hand-built in B and C).
- **Search / data / messaging** specifics; for C give 2–3 named example events tied to real stories (e.g. `ReviewPosted` → update average rating).
- **Deployment** (one VPS + Docker Compose → PaaS/CDN → Kubernetes).
- **Pros / Cons** in one or two lines each.

### 4. Compare and recommend

- Comparison table with criteria as rows and options as columns: build effort, codebases, admin stories, mobile-ready, scaling, consistency, ops cost, best for.
- Give a conditional recommendation ("B if a mobile app is expected; otherwise A; C only once traffic or team size justifies it").
- Mention the middle path: a modular monolith with module boundaries matching C's services, split later only if needed.
- Ask (or note as open) the facts that would flip the recommendation: team size, mobile plans, expected traffic, existing skills, deadline/budget.

### 5. Start the Conversation Notes

Sections, in order:

1. **Context** — one paragraph on the product, the role table, and the user's ask with its date.
2. **Domain model** — entity table + open questions.
3. **Architecture A / B / C** — as in step 3.
4. **Comparison and recommendation** — table + recommendation. When a decision is made, put a `Decision (<date>): <user> chose X, recorded in ADR-NNN.` line at the top of this section and keep the original recommendation below it.
5. **Conversation log** — table `Date | Message | Outcome`, **newest first**, ending with the line "New rows are added as the conversation continues."

### 6. Handle follow-ups, and log every one

Typical follow-ups and how to answer them:

- **"Explain C in detail"** → walk through each component (gateway, identity, each domain service, DB-per-service, broker + events, search, frontend/BFF, observability), then trace 1–2 concrete stories end to end as event flows, then compare with A and B on effort, consistency, failure modes, ops.
- **"What's the difference between A and B?"** → where HTML is rendered, request flow, auth (sessions vs tokens), admin, codebases, deployment, SEO, testing; trace one story through both.
- **"I choose X"** → write the ADR (step 7), update the decision line, log it.

After each user message that changes or adds to the analysis, add one row to the log: what was asked (with the user's stated reasons) → what was produced. Summarise; don't paste the full answer into the notes.

### 7. Write the ADR when a choice is made

Separate document. Sections:

- **Title + one-sentence decision** under the date line.
- **Status** table: Status (Proposed / Accepted / Superseded), Decided (date), Decider, Supersedes.
- **Context**: product, story counts by role, team size, relevant experience, absent requirements (no mobile, low traffic…).
- **Decision drivers**: numbered list, drawn from what the user actually said (e.g. "one developer", "prior experience with this architecture") plus brief-derived ones (admin cost, consistency, hosting cost, SEO).
- **Considered options**: table Option | Summary | Pros | Cons, chosen one bolded and marked "(chosen)". Give rough relative effort (e.g. B ~1.5x, C ~4–5x of A).
- **Decision**: stack, modules, layers, auth, admin, search, deployment — concrete enough to start building.
- **Consequences**: Positive / Negative / Mitigations (e.g. keep business logic in service functions so an API can reuse it; respect module boundaries to keep extraction possible).
- **Revisit when**: concrete triggers that would move toward the other options.
- **Related**: link back to the Conversation Notes.

## Quality checks before delivering

- Story counts per role add up to the total; every role and story range appears in the role table.
- All three options cover every story group, especially admin and auth.
- Same section structure across A, B and C; comparison table has no empty cells.
- Dates are absolute (e.g. 27 Oct 2026), not "today".
- Recorded reasons and decisions are the user's own words; your recommendations are labelled as recommendations.
- Open questions are listed, not quietly resolved.
- Log is newest-first and has a row for every substantive message.

## Style

- Tables for anything compared across roles, entities or options; short bullets elsewhere.
- Concrete technology names, not "some framework".
- Keep each option section to roughly one screen; deep dives go in chat, not in the notes.
