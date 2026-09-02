# Drive Download Proof

## Requirements
- Download encrypted backup from Drive
- Verify checksum
- Decrypt to restore-staging
- Mark restore-ready for existing restore workflow

## Status
- Download workflow implemented: download encrypted bytes → verify checksum → decrypt → store as `RestoreJob` upload (`backend/sims/backup_center/google_drive.py`, `backend/sims/backup_center/views.py`).
- Endpoint: `POST /api/backup_center/backups/{id}/google-drive/download/`
- Live Drive API exercise pending real credentials.
