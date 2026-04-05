# Pilot Cleanup Summary

Timestamp: `2026-04-03T12:41:27Z`

Scope:
- Clean the live PGSIMS pilot environment without damaging structure, auth, migrations, master data, roles, permissions, departments, or hospital definitions.
- Remove demo, fake, seed, and test runtime data.
- Prepare a reusable cleanup path and a reusable pilot import path.
- Validate whether the system is ready for the first real pilot run.

System discovered:
- Backend: Django + DRF + Celery
- Frontend: Next.js
- Database: PostgreSQL 15
- Cache / broker: Redis 7
- Deployment: Docker Compose project `docker` via `docker/docker-compose.yml`
- Reverse proxy: external Caddy-oriented deployment assumptions in compose comments and env

Outcome:
- Live demo/test runtime data was purged from the active database.
- Canonical departments and the single canonical hospital were preserved.
- Backend startup was changed so normal service boot no longer runs `create_superadmin`.
- The app still boots and `admin` login still works.
- A fill-ready pilot source package was created under `pilot_data/first_pilot_run/`.
- Final pilot import still did not happen because those new files are intentionally empty until real pilot names are entered, and the conservative service recreate did not rebuild the backend image with the new import command.

Current readiness:
- Database cleanliness: achieved
- Deployment health: achieved
- Pilot data imported: not achieved
- First pilot readiness: `FAIL`

Primary blockers:
1. Real pilot roster values still do not exist; the new source files are present but header-only.
2. The live backend image was intentionally not rebuilt because the repository has many unrelated user changes; therefore the new `import_pilot_bundle` management command exists in the repo but not in the currently running backend container.

Reusable deliverables created in repo:
- `backend/sims/users/management/commands/cleanup_pilot_runtime.py`
- `backend/sims/users/management/commands/import_pilot_bundle.py`
- `pilot_data/first_pilot_run/final_supervisors_list.csv`
- `pilot_data/first_pilot_run/final_residents_list.csv`
- `pilot_data/first_pilot_run/final_pilot_workbook.xlsx`
- `scripts/build_pilot_workbook.py`
