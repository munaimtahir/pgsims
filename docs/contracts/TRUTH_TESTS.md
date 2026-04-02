# Truth Tests (Must Always Pass)

## Canonical Backend Gate

```bash
cd backend && pytest sims -q
```

Notes:
- `_legacy` test tree is intentionally excluded from pytest discovery.
- Active app test failures must never be masked.

## Contract Drift Gates (Training)

```bash
cd backend && pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -v
cd backend && pytest sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field -v
cd backend && pytest sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -v
```

These enforce:
- Research action compatibility for supervisor return (`supervisor-return`).
- Eligibility payload contract with canonical `reasons: string[]` field.

## Migration Gate — Canonical Department/Hospital/Rotation

```bash
cd backend && pytest sims/rotations/test_canonical_migration_gate.py -v
```

## Drift Gate (Static)

```bash
cd backend && pytest sims/_devtools/tests/test_drift_guards.py -v
```

Fail if forbidden patterns appear:
- legacy Notification create keys (`user=`, `message=`, `type=`, `related_object_id=`)
- reintroduction of duplicate Department models

## Frontend Gates

### Unit/Integration Gate

```bash
cd frontend && npm test -- --watch=false
```

### Lint and Type Gates

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd frontend && npm run build
```

### Smoke E2E Gate

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
cd frontend && npm run test:e2e:smoke:local
```

Notes:
- Canonical local smoke target is `http://127.0.0.1:8082` (frontend) with API at `http://127.0.0.1:8014`.
- For non-canonical targets, set `E2E_BASE_URL` and `E2E_API_URL` explicitly.
- Smoke scope: auth reachability, protected-route redirects, dashboard entry checks.

### Workflow E2E Gate

```bash
cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e
cd frontend && npx playwright install chromium
```

Run the workflow gate against the current checked-out runtime. Verified recovery-pass target:

```bash
cd backend && SECRET_KEY=test-secret python3 manage.py runserver 127.0.0.1:8000
cd frontend && PORT=3001 INTERNAL_API_URL=http://127.0.0.1:8000 NEXT_PUBLIC_API_URL=/api npm run start:next
cd frontend && E2E_BASE_URL=http://127.0.0.1:3001 E2E_API_URL=http://127.0.0.1:8000 npx playwright test --project=workflow-gate
```

Workflow scope (promoted deterministic contract-critical browser flows):
- Forgot-password request submits through real UI/API path.
- Supervisor approvals page renders canonical `resident_name`.
- Supervisor return workflow (`supervisor-return`) works and visible success/result state is rendered in browser.
- Resident dashboard displays canonical eligibility reason strings.
- Resident leave draft can be submitted from the active schedule page and approved from the active supervisor dashboard.
- Rotation workflow closes across active UTRMC, resident, and supervisor routes.
- Postings workflow closes across active resident and UTRMC routes.

Deferred from workflow gate for now:
- broader regression suites and mutation-heavy org-management flows.

Important:
- Docker runtime can be used for smoke checks, but do not treat long-running containers as current-tree truth unless they were rebuilt after the code under test changed.
