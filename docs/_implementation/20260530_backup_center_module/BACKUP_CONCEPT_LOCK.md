# Backup Concept Lock - PGSIMS Backup Center

## 1. Routine Application Data Backup (.pgsimsbak)
- **Purpose**: Operational backup for migrations, updates, and daily use.
- **Scope**: Full database state + all user-uploaded media.
- **Format**: Single compressed archive containing:
  - Database dump (native format based on engine).
  - `media/` folder contents.
  - `manifest.json`: Metadata about the backup.
  - `checksum.sha256`: Integrity verification.
  - `backup_report.json`: Detailed summary of rows and files.
- **Portability**: Must be restorable on any compatible PGSIMS installation.
- **User Continuity**: Must preserve all users, password hashes, roles, and records.

## 2. Full Disaster Recovery Backup (.pgsimsdr)
- **Purpose**: Server-level recovery after total loss of environment.
- **Scope**: Routine Application Data Backup + Infrastructure metadata.
- **Format**: Single compressed archive containing:
  - Routine Backup (.pgsimsbak).
  - `deployment_metadata/`: OS, Docker, and engine versions.
  - `env_templates/`: Template `.env` files (no actual secrets).
  - `restore_instructions.md`: Step-by-step guide for fresh server setup.
  - `scripts/`: Optional helper scripts for environment initialization.
- **Secrets Policy**: No plain-text secrets. Optional encrypted bundle if passphrase provided.

## 3. Restore Logic
- **Safety First**: Always create an automatic safety backup before any restore.
- **Validation**: Mandatory checksum and manifest verification before allowing restore.
- **Admin Only**: Super Admin role required for all restore operations.
- **Confirmation**: Required: Password, typed "RESTORE", and checkbox confirmation.

## 4. Audit & History
- Every action (backup, download, delete, validate, restore) is logged in `BackupAuditLog`.
- Status tracking for every `BackupJob` and `RestoreJob`.
