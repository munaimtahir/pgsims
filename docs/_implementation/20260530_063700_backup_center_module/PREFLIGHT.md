# PREFLIGHT: Backup Center Module

## Environment Overview
1. **Current branch**: `main`
2. **Working tree status**: Ahead of origin/main by 1 commit, with uncommitted files (bulk data setup files, E2E tests).
3. **Latest commit hash**: `8024cacf422259c0ed050cfc2757a99f43eb65a8`
4. **Current app version**: Pilot Baseline v1.0 (Real-Data Ready Candidate / GO) based on docs/CURRENT_FINAL_STATE.md
5. **Docker/service status**: `docker compose ps` shows services are running (backend, frontend, postgres db, redis, celery beat, celery worker).
6. **Backend framework structure**: Django REST Framework API under `backend/`. Apps: users, academics, rotations, bulk, training, notifications, audit.
7. **Frontend framework structure**: Next.js 14 under `frontend/`.
8. **Database engine**: PostgreSQL (running in Docker `pgsims_db`). Fallback SQLite in settings.
9. **Media folder path**: `backend/media` (`MEDIA_ROOT = BASE_DIR / "media"`).
10. **Admin/system menu structure**: Django Admin is enabled. React frontend has specific routing for UTRMC admin operations. Will integrate Backup UI into frontend UTRMC system dashboard.
11. **Authentication and RBAC**: JWT authentication (`rest_framework_simplejwt`). Custom `User` model with roles (super admin, admin, hod, supervisor, resident).
12. **Audit log pattern**: `django-simple-history` is actively used (`HistoricalUser`, `HistoricalResidentTrainingRecord`).
13. **Import/onboarding backup needs**: Needs to be implemented before real-data onboarding to allow safe fallback.

## Preflight Command Results
- `docker compose -f docker/docker-compose.yml ps`: All containers up.
- `python manage.py check`: Passed with 0 silenced issues.
- `python manage.py showmigrations`: All core migrations applied.
- `python manage.py makemigrations --check --dry-run`: No changes detected.
