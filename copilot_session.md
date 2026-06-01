# Copilot Session - Backup Center Google Drive Connector

SESSION WINDOW (2026-06-01 UTC)
==============================

PRIMARY PURPOSE
  Implement Google Drive OAuth connection + encrypted upload/download for Backup Center (first cloud connector).

IN-SCOPE (ALLOWED)
  - Backend: OAuth connect/callback/disconnect, token storage (encrypted), Drive folder create/select, upload/verify/download, management commands
  - Frontend: minimal Google Drive panel in existing Backup Center page (no route/nav changes)
  - Tests: backend unit/integration tests with mocks; frontend tests only if UI changes require them
  - Docs: evidence folder + operator/setup documentation + contracts updates (terminology note)

OUT-OF-SCOPE (FORBIDDEN)
  - New providers (GCS/S3/MinIO/etc) beyond placeholders/interfaces
  - Major Backup Center redesign or terminology changes beyond explicitly documented note
  - Retention automation / deletions in Drive

SUCCESS CRITERIA
  - Super Admin can connect Google Drive (OAuth) and disconnect
  - Tokens stored encrypted (no raw tokens in DB/API responses)
  - Drive folder ensured/selected and persisted
  - Encrypted backup + manifest + checksum upload to Drive, verified, recorded in BackupCloudCopy
  - Download verified Drive copy, decrypt to restore-staging, mark restore-ready for existing restore workflow
  - Existing local Backup Center flow remains intact
  - Tests pass (`python manage.py test`; frontend checks if touched)

FALLBACK PLAN
  If live OAuth cannot be exercised (no client ID/secret):
  1) Ensure mocked tests cover OAuth/token refresh/upload/download behaviors
  2) Document manual Google Console setup steps
  3) Mark verdict as CONDITIONAL GO

GUARDRAILS ACTIVE
  - Contract-first: document API + terminology note under `docs/contracts/`
  - Frozen UX: no route/nav label changes; only additive “Google Drive Backup” panel
  - No secrets committed

---

## Current Branch / Commit
- Branch: `main`
- Commit: `68d0689a9cd852ffb085d165af4c760d69cd0bad`

## Sprint Objective
Super Admin connects Google Drive → secure token storage → Drive folder selection → upload encrypted backup + manifest + checksum → verify → record metadata → download + decrypt for restore staging.

## Checklist (living)
- [ ] Create evidence folder under `docs/_implementation/20260601_backup_center_google_drive_connector/`
- [ ] Add env var docs + code gating `GOOGLE_DRIVE_BACKUP_ENABLED`
- [ ] Implement `BackupCloudConnection` + `BackupCloudCopy` models + migrations
- [ ] Implement encrypted token storage helpers
- [ ] Implement OAuth connect/callback/disconnect endpoints + CSRF state
- [ ] Implement Drive provider: health check, folder ensure, upload, verify, download
- [ ] Implement Backup Center endpoints for status/upload/verify/download/list
- [ ] Add management commands
- [ ] Add minimal UI panel in Backup Center
- [ ] Add backend tests (OAuth, encryption, provider mocks, RBAC)
- [ ] Run tests (backend required; frontend if changed)
- [ ] Update contracts + docs + evidence proofs
- [ ] Commit: `Add Google Drive backup connector`

## Files Inspected (living)
- `docs/ANTI_DRIFT_GUARDRAILS.md`
- `docs/PROD_GATE_CLOSURE/00_README.md`
- `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md`
- `backend/sims/backup_center/encryption.py`
- `backend/sims/backup_center/models.py`
- `backend/sims/backup_center/services.py`
- `backend/sims/backup_center/views.py`
- `backend/sims/backup_center/urls.py`
- `frontend/app/dashboard/utrmc/backup/page.tsx`
- `frontend/lib/auth/fetch.ts`

## Files Changed (living)
- `copilot_session.md`
- `backend/sims/backup_center/encryption.py`
- `backend/sims/backup_center/google_drive.py`
- `backend/sims/backup_center/models.py`
- `backend/sims/backup_center/views.py`
- `backend/sims/backup_center/urls.py`
- `backend/sims/backup_center/admin.py`
- `backend/sims/backup_center/tests.py`
- `backend/sims/backup_center/migrations/0005_backupcloudconnection_alter_backupauditlog_action_and_more.py`
- `backend/sims/backup_center/management/commands/google_drive_backup_status.py`
- `backend/sims/backup_center/management/commands/google_drive_backup_health_check.py`
- `backend/sims/backup_center/management/commands/upload_backup_to_google_drive.py`
- `backend/sims/backup_center/management/commands/verify_google_drive_backup.py`
- `backend/sims/backup_center/management/commands/download_google_drive_backup.py`
- `frontend/components/backup/GoogleDrivePanel.tsx`
- `frontend/components/backup/RestoreModal.tsx`
- `frontend/app/dashboard/utrmc/backup/page.tsx`
- `docs/GOOGLE_DRIVE_BACKUP_CONNECTOR.md`
- `docs/ENVIRONMENT_VARIABLES.md`
- `docs/BACKUP_AND_RESTORE.md`
- `docs/OPERATIONS_GUIDE.md`
- `docs/contracts/API_CONTRACT.md`
- `docs/contracts/ROUTES.md`
- `docs/contracts/TERMINOLOGY.md`
- `docs/_implementation/20260601_backup_center_google_drive_connector/*`

## Commands Executed (living)
- `git rev-parse --abbrev-ref HEAD`
- `git rev-parse HEAD`
- `sed -n '1,200p' docs/ANTI_DRIFT_GUARDRAILS.md`
- `sed -n '1,200p' docs/PROD_GATE_CLOSURE/00_README.md`
- `sed -n '1,120p' docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md`
- `rg -n "Backup Center|backup center|backup_history|restore wizard|BackupCloud|cloud copy|backup" backend/sims -S | head`
- `sed -n '1,220p' backend/sims/backup_center/encryption.py`
- `sed -n '1,260p' backend/sims/backup_center/providers.py`
- `sed -n '1,260p' backend/sims/backup_center/models.py`
- `sed -n '840,1120p' backend/sims/backup_center/services.py`
- `sed -n '1,240p' frontend/app/dashboard/utrmc/backup/page.tsx`
- `sed -n '1,220p' frontend/lib/auth/fetch.ts`
- `cd backend && python3 manage.py makemigrations backup_center`
- `cd backend && python3 manage.py test`
- `cd frontend && npm test`
- `cd frontend && npm run typecheck`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`

## Tests Run (living)
- Backend: `cd backend && python3 manage.py test` (PASS)
- Frontend: `cd frontend && npm test` (PASS)
- Frontend: `cd frontend && npm run typecheck` (PASS)
- Frontend: `cd frontend && npm run lint` (PASS)
- Frontend: `cd frontend && npm run build` (PASS)

## Evidence Generated (living)
- `docs/_implementation/20260601_backup_center_google_drive_connector/` (proof docs + final report)

## Final Verdict
- CONDITIONAL GO (implementation + tests pass; live OAuth/upload/download requires operator credentials)
