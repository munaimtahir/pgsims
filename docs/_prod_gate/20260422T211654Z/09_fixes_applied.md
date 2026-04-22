# Fixes Applied

## Backend
- Wired drf-spectacular into settings and URL routing.
- Added schema endpoint smoke test.
- Added UTRMC org graph route/API tests.
- Added UTRMC read-only direct mutation denial tests.
- Added logbook and leave invalid transition tests.

## Frontend
- Added UTRMC HOD page behavior tests.
- Added UTRMC hospital-department matrix behavior tests.
- Stabilized Jest path ignores for `.next/`.

## Runtime Harness
- Aligned E2E bring-up and seed scripts to use the same `.env` source.
- Fixed E2E DB password mismatch.
- Added `backend` to E2E `ALLOWED_HOSTS`.
- Removed seed-time migration race from `scripts/e2e_seed.sh`.

## Contracts
- Added live `/api/schema/` endpoint.
- Strict schema command is now available but failing on schema warnings/errors.
