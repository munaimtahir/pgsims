# OAuth Flow Proof

## What to capture
- Connect endpoint response (sanitized) showing authorization URL generated
- Callback success path stores connection and redirects to Backup Center
- Callback failure path records safe error and redirects with failure indicator

## Status
- Implemented endpoints:
  - `GET /api/backup_center/google-drive/connect/` (returns `authorization_url`)
  - `GET /api/backup_center/google-drive/oauth/callback/` (validates state, exchanges code, stores encrypted tokens, redirects back)
  - `POST /api/backup_center/google-drive/disconnect/`
- Test coverage: mocked OAuth exchange + state validation in `backend/sims/backup_center/tests.py`
- Live OAuth: pending operator credentials (see `docs/GOOGLE_DRIVE_BACKUP_CONNECTOR.md`)
