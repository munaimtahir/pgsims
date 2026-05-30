# Backup Scope and Safety Design

## Overview
The Backup Center Module provides a secure and reliable way to create full system backups and restore them if necessary. This design prioritizes the safety of existing data by introducing mandatory validations, confirmations, and safety backups before any destructive operations are performed.

## 1. Backup Scope
### Included Components
- **Database Dump**: Full relational database state (PostgreSQL `pg_dump` output or SQLite `db.sqlite3` copy).
- **Media Files**: Contents of the `media/` directory (if it exists).
- **Manifest (`manifest.json`)**: Contains backup metadata.
- **Checksum (`checksum.txt`)**: SHA-256 hash of the backup content for integrity verification.
- **Backup Report**: A structured JSON or markdown report detailing the backup job.

### Excluded Components
- `.env` files and environment variables.
- Secret keys, API tokens, and passwords.
- Source code directories (`node_modules`, `venv`, `__pycache__`).
- Temporary/cache files.

## 2. Backup Manifest Structure
The `manifest.json` file will contain the following fields:
```json
{
  "app_name": "PGSIMS",
  "backup_format_version": "1.0",
  "backup_type": "full",
  "created_at": "ISO-8601 Timestamp",
  "created_by": "username or email",
  "branch": "main",
  "commit_hash": "8024cacf422259c0ed050cfc2757a99f43eb65a8",
  "app_version": "Pilot Baseline v1.2",
  "database_engine": "django.db.backends.postgresql",
  "database_included": true,
  "media_included": true,
  "media_path": "media/",
  "included_components": ["database", "media", "manifest"],
  "excluded_components": ["secrets", "node_modules", ".venv"],
  "backup_file_name": "pgsims_backup_20260530_063700.zip",
  "backup_size": 10485760,
  "checksum_algorithm": "sha256",
  "checksum": "abc123hash...",
  "notes": "Pre-import safety backup"
}
```

## 3. Restore Safety Measures
Restoring a backup replaces current system data, making it a high-risk operation. The following safety measures are implemented:
1. **Validation Gate**: A backup ZIP file must pass stringent structural and checksum validations before it can be used for restore.
2. **Super Admin Restriction**: Only users with `is_superuser=True` can initiate a restore.
3. **Double Confirmation**: The user must enter their password and manually type "RESTORE" to proceed.
4. **Automatic Safety Backup**: Before any data is overwritten, a non-bypassable "safety backup" of the current state is created.
5. **Maintenance Lock**: (Optional/Deferred) During restore, the system may reject standard API traffic to avoid partial writes.
6. **Audit Trail**: Every step of the backup and restore process is securely logged to `BackupAuditLog`.
