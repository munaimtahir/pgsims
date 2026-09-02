# Workflow E2E Promotion Baseline — Summary

## Outcome

Completed. A deterministic workflow-level browser gate now exists on top of the green smoke baseline.

## Workflows promoted

1. Forgot-password request flow
2. Supervisor approvals list correctness + supervisor-return flow
3. Resident eligibility display workflow

## Workflows deferred

1. Userbase/org-management mutation workflow
   - deferred to avoid widening this milestone into brittle cross-entity regression coverage.

## Canonical gate commands

Seed:
```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
```

Smoke:
```bash
cd frontend && npm run test:e2e:smoke:local
```

Workflow:
```bash
cd frontend && npm run test:e2e:workflow:local
```

## Final pass/fail counts

- Smoke gate: `17 passed, 0 failed`
- Workflow gate: `3 passed, 0 failed`

## Updated status reading

- Smoke remains green.
- Workflow verification is now browser-backed for stabilized contract-critical surfaces.
- Gate size remains intentionally small and trustworthy.
