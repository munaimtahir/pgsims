# E2E Auth & Environment Baseline — Summary

## Outcome

Milestone objective achieved: Playwright smoke moved from "runnable but unreliable" to a deterministic local baseline.

## What was fixed

1. Canonical local browser target is now explicit and defaulted:
   - frontend `http://127.0.0.1:8082`
   - backend `http://127.0.0.1:8014`

2. Auth helper no longer falls back to accidental `localhost:8000`.

3. Deterministic user/data precondition is documented and reproducible via `seed_e2e`.

4. Canonical smoke command established:
   - `npm run test:e2e:smoke:local`

5. Governance/testing docs updated to executable truth.

## Verification result

- `seed_e2e` executed successfully.
- Smoke suite result: **17 passed, 0 failed**.
- Default smoke command (`npm run test:e2e:smoke`) also passes under updated local defaults.

## Canonical contracts chosen

- Local E2E execution model is Docker-backed (`8082/8014`) for reproducibility.
- Smoke gate scope remains small and meaningful (public, login, dashboard reachability).
- Environment overrides remain supported through `E2E_BASE_URL` and `E2E_API_URL`.

## Remaining limitations

- This milestone stabilizes smoke only; broader suites (critical/workflows/regression) are not promoted as mandatory gate in this run.

## Classification snapshot (for this milestone scope)

- Done:
  - canonical local E2E model
  - explicit FE↔BE URL behavior in smoke
  - deterministic smoke user provisioning
  - login success in Playwright for canonical users
  - at least one meaningful end-to-end smoke journey (full smoke suite) passing
  - reproducibility docs updated

- Partially done:
  - broader non-smoke E2E suites (runnable but not baseline-gated in this milestone)

- Broken:
  - none in canonical smoke baseline

Milestone status: **Complete** (for requested E2E auth/environment baseline scope).
