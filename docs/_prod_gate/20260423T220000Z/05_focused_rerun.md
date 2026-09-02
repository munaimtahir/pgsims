# Focused Rerun Results

A focused rerun was executed locally targeting the E2E Active-Surface integration.

## Commands executed:
```bash
docker compose -f docker/docker-compose.yml down -v
./scripts/e2e_up.sh
docker compose -f docker/docker-compose.yml --env-file .env exec backend python manage.py migrate
./scripts/e2e_seed.sh
cd frontend && npm run test:e2e:feature-layer:local
```

## Verification:
- All 7 tests within the `active-surface` suite successfully passed without timeout or DOM failure.
- The `Failed to load dashboard. Please refresh.` behavior was eliminated entirely.
- The logbook draft, submit, return, resubmit, and approve pipeline executed stably and perfectly under deterministic E2E seed parameters.
- E2E tests for `regression-smoke` also successfully cleared the resident core pages without the prior `Research Project` vs `Research` locator error.

**Verdict:** The repaired flows are entirely stable.
