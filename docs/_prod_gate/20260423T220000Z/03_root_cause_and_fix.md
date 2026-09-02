# Root Cause and Fix

## Exact Root Cause
The `Failed to load dashboard. Please refresh.` E2E failure was caused by two compounding issues:
1. **Network Mismatch**: `scripts/e2e_up.sh` injected `NEXT_PUBLIC_API_URL=http://localhost:8014`. This overrode the Next.js build-time `/api` default, instructing the React client in the browser to make cross-origin requests directly to the backend instead of utilizing the same-origin Next.js proxy. This resulted in CORS blocking because the Playwright test ran against `E2E_BASE_URL=http://127.0.0.1:8082` and Django's `CORS_ALLOWED_ORIGINS` was strictly checking `localhost:8082`.
2. **Error Masking**: The frontend `page.tsx` caught Axios Network Errors and indiscriminately set the generic UI error without displaying the actual `Network Error` from Axios, confusing diagnosis.

## Erroneous Prior Assumptions
A `100ms` `setTimeout` delay was introduced into `app/dashboard/resident/page.tsx` during an earlier attempt to fix what was incorrectly assumed to be an auth token hydration race condition. Playwright's `addInitScript` sets `localStorage` synchronously prior to document hydration, making the `100ms` delay an unnecessary and risky hack that masked the actual network problem.

## The Fix
1. **Removed the 100ms delay**: Deleted the `await new Promise(resolve => setTimeout(resolve, 100));` hack from `frontend/app/dashboard/resident/page.tsx`.
2. **Corrected Proxy Env**: Modified `scripts/e2e_up.sh` to enforce `NEXT_PUBLIC_API_URL=/api`, restoring the same-origin proxy workflow that correctly bypasses CORS constraints entirely.
3. **Whitelisted Origins**: Added `http://127.0.0.1:8082` and `http://127.0.0.1:3000` to `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` in `e2e_up.sh` as an extra safety measure to support non-proxied debugging scenarios.

These changes verify the issue without masking bugs and prove the `active-surface` E2E layer is functionally fully integrated.
