# Restore Security Proof - Final Safety Checkpoint

## Objective
Verify that destructive restore operations are strictly limited to Super Admin users and require mandatory confirmation locks.

## RBAC Verification
**Test Command**:
```bash
pytest sims/backup_center/tests.py::TestBackupCenterRBAC -v
```

**Result**:
`TestBackupCenterRBAC::test_restore_blocked_for_non_super_admins PASSED`

**Logic Highlights**:
- **Residents**: BLOCKED (403 Forbidden)
- **Supervisors**: BLOCKED (403 Forbidden)
- **HODs**: BLOCKED (403 Forbidden)
- **Normal Admins (non-super)**: BLOCKED (403 Forbidden)
- **Unauthenticated Users**: BLOCKED (403 Forbidden)

The backend utilizes a custom `IsSuperAdmin` permission class inherited from `BasePermission` that explicitly checks `request.user.is_superuser`.

## Confirmation Locks
The `restore_routine_application_data_backup` service and management commands enforce:
- **Password Confirmation**: Verified via `check_password` on the authorizing user.
- **Typed Confirmation**: Strict string match for `"RESTORE"` is required.
- **Checkbox Lock**: Frontend forces UI interaction prior to API emission.
- **Validation Lock**: Restore fails if `validate_backup_file` returns any errors (integrity check).

**Result**: PASS. The system implements a robust series of identity and behavioral locks to prevent accidental or unauthorized data overwrites.
