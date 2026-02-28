# USERBASE FEATURE PACK AUDIT — 2026-02-28

## Scope
- Implemented canonical userbase/org-graph feature pack:
  - profiles, memberships, assignments, linking, HOD, rosters
  - RBAC enforcement
  - UTRMC userbase UI
  - tests + OpenAPI refresh + cleanup

## Contract Updates
- Updated:
  - `docs/contracts/API_CONTRACT.md`
  - `docs/contracts/RBAC_MATRIX.md`
  - `docs/contracts/ROUTES.md`
  - `docs/contracts/TERMINOLOGY.md`

## Implementation Highlights
- Backend:
  - new models in `sims.users.models`
  - new endpoints via `sims.users.userbase_views` / `userbase_urls`
  - `/api/auth/me/` alias added
- Frontend:
  - new UTRMC console pages under `/dashboard/utrmc/*`
  - new `frontend/lib/api/userbase.ts`
  - role support added for `resident`, `faculty`
- Cleanup:
  - removed duplicate legacy rotations master-data API viewsets/routes/serializers.

## Verification
- Backend checks/migrate/tests passed (local venv and docker exec runs).
- Frontend lint/build passed.
- Playwright:
  - new userbase scenario implemented
  - remote run guarded/skipped when new pages not deployed at configured baseURL.
- Full evidence in:
  - `OUT/70_FEATURE_USERBASE_SPEC_LOCK.md` through `OUT/76_DELETION_CLEANUP_REPORT.md`
