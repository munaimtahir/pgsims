# Trace & Auth Diagnosis

**Hypothesis Evaluated:** Auth token injection timing or state propagation failure.

## Findings

1. **Token Injection Timing**: Playwright uses `page.addInitScript()` to set `localStorage` tokens. This script executes synchronously on page load, *before* React hydration. Timing was proven to be **NOT** the issue.
2. **CORS / Proxy Issue**: The actual failure occurred because `scripts/e2e_up.sh` overrode `NEXT_PUBLIC_API_URL` to `http://localhost:8014`.
   - This forced the browser to make cross-origin requests to `localhost:8014` instead of using the Next.js same-origin proxy at `/api`.
   - Django's `CORS_ALLOWED_ORIGINS` was configured to allow `localhost:8082`, but Playwright accessed the site via `127.0.0.1:8082`.
   - The origin mismatch resulted in a CORS block / Network Error in Axios.
3. **Error Masking**: The frontend `page.tsx` was discarding the actual Axios error message and unconditionally setting `"Failed to load dashboard. Please refresh."`, making it look like a generic hydration/auth failure.

**Conclusion:** The auth state was fine. The network request was rejected due to a cross-origin CORS policy mismatch induced by bypassing the `/api` proxy.
