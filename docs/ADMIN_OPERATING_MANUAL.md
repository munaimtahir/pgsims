# PGMS Admin Operating Manual

This manual outlines standard procedures for PGMS administrative operations.

---

## 1. Authentication & Setup
### Sign In
1. Navigate to `/login`.
2. Input credentials (username and password).
3. If logging in for the first time, you will be redirected to `/change-password` to update your default temporary password (`pgfmu123`).

### Complete Profile
Ensure your administrative metadata (full name, phone number, email, and department reference) is updated by navigating to `/complete-profile` if prompted.

---

## 2. User & Directory Management
### Register a New User
1. Go to `/users` or `/users/new`.
2. Select the role (only `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF` are permitted).
3. Select training program, department, and academic session as appropriate.
4. On submit, the system atomically inserts a User and a linked Profile record.
5. Provide the user with their auto-generated username and the default password `pgfmu123`.

### Manage Masters and Sites
1. Navigate to `/masters`.
2. Create or edit Hospitals and Departments.
3. Establish link associations using the Hospital-Department matrix.

---

## 3. Supervision & Spines
### Create Supervision Assignments
1. Navigate to `/supervision/assignments/new`.
2. Select the resident and target supervisor.
3. Mark assignment type as `PRIMARY` or `CO_SUPERVISOR`.
4. Submit. Note that the system strictly enforces a limit of exactly one active `PRIMARY` supervisor assignment per resident.

### Establish Training Spine
1. Go to `/academics/training-records`.
2. Click **Create Training Record**.
3. Select Resident, Program, Session, and starting year.
4. Set start and expected end dates. Submit to initialize the academic timeline.

---

## 4. Operational Monitoring & Reports
### Check Operational telemetry
1. Open `/academics/monitoring` to review active coverage counts, review queue workloads, and pending logs.
2. Review specific program or session metrics using the breakdown tabs.

### Export Reports
- **Resident progress**: Go to `/academics/reports/resident-progress` to view or download progress logs.
- **Supervisor workload**: Open `/academics/reports/supervisor-workload` to audit teaching workloads.
- **Evaluations/Logbooks**: Go to `/academics/reports/evaluations` or `/academics/reports/logbook` to filter and export CSV lists.

---

## 5. Maintenance & CLI Admin
### Repair Profiles
If user profiles drift or links fail, run:
```bash
python manage.py repair_identity_profiles
```

### Database Backups
Create a backup:
```bash
bash scripts/backup_pgms_db.sh
```
Verify the dump:
```bash
bash scripts/verify_pgms_backup.sh <path_to_backup_file>
```
Restore if necessary (requires explicit confirmation):
```bash
bash scripts/restore_pgms_db.sh <path_to_backup_file> --confirm
```
