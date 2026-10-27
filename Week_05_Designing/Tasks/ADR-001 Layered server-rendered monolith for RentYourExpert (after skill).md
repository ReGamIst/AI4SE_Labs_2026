# ADR-001: Layered server-rendered monolith for RentYourExpert

Oct 27, 2026 · @Alex

RentYourExpert will be built as a single Django application with server-rendered pages, one PostgreSQL database and Django admin for back-office work.

## Status

| Field | Value |
| --- | --- |
| Status | Accepted |
| Decided | 27 Oct 2026 |
| Decider | Alex (sole developer) |
| Supersedes | None |

## Context

RentYourExpert connects customers with skilled workers, searchable by skill and location, with Q&A, requests, reviews and an admin back office. The brief has 35 user stories: 15 customer, 7 worker, 13 admin.

- **Team:** one developer (Alex), who has implemented a similar layered server-rendered architecture before.
- **Absent requirements:** no mobile app, no stated traffic targets, no payments, no separate frontend team.
- **Analysis:** three options were compared in the Conversation Notes: A layered monolith, B REST API + SPA, C event-driven microservices.

## Decision drivers

1. **Single developer** (Alex's stated reason): one codebase and one deploy to build, run and debug.
2. **Prior experience** (Alex's stated reason): Alex has already implemented a similar architecture, which lowers delivery risk.
3. **Admin cost:** 13 of 35 stories are admin CRUD; a built-in admin covers most of them without UI work.
4. **Consistency:** cascades such as deleting a customer (story 18) and updating a worker's rating after a review (11, 12, 31) are simplest as single database transactions.
5. **Hosting cost:** one small VPS instead of a CDN + API host or a Kubernetes cluster.
6. **SEO:** public worker pages should be indexable without extra server-side rendering work.

## Considered options

| Option | Summary | Pros | Cons |
| --- | --- | --- | --- |
| **A: Layered monolith (chosen)** | One Django app, server-rendered HTML, one PostgreSQL DB. Effort 1x | One codebase, ACID transactions, Django admin covers admin stories, SEO by default, cheapest hosting | No API for mobile out of the box; vertical scaling; limited UI interactivity |
| B: REST API + SPA | JSON API + React SPA, JWT auth. Effort \~1.5x | Mobile-ready, richer UI, clean frontend/backend split | Two codebases and deploys, hand-built admin, token and CORS handling, SEO needs SSR |
| C: Microservices, event-driven | Gateway, Keycloak, 6–7 services, broker, DB per service, OpenSearch, Kubernetes. Effort \~4–5x | Independent scaling and deploys, fault isolation, team autonomy, strong search | Eventual consistency, sagas for cascades, distributed failures, high ops cost; oversized for 35 stories and one developer |

## Decision

Build RentYourExpert as a modular, layered Django monolith.

- **Stack:** Python 3.12, Django 5, Django templates + HTMX, PostgreSQL 16.
- **Modules (Django apps):** `accounts` (custom User with role, CustomerProfile, WorkerProfile, registration, login/logout), `catalogue` (Skill, worker list, worker page, search), `requests` (Request lifecycle), `qa` (Question, Answer), `reviews` (Review, rating aggregate), `staff` (admin customisations).
- **Layers in each app:** views (HTTP, forms, templates) → services (business rules, transactions) → models (ORM). Views never touch another app's models directly; they call that app's services.
- **Auth:** Django sessions with CSRF protection; `role` field on User; access enforced server-side with `login_required` and role mixins; ownership checks (own review, own request) in services.
- **Admin (stories 14–22, 29–31, 34):** Django admin with ModelAdmin classes for customers, workers, requests, reviews and questions (answers inline); a separate admin role, not the Django superuser, for day-to-day use.
- **Search:** ORM filtering by skill and city with database indexes, paginated; PostgreSQL full-text on bio when needed.
- **Rating:** `avg_rating` and `review_count` on WorkerProfile, updated in the same transaction as review create, update or delete.
- **Deployment:** one VPS, Docker Compose with Gunicorn + Django, PostgreSQL and Caddy (TLS, static files); nightly `pg_dump` backups.

## Consequences

**Positive**

- Fastest path to all 35 stories; most admin stories need configuration, not UI work.
- Every cascade and rating update is one transaction, so no stale or half-applied data.
- One repository, one test suite, one deploy; low hosting cost.
- Worker pages are server-rendered HTML and indexable.

**Negative**

- No public API; a mobile app would need one added.
- Scaling is vertical plus app replicas behind one database.
- Interactive UI is limited to what HTMX offers.
- Without discipline, apps can become tangled and hard to split later.

**Mitigations**

- Keep business logic in service functions, so a DRF API can reuse them without rewriting rules.
- Respect module boundaries: apps call each other's services and reference other apps' data by ID where practical, keeping extraction into services possible.
- Keep Gunicorn stateless (sessions in the DB or Redis) so app replicas can be added behind Caddy.

## Revisit when

- A mobile app or third-party integration is planned → add a DRF API over the existing services (toward B).
- A dedicated frontend developer joins or the UI needs rich client-side interaction → consider an SPA (B).
- Search needs full-text ranking, facets or geo radius beyond PostgreSQL → add OpenSearch alongside the monolith.
- Traffic outgrows one database server, or several teams need independent deploys → extract the hottest module into a service (toward C).
