# FINAL_REPORT — Backup Center Final Verified Module (Pilot Baseline v1.2)

Date (UTC): 2026-05-30

## 1) Executive summary
Backup Center is verified end-to-end for:
- Creating **Regular System Backups** (`.pgsimsbak`) that include **database + media + manifest + integrity checks**
- Creating **Full Server Recovery Backups** (`.pgsimsdr`) that embed a routine backup plus recovery notes
- Validating backup archives (integrity + required contents)
- Running **dry-run restore validation** safely (non-destructive)
- Proving **fresh-compatible restore** behavior in an isolated test harness (IDs + password hash + same-password login + media)
- Providing a safer, operator-facing Backup Center UI + tests + E2E smoke coverage

## 2) Branch and commit hash
- Branch: `main`
- HEAD: `5861184352634d8a75b5709ae6e32c935d4126ed`

## 3) Baseline version before sprint
- `docs/CURRENT_FINAL_STATE.md` previously reported Pilot Baseline v1.0 (out-of-sync with current Backup Center module state).

## 4) Target version after sprint
- Pilot Baseline v1.2 — Backup Center Final Verified Module

## 5) Database engine detected
- Local/dev verification: SQLite (`django.db.backends.sqlite3`)
- Docker runtime verification: PostgreSQL (`django.db.backends.postgresql`)

## 6) Regular System Backup scope (.pgsimsbak)
See `BACKUP_CONCEPT_LOCK.md` for full contract.

Key behaviors:
- DB dump (PostgreSQL native `pg_dump` / SQLite `dumpdata`)
- Media folder included when present
- `manifest.json`, `backup_report.json`, `checksum.sha256`
- Table counts + media summary (+ media tree hash) captured in manifest

## 7) Full Server Recovery Backup scope (.pgsimsdr)
See `BACKUP_CONCEPT_LOCK.md` for full contract.

Key behaviors:
- Disaster bundle contains an internal `.pgsimsbak`
- Includes deployment metadata + env template + restore instructions
- Excludes unencrypted secrets

## 8) Files changed
See `FILES_CHANGED.md`.

## 9) Models verified/added
Models are present and aligned with module requirements:
- `BackupJob`, `RestoreJob`, `BackupAuditLog`
See `MODEL_DECISIONS.md`.

## 10) Services verified/added
Location: `backend/sims/backup_center/services.py`
- Routine backup creation (DB + media + manifest + checksums)
- Disaster backup creation (wraps routine backup + metadata)
- Validation (required entries + supported version + integrity verification)
- Restore flow:
  - Super Admin only
  - Dry-run path is non-destructive
  - Destructive restore requires typed `RESTORE` + password confirmation
  - Automatic safety backup before destructive restore
  - Media restore + sequence reset (fixture-based restore)

## 11) API endpoints verified/added
Base prefix:
- `/api/backup_center/` (existing routing)

Verified endpoints:
- `GET /api/backup_center/backups/`
- `POST /api/backup_center/backups/create-routine/`
- `POST /api/backup_center/backups/create-disaster/`
- `GET /api/backup_center/backups/<id>/download/`
- `DELETE /api/backup_center/backups/<id>/delete/`
- `POST /api/backup_center/backups/<id>/validate/` (added)
- `POST /api/backup_center/restores/upload/`
- `POST /api/backup_center/restores/<id>/validate/`
- `POST /api/backup_center/restores/<id>/dry-run/`
- `POST /api/backup_center/restores/<id>/confirm/`
- `GET /api/backup_center/restores/`
- `GET /api/backup_center/audit-logs/`

## 12) UI pages verified/added
Route:
- `/dashboard/utrmc/backup`

Operator-facing sections verified:
- Status summary cards
- Create Backup section with two pathways
- Backup History table with Download / Check File / View Details / Delete
- Restore Wizard section with strong warnings and confirm locks
- Audit Log section

## 13) Management commands verified/added
Verified:
- `python3 manage.py create_system_backup --routine`
- `python3 manage.py create_system_backup --disaster`
- `python3 manage.py validate_system_backup <path>.pgsimsbak`
- `python3 manage.py validate_system_backup <path>.pgsimsdr`
- `python3 manage.py restore_system_backup <path>.pgsimsbak --dry-run`

## 14) Access control behavior
- API endpoints are protected by authentication + Super Admin checks.
- UI hides restore initiation controls for non-admin roles (backend remains source of truth).

## 15) Manifest behavior
`manifest.json` includes:
- app name/version
- backup kind + format version
- database engine
- media included flag + media summary (+ tree hash when available)
- table count summary
- optional notes

## 16) Checksum / file integrity behavior
`checksum.sha256` contains component-level hashes:
- database dump
- manifest
- backup report
- optional media tree hash

Validation recomputes and rejects mismatches.

## 17) Table count behavior
- `table_counts` captures ORM counts per model label at backup time.

## 18) Media backup behavior
- Media folder is copied into archive when present.
- Media summary includes file count + total bytes.
- Optional media tree hash is computed for integrity verification.

## 19) Backup validation behavior
Validation checks:
- extension + ZIP validity
- required members present
- manifest app/kind/version fields
- media presence when `media_included=true`
- checksum file present + integrity verified
- `.pgsimsdr` internal `.pgsimsbak` is validated too

## 20) Routine restore behavior
Restore behavior verified in isolated harness (see `RESTORE_PROOF.md`):
- preserves primary keys
- preserves password hashes
- preserves same-password login
- restores media file contents

## 21) Disaster recovery behavior
- Disaster bundle validation + internal routine restore support verified (validation path).

## 22) Safety backup behavior
- Destructive restore triggers a `safety_pre_restore` routine backup automatically before applying DB/media changes.

## 23) Password hash/user login preservation behavior
- Proven in isolated restore test: user password hash preserved exactly; same password authenticates post-restore.

## 24) Fresh-compatible install restore proof
See `RESTORE_PROOF.md`.

## 25) UI verification
See `UI_VERIFICATION.md`.

## 26) Frontend test/build results
See `TEST_RESULTS.md`.

## 27) Backend test results
See `TEST_RESULTS.md`.

## 28) E2E/smoke test results
See `TEST_RESULTS.md` (`Playwright smoke: 24 passed`).

## 29) Runtime/Docker health result
Docker services were running and smoke tests executed against the local Docker frontend/backend URLs (see `PREFLIGHT.md` and `TEST_RESULTS.md`).

## 30) Known issues
- Docker images typically do not contain `.git/` or `git`; manifest branch/commit may be `unknown`. Supported env overrides: `PGSIMS_GIT_BRANCH`, `PGSIMS_GIT_COMMIT`.
- Local `npm install` reports known npm dependency vulnerabilities; not auto-fixed in this sprint to avoid unintended upgrades.

## 31) Deferred items
- Optional encrypted secrets bundle for `.pgsimsdr` (intentionally deferred for safety).
- Postgres destructive restore proof on a fully separate disposable DB instance (dry-run + validation + backup creation validated; destructive restore remains restricted to an isolated/safe environment only).

## 32) Final verdict
**GO** for Backup Center module readiness for pilot operations *with the non-negotiable rule preserved*: destructive restore must only be performed on an isolated/safe target (never staging/real without explicit operator procedure).

## 33) Exact next steps before real data import
1. In production environment, ensure `SECRET_KEY` and DB credentials are set (Docker compose uses an env file).
2. From Backup Center, create and download a **Regular System Backup** before first real import.
3. Store backups off-server (operator policy).
4. Validate the backup file (“Check File”) before any restore operation.

