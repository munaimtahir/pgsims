# PGSIMS Backup and Restore Operations Guide

## 1. Purpose
This document outlines the procedures for creating, downloading, validating, and restoring system backups in the PGSIMS application. The Backup Center module is designed to prioritize data safety and provide an audit trail for all backup and restore activities.

## 2. Who Can Use Backup Center
- **Super Admins**: Full access to create, download, validate, delete backups, and perform system restores.
- **Admins**: Limited access to create and download backups (if enabled by policy). Cannot perform restores.
- **HODs, Supervisors, Residents**: No access.

## 3. What the Backup Includes
- **Database Dump**: Full relational database state.
- **Media Files**: Contents of the `media/` directory (user uploads, certificates, etc.).
- **Manifest (`manifest.json`)**: Backup metadata (timestamps, versions, included components).
- **Checksum (`checksum.txt`)**: Integrity verification hash.
- **Backup Report**: Summary of the backup job.

## 4. What the Backup Excludes
- `.env` files and environment variables.
- Secret keys, API tokens, and passwords.
- Source code directories (`node_modules`, `.venv`).
- Temporary/cache files.

## 5. How to Create a Manual Backup
**Via UI**:
1. Log in as a Super Admin.
2. Navigate to the **Backup Center** in the system dashboard.
3. Click **Create Full Backup**.
4. The backup job will run in the background. Its status will update to `completed` in the Backup History table once finished.

**Via CLI**:
```bash
python manage.py create_system_backup --full --notes "Manual backup before major update"
```

## 6. How to Download a Backup
1. In the **Backup Center**, locate the completed backup in the history table.
2. Click the **Download** button to securely fetch the ZIP archive.

## 7. How to Validate a Backup
**Via UI**:
1. In the **Restore Backup** section, upload the backup ZIP file.
2. Click **Validate Backup**.
3. The system will verify the ZIP integrity, checksums, and manifest file. The restore button will remain disabled if validation fails.

**Via CLI**:
```bash
python manage.py validate_system_backup /path/to/backup.zip
```

## 8. How Restore Works
A restore operation replaces the current database and media files with those from the backup. This is a highly destructive operation.

To restore:
1. Upload and successfully validate a backup file.
2. An automatic "Safety Backup" of the current system state is generated in the background.
3. Enter your Super Admin password.
4. Type `RESTORE` into the confirmation box.
5. Check the final confirmation checkbox and click **Restore**.

## 9. Why Restore is Restricted
Restoring a backup completely overwrites active production data. To prevent accidental data loss or unauthorized tampering, the restore function is strictly limited to Super Admins and shielded by multiple confirmation layers.

## 10. Automatic Safety Backup Before Restore
Before any destructive restore begins, the system forces a full backup of the existing state. If the restore fails or causes unintended issues, the system can be rolled back using this safety backup.

## 11. Backup Before Real Import
Before performing bulk data imports (e.g., onboarding residents):
1. Create a full backup.
2. Download and validate the backup.
3. Run the import dry-run.
4. Execute the import.

## 12. Backup After Real Import
Once the import is successfully verified:
1. Create a post-import full backup to lock in the new baseline.

## 13. Restore Emergency Steps
If a restore fails mid-operation:
1. Do not initiate another restore immediately.
2. Check the server logs (or BackupAuditLog) to identify the failure point.
3. Locate the automatic safety backup created just before the restore attempt.
4. Use the CLI to dry-run the safety backup restore: `python manage.py restore_system_backup /path/to/safety_backup.zip --dry-run`
5. Proceed with CLI restore once the issue is identified.

## 14. Management Commands
- `python manage.py create_system_backup --full`
- `python manage.py validate_system_backup <path>`
- `python manage.py restore_system_backup <path> --confirm --typed-confirmation RESTORE`

## 15. Future Scheduled Backup Plan
A Celery-based scheduled backup task scaffold will be provided. In the future, this can be configured to run nightly database dumps automatically.

## 16. Offsite Backup Recommendation
It is strongly recommended to copy downloaded backup archives to secure, offsite cold storage (e.g., AWS S3 or dedicated backup servers) regularly.

## 17. Known Limitations
- Partial restores (e.g., restoring only one table) are not supported. Only full system restores are permitted.
- The UI restore process requires a stable HTTP connection during the upload and validation phases. Large backups may require CLI restoration to avoid HTTP timeouts.
