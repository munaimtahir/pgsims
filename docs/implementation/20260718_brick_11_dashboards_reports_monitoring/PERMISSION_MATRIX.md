# Permission Matrix - Brick 11: Dashboards, Reports, and Exports

The backend enforces user role restrictions on all dashboard, reports, and export endpoints.

| Endpoint | ADMIN | SUPERVISOR | RESIDENT | SUPPORT_STAFF |
| :--- | :---: | :---: | :---: | :---: |
| `/monitoring/admin-dashboard/` | ✅ | ❌ | ❌ | ❌ |
| `/monitoring/supervisor-dashboard/` | ✅ | ✅ (assigned) | ❌ | ❌ |
| `/monitoring/my-progress/` | ✅ | ❌ | ✅ | ❌ |
| `/monitoring/departments/` | ✅ | ❌ | ❌ | ❌ |
| `/reports/resident-progress/` | ✅ | ✅ (assigned) | ✅ (self) | ❌ |
| `/reports/supervisor-workload/` | ✅ | ✅ (self) | ❌ | ❌ |
| `/reports/evaluations/` | ✅ | ✅ (assigned) | ✅ (self) | ❌ |
| `/reports/logbook/` | ✅ | ✅ (assigned) | ✅ (self) | ❌ |
| `/reports/data-quality/` | ✅ | ❌ | ❌ | ❌ |
| `/*/export.csv` | ✅ | ✅ (assigned) | ✅ (self) | ❌ |
