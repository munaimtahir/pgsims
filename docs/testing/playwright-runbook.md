# PGSIMS Playwright Runbook

## Canonical local E2E baseline (smoke + workflow + active-surface)

This repository's canonical local smoke model is:

- Frontend URL: `http://127.0.0.1:8082` (Docker `frontend` service)
- Backend API URL: `http://127.0.0.1:8014` (Docker `backend` service)
- Deterministic users/data: `python manage.py seed_e2e`
- Smoke command: `npm run test:e2e:smoke:local`
- Workflow command: `npm run test:e2e:workflow:local`
- Active-surface command: `npm run test:e2e:active-surface:local`

`frontend/playwright.config.ts` defaults now target this local model.  
Override with env vars only when intentionally testing a different environment.

## Prerequisites

- Docker + Docker Compose
- Node.js 18+

## 1) Start runtime services

```bash
# From repo root
docker compose -f docker/docker-compose.yml --env-file .env up -d db redis backend frontend

# Verify reachability
curl -sSf http://127.0.0.1:8014/health/ >/dev/null && echo "backend ok"
curl -sSf http://127.0.0.1:8082/login >/dev/null && echo "frontend ok"
```

## 2) Seed deterministic E2E users/data

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend \
  python manage.py seed_e2e
```

This command is idempotent (`update_or_create`) and provisions canonical smoke users:

- `e2e_utrmc_admin / UtrmcAdmin123!`
- `e2e_utrmc_user / Utrmc123!`
- `e2e_admin / Admin123!`
- `e2e_supervisor / Supervisor123!`
- `e2e_pg / Pg123456!`
- `resident_user / ResidentUser123!`
- `supervisor_user / SupervisorUser123!`
- `hod_user / HodUser123!`
- `utrmc_admin_user / UtrmcAdminUser123!`
- `utrmc_staff_user / UtrmcStaffUser123!`
- `negative_role_user / NegativeRole123!`

## 3) Run canonical smoke gate

```bash
cd frontend
npm run test:e2e:smoke:local
```

Expected baseline: all smoke specs pass (currently 17 tests).

Smoke responsibility:
- app availability and auth reachability
- public-route guards
- role dashboard entry paths

## 4) Run canonical workflow gate

```bash
cd frontend
npm run test:e2e:workflow:local
```

Workflow responsibility (contract-critical promoted flows):
- forgot-password real UI submit path
- supervisor research approvals list rendering (`resident_name`)
- supervisor return flow (`supervisor-return`) with visible success/result state
- resident eligibility reasons rendered in browser

## 5) Run active-surface verification suite

```bash
cd frontend
npm run test:e2e:active-surface:local
```

The active-surface npm scripts reseed `resident_user` and related deterministic fixtures before execution.
If you bypass npm and call raw `npx playwright test --project=active-surface ...`, run `scripts/e2e_seed.sh` first.

Active-surface suite responsibility:
- logbook end-to-end review loop
- logbook review-queue permission boundaries
- auth/session reachability for the promoted resident, supervisor, and UTRMC surfaces

The broader inactive-depth verification suite remains available for inactive-depth checks:

```bash
cd frontend
npm run test:e2e:inactive-depth:local
```

Inactive-depth responsibility:
- dashboard counters that depend on inactive-depth state
- synopsis/thesis completeness + certificate issuance visibility
- rotation phase-1 lifecycle and verification queue
- regression smoke for the inactive depth routes

## 6) Optional: run with explicit env overrides

```bash
cd frontend
E2E_BASE_URL=http://127.0.0.1:8082 \
E2E_API_URL=http://127.0.0.1:8014 \
npm run test:e2e:smoke
```

## 7) Other suites (not part of smoke/workflow/active-surface gates)

```bash
cd frontend
npm run test:e2e:auth
npm run test:e2e:rbac
npm run test:e2e:navigation
npm run test:e2e:dashboard
npm run test:e2e:workflows
npm run test:e2e:negative
```

## 8) Screenshot catalog

```bash
cd frontend
npm run test:e2e:screenshots:local
```

This produces a presentation-oriented screenshot catalog under:

- `output/playwright/screenshots-catalog/`

For a single command that runs the full Playwright suite and retains the screenshot catalog path:

```bash
cd frontend
npm run test:e2e:full:local
```

## 9) Reports and artifacts

| Artifact | Location |
|----------|----------|
| HTML report | `output/playwright/report/index.html` |
| Test results | `output/playwright/results/` |
| Screenshots/traces/videos | `output/playwright/results/` |
| Catalog screenshots | `output/playwright/screenshots-catalog/` |

```bash
cd frontend
npm run test:e2e:report
```

## 10) Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `E2E_BASE_URL` | Frontend URL for browser navigation | `http://127.0.0.1:8082` |
| `E2E_API_URL` | Backend URL used by API login helper | `http://127.0.0.1:8014` |
| `E2E_SCREENSHOTS_DIR` | Output directory for screenshot catalog | `../output/playwright/screenshots-catalog` |

## Known limitations

- Canonical gates intentionally stay small and deterministic.
- Broad regression suites (`critical`, `workflows`, `negative`, `screenshots`) are runnable but not gate-promoted yet.
- User/org-management mutation workflows are deferred from workflow gate for now to avoid flaky cross-data coupling.
- Docker's backend container healthcheck currently targets `/healthz/`; use `/health/` for simple local reachability checks when bringing the stack up manually.
