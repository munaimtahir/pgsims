# Fix Log

Date: 2026-06-26

## Deployment Fixes

- Freed Docker build space with `docker builder prune -af`.
- Added `frontend/.dockerignore` to exclude generated/cache directories from Docker build context:
  - `node_modules/`
  - `.next/`
  - coverage/test/playwright output folders
  - local env/log artifacts
- Evidence: frontend Docker context reduced from about `905MB` to `1.41MB`.

## Frontend Build Fixes

Fixed deployment-blocking `next build` lint errors only:

- Removed unused `axios` import from `frontend/app/dashboard/change-password/page.tsx`.
- Replaced `Record<string, any>` with `UserbaseUserUpsert` in `frontend/app/dashboard/utrmc/supervisors/page.tsx`.
- Removed unused `useAuthStore` import from `frontend/app/register/page.test.tsx`.
- Removed unused `useRouter` import/variable from `frontend/app/reset-password/[uid]/[token]/page.tsx`.

## Caddy/Routing Fixes

- No repo Caddy changes were needed: `deploy/Caddyfile.pgsims` already includes `pg.fmu.edu.pk` and `/healthz*`.
- Active system Caddy config validates and routes app/API/static correctly.
- Attempted active `/etc/caddy/Caddyfile` health-route correction was blocked by non-interactive `sudo`.
- Remaining Caddy drift: active system Caddy lacks `/healthz*` handler, so `/healthz` returns frontend 404.

## Seed/Data Cleanup Actions

- Backup created before mutation: `pre_cleanup_backup.sql`.
- Active users kept/created:
  - `admin` role `admin`
  - `pgr001` role `resident`
  - `sup001` role `supervisor`
- Users deactivated/archived: 26.
- Sample link created: `sup001 -> pgr001`.
- UTRMC hospital action: deactivated, not deleted, to preserve FK/matrix integrity.
- Other hospitals preserved.

## Tests/Smoke Checks Run

- Docker build/start: passed.
- `docker compose ps`: backend/frontend/db/redis healthy.
- Caddy validation:
  - `deploy/Caddyfile.pgsims`: valid
  - `/etc/caddy/Caddyfile`: valid
- Domain:
  - `/`: 200
  - `/login`: 200
  - `/api/`: 401 expected unauthenticated
  - `/static/admin/css/base.css`: 200
  - `/healthz`: 404 due active Caddy health-route drift
- Backend:
  - `python manage.py check`: passed
  - `python manage.py test sims.users.test_userbase_api`: passed
  - requested combined command with `sims.users.test_resident_onboarding`: failed because module is absent
- Frontend:
  - `npm run typecheck`: passed
  - `npm test -- --runInBand`: 39 suites / 114 tests passed

