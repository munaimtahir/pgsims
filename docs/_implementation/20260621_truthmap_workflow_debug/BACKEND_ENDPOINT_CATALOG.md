# Backend Endpoint Catalog

Scope: workflow-related endpoints in the audited URL files and the supporting admin surfaces that affect the truth map.

| Endpoint | Method | View / ViewSet | Serializer / Shape | Role / RBAC | Expected payload | Frontend exposure |
| --- | --- | --- | --- | --- | --- | --- |
| `/api/users/` | GET, POST | `UserViewSet` | `UserManagementSerializer` | Admin / `utrmc_admin` for management, other roles limited by queryset | User create/update fields including `role`, `supervisor`, `home_department`, `home_hospital`, `year`, `password` | Yes, `frontend/app/dashboard/utrmc/users/page.tsx` |
| `/api/users/{id}/` | GET, PUT, PATCH, DELETE | `UserViewSet` | `UserManagementSerializer` | Same as above | Full user update payload | Yes, row actions on Users page; DELETE archives instead of hard delete |
| `/api/users/{id}/reset-password/` | POST | `UserViewSet.reset_password` | `{ password }` | Admin / `utrmc_admin` | `{ password: "pgfmu123" }` | Yes, Users page row action |
| `/api/users/{id}/deactivate/` | POST | `UserViewSet.deactivate` | no body required | Admin / `utrmc_admin` | none | Yes, Users page row action |
| `/api/users/{id}/archive/` | POST | `UserViewSet.archive` | no body required | Admin / `utrmc_admin` | none | Yes, Users page row action and DELETE alias |
| `/api/users/assigned-pgs/` | GET | `SupervisorAssignedPGsView` | read-only assignment list | Supervisor / faculty / HOD context | none | Indirectly used by supervisor workflows |
| `/api/departments/` | GET, POST, PATCH, DELETE | `DepartmentViewSet` | canonical department serializer | Admin / `utrmc_admin` | Department model payload | Yes, Users / supervision / HOD lookups |
| `/api/hospitals/` | GET, POST, PATCH, DELETE | `HospitalViewSet` | hospital serializer | Admin / `utrmc_admin` | Hospital payload | Yes, organization lookup UI |
| `/api/hospital-departments/` | GET, POST, PATCH, DELETE | `HospitalDepartmentViewSet` | hospital-department serializer | Admin / `utrmc_admin` | `hospital_id`, `department_id`, active | Yes, matrix pages and dashboard stats |
| `/api/residents/` | GET, POST, PATCH, DELETE | `ResidentProfileViewSet` | resident profile serializer | Admin / `utrmc_admin` | resident profile payload | Yes, resident-related admin screens |
| `/api/staff/` | GET, POST, PATCH, DELETE | `StaffProfileViewSet` | staff profile serializer | Admin / `utrmc_admin` | staff profile payload | Yes, supervisor/faculty management |
| `/api/department-memberships/` | GET, POST, PATCH, DELETE | `DepartmentMembershipViewSet` | membership serializer | Admin / `utrmc_admin` | membership payload | Yes, organizational admin screens |
| `/api/hospital-assignments/` | GET, POST, PATCH, DELETE | `HospitalAssignmentViewSet` | assignment serializer | Admin / `utrmc_admin` | `user_id`, `hospital_department_id`, `assignment_type`, dates, active | Yes, matrix-related pages |
| `/api/supervision-links/` | GET, POST, PATCH, DELETE | `SupervisionLinkViewSet` | `SupervisorResidentLinkSerializer` | UTRMC/admin oversight roles for read, manager roles for write | `supervisor_user_id`, `resident_user_id`, `department_id`, `start_date`, `active` | Yes, `frontend/app/dashboard/utrmc/supervision/page.tsx` |
| `/api/hod-assignments/` | GET, POST, PATCH, DELETE | `HODAssignmentViewSet` | `HODAssignmentSerializer` | UTRMC/admin oversight roles for read, manager roles for write | `department_id`, `hod_user_id`, `start_date`, `active` | Yes, `frontend/app/dashboard/utrmc/hod/page.tsx` |
| `/api/admin/data-quality/summary` | GET | `DataQualitySummaryView` | JSON summary | Admin / `utrmc_admin` | none | Yes, monitoring dashboard data |
| `/api/admin/data-quality/users` | GET | `DataQualityUsersView` | JSON list | Admin / `utrmc_admin` | `filter` query param | Yes, data-quality monitoring surfaces |
| `/api/admin/data-quality/recompute` | POST | `DataQualityRecomputeView` | JSON summary | Admin / `utrmc_admin` | none | Yes, admin monitoring action |
| `/api/admin/data-quality/audit` | GET | `DataCorrectionAuditView` | audit list | Admin / `utrmc_admin` | none | Yes, audit/monitoring surfaces |
| `/api/auth/login/` | POST | token obtain view | JWT login payload | public auth | username/password | Yes, login page |
| `/api/auth/refresh/` | POST | refresh token | JWT refresh payload | authenticated | refresh token | Yes, auth client |
| `/api/auth/logout/` | POST/GET depending caller | logout view | session/token logout | authenticated | none | Yes, auth client |
| `/api/auth/password-reset/` | POST | password reset request | email payload | public auth | email | Yes, reset-password page |
| `/api/auth/password-reset/confirm/` | POST | password reset confirm | token + new password | public auth | token, uid, password | Yes, reset-password page |
| `/api/auth/change-password/` | POST | change-password | current/new password payload | authenticated | old/new password | Yes, resident completion and profile pages |
| `/api/onboarding/residents/*` | GET/POST depending action | onboarding views | upload/map/preview/import/login sheet | admin / `utrmc_admin` | workbook upload, mapping, import actions | Yes, onboarding wizard pages |
| `/api/resident/*` | GET/POST depending action | resident self-service views | profile completion and status | resident / PG | profile completion payload | Yes, resident complete-profile flow |
| `/api/backup_center/*` | GET/POST depending action | backup views | backup/restore payloads | admin / `utrmc_admin` on some actions | backup and restore forms | Yes, Backup Center page |
| `/api/backup_center/google-drive/*` | GET/POST depending action | Google Drive connector views | connector payloads | admin only | OAuth/connectivity payloads | Hidden from the active onboarding workflow |
| `/api/rotations/*` | mostly redirects / dummy pages | `rotations.urls` | legacy route shell | depends on route | none | Hidden/legacy, not in current nav |

## Notes

- `SupervisionLinkViewSet` and `HODAssignmentViewSet` are the main write surfaces behind the live UI fixes.
- `ResidentTrainingRecordViewSet` is the backend for the new resident programme assignment page.
- The AdminOps callback route exists but is intentionally paused from the active pilot workflow.
