# API Discovery (2026-06-02 UTC)

Base prefix: `/api/backup_center/`

## Google Drive connector endpoints (Super Admin only)
- `GET  /api/backup_center/google-drive/status/`
  - Response keys: `enabled`, `status`, `connected_account`, `backup_folder`, `token_expiry`, `last_health_check_at`, `last_error`, `updated_at`
- `GET  /api/backup_center/google-drive/connect/` → `{ authorization_url }`
- `GET  /api/backup_center/google-drive/oauth/callback/` (browser redirect target)
- `POST /api/backup_center/google-drive/disconnect/`
- `POST /api/backup_center/google-drive/health-check/`
- `POST /api/backup_center/google-drive/create-folder/` → `{ status: "ready", backup_folder: {id,name} }`
- `GET  /api/backup_center/google-drive/list/` → `{ results: BackupCloudCopy[] }`

## Per-backup actions
- `POST /api/backup_center/backups/{backup_id}/google-drive/upload/` → `{ status: "uploaded", cloud_copy_id }`
- `POST /api/backup_center/backups/{backup_id}/google-drive/verify/` → `{ status: "verified", cloud_copy_id }`
- `POST /api/backup_center/backups/{backup_id}/google-drive/download/`
  - Success: `{ status: "restore_ready", restore_job_id, cloud_copy_id }`

## Notes
- API never returns tokens/secrets.
- `connected_account` may be null when using least-privilege scope (`drive.file`).

