# Harness Stabilization

## Fixed
- `frontend/jest.config.js` now ignores `.next/` for module and watch paths, preventing the `.next/standalone/package.json` haste collision from contaminating Jest coverage runs.
- `scripts/e2e_up.sh` now uses `.env` consistently with `scripts/e2e_seed.sh`.
- `scripts/e2e_up.sh` default DB password now matches `.env` for the documented E2E stack.
- `scripts/e2e_up.sh` includes `backend` in `ALLOWED_HOSTS`, which is required for the Next same-origin proxy to call `http://backend:8014`.
- `scripts/e2e_seed.sh` no longer races the backend entrypoint migration. It waits for Django readiness and then runs seed commands.

## Evidence
- Docker stack rebuilt and started.
- `scripts/e2e_seed.sh` completed successfully after the harness fixes.
- Frontend same-origin proxy to `/api/residents/me/summary` returned `200` after `backend` was allowed as a host.

## Remaining Gap
The runtime harness is substantially improved, but the active-surface E2E suite still fails product/runtime checks, so this does not satisfy GO.
