# 01 Pre-Import Runtime State

## Repository / Runtime Discovery

- Repo root: `/home/munaim/srv/apps/pgsims`
- Active branch: `main`
- Compose file: `docker/docker-compose.yml`
- Runtime services:
  - `pgsims_backend`
  - `pgsims_frontend`
  - `pgsims_db`
  - `pgsims_redis`
  - `pgsims_worker`
  - `pgsims_beat`

## Pre-Import Safety Artifacts

- Database backup:
  - `docs/_pilot_import/20260403T202004Z/pre_import_db_backup.sql`
  - size at creation: `~265K`
- Canonical package presence verified:
  - `pilot_data/first_pilot_run/final_supervisors_list.csv`
  - `pilot_data/first_pilot_run/final_residents_list.csv`
  - `pilot_data/first_pilot_run/final_supervision_links.csv`
  - `pilot_data/first_pilot_run/final_training_programs.csv`
  - `pilot_data/first_pilot_run/final_resident_training_records.csv`
  - `pilot_data/first_pilot_run/final_pilot_workbook.xlsx`

## Runtime Health (Pre-Import)

- Backend health: `{"status":"healthy","checks":{"database":"ok","cache":"ok","celery":"ok"}}`
- Frontend status: `HTTP/1.1 200 OK`
- Compose status: all six services up and healthy/started

## Active Runtime Env Snapshot (backend container)

- `DATABASE_URL=postgresql://sims_user:...@db:5432/sims_db`
- `DEBUG=False`
- `ALLOWED_HOSTS` includes deployed domains plus localhost/internal service names
- `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` configured for deployed domains
- Redis/Celery broker URLs set and resolved

## Notes

- During service rebuild, an intermediate crash-loop happened when compose was launched without explicit env binding. Recovery was completed using `docker compose --env-file .env ...`, and health returned to green before import resumed.

