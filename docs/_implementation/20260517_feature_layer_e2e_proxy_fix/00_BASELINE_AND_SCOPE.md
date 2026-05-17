# Baseline And Scope

## Session Window

- Primary purpose: fix the remaining feature-layer Playwright blocker that prevented the full active-surface suite from passing.
- In scope: auth/session helper reliability, local Next API proxy behavior, logbook workflow verification, targeted E2E rerun.
- Out of scope: broad UI redesign, contract changes, unrelated coverage expansion, backend schema work.

## Baseline

- Branch: `codex/dead-code-cleanup`
- Commit before changes: `e21ec23`
- Prior blocker evidence: `docs/PROD_GATE_CLOSURE/`
- Prior UI evidence: `docs/_implementation/20260516_ui_pilot_readiness_repair/`

## Observed Failure

- Feature-layer active-surface suite failed on:
  - `frontend/e2e/feature-layer/auth-and-smoke.spec.ts`
  - `frontend/e2e/feature-layer/logbook.spec.ts`
  - `frontend/e2e/feature-layer/permissions.spec.ts`
- The browser session was authenticating, but same-origin API calls through the local Next dev server were returning proxy errors.
- The logbook save flow did not surface the success state in Playwright until the proxy path was fixed.

## Scope Lock

- Only fix the runtime path required for the failing E2E surfaces.
- Do not redesign dashboards or expand into additional blocker classes.
