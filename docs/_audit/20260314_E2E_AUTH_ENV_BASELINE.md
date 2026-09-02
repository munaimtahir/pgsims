# 2026-03-14 — E2E Auth & Environment Baseline

## Scope

Stabilize Playwright smoke from runnable-but-unreliable to deterministic local baseline.

## Key decisions

- Canonical local smoke runtime uses Docker service ports:
  - frontend `http://127.0.0.1:8082`
  - backend `http://127.0.0.1:8014`
- Deterministic auth/data precondition is `seed_e2e`.
- Removed helper fallback to `localhost:8000` as non-canonical.

## Implemented changes

- Playwright base URL defaults updated to local canonical target.
- E2E auth helper default API target updated to local backend canonical target.
- Added local smoke script: `npm run test:e2e:smoke:local`.
- Updated E2E docs/contracts to match executable model.

## Verification

- Backend health `200`, frontend login route `200`
- `seed_e2e` successful
- Smoke suite: `17 passed`

## Evidence files

- `audit/E2E_FAILURE_ANALYSIS.md`
- `audit/E2E_CANONICAL_MODEL.md`
- `audit/E2E_RUN_LOG.md`
- `audit/E2E_TEST_RESULTS.md`
- `audit/E2E_DIFF_NOTES.md`
- `audit/E2E_SUMMARY.md`
