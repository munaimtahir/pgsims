# API Verification - Brick 11: Dashboards, Reports, and Exports

All endpoints have been verified using Django integration tests and system validation checks.

## Endpoints Verified
1. **Global Dashboard**: `GET /api/academics/monitoring/admin-dashboard/` -> Returns total counts of residents, missing records, evaluations and breakdowns by department.
2. **Supervisor Workload**: `GET /api/academics/monitoring/supervisor-dashboard/` -> Returns scoping lists of active tasks and assigned postgraduate progress.
3. **Resident Progress View**: `GET /api/academics/monitoring/my-progress/` -> Scopes training records and supervisors to self.
4. **Summary breakdowns**: `GET /api/academics/monitoring/departments/`, `programs/`, `sessions/` -> Returns lists of breakdown details.
5. **Reports**: `GET /api/academics/reports/evaluations/`, `logbook/`, `data-quality/` -> Query sets with filters (status, date ranges).
6. **CSV Export Actions**: `/api/academics/reports/.../export.csv` -> Returns CSV attachment header.
