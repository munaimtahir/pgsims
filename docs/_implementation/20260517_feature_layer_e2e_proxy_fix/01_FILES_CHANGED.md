# Files Changed

## Runtime Fixes

- `frontend/e2e/helpers/auth.ts`
  - Set auth cookies for both `127.0.0.1` and `localhost` origins so Playwright sessions match the host used by the browser.
- `frontend/app/api/[...path]/route.ts`
  - Added a development fallback to `http://127.0.0.1:8014` when `INTERNAL_API_URL` is not set.
  - Preserved the Docker path via `INTERNAL_API_URL`.

## Verification

- Re-ran the feature-layer active-surface suite.
- Re-ran lint, typecheck, and build after the proxy change.

## Notes

- No contract changes were required.
- No route structure changes were made.
