# Drive Upload Proof

## Requirements
- Encrypt backup locally before upload
- Upload encrypted backup + manifest + checksum to Drive folder
- Record file ids and metadata
- Verify remote copy

## Status
- Upload workflow implemented (encrypted backup + manifest + checksum) and records `BackupCloudCopy` (`backend/sims/backup_center/google_drive.py`).
- Endpoint: `POST /api/backup_center/backups/{id}/google-drive/upload/`
- Live Drive API exercise pending real credentials.
