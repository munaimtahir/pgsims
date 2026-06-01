# Architecture

## Components
- Django backend (`sims.backup_center`)
  - Models: Drive connection + Drive cloud copy metadata
  - OAuth: connect + callback + disconnect
  - Drive API client: folder ensure, upload, verify, download
  - RBAC: Super Admin only for Drive operations
- Next.js frontend (Backup Center page)
  - Minimal “Google Drive Backup” panel for Super Admin actions and status

## Security
- OAuth tokens are stored encrypted at rest.
- Tokens/secrets are never returned in API responses.
- Uploads are encrypted locally before sending to Google Drive.

