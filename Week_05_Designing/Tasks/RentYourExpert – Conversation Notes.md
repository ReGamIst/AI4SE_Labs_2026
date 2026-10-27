# RentYourExpert – Conversation Notes

Oct 27, 2026 · @Alex

## Context

RentYourExpert is a marketplace connecting customers with expert workers. The brief (RentYourExpert.txt) lists six features and 35 user stories across three roles.

| Role | Stories | Key capabilities |
| --- | --- | --- |
| Customer | 1–13, 32, 35 | Register/login, browse catalogue, view worker page, send/delete requests, ask questions, write/edit/delete reviews |
| Worker | 23–28, 33 | Register/login, edit profile, view and accept/reject requests, answer questions |
| Admin | 14–22, 29–31, 34 | Manage customers, workers, requests; moderate reviews and Q&A |

Ask (27 Oct 2026): propose three different architectural implementations, and keep notes on the whole conversation, including later messages.

## Domain model

Six entities cover every story; all three architectures share them.

| Entity | Main fields | Relations |
| --- | --- | --- |
| User | email, password hash, role (customer / worker / admin), name | One-to-one with a profile |
| WorkerProfile | skills, location, bio, hourly rate | Belongs to a User; has many Requests, Questions, Reviews |
| CustomerProfile | phone, address | Belongs to a User; has many Requests, Reviews |
| Request | description, status (pending / accepted / rejected / cancelled), created\_at | Customer → Worker |
| Question | text, answer, answered\_at | Customer → Worker; answer written by the worker (story 33) |
| Review | rating 1–5, comment | Customer → Worker; one per completed request is a sensible rule |

Open question: should a customer only review a worker after an accepted request? The brief doesn't say.

## Architecture A: Layered monolith (server-rendered MVC)

One deployable app renders HTML on the server and talks to one database. Fastest to build; the right fit for a course project or MVP.

- **Stack:** Django (or Spring Boot + Thymeleaf, or Laravel), PostgreSQL, Bootstrap/HTMX for interactivity.
- **Structure:** one app per bounded area — `accounts` (users, roles), `catalogue` (worker profiles, search), `requests`, `qa` (questions/answers), `reviews`, `adminpanel`.
- **Layers:** views/controllers → service layer (business rules, e.g. "only the worker can accept a request") → ORM models → database.
- **Auth:** session cookies, built-in password hashing, role-based decorators/permissions (customer, worker, admin). Django admin can cover most admin stories (14–22, 29–31, 34) almost for free.
- **Search:** SQL filters on skill and location; PostgreSQL full-text search if needed.
- **Deployment:** Gunicorn + Nginx on one VPS, Docker Compose with app + Postgres.

Pros: least code, one codebase, simple transactions, easy to test end to end. Cons: UI and backend are coupled; a mobile app later needs an API added; scales vertically first.

## Architecture B: REST API backend + SPA frontend

A stateless JSON API serves a separate single-page app; the same API can later serve a mobile app.

- **Backend:** Django REST Framework, FastAPI, Spring Boot or NestJS; PostgreSQL; OpenAPI spec generated from the code.
- **Frontend:** React or Vue (Vite), React Router for pages (catalogue, worker page, profile, requests, admin), a query library (TanStack Query) for caching.
- **Auth:** JWT access + refresh tokens (or httpOnly session cookie), role claim checked by API permission classes; frontend hides buttons by role but the API enforces it.
- **Resources:** `/auth`, `/workers` (search with `?skill=&location=`), `/workers/{id}/questions`, `/workers/{id}/reviews`, `/requests` (PATCH status for accept/reject), `/admin/*`.
- **Extras:** pagination and filtering on lists, rate limiting on login, CORS config, file storage (S3/MinIO) for profile photos.
- **Deployment:** API container + static SPA on a CDN or Nginx; Docker Compose or a PaaS.

Pros: clean separation, frontend and backend can be built by different people, mobile-ready, easy to document and test the API. Cons: two codebases, more auth plumbing, admin UI must be built by hand.

## Architecture C: Microservices, event-driven

Each business capability is its own service with its own database, behind an API gateway, communicating through events. Built for scale and independent teams.

- **Services:** Identity (registration, login, roles, tokens), Worker Catalogue (profiles, skills, search), Customer, Request (lifecycle: pending → accepted/rejected/cancelled), Q&A, Review, Notification (email when a request or question arrives).
- **Edge:** API gateway (Kong, Traefik or Spring Cloud Gateway) validates JWTs and routes; one SPA frontend (React) or a BFF per client.
- **Data:** database per service (PostgreSQL); Elasticsearch/OpenSearch fed by catalogue events for skill + location search; Redis for caching.
- **Messaging:** RabbitMQ or Kafka. Example events: `ReviewPosted` → Catalogue updates the worker's average rating; `RequestCreated` → Notification emails the worker; `WorkerDeleted` → Request, Q&A and Review clean up.
- **Auth:** central identity provider (Keycloak or the Identity service), OAuth2/OIDC tokens, role checks in each service.
- **Ops:** Docker + Kubernetes, CI/CD per service, centralised logging and tracing (OpenTelemetry, Grafana).

Pros: services scale and deploy independently; fault isolation; search can grow separately. Cons: much higher complexity (distributed data, eventual consistency, ops cost); overkill for 35 stories unless scale or team size demands it.

## Comparison and recommendation

Decision (27 Oct 2026): Alex chose A, recorded in ADR-001. Original recommendation: B if a separate frontend or mobile app is expected; otherwise A. Treat C as the target only once traffic or team size justifies it.

| Criterion | A: Monolith | B: API + SPA | C: Microservices |
| --- | --- | --- | --- |
| Build effort | Low | Medium | High |
| Codebases | 1 | 2 | 7+ services + frontend |
| Admin stories | Mostly free (Django admin) | Build admin pages | Build admin pages |
| Mobile-ready | No (API needed) | Yes | Yes |
| Scaling | Vertical, then replicas | Horizontal API replicas | Per service |
| Consistency | Simple DB transactions | Simple DB transactions | Eventual, via events |
| Ops cost | One VPS | VPS/PaaS + CDN | Kubernetes, broker, monitoring |
| Best for | Course project, MVP | Product with web + mobile | Large scale, many teams |

A common path: build B as a modular monolith (one API, clear modules matching C's services), then split modules out only if needed.

## Conversation log

| Date | Message | Outcome |
| --- | --- | --- |
| 27 Oct 2026 | Alex chose Architecture A (single developer, prior experience with this architecture) and asked for an ADR in a separate file | Wrote ADR-001: Layered monolith for RentYourExpert (status Accepted) as a separate doc |
| 27 Oct 2026 | Alex asked for a detailed explanation of C and its components, compared with A and B | Explained gateway, identity, 6 domain services, database-per-service, message broker + events, search, frontend/BFF, observability; walked through stories 6 and 11 as event flows; compared C vs A vs B on effort, data consistency, failure modes, ops |
| 27 Oct 2026 | Alex asked to explain the differences between A and B | Explained: where HTML is rendered, request flow, auth (sessions vs tokens), admin, codebases, deployment, SEO, testing; walked through story 6 in both |
| 27 Oct 2026 | Alex shared RentYourExpert.txt and asked for 3 architectural implementations plus running notes on the conversation | Proposed A (layered monolith), B (REST API + SPA), C (microservices, event-driven); started this doc |

New rows are added as the conversation continues.
