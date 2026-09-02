# Runtime Failure Map

**Failure Description:** Active-surface E2E tests and logbook workflow were failing with "Failed to load dashboard. Please refresh."

## Failing Tests Mapped

1. **Spec**: `e2e/feature-layer/auth-and-smoke.spec.ts`
   - **Test Name**: core feature roles can login and reach their dashboard surfaces
   - **Role**: `resident_user`, `supervisor_user`, `hod_user`, `utrmc_admin_user`, `utrmc_staff_user`
   - **Route Involved**: `/dashboard/*`
   - **Failing Step**: Expected heading to be visible.
   - **Exact UI Error**: "Failed to load dashboard: Request failed with status code 500. Please refresh." (when proxy failed) / "Failed to load dashboard: Network Error. Please refresh." (when CORS blocked the request). The UI masked the real error with "Failed to load dashboard. Please refresh." prior to the recent logging update.
   - **Network Request**: `GET /api/residents/me/summary/` or equivalent.
   - **Timing**: Happened immediately upon hydration (after API response).

2. **Spec**: `e2e/feature-layer/logbook.spec.ts`
   - **Test Name**: resident draft -> submit -> supervisor return -> resident resubmit -> supervisor approve
   - **Role**: `resident_user`
   - **Route Involved**: `/dashboard/resident/progress`
   - **Failing Step**: Failed to submit draft because the entire page errored out on load.
   - **Timing**: Happened on page load.
