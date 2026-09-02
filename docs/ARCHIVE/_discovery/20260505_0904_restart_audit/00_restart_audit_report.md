# PGSIMS Restart Audit Report

Session window (UTC): 2026-05-05 09:04 → 09:18
Repo: /home/munaim/srv/apps/pgsims
Branch: main
Commit: ad721197ef7e45e5802197aae1c10f023485d4cb

## Safety confirmations
- No application code modified; only docs under docs/_discovery/ were created/edited.
- No destructive commands (no db reset/flush/seed).
- Secrets are not recorded; any discovered secret-like values were redacted in evidence outputs.

## Evidence index
- Repo inventory: docs/_discovery/20260505_0904_restart_audit/01_repo_inventory.txt
- Tree + manifests: docs/_discovery/20260505_0904_restart_audit/02_tree_and_manifests.txt
- Docker state: docs/_discovery/20260505_0904_restart_audit/03_docker_state.txt
- PGSIMS compose: docs/_discovery/20260505_0904_restart_audit/05_pgsims_compose.txt
- Container health: docs/_discovery/20260505_0904_restart_audit/06_pgsims_container_health.txt
- Backend HTTP checks: docs/_discovery/20260505_0904_restart_audit/07_backend_http_checks.txt
- Backend manage.py checks (sanitized): docs/_discovery/20260505_0904_restart_audit/08_backend_managepy_checks.txt
- DB status: docs/_discovery/20260505_0904_restart_audit/09_db_status.txt
- Runtime OpenAPI spec: docs/_discovery/20260505_0904_restart_audit/openapi_runtime.yaml
- Frontend HTTP checks: docs/_discovery/20260505_0904_restart_audit/11_frontend_http_checks.txt
- Backend code snapshot: docs/_discovery/20260505_0904_restart_audit/12_backend_code_snapshot.txt
- Frontend code snapshot: docs/_discovery/20260505_0904_restart_audit/13_frontend_code_snapshot.txt
- Contracts excerpt: docs/_discovery/20260505_0904_restart_audit/14_contracts_docs_excerpt.txt
- OpenAPI tags (corrected): docs/_discovery/20260505_0904_restart_audit/15b_openapi_tags_corrected.txt
- Auth probes (no creds): docs/_discovery/20260505_0904_restart_audit/22_auth_rbac_runtime_probes.txt
- Frontend↔Backend wiring: docs/_discovery/20260505_0904_restart_audit/21_ui_api_wiring.txt
- Backend pytest: docs/_discovery/20260505_0904_restart_audit/18_backend_pytest.txt
- Frontend jest: docs/_discovery/20260505_0904_restart_audit/19_frontend_jest.txt
- Readonly Playwright smoke: docs/_discovery/20260505_0904_restart_audit/17e_playwright_readonly_smoke.txt
- Git + deploy snapshot: docs/_discovery/20260505_0904_restart_audit/20_git_and_deploy_snapshot.txt

## 1) Codebase structure (what exists)
Backend appears to be a Django monolith with modular apps under backend/sims/: users, academics, rotations, training, bulk, notifications, audit.
Frontend is a Next.js app using the app router under frontend/app/ (login/register/dashboard per role).
Contracts are centralized under docs/contracts/ and are present.

## 2) Git status
- Working tree was clean at start. Current changes are evidence files under docs/_discovery/ (see git status in 20_git_and_deploy_snapshot.txt).

## 3) Docker/runtime state (what is running)
- PGSIMS stack is already running via docker/docker-compose.yml: backend (8014), frontend (8082), postgres, redis, celery worker, celery beat.
- Containers report healthy for backend/db/redis/frontend (see 03_docker_state.txt and 06_pgsims_container_health.txt).

## 4) Backend status (runtime)
- Backend responds on http://127.0.0.1:8014 with /healthz/ = 200 and database/cache/celery checks ok.
- OpenAPI schema served at /api/schema/ (YAML, ~328KB).
- Backend root (/) serves an HTML page (Bootstrap template).

## 5) Frontend status (runtime)
- Frontend responds on http://127.0.0.1:8082/ and /login (see 11_frontend_http_checks.txt).
- Readonly Playwright smoke confirms frontend landing + login load (see 17e_playwright_readonly_smoke.txt).

## 6) Database/migration status
- Postgres is running inside pgsims_db (postgres:15-alpine).
- Django migrations show applied across apps: academics/users/training/rotations/bulk/notifications/audit + django_celery_beat (see 08_backend_managepy_checks.txt, 09_db_status.txt).

## 7) API status (surface)
- OpenAPI includes at least two main namespaces: /api/* and /academics/api/* (see 15_module_surface_summary.txt, openapi_runtime.yaml).
- Auth endpoints present under /api/auth/* (login/logout/me/refresh/register/password reset/change password).

## 8) Authentication/RBAC status (probe-only)
- Without credentials: POST /api/auth/login/ with {} returns validation error as expected; protected endpoints return 401/403 (see 22_auth_rbac_runtime_probes.txt).
- RBAC contract doc exists at docs/contracts/RBAC_MATRIX.md (see 14_contracts_docs_excerpt.txt).

## 9) Feature/module status (implemented vs surfaced)
Backend implemented modules (from INSTALLED_APPS / openapi tags): academics, rotations, training/logbook/cases, bulk import/export, notifications, audit, users.
Frontend implemented routes: /login, /register, /forgot-password, /dashboard/* (resident/supervisor/utrmc/pg) (see 15_module_surface_summary.txt).
Frontend contains an API passthrough under frontend/app/api/[...path] which strongly suggests UI calls /api/* on the same origin and proxies to backend (see 21_ui_api_wiring.txt).

## 10) Test suite status
- Backend: pytest collected 294 tests and all passed (294 passed) using settings_test (see 18_backend_pytest.txt).
- Frontend unit tests: jest ran 29 suites / 81 tests and all passed (see 19_frontend_jest.txt).
- Frontend e2e suites exist under frontend/e2e/ (Playwright), but were NOT run here to avoid DB mutation; only a readonly smoke spec was run.

## 11) Runtime browser verification
- Playwright readonly smoke (GET-only) passed against running Docker services: 4/4 checks (see 17e_playwright_readonly_smoke.txt).

## 12) Documentation freshness
- Contracts exist and are timestamped in repo inventory (see 01_repo_inventory.txt and 14_contracts_docs_excerpt.txt).
- PROD gate closure package exists under docs/PROD_GATE_CLOSURE/ and states NO-GO with 11 blockers as of 2026-04-23 (see docs/PROD_GATE_CLOSURE/00_README.md).

## 13) Deployment readiness (current state)
- docker/docker-compose.yml is production-oriented (migrate+collectstatic+gunicorn; NEXT_PUBLIC_API_URL build arg; proxy-related env toggles).
- Compose depends on environment variables (DB_PASSWORD, SECRET_KEY, etc). Compose warnings show these are not set in the current shell when running docker compose commands without an env file.
- Running backend appears to have DEBUG=True (see 08_backend_managepy_checks.txt); verify production env expectations before any external exposure.

## 14) Clear next-action roadmap (safest next phase)
1. Decide target environment for validation: local docker (current) vs staging/production.
2. Run the official Truth Tests / gates from docs/contracts/TRUTH_TESTS.md and docs/PROD_GATE_CLOSURE/06_testing_procedures.md in a controlled environment (these may seed data).
3. Pick exactly one production gate blocker from docs/PROD_GATE_CLOSURE/01_blocker_analysis.md and follow docs/ANTI_DRIFT_GUARDRAILS.md session window rules.
4. If the immediate goal is demo: run only non-destructive smoke checks + read-only dashboards first; defer write-workflows until e2e fixtures are validated.
