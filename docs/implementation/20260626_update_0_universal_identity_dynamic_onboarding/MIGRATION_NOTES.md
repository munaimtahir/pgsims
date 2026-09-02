# Migration Notes — Update 0

## Migration Process
1. Model changes and schema definitions for `AdminProfile`, `ResidentProfile`, `SupervisorProfile`, and `SupportStaffProfile` are fully defined.
2. A database schema check was performed, verifying that the current sqlite database is fully up to date and has all migrations applied:
   - Migration `users.0007_adminprofile_historicaladminprofile_and_more` is active and applied.
3. No pending model changes exist (`makemigrations --check --dry-run` reports no changes detected).

## Profile Cleanup & Integrity Repair
- Database integrity has been checked and verified using `python manage.py repair_identity_profiles`.
- Mismatching profiles and duplicate profiles are cleaned up by the command, and completion states recalculated.
