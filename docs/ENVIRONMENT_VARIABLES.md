# Environment Variables

This document lists notable environment variables used by PGSIMS operations workflows.

## Backup Encryption (required for Drive upload)
- `PGSIMS_BACKUP_ENCRYPTION_KEY` (string; raw key material; used to derive a Fernet key)
- `PGSIMS_BACKUP_ENCRYPTION_KEY_FILE` (file path; alternative to `PGSIMS_BACKUP_ENCRYPTION_KEY`)

If neither is set, encrypted upload/download workflows are blocked.

## Google Drive Backup Connector
- `GOOGLE_DRIVE_BACKUP_ENABLED` (`true|false`, default `false`)
- `GOOGLE_DRIVE_CLIENT_ID` (OAuth client id; do not commit)
- `GOOGLE_DRIVE_CLIENT_SECRET` (OAuth client secret; do not commit)
- `GOOGLE_DRIVE_REDIRECT_URI` (must match Google Console redirect URI exactly)
- `GOOGLE_DRIVE_SCOPES` (default: `https://www.googleapis.com/auth/drive.file`)
- `GOOGLE_DRIVE_BACKUP_FOLDER_NAME` (default: `PGSIMS Backups`)
- `GOOGLE_DRIVE_BACKUP_FOLDER_ID` (optional; if set, overrides folder discovery/creation)

