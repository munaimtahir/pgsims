# Reproduction Log — `admin_analytics_live_feed.spec.ts`

## Command
```bash
cd /home/munaim/srv/apps/pgsims/frontend
npx playwright test admin_analytics_live_feed.spec.ts --workers=1 --reporter=line --trace=on --retries=0
```

## Observed Failure (initial repro)
- Setup test passed.
- Failing test: `e2e/critical/admin_analytics_live_feed.spec.ts`
- Error:
  - `expect(locator).toBeVisible() failed`
  - Locator: `getByText(/submitted for supervisor review/i)`
  - Timeout: `5000ms`
  - Source: `frontend/e2e/critical/admin_analytics_live_feed.spec.ts:26`

## Artifact Paths from Repro Run
- Screenshot: `frontend/test-results/critical-admin_analytics_l-994a8--PG-logbook-submit-workflow-chromium/test-failed-1.png`
- Video: `frontend/test-results/critical-admin_analytics_l-994a8--PG-logbook-submit-workflow-chromium/video.webm`
- Error context: `frontend/test-results/critical-admin_analytics_l-994a8--PG-logbook-submit-workflow-chromium/error-context.md`
- Trace: `frontend/test-results/critical-admin_analytics_l-994a8--PG-logbook-submit-workflow-chromium/trace.zip`

## Failure Type Classification
- **D) selectors unstable / race condition** (primary):
  - Spec did not handle the native submit confirmation dialog, so submission could be canceled and success banner never appear.
- **D) timing** (secondary):
  - Test used `waitForTimeout(8000)` instead of deterministic API/DOM synchronization for live-feed readiness.
