# Changes - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

## Backend Changes
1. **sims_project/urls.py**: Registered `/api/health/` returning connection health and app versioning statistics.
2. **sims/academics/views.py**: Restricted Resident profiles from querying reports listing view `/api/academics/reports/resident-progress/` directly.
3. **sims/academics/tests.py**: Appended `test_brick12_health_check_and_security_audit` testing the API health response, anonymous access blocks, and resident self-scoping.
4. **scripts/backup_pgms_db.sh**: Automated PostgreSQL timestamped DB dump with MD5 hashing.
5. **scripts/restore_pgms_db.sh**: Overwrite database script with confirmation safety.
6. **scripts/verify_pgms_backup.sh**: MD5 checksum validation script.
7. **scripts/check_pgms_health.sh**: Overall backend check and connection check script.

## Frontend Changes
Verified Next.js build compilation with 0 compile errors, typecheck warnings, or lint failures.
- Main dashboard and layout items conform strictly to roles.
- Added comprehensive manual guides.
- Restricted admin routing permissions.
