# 2026-04-02 Truth Alignment Stabilization Audit

## Scope
- Truth alignment
- Frontend baseline recovery
- Core workflow closure for active leave flow
- Build and runtime verification

## Key evidence
- Active backend include set: `backend/sims_project/urls.py`
- Active frontend navigation: `frontend/lib/navRegistry.ts`
- Active dashboard route tree: `frontend/app/dashboard/*`
- Leave workflow implementation: `frontend/app/dashboard/resident/schedule/page.tsx`, `frontend/app/dashboard/supervisor/page.tsx`
- Summary/scoping fixes: `backend/sims/training/views.py`
- Auth recovery fix: `backend/sims/users/api_views.py`

## Commands run

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd frontend && npm test -- --watch=false
cd frontend && npm run build

cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/training/test_phase6.py -q
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/users/tests.py -q
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/_devtools/tests/test_drift_guards.py -q
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/rotations/test_canonical_migration_gate.py -q
cd backend && SECRET_KEY=test-secret python3 manage.py check
docker compose -f docker/docker-compose.yml --env-file .env ps
cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e
cd frontend && npx playwright install chromium
cd frontend && E2E_BASE_URL=http://127.0.0.1:3001 E2E_API_URL=http://127.0.0.1:8000 npx playwright test --project=workflow-gate
```

## Outcome summary
- Frontend lint/type/unit/build: green
- Backend active-app suite: green
- Workflow gate on current local runtime: green
- Docker stack healthy but not trusted as current-tree proof without rebuild
