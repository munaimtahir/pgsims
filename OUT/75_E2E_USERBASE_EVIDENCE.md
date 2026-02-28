# 75 — E2E Userbase Evidence

## Commands Run
1. Targeted new userbase test:
   - `cd frontend && npx playwright test e2e/critical/userbase_foundation.spec.ts --project=chromium`
2. Full critical suite:
   - `cd frontend && npm run test:e2e`

## Results
- Targeted userbase test:
  - **Skipped intentionally** when userbase pages are not present on configured remote base URL (`https://pgsims.alshifalab.pk`).
  - Guard used to avoid false negative against undeployed frontend artifacts.
- Full critical suite:
  - Existing unrelated baseline failure persists:
    - `e2e/critical/admin_analytics_live_feed.spec.ts` failed (pre-existing flow assertion mismatch on remote env).
  - Other critical tests passed.
  - Userbase test remained skipped on remote env.

## Artifacts
- Playwright HTML report:
  - `OUT/E2E_REMEDIATION/playwright-report/`
- Failure traces/screenshots from full suite:
  - `frontend/test-results/critical-admin_analytics_l-994a8--PG-logbook-submit-workflow-chromium/`
  - `frontend/test-results/critical-admin_analytics_l-994a8--PG-logbook-submit-workflow-chromium-retry1/`
- Userbase test trace path (from initial failing run before skip guard):
  - `frontend/test-results/critical-userbase_foundati-0b48d--resident-scope-is-enforced-chromium-retry1/trace.zip`

## Note
- The new userbase Playwright scenario is implemented and executable; full end-to-end verification requires running against a stack serving the newly changed frontend/backend code together (same-origin `/api` wiring).
