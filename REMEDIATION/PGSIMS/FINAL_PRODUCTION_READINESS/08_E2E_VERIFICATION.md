# E2E verification

Status: CONDITIONAL / NOT CLEARED.

An isolated canonical PostgreSQL 15 → Django → Next.js stack was built and started with disposable
test-only environment values. Migration completed from an empty database, synthetic seed data was
loaded, and the stack was removed with its project-scoped volumes after testing. No VPS production
service, database, or volume was touched.

Playwright Chromium was installed locally. After migrating the smoke fixtures to the canonical
four-role routes, labels, credentials, and disabled public-registration contract, smoke passed
25/25. Workflow-gate executed 4 tests and passed 4/4 after migrating contracts to `/masters`, the
flexible-import flow, and `/academics/leave-requests`; the leave test verified final `APPROVED`
state after resident submission and supervisor approval.

The combined RBAC/negative run executed 31 tests: 24 passed and 7 failed on stale contracts
targeting retired UTRMC/HOD role semantics and duplicate UTRMC add-form routes. Canonical role
boundaries, unauthenticated redirects, API denial, and login validation checks passed.

The VPS production checkout was verified read-only over `ssh test`: backend `/healthz/` reported
database/cache/Celery healthy, frontend root returned HTTP 200, and no production service or
database mutation was performed.
