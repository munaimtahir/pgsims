# PGSIMS SESSION A AUDIT COMPLETE

## Meta
- Baseline SHA: 94d2a867a1b3683009d972adfb780ddc8e365754
- Audit branch: audit/pgsims-a-truthmap
- Target Scope: Pre-production certification of backend endpoints, frontend routes, Android integration, and contract integrity.

## Metrics
- Frontend routes discovered: 76 API calls (and ~50 NextJS pages).
- Backend endpoints discovered: 855 Django routes.
- Frontend mapping percentage: 50% (38/76 explicitly mapped).
- Backend classification percentage: 62% consumed explicitly (others are legacy, django-admin, or orphans).
- Android API actions mapped: ~34 Retrofit calls mapped to DRF endpoints.

## Major Findings Snapshot
- **P1**: Significant drift between frontend API clients (`/api/academics/`) and backend DRF viewsets (`sims.training`).
- **P2**: Leftover monolith dummy endpoints (`/cases/`, `/logbook/`) are still exposed on the backend and pollute the API surface.
- **P1**: Route-level Next.js proxying (`app/api/[...path]/route.ts`) relies on environment variables but falls back to `127.0.0.1:8014` which may fail in certain docker network topographies if `.env` is misconfigured.

## Conclusion
The backend is a robust Django/DRF stack, but the React frontend's API client definitions are severely out of sync with the backend's module refactoring (e.g., `academics` vs `training` modules). The Android app is present and functional but covers only a subset of endpoints.
