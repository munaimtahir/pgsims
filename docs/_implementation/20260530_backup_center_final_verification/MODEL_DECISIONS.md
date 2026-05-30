# MODEL_DECISIONS — Backup Center

Date (UTC): 2026-05-30

## Models (backend)
Location: `backend/sims/backup_center/models.py`

### BackupJob
Fields include:
- `backup_kind`: `routine_application_data` | `disaster_recovery`
- `backup_type`: `manual` | `automatic` | `safety_pre_restore`
- `status`: `pending` | `running` | `completed` | `failed` | `cancelled` | `deleted`
- File metadata: `file_path`, `file_name`, `file_size`, `checksum`
- Content metadata: `manifest_json`, `database_engine`, `media_included`, `table_counts_json`, `media_summary_json`
- Build metadata: `app_version`, `branch`, `commit_hash`
- Audit metadata: `created_by`, `created_at`, `completed_at`, `error_message`, `notes`

### RestoreJob
Fields include:
- `restore_kind`: `routine_application_data_restore` | `disaster_recovery_restore`
- Linkage: `backup_job` (nullable), `safety_backup` (nullable)
- Upload: `uploaded_file` (stored under `restore_uploads/`), `uploaded_file_name`
- `status`: `pending` | `validation_failed` | `validation_passed` | `restoring` | `restored` | `failed` | `cancelled`
- `validation_result_json`, `post_restore_check_json`, `restored_by`, `started_at`, `completed_at`, `error_message`, `notes`

### BackupAuditLog
Fields include:
- `action`: includes backup/create/validate/download/delete + restore/upload/validate/dry-run/complete/fail
- `actor`, `backup_job`, `restore_job`
- `ip_address`, `user_agent`, `details_json`, `created_at`

## Key design constraints
- Restore operations replace the database state; post-restore tracking records are written into the restored DB state.
- Restore upload files are stored via the model `FileField` (no ad-hoc storage path strings).

