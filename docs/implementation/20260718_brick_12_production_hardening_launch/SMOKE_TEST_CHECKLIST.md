# Smoke Test Checklist - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

Perform the following manual smoke tests on the running pilot server:

## 1. Authentication
- [ ] Admin login succeeds.
- [ ] First-time login forces password change at `/change-password`.
- [ ] Profile completion is requested at `/complete-profile` if fields are missing.

## 2. Directory & Setup
- [ ] Create a department, hospital, and program via `/masters`.
- [ ] Register Resident profile and Supervisor profile via `/users/new`.
- [ ] Create supervision assignment.
- [ ] Initialize training record.

## 3. Academic Workflows
- [ ] Resident submits evaluation form -> status is `SUBMITTED`.
- [ ] Supervisor reviews evaluation -> status updates (e.g. `APPROVED` or `RETURNED`).
- [ ] Resident logs logbook case entry -> status is `SUBMITTED`.
- [ ] Supervisor verifies logbook procedure -> status is `VERIFIED`.

## 4. Dashboards & Exports
- [ ] Open Admin Monitoring dashboard at `/academics/monitoring`.
- [ ] Open Supervisor Workload dashboard at `/academics/supervisor-workload`.
- [ ] Open Resident Progress dashboard at `/academics/my-progress`.
- [ ] Click **Export CSV** on report views and verify CSV attachment file downloads.
- [ ] Verify database backup command execution.
