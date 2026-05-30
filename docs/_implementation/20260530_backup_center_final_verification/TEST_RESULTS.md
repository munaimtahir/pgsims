# TEST_RESULTS — Backup Center Final Verification

Date (UTC): 2026-05-30

## Runtime / Docker
- `docker compose -f docker/docker-compose.yml ps`: backend + frontend healthy (see `PREFLIGHT.md` for captured output).
- Frontend image rebuilt and container recreated to include latest Backup Center UI changes.

## Backend (Django)
Commands run:
- `cd backend && python3 manage.py check` → OK
- `cd backend && python3 manage.py makemigrations --check --dry-run` → No changes detected
- `cd backend && pytest` → **379 passed**
- `cd backend && python3 manage.py test` → **267 tests OK**

Focused module tests:
- `cd backend && pytest sims/backup_center/tests.py -q` → **11 passed**

## Management commands (non-destructive)
Commands run:
- `cd backend && python3 manage.py migrate` → `backup_center.0001_initial` applied (local sqlite dev DB)
- `cd backend && python3 manage.py create_system_backup --routine --notes "evidence: microsecond filename"`
  - Output (example): `PGSIMS_DATA_BACKUP_2026-05-30_225349_754696.pgsimsbak`
- `cd backend && python3 manage.py create_system_backup --disaster` → `.pgsimsdr` created
- `cd backend && python3 manage.py validate_system_backup <path>.pgsimsbak` → VALID
- `cd backend && python3 manage.py validate_system_backup <path>.pgsimsdr` → VALID (includes internal `.pgsimsbak` validation)
- `cd backend && python3 manage.py restore_system_backup <path>.pgsimsbak --dry-run` → Dry-run validation passed
- `cd backend && python3 manage.py restore_system_backup <path>.pgsimsbak --confirm` → refused (requires `--typed-confirmation RESTORE`)

## Docker backend (PostgreSQL) — Routine backup evidence
After rebuilding `docker-backend` and applying a drift-repair migration, the running Docker backend (PostgreSQL) successfully created and validated a routine backup:
- `docker exec pgsims_backend python manage.py create_system_backup --routine --notes "docker postgres routine backup evidence"`
- `docker exec pgsims_backend python manage.py validate_system_backup /app/backups/<generated>.pgsimsbak` → VALID
Notes:
- Git metadata inside Docker may show `branch=unknown` / `commit_hash=unknown` when `git` and `.git/` are not present (supported env overrides: `PGSIMS_GIT_BRANCH`, `PGSIMS_GIT_COMMIT`).

## Frontend (Next.js)
Commands run:
- `cd frontend && npm install` → OK (reported vulnerabilities noted; not auto-fixed in this sprint)
- `cd frontend && npm run lint` → OK
- `cd frontend && npm run typecheck` → OK
- `cd frontend && npm run build` → OK
- `cd frontend && npm run test` → **32 suites passed / 89 tests passed**

## E2E (Playwright)
Command run:
- `cd frontend && npm run test:e2e:smoke:local`
Result:
- **24 passed**
Includes Backup Center route smoke: `frontend/e2e/smoke/backup_center.spec.ts`
