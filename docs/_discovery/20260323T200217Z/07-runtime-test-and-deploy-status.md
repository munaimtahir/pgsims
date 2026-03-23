# Runtime, Test, and Deploy Status

## Commands run and outcomes

- `cd backend && pytest sims -q` with temporary `SECRET_KEY`: **PASS** (`188 passed`).
- `cd backend && pytest sims/_devtools/tests/test_drift_guards.py -q`: **PASS** (`2 passed`).
- `cd backend && pytest sims/rotations/test_canonical_migration_gate.py -q`: **PASS** (`2 passed`).
- `cd backend && SECRET_KEY=... python3 manage.py check`: **PASS** (0 issues; warning about file-log permission).
- `cd backend && SECRET_KEY=... python3 manage.py showmigrations --plan`: **PASS** (all shown as applied).
- `cd frontend && npm run lint`: **FAIL** (multiple lint errors).
- `cd frontend && npm test -- --watch=false`: **PASS** (2 suites, 4 tests; haste-map warning due `.next/standalone/package.json` collision).
- `cd frontend && npm run build`: **PARTIAL** (compiled and generated pages; process did not finish cleanly in this run and was stopped after prolonged trace finalization output).
- `docker compose ... config --services`: **PASS** (`db redis backend frontend worker beat` in both default/prod files).

## Runtime/deployment readiness

- Compose service definitions are complete and include health checks.
- Config warnings indicate missing required secrets in environment (`SECRET_KEY`, `DB_PASSWORD`) when inspected without env.
- `docker-compose.prod.yml` warns `version` key is obsolete.

## Environment state findings

- Backend requires `SECRET_KEY`; tests fail immediately without it.
- Frontend env example defaults to `NEXT_PUBLIC_API_URL=http://localhost:8000`, while app proxy patterns also use `/api` and internal backend URL; needs disciplined environment selection per deployment mode.

## Blockers to “runs cleanly everywhere”

1. Frontend lint gate failing.
2. Build command stability/termination unclear in this environment run.
3. Required secrets not always provided in local command context.
4. Log file path permission issue in current environment for backend checks.
