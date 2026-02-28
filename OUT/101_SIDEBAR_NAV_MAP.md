# OUT/101 — Sidebar Nav Map

## Registry: `frontend/lib/navRegistry.ts`

### Admin Console (roles: admin)
| Label | Route |
|-------|-------|
| Overview | /dashboard/admin |
| Users | /dashboard/admin/users |
| Analytics | /dashboard/admin/analytics |
| Audit Logs | /dashboard/admin/audit-logs |
| Reports | /dashboard/admin/reports |

### UTRMC (roles: admin, utrmc_admin, utrmc_user)
| Label | Route | Restricted Roles |
|-------|-------|-----------------|
| Overview | /dashboard/utrmc | all |
| Hospitals | /dashboard/utrmc/hospitals | admin, utrmc_admin |
| Departments | /dashboard/utrmc/departments | admin, utrmc_admin |
| H-D Matrix | /dashboard/utrmc/matrix | admin, utrmc_admin |
| Users | /dashboard/utrmc/users | admin, utrmc_admin |
| Supervision Links | /dashboard/utrmc/linking/supervision | admin, utrmc_admin |
| HOD Assignments | /dashboard/utrmc/linking/hod | admin, utrmc_admin |
| Cases | /dashboard/utrmc/cases | all |
| Reports | /dashboard/utrmc/reports | all |

### Data Admin (roles: admin, utrmc_admin)
| Label | Route |
|-------|-------|
| Import Hospitals | /dashboard/utrmc/data-admin/hospitals |
| Import Departments | /dashboard/utrmc/data-admin/departments |
| Import Matrix | /dashboard/utrmc/data-admin/matrix |
| Import Supervisors | /dashboard/utrmc/data-admin/supervisors |
| Import Residents | /dashboard/utrmc/data-admin/residents |
| Import Links | /dashboard/utrmc/data-admin/links |
| Export Data | /dashboard/utrmc/data-admin/export |
| Templates | /dashboard/utrmc/data-admin/templates |

### Supervisor (roles: supervisor, faculty)
| Label | Route |
|-------|-------|
| Overview | /dashboard/supervisor |
| Logbooks | /dashboard/supervisor/logbooks |
| Cases | /dashboard/supervisor/cases |
| My PGs | /dashboard/supervisor/pgs |

### My Training (roles: pg, resident)
| Label | Route |
|-------|-------|
| Overview | /dashboard/pg |
| Logbook | /dashboard/pg/logbook |
| Cases | /dashboard/pg/cases |
| Rotations | /dashboard/pg/rotations |
| Results | /dashboard/pg/results |
| Certificates | /dashboard/pg/certificates |
| Notifications | /dashboard/pg/notifications |
