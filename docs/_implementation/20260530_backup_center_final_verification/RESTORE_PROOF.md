# RESTORE_PROOF — Fresh-Compatible Restore (Regular System Backup)

Date (UTC): 2026-05-30

## Question answered
Can a **Regular System Backup** (`.pgsimsbak`) restore a *fresh compatible* PGSIMS installation so existing users can continue working with the **same password**?

## Verdict
**YES (proven in isolated test harness).**

## Proof method (safe / isolated)
This proof is implemented as an automated backend test that:
1. Creates dummy/safe data in a Django test database (isolated).
2. Creates a routine `.pgsimsbak` backup including a media file.
3. Mutates the database and deletes the media file to simulate “fresh/changed” state.
4. Performs a destructive restore **inside the isolated test DB** (not staging/real).
5. Verifies identity + password + media preservation.

## Evidence (test)
Test location:
- `backend/sims/backup_center/tests.py` (`test_restore_proof_sqlite_preserves_ids_passwords_and_media`)

Run command:
- `cd backend && pytest sims/backup_center/tests.py -k restore_proof -q`

Assertions performed by the test:
1. **Same user ID** preserved (PK stable).
2. **Same password hash** preserved exactly (no re-hashing).
3. **Same password works** post-restore (`check_password("password123") == True`).
4. **Same Department PK** preserved.
5. **Same HospitalDepartment PK** preserved.
6. **Uploaded media file** restored and matches original `sha256`.

## Critical bug fixed during proof
Safety backups created inside restore could overwrite the target backup file if both were created in the same second.

Fix applied:
- Backup filenames now include microseconds (`%Y-%m-%d_%H%M%S_%f`) to prevent collisions.

