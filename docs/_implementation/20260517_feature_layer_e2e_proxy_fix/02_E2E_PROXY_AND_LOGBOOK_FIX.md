# E2E Proxy And Logbook Fix

## What Was Broken

- The local Next dev server was proxying `/api/*` requests to `http://backend:8014` by default.
- That backend host only exists inside Docker, so local Playwright runs on `http://127.0.0.1:3006` were hitting proxy failures.
- The feature-layer auth helper also needed to set cookies on both common local hostnames.

## What Changed

- The API proxy now uses:
  - `INTERNAL_API_URL` when explicitly configured
  - `http://127.0.0.1:8014` in development when no internal URL is provided
  - `http://backend:8014` outside development as the safe Docker default
- The auth helper now applies cookies to both `localhost` and `127.0.0.1`.

## Why This Fixed The Workflow

- Dashboard shell routes could render, but API-driven logbook actions were failing through the local dev proxy.
- After the proxy fallback change, the logbook draft POST succeeded and the UI workflow could complete.
- The helper change removed host mismatch risk between the browser and the auth cookie origin.

## Evidence

- Browser reproduction initially showed proxy errors on same-origin API calls.
- After the fix, same-origin API calls returned `200`/`201` responses and the logbook workflow passed.
