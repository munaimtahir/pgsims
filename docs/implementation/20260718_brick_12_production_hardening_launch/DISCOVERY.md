# Discovery - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

## Current Status
We have successfully implemented:
- Update 0: Identity and Profile synchronization.
- Brick 6: Core Masters and Directory structure.
- Brick 7: Clean Supervision Spine.
- Brick 8: Academic Workflow Foundation.
- Brick 9-10: Rotation Evaluations & Logbooks / Case Procedures workflows.
- Brick 11: Telemetry dashboards, compliance checks, reports, and CSV exports.

## Discovery Findings
1. **Settings / Configuration**: Currently, settings are defined in `backend/sims_project/settings.py` or separate dev/prod settings if present. We need to verify how `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` are loaded.
2. **Backup/Restore**: No automated or hardened backup/restore scripts exist currently in `scripts/`. We need to create:
   - `scripts/backup_pgms_db.sh`
   - `scripts/restore_pgms_db.sh`
   - `scripts/verify_pgms_backup.sh`
3. **Health Check Endpoint**: We need to implement `GET /api/health/` returning basic status checks.
4. **Safety & Policy Documentation**: We must deliver the operational guides (Admin, Resident, Supervisor) and launch data policy documentation.
5. **No regressions**: HOD role/model references and legacy modules must remain completely absent.
