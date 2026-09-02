# Build and Runtime Verification

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
cd backend && SECRET_KEY=test-secret python3 manage.py runserver 127.0.0.1:8000
cd frontend && PORT=3001 INTERNAL_API_URL=http://127.0.0.1:8000 NEXT_PUBLIC_API_URL=/api npm run start:next
cd frontend && npx playwright install chromium
cd frontend && E2E_BASE_URL=http://127.0.0.1:3001 E2E_API_URL=http://127.0.0.1:8000 npx playwright test --project=workflow-gate
```

## Outcomes
- Frontend lint: PASS
- Frontend typecheck: PASS
- Frontend unit tests: PASS
- Frontend production build: PASS
- Backend full active-app suite: PASS (`192 passed`)
- Backend phase-6 training suite: PASS (`40 passed`)
- Backend users/auth tests: PASS (`7 passed`)
- Drift guards: PASS
- Canonical model migration gate: PASS
- `manage.py check`: PASS
- Workflow gate browser suite on current local runtime: PASS (`4 passed`)

## Runtime checks
- Docker services were up and healthy at the process level.
- Docker frontend/backend were not treated as the authoritative verification target for this recovery pass because they could be stale relative to the checked-out code.
- Current-tree browser verification therefore used local Django + local Next.js processes on:
  - Backend: `http://127.0.0.1:8000`
  - Frontend: `http://127.0.0.1:3001`

## Confidence in reproducibility
- Medium-high for the active surface.
- The workflow gate is reproducible when deterministic seed data is loaded and the browser dependency is installed.
- Reproducibility is weaker if teams rely on long-running Docker containers without rebuilding after source changes.

## Remaining blockers
- Docker artifact drift can still mislead runtime checks unless rebuild discipline is enforced.
- `next.config.mjs` still allows production builds to skip lint/type failures, so explicit gates remain mandatory.
