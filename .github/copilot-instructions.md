# Copilot repository instructions

## Mission
Build the Janani backend as a secure, local-first, PostgreSQL-backed intelligence service for the Vasuki OS ecosystem.

## Operating principles
- Prefer explicit schemas over implicit behavior.
- Use PostgreSQL as the source of truth.
- Keep business logic in services, not controllers.
- Default to secure-by-design: authentication, authorization, audit logging, least privilege.
- Favor small, reviewable commits and incremental scaffolds.
- Never invent hidden access patterns, backdoors, or unsafe admin shortcuts.

## Stack
- Backend: FastAPI + Python
- Database: PostgreSQL
- ORM/migrations: SQLAlchemy or SQLModel plus Alembic if needed
- Async jobs: Celery/RQ/async workers only when justified
- Vector search: pgvector
- Storage: S3-compatible object storage
- Testing: pytest
- Formatting: ruff, black, isort

## Repo structure
- `app/api/` HTTP routes
- `app/core/` config, logging, auth
- `app/db/` engine, sessions, migrations helpers
- `app/models/` ORM and domain models
- `app/schemas/` Pydantic request/response schemas
- `app/services/` business logic
- `app/workers/` background jobs
- `docs/` architecture and operating notes
- `infra/` AWS and deployment assets
- `tests/` unit and integration tests

## Coding rules
- Use type hints everywhere possible.
- Add input validation at boundaries.
- Keep functions small and named by intent.
- Use dependency injection for DB sessions and services.
- Log structural events, not secrets.
- Prefer pure functions for transforms and extractors.
- When adding a new feature, update docs and tests in the same change.

## Database rules
- Every tenant-owned table must include a workspace/tenant key.
- Every exposed table should consider RLS.
- Add indexes for foreign keys, tenant filters, and time filters.
- Store raw payloads in JSONB only when schema is unstable; normalize stable entities.
- Keep embeddings in dedicated chunk tables, not mixed into raw artifact tables.

## API rules
- Version routes under `/api/v1`.
- Return predictable error shapes.
- Do not leak internal stack traces to clients.
- Separate read models from write models when useful.

## Build and test expectations
- Before merge, ensure tests pass and lint is clean.
- Add tests for schema changes, auth checks, and ingestion logic.
- If a task is ambiguous, prefer creating scaffolding plus TODO markers rather than over-committing to a design.

## Initial deliverables Copilot should create first
1. `README.md`
2. `.env.example`
3. `app/main.py`
4. `app/core/config.py`
5. `app/db/session.py`
6. `app/models/base.py`
7. `app/schemas/common.py`
8. `app/api/v1/router.py`
9. `tests/test_health.py`
10. `docs/architecture.md`
11. `infra/aws/` deployment notes

## Important constraints
- Do not add fragile shortcuts just to make the demo look complete.
- Do not couple ingestion, storage, and retrieval into one monolith function.
- Do not introduce provider lock-in unless explicitly requested.
- Keep the codebase ready for local-first fallback and cloud deployment.
