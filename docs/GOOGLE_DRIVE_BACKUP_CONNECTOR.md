# Google Drive Backup Connector (OAuth)

## Purpose
This connector allows a **Super Admin** to connect Google Drive and upload **encrypted** PGSIMS backup artifacts (backup + manifest + checksum) into a dedicated Drive folder, then verify and download a copy back for restore staging.

This is the first cloud-backup connector for Backup Center and is designed to be additive (does not break local backup workflows).

## RBAC
Only **Super Admin** can:
- Connect / disconnect Google Drive
- Create/use the Drive backup folder
- Upload backups to Drive
- Verify Drive copies
- Download Drive copies for restore preparation

## Environment Variables
See `docs/ENVIRONMENT_VARIABLES.md` for the canonical list.

Minimum required:
- `GOOGLE_DRIVE_BACKUP_ENABLED=true`
- `GOOGLE_DRIVE_CLIENT_ID=...`
- `GOOGLE_DRIVE_CLIENT_SECRET=...`
- `GOOGLE_DRIVE_REDIRECT_URI=...`
- `PGSIMS_BACKUP_ENCRYPTION_KEY=...` (or `PGSIMS_BACKUP_ENCRYPTION_KEY_FILE=...`)

## OAuth Scopes
Default (recommended for least-privilege):
- `https://www.googleapis.com/auth/drive.file`

Note: `drive.file` can only access files/folders created by the app. The connector creates its own folder (default name `PGSIMS Backups`) and places all backup artifacts there.

## Backend Endpoints (current)
All endpoints are under `api/backup_center/`.

Connection:
- `GET  /api/backup_center/google-drive/status/`
- `GET  /api/backup_center/google-drive/connect/` (returns `authorization_url`)
- `GET  /api/backup_center/google-drive/oauth/callback/` (OAuth redirect target)
- `POST /api/backup_center/google-drive/disconnect/`
- `POST /api/backup_center/google-drive/health-check/`
- `POST /api/backup_center/google-drive/create-folder/`

Per-backup actions:
- `POST /api/backup_center/backups/{backup_id}/google-drive/upload/`
- `POST /api/backup_center/backups/{backup_id}/google-drive/verify/`
- `POST /api/backup_center/backups/{backup_id}/google-drive/download/`

List copies:
- `GET  /api/backup_center/google-drive/list/`

## Manual Google Console Setup (operator runbook)
1. Open Google Cloud Console.
2. Create/select a project.
3. Enable **Google Drive API**.
4. Configure OAuth consent screen.
5. Create OAuth client ID (Web application).
6. Add authorized redirect URI:
   - Example (prod): `https://your-domain.com/api/backup_center/google-drive/oauth/callback/`
   - Example (local): `http://localhost:8000/api/backup_center/google-drive/oauth/callback/`
7. Copy client ID + client secret into server environment variables:
   - `GOOGLE_DRIVE_CLIENT_ID`
   - `GOOGLE_DRIVE_CLIENT_SECRET`
8. Set:
   - `GOOGLE_DRIVE_REDIRECT_URI` (must match exactly)
   - `GOOGLE_DRIVE_BACKUP_ENABLED=true`
9. Restart backend.
10. Log in as Super Admin → Backup Center → “Google Drive Backup” panel → Connect.

Do not commit secrets into the repository.

## Troubleshooting
- “Google Drive backup is disabled”: set `GOOGLE_DRIVE_BACKUP_ENABLED=true` and restart.
- “Missing Google OAuth configuration”: ensure `GOOGLE_DRIVE_CLIENT_ID`, `GOOGLE_DRIVE_CLIENT_SECRET`, `GOOGLE_DRIVE_REDIRECT_URI` are set.
- “Backup encryption key is not configured”: set `PGSIMS_BACKUP_ENCRYPTION_KEY` (or `PGSIMS_BACKUP_ENCRYPTION_KEY_FILE`).
- “Invalid or expired OAuth state”: restart the OAuth connect flow; states expire after ~10 minutes.
- “Token refresh failed”: Google may have revoked refresh token; disconnect and reconnect.

