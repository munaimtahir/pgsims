# Deployment Checklist - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

Verify the following checklist steps before launching:

## Phase 1: Environment & Config Hardening
- [ ] Ensure `.env` is populated with a custom production `SECRET_KEY`.
- [ ] Ensure `DEBUG=False` is set.
- [ ] Configure `ALLOWED_HOSTS` to match actual domains.
- [ ] Configure `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` to prevent cross-site request forgery.
- [ ] Configure `DATABASE_URL` for PostgreSQL.

## Phase 2: Database Setup & Backup Verify
- [ ] Run initial migrations (`python manage.py migrate`).
- [ ] Run `python manage.py repair_identity_profiles` to assert initial profile state.
- [ ] Verify that backup scripts are executable:
  - `scripts/backup_pgms_db.sh`
  - `scripts/verify_pgms_backup.sh`
  - `scripts/restore_pgms_db.sh`
- [ ] Take a pre-launch backup.

## Phase 3: Frontend Compilation
- [ ] Verify that `npm run build` succeeds inside `frontend`.
- [ ] Verify that typecheck and lint checks pass without warnings.
- [ ] Confirm proxy configuration redirects `/api` requests to backend port `8014`.

## Phase 4: Verification Checks
- [ ] Run `scripts/check_pgms_health.sh` to check system health.
- [ ] Run `scripts/check_all_pgms_gates.sh` to verify all coding gates pass.
