# Terminology Lock (UI Dictionary)

These are user-facing terms. Do not change once pilot begins.

- **Submitted**: entry sent to supervisor for review (backend status may be `pending`)
- **Returned**: supervisor requests edits
- **Rejected**: supervisor declines entry (must include feedback/reason)
- **Approved**: supervisor verifies entry
- **Feedback**: supervisor message shown to PG
- **Home Hospital**: trainee’s primary hospital until graduation
- **Home Department**: trainee’s primary department until graduation
- **Rotation**: time-bounded posting in a (Hospital, Department) pair
- **Resident**: postgraduate trainee role (legacy `pg` remains accepted)
- **Faculty**: senior academic role that may supervise residents and hold HOD assignment
- **HOD**: active head-of-department assignment tracked with effective dates
- **Bulk Setup**: prerequisite-aware import/export workspace on the UTRMC overview page for canonical hospitals, departments, matrix, users, and assignments
- **Dry Run**: validates uploaded rows without writing to the database
- **Template CSV**: the canonical downloadable file showing the exact expected columns for a bulk import type
- **Backup & Restore Center**: UTRMC operational page for creating, downloading, checking, and restoring backups
- **Regular System Backup**: routine application data backup (`.pgsimsbak`) including database + uploaded files
- **Full Server Recovery Backup**: disaster recovery bundle (`.pgsimsdr`) including an internal regular backup plus recovery notes (no unencrypted secrets)
- **Check Backup File**: validates a backup archive’s integrity and required contents
- **Automatic Protection Backup**: automatic safety backup created before a destructive restore
- **Backup Record**: internal `BackupJob` record
- **Restore Request**: internal `RestoreJob` record
- **Google Drive Backup**: Backup Center panel for connecting Google Drive and managing encrypted Drive copies of backups
- **Drive Backup Folder**: the Google Drive folder used to store encrypted backup artifacts (default name: `PGSIMS Backups`)
- **Drive Copy**: internal record of an uploaded Google Drive backup artifact set (internal `BackupCloudCopy`)
- **Under Review**: submission completeness review is in progress by supervisor/HOD/UTRMC reviewer
- **Certificate Issued**: a verified synopsis/thesis/rotation-completion certificate exists with issue timestamp
- **Rotation Completion Verification**: post-rotation check where department confirms and UTRMC verifies completion
- **Logbook**: active resident page for logbook draft/submission and threshold state; replaces the previous active navigation label "Academic Progress" as of 2026-04-21
- **Deferred Workflow**: implemented or partially implemented route/API that is intentionally hidden from active navigation and excluded from the release gate

Notes:
- UI displays **Submitted** even if backend enum is `pending`.
- UI reads `feedback` from API (alias of `supervisor_feedback`).
- 2026-04-21 terminology lock update: synopsis, thesis, postings, and rotations phase-1 are deferred workflows, not active release claims.
- 2026-05-30 terminology lock update: Backup Center operator terms added for pilot operations.
- 2026-06-01 terminology lock update: additive Google Drive Backup connector terms added (no renames of existing terms).
