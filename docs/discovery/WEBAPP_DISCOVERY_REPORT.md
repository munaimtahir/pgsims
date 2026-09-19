# PGSIMS Web Application Discovery and Frontend–Backend Audit

Audit date: 2026-09-19 UTC. Repository: `/home/munaim/srv/apps/pgsims`. HEAD `649b02556b9830c082b5f947ba79b77e1778a7db`, branch `main`, three commits ahead of `origin/main`. This is a discovery package only; no product implementation or data mutation was performed.

## Verdict

Build health is CONDITIONAL: Django checks and migration consistency pass, frontend typecheck/lint pass, Docker Compose config parses, frontend Jest has one deterministic failure, production build is blocked by root-owned stale `.next` files, and browser smoke is partially blocked by missing configured baseline credentials. Product completeness is not established. Integration is broad but incomplete: built workflows exist for identity, supervision, academics, documents, backup, monitoring and reports, while navigation omits several of them and active code/contracts retain forbidden HOD/faculty-era concepts.

Feature matrix counts (30 rows; primary status, not route count):

| Status | Count |
|---|---:|
| BUILT_WORKING | 3 |
| BUILT_NEEDS_DEBUG | 4 |
| PARTIALLY_BUILT | 10 |
| NOT_BUILT | 3 |
| BLOCKED_UNVERIFIED | 10 |

The matrix and maps are the detailed source of truth. Counts are not a claim that every individual page or database record was exercised.

## Baseline and architecture

- Monorepo with Django 4.2/DRF backend and Next.js 16 App Router, TypeScript, React Query/Zustand/Axios frontend.
- Package managers: npm lockfile in `frontend/`; Python requirements and `pyproject.toml` in `backend/`.
- Local Docker deployment is running on frontend `127.0.0.1:8082`, backend `127.0.0.1:8014`, PostgreSQL and Redis containers; health endpoints reported healthy.
- Current frontend role types are `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`. Active backend code and contracts still expose `HOD`, `faculty`, `designation_ref`, and legacy role terms, contrary to current clean-room governance.
- Active backend apps include users, academics, rotations, training, supervision, bulk, notifications, audit and backup_center. `sims/_legacy` is not installed, but active URL compatibility modules still mount dummy legacy routes.

## Build health evidence

- `python3 manage.py check`: PASS, 0 issues.
- `python3 manage.py makemigrations --check --dry-run`: PASS, no changes.
- `npm run typecheck`: PASS.
- `npm run lint`: PASS.
- `npm test -- --runInBand --watch=false`: 38/39 suites pass; 239/240 tests pass. `app/dashboard/utrmc/page.test.tsx` fails because the mock defines `getOverview` while the page calls `getAdminDashboardMonitoring`.
- `npm run build`: BLOCKED before compilation by `EACCES` opening root-owned `frontend/.next/trace-build`; do not remove/chown those artifacts as part of this audit.
- `docker compose -f docker/docker-compose.yml config --quiet`: PASS with unset `SECRET_KEY` and `DB_PASSWORD` warnings.
- `npx playwright test --project=smoke`: 19 passed, 6 failed of 25. The six failed at an API 401 (`No active account found with the given credentials`) in baseline-admin login helpers. Passed tests covered public/auth failure handling, three successful configured logins, dashboard access, Backup Center, hospitals, departments and matrix.
- Backend `python3 -m pytest sims -q`: PASS; 1,211 passed, 9 skipped, 50 warnings, 82.13% coverage in 625.10 seconds. The backend suite is green under its repository test configuration.

## Feature and workflow findings

Working or strongly evidenced: public login/refresh path, master-data page access, Backup Center controls, training-record page/unit behavior, and basic dashboards for accounts present in the running database. “Working” is constrained to the exercised path; it does not certify all permissions or mutation lifecycles.

Needs debugging or partial: admin monitoring test contract drift; rotation and leave workflows have UI/API lifecycles but no complete browser proof; logbook and evaluations have draft/submit/review pages and APIs but are absent from primary navigation; reports and monitoring pages are similarly direct-link or incidental-link surfaces; documents and notification mutations are not browser-verified.

Missing or unresolved web coverage: current backend research, thesis/synopsis and workshop capabilities have no usable current web pages. Older docs describe these surfaces as deferred, so they remain `REQUIREMENT_UNCONFIRMED` until product scope is reaffirmed rather than being silently called required.

## Major findings

### WEB-DISC-001 — dashboard monitoring test/API mock drift (P1)

`frontend/app/dashboard/utrmc/page.tsx:26` calls `academicsApi.getAdminDashboardMonitoring()`, while `frontend/app/dashboard/utrmc/page.test.tsx:15-19` mocks only `getOverview`; Jest fails with `TypeError ... is not a function`. Repair the test contract and add a response-shape assertion. Backend support exists at `/api/academics/monitoring/admin-dashboard/`.

### WEB-DISC-002 — dynamic/onboarding and identity role workflows are not fully verified (P1)

The UI and endpoints exist (`/api/auth/me/`, `/api/auth/complete-profile/`, `/api/users/`), but this audit did not safely mutate synthetic identities. Smoke role fixtures are inconsistent: six browser tests receive 401 for their baseline admin helper. Acceptance must use disposable records and verify all four roles, profile creation, rollback, missing fields and next-login routing.

### WEB-DISC-003 — primary navigation omits implemented academic/report workflows (P1)

`frontend/app/academics/` contains logbook, evaluations, monitoring, progress, workload, workflow QA and reports, but `frontend/lib/navRegistry.ts` omits them. Some pages are linked only from other direct-link pages; logbook and evaluation workflows are not available from the main sidebar. Add intentional role-aware links after confirming permissions.

### WEB-DISC-004 — legacy compatibility routes are actively mounted and misleading (P2)

`backend/sims_project/urls.py` mounts `/cases/`, `/logbook/`, `/certificates/` and `/rotations/`; their URL modules route all business paths to `dummy_redirect`. This is not a working feature and conflicts with the clean-room legacy deletion rule. Remove or explicitly document/test the compatibility boundary in a future controlled change.

### WEB-DISC-005 — HOD/faculty-era drift remains in active backend/contracts (P0)

Static scan found HOD assignments/designation logic, faculty role terminology, HOD endpoints in generated truth maps/contracts, HOD seed/test data and HOD-oriented rotation approval text in active code. This violates the current four-role/HOD-not-a-role decision and can mislead permissions and UI requirements. Scope a dedicated cleanup/migration before relying on role-completeness claims.

### WEB-DISC-006 — browser and production-build verification blockers (P1)

The live deployment is healthy, but baseline E2E credentials are missing/inconsistent and the checkout’s `.next` output contains root-owned files. Resolve with a disposable seeded test database and an isolated build workspace or corrected artifact ownership by the environment owner; do not seed production or change permissions during this audit.

## Frontend → backend integrity

The full relationship map is in `WEBAPP_FRONTEND_BACKEND_MAP.csv`. Positive traces include auth → JWT views → User; training records → academic viewset → `academics.ResidentTrainingRecord`; rotation/leave pages → training viewsets/actions; logbook/evaluation pages → academic routers/actions; supervision pages → supervision service/model; documents → onboarding viewsets/media; and monitoring/reports → aggregate/report views. The main negative result is not a missing endpoint but missing discoverability, missing page-level tests, and unverified role/ownership behavior.

## Backend → frontend coverage

The backend map classifies current capabilities. Web coverage is present for identity, masters, supervision, training, rotations, leave, logbook, evaluations, monitoring, reports, documents, backup and notifications. Coverage is absent for research, thesis/synopsis and workshops, with historical deferral evidence but no current approved scope lock. Legacy dummy routes and HOD-era capability are not valid product coverage.

## Navigation/layout/orphan assessment

Public/auth routes and authenticated shell routes render 200 in the running deployment, and smoke confirms login redirects and core dashboard access for configured accounts. Direct route HEAD checks for `/login` and `/academics/logbook` return 200. The primary defect is discoverability: multiple built pages are reachable only by direct URL/incidental links. Redirect-only legacy dashboard families should be treated as compatibility aliases, not implemented features. `/register` is a dead/default-disabled self-registration path; universal creation is `/users/new`.

## Coverage metrics

- Frontend route patterns discovered: 92; static inventory assessed: 92/92; browser exercised: 19 passing core smoke cases plus direct HEAD checks, not every route.
- Meaningful frontend actions mapped: 24 rows in the frontend map; static mapping 24/24; end-to-end verified 0 full business mutation workflows in this audit.
- Backend capabilities classified: 20 rows in backend map; static classification 20/20; runtime business verification limited to health, auth/dashboard access and Backup Center controls.
- Roles defined in frontend: 4; browser login success observed for 3 configured role paths, but role matrix is unverified because baseline fixtures are inconsistent.
- Workflows identified: 17; exercised end-to-end: 0 full state-transition workflows; smoke-level auth/navigation: 19 passing cases.
- Intentional/non-web exclusions: health, token refresh internals, audit/service internals, background jobs, mobile consumers and historically deferred research/thesis/workshop surfaces.

## Recommended implementation order (do not execute in this phase)

1. **Sprint 1 — restore trustworthy verification and contract truth.** Include WEB-DISC-005, WEB-DISC-006, WEB-DISC-001. Prerequisites: disposable E2E database/credentials and environment-owner resolution of `.next` ownership. Acceptance: four-role fixture is reproducible; Jest green; build runs; HOD/legacy role exposure is classified and current contract files no longer contradict the locked role system.
2. **Sprint 2 — make existing web workflows discoverable and testable.** Include WEB-DISC-003, WEB-DISC-008, WEB-DISC-009, WEB-DISC-010, WEB-DISC-011, WEB-DISC-013, WEB-DISC-015, WEB-DISC-028. Add role-aware navigation and page-level tests; execute resident → supervisor review → correction/resubmit for logbook/evaluation/rotation/leave.
3. **Sprint 3 — identity, documents, and data-quality acceptance.** Include WEB-DISC-002, WEB-DISC-004, WEB-DISC-017, WEB-DISC-018, WEB-DISC-020, WEB-DISC-021. Verify transaction rollback, ownership boundaries, uploads/downloads, data refresh and audit events.
4. **Sprint 4 — scope-locked backend-ready surfaces.** Include WEB-DISC-022 through WEB-DISC-025 only after product confirms which deferred backend capabilities are required on web; otherwise mark them approved backend-only/mobile/deferred with evidence.

Backend-ready frontend work: navigation for existing academic/report/monitoring pages; page-level tests; research/thesis/workshop UI if scope is approved. Backend-dependent work: role/HOD cleanup, identity/onboarding acceptance, document review durability, and any workflow whose assignment/permission data is not yet cleanly verified.

## Limitations

No production data was changed, no real emails/SMS/integrations were triggered, and no credentials or personal documents were recorded. Browser tests did not complete mutation workflows because the configured baseline credentials were unavailable. The report therefore intentionally uses `BLOCKED_UNVERIFIED` where evidence is incomplete.

See the CSV matrices and root backlog for actionable findings and acceptance criteria.
