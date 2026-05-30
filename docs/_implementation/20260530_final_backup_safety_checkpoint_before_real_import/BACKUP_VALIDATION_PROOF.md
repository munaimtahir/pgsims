# Backup Validation Proof - Final Safety Checkpoint

## Objective
Verify that the `validate_system_backup` management command correctly parses and validates a generated `.pgsimsbak` archive, and rejects invalid files.

## Valid Archive Execution
**Command**:
```bash
python manage.py validate_system_backup /home/munaim/srv/apps/pgsims/backend/backups/PGSIMS_DATA_BACKUP_2026-05-30_230210_597213.pgsimsbak
```

**Output Highlight**:
```
Validating: /home/munaim/srv/apps/pgsims/backend/backups/PGSIMS_DATA_BACKUP_2026-05-30_230210_597213.pgsimsbak
Kind: routine_application_data
STATUS: VALID
--- Manifest Summary ---
{
  "app_name": "PGSIMS",
  "backup_format_version": "1.2",
  "backup_kind": "routine_application_data",
  "created_at": "2026-05-30T23:02:10.810890+00:00",
  "created_by": "system",
  "app_version": "1.0.0",
  "branch": "main",
  ...
```

**Key Extractions**:
- Validation mechanism confirms file integrity and the presence of `manifest.json`, `checksum.sha256`, and structural files.
- Identifies backup as `routine_application_data`.
- Extracts `table_counts` successfully.
- Extracts `media_summary` successfully.

## Invalid Archive Execution
**Command**:
```bash
echo "not a zip file" > /tmp/invalid.pgsimsbak
python manage.py validate_system_backup /tmp/invalid.pgsimsbak
```

**Output**:
```
Validating: /tmp/invalid.pgsimsbak
Kind: unknown
STATUS: INVALID
ERROR: File is not a valid ZIP archive.
```

**Result**: PASS. The validation system correctly authorizes structurally sound archives while aggressively rejecting broken/corrupted payloads.
