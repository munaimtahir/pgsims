# Runtime Verification

## Commands Run

### Baseline and regression gates

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd frontend && npm test -- --watch=false
cd frontend && npm run build
cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q
cd backend && SECRET_KEY=test-secret python3 manage.py check
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -v
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/rotations/test_canonical_migration_gate.py -v
cd backend && SECRET_KEY=test-secret python3 -m pytest sims/_devtools/tests/test_drift_guards.py -v
docker compose -f docker/docker-compose.yml --env-file .env ps
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
cd frontend && npm run test:e2e:smoke:local
```

### Current-tree workflow gate

```bash
cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e
cd backend && SECRET_KEY=test-secret python3 manage.py runserver 127.0.0.1:8000
cd frontend && PORT=3003 INTERNAL_API_URL=http://127.0.0.1:8000 NEXT_PUBLIC_API_URL=/api npm run start:next
cd frontend && E2E_BASE_URL=http://127.0.0.1:3003 E2E_API_URL=http://127.0.0.1:8000 npx playwright test --project=workflow-gate
```

## Outcomes

- `npm run lint`: pass
- `npx tsc --noEmit`: pass
- `npm test -- --watch=false`: pass
- `npm run build`: pass
- `pytest sims -q`: pass (`195 passed`)
- `manage.py check`: pass
- named contract drift tests: pass
- canonical migration gate: pass
- drift guard gate: pass
- docker smoke E2E gate: pass (`17 passed`)
- current-tree workflow gate: pass (`6 passed`)

## Verified Workflow Evidence

- Rotation workflow:
  - draft created on `/dashboard/utrmc`
  - resident saw the draft on `/dashboard/resident/schedule`
  - resident submitted it
  - supervisor approved it on `/dashboard/supervisor`
  - UTRMC admin activated and completed it on `/dashboard/utrmc`
  - resident saw the completed status on `/dashboard/resident/schedule`
- Postings workflow:
  - resident created the posting request on `/dashboard/resident/postings`
  - UTRMC admin approved it on `/dashboard/utrmc/postings`
  - UTRMC admin completed it on `/dashboard/utrmc/postings`
  - resident saw completed state on `/dashboard/resident/postings`

## Confidence

- Build reproducibility: high
- Active-surface runtime confidence: high
- Rotation workflow closure confidence: high
- Postings workflow closure confidence: high
