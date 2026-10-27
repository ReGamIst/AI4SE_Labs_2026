# ADR-001: Layered monolith for RentYourExpert

Oct 27, 2026 · @Alex

RentYourExpert will be built as a single server-rendered Django application (Architecture A), structured as a modular monolith.

## Status

| Field | Value |
| --- | --- |
| Status | Accepted |
| Decided | 27 Oct 2026 |
| Decider | Alex (sole developer) |
| Supersedes | — |

## Context

RentYourExpert is a marketplace connecting customers with expert workers. The brief defines 35 user stories across three roles: customer (15), worker (7) and admin (13). Core entities are users, worker and customer profiles, requests, questions/answers and reviews.

The platform is built and maintained by one developer who already has experience with server-rendered MVC applications in Django. There is no stated need for a mobile app, high traffic or independent teams.

## Decision drivers

1. One developer: minimise codebases, moving parts and operational work.
2. Existing experience with this architecture: lower risk and faster delivery.
3. Cover all 35 stories quickly; 13 admin stories should cost as little as possible.
4. Simple data consistency: cascade deletes and rating averages in one transaction.
5. Cheap hosting: one VPS.
6. Public catalogue should be indexable by search engines.

## Considered options

| Option | Summary | Pros | Cons |
| --- | --- | --- | --- |
| **A: Layered monolith (chosen)** | One Django app, server-rendered templates, one PostgreSQL DB | 1 codebase; Django admin covers most admin stories; simple transactions; good SEO; cheapest to host; matches existing skills | Coupled UI and backend; full page reloads; API needed later for mobile |
| B: REST API + SPA | DRF/FastAPI JSON API, separate React/Vue frontend, JWT | Clean separation; mobile-ready; app-like UI | 2 codebases; auth/CORS plumbing; admin UI built by hand; \~1.5x effort |
| C: Microservices, event-driven | \~8 services with own DBs, API gateway, message broker, OpenSearch, Kubernetes | Independent scaling and deployment; fault isolation | Eventual consistency; distributed debugging; high ops cost; \~4–5x effort; built for multiple teams |

## Decision

Chosen: **Option A**, a server-rendered Django monolith, organised as a modular monolith so modules could later be extracted.

- **Stack:** Django, PostgreSQL, Django templates + Bootstrap, HTMX for partial updates (e.g. accept/reject, posting a question).
- **Apps (modules):** `accounts` (custom User with role), `catalogue` (worker profiles, search), `customers`, `requests`, `qa`, `reviews`.
- **Layers:** views → service functions (business rules) → models. Views stay thin; rules like "only the target worker can accept a request" live in services.
- **Auth:** Django sessions, built-in password hashing, CSRF protection, role checks via permission mixins/decorators.
- **Admin:** Django admin for customers, workers, requests, reviews and questions (stories 14–22, 29–31, 34).
- **Search:** ORM filters on skill and location; PostgreSQL full-text search if needed.
- **Deployment:** Docker Compose (app + Postgres), Gunicorn behind Nginx on one VPS.

## Consequences

**Positive**

- Fastest path to all 35 stories; Django admin removes most admin UI work.
- One codebase, one deploy, one database: easy to test, debug and back up.
- Cascade deletes and rating averages are consistent within one transaction.
- Server-rendered catalogue and worker pages are SEO-friendly.

**Negative**

- UI and backend are coupled; a mobile client would need an API added.
- Less interactive than an SPA without extra work.
- Scales vertically first; horizontal scaling needs shared sessions/cache.

**Mitigations**

- Keep business logic in service functions, not views, so a DRF API can reuse it later.
- Use HTMX where interactivity matters.
- Respect module boundaries (no cross-app model imports beyond foreign keys) to keep extraction possible.

## Revisit when

- A mobile app or third-party integration is planned → add a DRF API next to the templates (move toward B).
- More developers join, or one area (e.g. search) needs to scale independently → extract that module (toward C).

Related: RentYourExpert – Conversation Notes (comparison of A, B and C).
