# RentYourExpert – Conversation Notes

Oct 27, 2026 · @Alex

## Context

RentYourExpert is a marketplace where customers find, question, hire and review skilled workers, searchable by skill and location, with an admin who manages customers, workers, requests, reviews and Q&A. The brief has 35 user stories across three roles; Alex is building it as a single developer.

| Role | Stories | Count | Key capabilities |
| --- | --- | --- | --- |
| Customer | 1–13, 32, 35 | 15 | Register, log in/out, edit profile, browse catalogue and worker pages, send and delete requests, ask questions, read Q&A and reviews, post/edit/delete reviews |
| Worker | 23–28, 33 | 7 | Register, log in, edit profile, see requests, accept/reject requests, answer questions |
| Admin | 14–22, 29–31, 34 | 13 | Log in, list/view/add/delete customers and workers, view/add/delete requests, delete reviews, delete questions with their answers |
| **Total** |  | **35** |  |

Not covered by any story but in the feature list: **search by skill and location** (stories 4–5 only say "catalogue"). It is carried into every option below. Story 14 says "e-commerce"; read as "the platform".

**Ask (27 Oct 2026):** propose three different architectural implementations, following the architecture-options skill, and keep notes on the whole conversation including later messages.

## Domain model

Eight entities cover every story and are shared by all three options; only where they live changes (one schema in A and B, split per service in C).

| Entity | Main fields | Relations |
| --- | --- | --- |
| User | email, password hash, role (customer / worker / admin), is\_active, created\_at | 1–1 CustomerProfile or WorkerProfile |
| CustomerProfile | name, phone, city | User; has many Requests, Questions, Reviews |
| WorkerProfile | name, bio, city, hourly rate, avg\_rating, review\_count | User; many-to-many Skill; has many Requests, Questions, Reviews |
| Skill | name, slug | many-to-many WorkerProfile |
| Request | description, preferred date, status (pending / accepted / rejected / cancelled / completed), created\_at | Customer → Worker |
| Question | text, created\_at | Customer → Worker; has 0..n Answers |
| Answer | text, created\_at | Question; written by the Worker |
| Review | rating 1–5, text, created\_at, updated\_at | Customer → Worker; optionally linked to a Request |

**Open questions** (defaults proposed, not decided):

- Can a customer review a worker without an accepted/completed request? *Default: only after an accepted request, one review per request.*
- Does "delete request" (story 8) work after the worker accepted it? *Default: pending → deleted; accepted → status cancelled.*
- What does "location" mean: city text or geo radius? *Default: city field; geo search later.*
- Are prices, payments or messaging beyond Q&A in scope? *Default: no payments; hourly rate is display-only.*
- Can admins create requests on behalf of customers (story 22), and do deletions cascade (story 18: customer's requests and reviews)? *Default: yes to both, with soft delete.*
- Do workers need approval before appearing in the catalogue? *Default: no.*

## Architecture A: Layered monolith (server-rendered MVC)

One application, one database, HTML rendered on the server. The browser sends form posts and page requests; the app runs business logic and returns finished pages. Fits a course project, an MVP, or a solo developer.

- **Stack:** Django 5 + Django templates + HTMX (alternatives: Spring Boot + Thymeleaf, Laravel + Blade); PostgreSQL.
- **Structure:** one project, one app per area: `accounts` (User, profiles, registration), `catalogue` (Skill, worker list, worker page, search), `requests`, `qa` (Question, Answer), `reviews`, `staff` (custom admin views if needed). Layers inside each app: views → services (business rules) → models.
- **Auth:** Django session cookies, CSRF on every form, custom `User` with a `role` field. Role checks server-side via `@login_required` + role mixins (`CustomerRequiredMixin`, `WorkerRequiredMixin`); object ownership checked in services (only the author edits a review).
- **Admin stories (14–22, 29–31, 34):** Django admin covers list/view/add/delete for customers, workers, requests, reviews and questions out of the box; cascade rules live on the models. Roughly zero UI work.
- **Search/data:** catalogue filters with ORM queries on skill + city, indexes on both; PostgreSQL full-text for bio later. `avg_rating` updated in the same transaction as review save/delete.
- **Deployment:** one VPS with Docker Compose: Gunicorn + Django, PostgreSQL, Caddy/Nginx for TLS and static files; nightly `pg_dump`.
- **Pros:** fastest to build, one codebase, ACID transactions everywhere, admin nearly free, good SEO by default.
- **Cons:** no API for a future mobile app without extra work; scales vertically and by replicas only; UI interactivity limited to HTMX-level.

## Architecture B: REST API + SPA

A stateless JSON API owns all data and rules; a separate single-page app renders the UI in the browser. The same API can later serve a mobile app. Fits teams that split frontend and backend, or products that expect web + mobile.

- **Stack:** Django REST Framework or NestJS (alternative: Spring Boot) for the API; React + Vite or Next.js for the SPA; PostgreSQL; OpenAPI spec generated from the API.
- **Structure:** API modules mirror A's apps: `/auth`, `/customers`, `/workers` (+ `/workers/{id}/questions`, `/workers/{id}/reviews`), `/requests`, `/questions/{id}/answers`, `/skills`. SPA routes: catalogue, worker page, my profile, my requests, worker dashboard, admin area.
- **Auth:** short-lived JWT access token + refresh token in an httpOnly cookie (or same-site session cookies if the SPA shares the domain). Every endpoint enforces role and ownership in permission classes; the SPA only hides buttons.
- **Admin stories:** hand-built admin section in the SPA (or React-Admin on top of the same API), with `admin`-only endpoints for create/delete of customers, workers, requests, reviews, questions.
- **Search/data:** `GET /workers?skill=&city=&page=` with server-side filtering and pagination; same transaction for review + `avg_rating`.
- **Deployment:** API container on a VPS or PaaS (Render, Fly.io); SPA as static files on a CDN (Cloudflare Pages, Netlify); CORS configured between them.
- **Pros:** mobile-ready, clean frontend/backend split, richer UI, API testable in isolation.
- **Cons:** two codebases and two deploys, token handling and CORS to get right, admin UI built by hand, SEO needs SSR (Next.js) for public worker pages.

## Architecture C: Microservices, event-driven

One service per capability, each with its own database, behind an API gateway; services react to each other through events on a message broker. Fits large scale, independent deploys and several teams.

- **Stack:** services in Spring Boot, Go or NestJS; Keycloak for identity; Kong or Traefik as gateway; RabbitMQ or Kafka as broker; PostgreSQL per service; OpenSearch for search; React/Next.js frontend with a BFF.
- **Structure:** Identity (Keycloak), Profiles (customers + workers), Catalogue/Search (read model in OpenSearch), Requests, Q&A, Reviews, plus an Admin BFF that fans out to the others. Notifications service optional.
- **Auth:** OIDC via Keycloak; gateway validates JWTs, each service re-checks roles and ownership from token claims.
- **Admin stories:** Admin BFF + hand-built admin UI; deleting a customer (story 18) becomes a `CustomerDeleted` event that Requests, Q&A and Reviews each handle.
- **Events (examples):** `ReviewPosted` / `ReviewDeleted` (stories 11, 12, 31) → Profiles recalculates `avg_rating`, Search reindexes the worker · `WorkerProfileUpdated` (story 28) → Search updates the catalogue · `RequestStatusChanged` (story 24) → Notifications emails the customer. Outbox pattern for reliable publishing.
- **Search/data:** no cross-service joins; catalogue reads from the OpenSearch projection; consistency is eventual (a new review shows in the rating after the event lands).
- **Deployment:** Kubernetes (managed, e.g. DOKS/GKE) with a CI pipeline per service; OpenTelemetry tracing, Prometheus + Grafana, centralized logs.
- **Pros:** independent scaling and deploys, fault isolation, team autonomy.
- **Cons:** several times the build effort, distributed failures and eventual consistency to handle, high ops cost; far beyond what 35 stories need today.

## Comparison and recommendation

**Decision (27 Oct 2026):** Alex chose A, the layered server-rendered monolith, recorded in ADR-001: Layered server-rendered monolith for RentYourExpert. The original comparison and recommendation are kept below.

&#91;embedded content: three architectures side by side · same 8-entity domain\]

All three cover every story group; they differ in how many pieces you build, deploy and keep consistent.

| Criterion | A: Monolith | B: API + SPA | C: Microservices |
| --- | --- | --- | --- |
| Build effort (relative) | 1x | \~1.5x | \~4–5x |
| Codebases / deploys | 1 / 1 | 2 / 2 | 6–8 / 6–8 |
| Admin stories (13) | Mostly free via Django admin | Hand-built admin screens | Hand-built UI + Admin BFF + cascade events |
| Mobile-ready | No; add an API later | Yes | Yes |
| Scaling | Vertical + app replicas | API replicas + CDN for the UI | Per service |
| Consistency | ACID, one database | ACID, one database | Eventual across services |
| Ops cost | One small VPS | VPS or PaaS + static host | Managed Kubernetes, broker, several DBs, observability |
| SEO for worker pages | Built in | Needs SSR (Next.js) | Needs SSR |
| Best for | Solo dev, MVP, course project | Web + mobile, split frontend/backend | High traffic, several teams |

**Recommendation (Claude's, not yet a decision):** A for a single developer with no mobile app in the brief. B if a mobile app or a separate frontend developer is expected. C only once traffic or team size justifies it.

**Middle path:** build A as a modular monolith whose apps match C's service boundaries (accounts/profiles, catalogue, requests, qa, reviews), keep business logic in service functions, and let apps reference each other by ID only. An API (B) or a service split (C) can then be added later without a rewrite.

**Facts that would flip it:** a planned mobile app, team size, expected traffic, deadline and budget, and which stack is most familiar (Django vs Java vs Node).

## Conversation log

| Date | Message | Outcome |
| --- | --- | --- |
| 27 Oct 2026 | Chose A because "I am a single developer" and "already have experience with implementing a similar architecture"; asked for an ADR in a separate file | ADR-001: Layered server-rendered monolith for RentYourExpert written (status Accepted); decision line added to Comparison and recommendation |
| 27 Oct 2026 | Asked for a detailed explanation of C and its components, compared with A and B | Chat deep dive: gateway, identity, six domain services, DB per service, broker + outbox events, search read model, frontend/BFF, observability; stories 11 (post review) and 18 (admin deletes customer) traced as event flows; comparison with A and B on effort, consistency, failure modes, ops |
| 27 Oct 2026 | Asked to explain the differences between A and B | Chat explanation: where HTML is rendered, request flow, auth (sessions vs JWT), admin, codebases, deployment, SEO, testing; story 6 (send a request) traced through both |
| 27 Oct 2026 | Shared the RentYourExpert brief (35 stories) and the architecture-options skill; asked for three architectural implementations and running notes on the conversation | Role table, 8-entity domain model with 6 open questions, Options A/B/C, comparison and recommendation; these notes started |

New rows are added as the conversation continues.
