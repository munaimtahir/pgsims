# Copilot Session - Backup Center Cloud Storage Infrastructure

## Session Info
- **Date**: 2026-05-31
- **Status**: IN_PROGRESS
- **Sprint**: PGSIMS Backup Center Cloud Storage Infrastructure Sprint
- **Objective**: Extend the Backup Center with native GCS and S3-compatible cloud storage, encryption-first workflows, testing, and UI integration.

## Execution Plan
1. [ ] Phase 1: Preflight and Environment setup (install packages: boto3, google-cloud-storage, cryptography)
2. [ ] Phase 2: Design and implement encryption/decryption utilities
3. [ ] Phase 3: Implement BackupStorageProvider abstraction and concrete GCS/S3 providers
4. [ ] Phase 4: Extend BackupJob model with cloud metadata and run migrations
5. [ ] Phase 5: Integrate providers with Backup Center services (upload, download, list, verify workflows)
6. [ ] Phase 6: Add management commands for cloud operations
7. [ ] Phase 7: Build API endpoints and adjust serializers
8. [ ] Phase 8: Integrate Cloud Backup settings and status in Frontend UI
9. [ ] Phase 9: Write comprehensive unit/integration tests
10. [ ] Phase 10: Run full gate checks, write documentation, and generate evidence proofs

## Storage Design Decisions
- **Provider Abstraction**: A clean interface `BaseBackupStorageProvider` in `sims/backup_center/providers.py` with `upload_backup`, `download_backup`, `list_backups`, `verify_remote_object`, and `health_check`.
- **Encryption**: Fernet symmetric encryption using `cryptography` package. Derives key via PBKDF2/SHA256 from `PGSIMS_BACKUP_ENCRYPTION_KEY` settings.
- **Provider Interchangeability**: Leverages settings variables `BACKUP_CLOUD_PROVIDER` ('local', 'gcs', 's3') to route calls dynamically.

## Files Inspected
- `backend/sims/backup_center/models.py`
- `backend/sims/backup_center/services.py`
- `backend/sims/backup_center/tests.py`
- `backend/sims/backup_center/views.py`
- `backend/sims/backup_center/urls.py`
- `frontend/app/dashboard/utrmc/backup/page.tsx`
- `frontend/components/backup/BackupList.tsx`

## Files Changed
- None yet

## Commands Executed
- None yet

## Tests Run
- None yet

## Evidence Generated
- None yet

## Final Verdict
- PENDING
