# Fixes Applied

## Test Harness
- Installed backend runtime/dev requirements in isolated gate venv under `OUT/prod_gate_artifacts/20260421T233708Z/backend-venv`.
- Updated `frontend/e2e/smoke/dashboards.spec.ts` to use non-ambiguous stat label locators.
- Updated `frontend/e2e/navigation/sidebar.spec.ts` to reflect active navigation:
  - resident has `My Dashboard`, `My Schedule`, `Logbook`
  - supervisor has `Overview`, `My Residents`
  - de-scoped research/synopsis/thesis/workshops are hidden
- Updated `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts` to keep only active workflow assertions and current selectors.

## Product Code
No new product feature scope was added during this production gate. Product changes from the prior truth-hardening sprint remained in place and were verified.

