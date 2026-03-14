# PGSIMS Playwright Runbook

## Canonical local E2E baseline (smoke + workflow)

This repository's canonical local smoke model is:

- Frontend URL: `http://127.0.0.1:8082` (Docker `frontend` service)
- Backend API URL: `http://127.0.0.1:8014` (Docker `backend` service)
- Deterministic users/data: `python manage.py seed_e2e`
- Smoke command: `npm run test:e2e:smoke:local`
- Workflow command: `npm run test:e2e:workflow:local`

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

## 5) Optional: run with explicit env overrides

```bash
cd frontend
E2E_BASE_URL=http://127.0.0.1:8082 \
E2E_API_URL=http://127.0.0.1:8014 \
npm run test:e2e:smoke
```

## 6) Other suites (not part of smoke/workflow gates)

```bash
cd frontend
npm run test:e2e:auth
npm run test:e2e:rbac
npm run test:e2e:navigation
npm run test:e2e:dashboard
npm run test:e2e:workflows
npm run test:e2e:negative
```

## 7) Reports and artifacts

| Artifact | Location |
|----------|----------|
| HTML report | `output/playwright/report/index.html` |
| Test results | `output/playwright/results/` |
| Screenshots/traces/videos | `output/playwright/results/` |

```bash
cd frontend
npm run test:e2e:report
```

## 8) Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `E2E_BASE_URL` | Frontend URL for browser navigation | `http://127.0.0.1:8082` |
| `E2E_API_URL` | Backend URL used by API login helper | `http://127.0.0.1:8014` |

## Known limitations

- Canonical gates intentionally stay small and deterministic.
- Broad regression suites (`critical`, `workflows`, `negative`, `screenshots`) are runnable but not gate-promoted yet.
- User/org-management mutation workflows are deferred from workflow gate for now to avoid flaky cross-data coupling.
- Docker's backend container healthcheck currently targets `/healthz/`; use `/health/` for simple local reachability checks when bringing the stack up manually.
