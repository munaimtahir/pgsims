# Phase B — Runtime Reset Report

Date (UTC): 2026-04-21

## Actions Executed
1. Took verified pre-purge snapshot at `docs/_archive/_snapshots/cleanup-20260421T053906Z`.
2. Stopped stack and removed compose-managed runtime volumes:
   - `docker compose -f docker/docker-compose.yml --env-file .env down -v --remove-orphans`
3. Purged local runtime/generated artifacts:
   - `output/`, `OUT/`, `frontend/e2e/output/`, `frontend/e2e/screenshots/`
   - `frontend/.next/`, backend runtime caches, local `backend/db.sqlite3`
4. Recreated clean runtime directories only.
5. Rebuilt runtime services:
   - `docker compose ... up -d`
6. Re-applied migrations and seeded only canonical organization reference data:
   - `python manage.py migrate --noinput`
   - `python manage.py seed_org_data`
7. Recreated minimal verification accounts by role (plus bootstrap admin):
   - `admin`
   - `pilot_pg`
   - `pilot_resident`
   - `pilot_supervisor`
   - `pilot_utrmc_admin`
   - `pilot_utrmc_user`

## Post-Reset Runtime State
- Services: backend/frontend/db/redis/worker/beat all running healthy.
- Runtime artifact dirs reset to minimal footprint (~4K each).
- DB baseline counts:
  - `users.User`: 6
  - `academics.Department`: 20
  - `rotations.Hospital`: 3
  - `rotations.HospitalDepartment`: 45
  - Transactional training data: 0 in key tables (`TrainingProgram`, `ResidentTrainingRecord`, `RotationAssignment`, `LeaveRequest`, `LogbookEntry`, `ResidentSubmission`)
  - Notifications: 0

## Notes
- During reset, a transient migrate invocation reported duplicate-column conflict while services were converging; final migration state converged to **no pending migrations** and baseline was rebuilt cleanly.
- This phase intentionally reset runtime state only; repository cleanup is handled separately in Phase C.
