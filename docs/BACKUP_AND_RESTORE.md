# Backup and Restore Guide

## Overview
PGSIMS provides a comprehensive Backup Center for ensuring data integrity and disaster recovery. The system supports two primary backup pathways.

## 1. Routine Application Data Backup (.pgsimsbak)
Used for routine operational safety. Includes everything needed to restore the application state on a compatible server.

**User label:** Regular System Backup

### Included:
- **Database**: Full dump of all tables, preserving primary keys, user IDs, and password hashes.
- **Media**: All user-uploaded documents, certificates, and profile images.
- **Metadata**: `manifest.json`, `backup_report.json`, `checksum.sha256`, and row/file count summaries.

### Excluded:
- System logs (non-audit).
- Temporary files and cache.
- Deployment-specific configuration (domain names, SSL certs).

## 2. Full Disaster Recovery Backup (.pgsimsdr)
Used for rebuilding PGSIMS on a completely fresh server.

**User label:** Full Server Recovery Backup

### Included:
- All contents of a Routine Application Data Backup.
- Deployment metadata (Docker versions, OS info).
- Environment templates.
- Restore instructions.

### Excluded:
- Plain-text secrets (.env files, API keys).
- Node modules / Virtual environments.
- Build artifacts.

## Restore Procedures

### Routine Restore
1. Log in as Super Admin.
2. Upload a valid `.pgsimsbak` file.
3. Click **Check Backup File** to validate integrity and compatibility.
4. Review Backup Details.
5. Confirm restore with password + typed `RESTORE` + acknowledgement checkbox.
6. System creates an **Automatic Protection Backup** and performs the restore.

### Disaster Recovery
1. Set up a fresh PGSIMS compatible environment.
2. Upload the `.pgsimsdr` file.
3. Follow the extracted `restore_instructions.md`.
4. Restore application data via the routine pathway.

## CLI (management commands)
Create backups:
- `python3 manage.py create_system_backup --routine`
- `python3 manage.py create_system_backup --disaster`

Validate backups:
- `python3 manage.py validate_system_backup /path/to/backup.pgsimsbak`
- `python3 manage.py validate_system_backup /path/to/backup.pgsimsdr`

Dry-run restore validation (non-destructive):
- `python3 manage.py restore_system_backup /path/to/backup.pgsimsbak --dry-run`

## Google Drive Connector (cloud copy)
If Google Drive is connected, a Super Admin can upload an **encrypted** copy of a backup (plus manifest + checksum) to Drive and later download it back for restore staging.

Operator documentation:
- `docs/GOOGLE_DRIVE_BACKUP_CONNECTOR.md`

## Real Data Safety Workflow

Follow these steps when handling real production data:

### Before First Real Import
1. Create a Routine Application Data Backup.
2. Download and validate the backup.
3. Perform a dry-run import.
4. Execute the real import.
5. Create a post-import Routine Backup.
6. Create a Disaster Recovery Backup.

### Before Bulk Changes
1. Create a Routine Backup.
2. Perform changes.
3. Verify integrity.
4. Create a post-change backup.

### Before Restore
1. Inform all administrators.
2. Enter Maintenance Mode (if available).
3. Upload and validate the target backup.
4. System automatically creates a safety backup.
5. Execute restore.
6. Run post-restore health checks.
