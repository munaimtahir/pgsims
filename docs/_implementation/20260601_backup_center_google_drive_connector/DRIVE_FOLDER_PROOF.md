# Drive Folder Proof

## Requirements
- Use `GOOGLE_DRIVE_BACKUP_FOLDER_ID` if configured
- Else create/find `PGSIMS Backups` folder via Drive API
- Persist folder id/name in connection

## Status
- Backend supports `GOOGLE_DRIVE_BACKUP_FOLDER_ID` override and “create/find by name” fallback (`backend/sims/backup_center/google_drive.py`).
- Live Drive API exercise pending real credentials.
