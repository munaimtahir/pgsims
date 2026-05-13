# 2026-05-12 Clean Deploy and Baseline Reset

## Scope
- Removed the previous compose deployment and rebuilt the application from the current repository state.
- Cleared generated runtime artifacts (`output/`, `OUT/`, `frontend/.next/`, `frontend/e2e/output/`, `frontend/e2e/screenshots/`, `backend/db.sqlite3`).
- Re-seeded canonical org data and restored only the minimal active baseline.
- Removed test/demo runtime identities and transactional rows with the dedicated cleanup command.

## Deployment Actions
1. Brought down the existing stack with `docker compose -f docker/docker-compose.yml --env-file .env down -v --remove-orphans`.
2. Rebuilt and started the stack with `docker compose -f docker/docker-compose.yml --env-file .env up -d --build`.
3. Seeded canonical org data:
   - `python manage.py seed_org_data`
4. Applied the cleanup command to remove non-baseline runtime data:
   - `python manage.py cleanup_pilot_runtime --apply`
5. Restored the minimal active baseline accounts:
   - `python manage.py seed_active_surface_baseline`

## Verification
- Backend health: `GET http://127.0.0.1:8014/healthz/` returned `200` with `database`, `cache`, and `celery` checks all `ok`.
- Frontend health: `GET http://127.0.0.1:8082/` returned `200`.
- Compose services were healthy after redeploy:
  - `backend`, `db`, `redis`, and `frontend` healthy
  - `worker` and `beat` running

## Post-Reset Baseline
- Users: `6`
- Baseline pilot users: `5`
- `e2e_*` users: `0`
- `demo_*` users: `0`
- Hospitals: `4`
- Departments: `20`
- Hospital-department matrix rows: `50`
- Resident training records: `4`
- Remaining users:
  - `admin`
  - `pilot_pg`
  - `pilot_resident`
  - `pilot_supervisor`
  - `pilot_utrmc_admin`
  - `pilot_utrmc_user`

## Notes
- The cleanup command correctly removed the test/demo users and related runtime rows, but it also removed the pilot baseline accounts; those were restored immediately with `seed_active_surface_baseline`.
- I intentionally did not run `seed_e2e`, because that command seeds `e2e_*` identities and test-harness data that conflicts with the requested baseline-only cleanup.
- The frontend build emitted a non-blocking Browserslist warning about `caniuse-lite` being outdated; the build itself completed successfully and the container started normally.

