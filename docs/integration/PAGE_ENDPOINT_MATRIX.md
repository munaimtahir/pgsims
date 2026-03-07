# Page → Endpoint Matrix

**Generated:** 2026-03-07  
**Source:** Frontend pages in `frontend/app/` + API client modules in `frontend/lib/api/`

---

## Authentication Pages

| Page | Route | Action | Frontend Function | API Endpoint | Roles |
|------|-------|--------|-------------------|-------------|-------|
| Login | `/login` | Submit login | `login(credentials)` | POST `/api/auth/login/` | All |
| Register | `/register` | Submit registration | `register(data)` | POST `/api/auth/register/` | All |
| Forgot Password | `/forgot-password` | Request reset | `requestPasswordReset(email)` | POST `/api/auth/password-reset/` | All |
| Reset Password | `/reset-password` | Confirm reset | `confirmPasswordReset(data)` | POST `/api/auth/password-reset/confirm/` | All |
| Any Page | Global | Load current user | `getCurrentUser()` | GET `/api/auth/profile/` | Authenticated |
| Any Page | Global | Token refresh | `refreshToken()` | POST `/api/auth/refresh/` | Authenticated |

---

## PG / Resident Dashboard Pages

| Page | Route | Action | Frontend Function | API Endpoint | Roles |
|------|-------|--------|-------------------|-------------|-------|
| PG Dashboard | `/dashboard/pg` | Load summary | `trainingApi.getResidentSummary()` | GET `/api/residents/me/summary/` | pg |
| PG Dashboard | `/dashboard/pg` | System settings | `trainingApi.getSystemSettings()` | GET `/api/system/settings/` | pg |
| Resident Dashboard | `/dashboard/resident` | Load summary | `trainingApi.getResidentSummary()` | GET `/api/residents/me/summary/` | pg/resident |
| Schedule | `/dashboard/resident/schedule` | Load rotations | (via resident summary) | GET `/api/my/rotations/` | pg |
| Research | `/dashboard/resident/research` | Load project | `trainingApi.getMyResearch()` | GET `/api/my/research/` | pg |
| Research | `/dashboard/resident/research` | Create project | `trainingApi.createMyResearch(data)` | POST `/api/my/research/` | pg |
| Research | `/dashboard/resident/research` | Update project | `trainingApi.updateMyResearch(data)` | PATCH `/api/my/research/` | pg |
| Research | `/dashboard/resident/research` | Upload synopsis | (direct apiClient.patch multipart) | PATCH `/api/my/research/` | pg |
| Research | `/dashboard/resident/research` | Load supervisors | (direct apiClient.get) | GET `/api/users/?role=supervisor` | pg |
| Research | `/dashboard/resident/research` | Trigger action | `trainingApi.researchAction(action)` | POST `/api/my/research/action/{action}/` | pg |

---

## Supervisor Dashboard Pages

| Page | Route | Action | Frontend Function | API Endpoint | Roles |
|------|-------|--------|-------------------|-------------|-------|
| Supervisor Dashboard | `/dashboard/supervisor` | Load summary | `trainingApi.getSupervisorSummary()` | GET `/api/supervisors/me/summary/` | supervisor |
| Supervisor Dashboard | `/dashboard/supervisor` | Load resident list | `getAssignedPGs()` | GET `/api/users/assigned-pgs/` | supervisor |
| Resident Progress | `/dashboard/supervisor/residents/{id}/progress` | Load progress | `trainingApi.getResidentProgress(id)` | GET `/api/supervisors/residents/{id}/progress/` | supervisor |
| Research Approvals | `/dashboard/supervisor` | Load pending | `trainingApi.getSupervisorResearchApprovals()` | GET `/api/supervisor/research-approvals/` | supervisor |
| Research Approvals | `/dashboard/supervisor` | Approve synopsis | `trainingApi.approveResearch(data)` | POST `/api/my/research/action/supervisor-approve/` | supervisor |
| Research Approvals | `/dashboard/supervisor` | Return synopsis | `trainingApi.returnResearch(data)` | POST `/api/my/research/action/supervisor-return/` | supervisor |

---

## UTRMC Dashboard Pages

| Page | Route | Action | Frontend Function | API Endpoint | Roles |
|------|-------|--------|-------------------|-------------|-------|
| UTRMC Dashboard | `/dashboard/utrmc` | Load eligibility | `trainingApi.getMilestoneEligibility()` | GET `/api/utrmc/eligibility/` | utrmc_admin, utrmc_user |
| Hospitals | `/dashboard/utrmc/hospitals` | List hospitals | `getHospitals()` / `userbaseApi.hospitals.list()` | GET `/api/hospitals/` | admin, utrmc_admin, utrmc_user |
| Hospitals | `/dashboard/utrmc/hospitals` | Create hospital | `createHospital(data)` / `userbaseApi.hospitals.create()` | POST `/api/hospitals/` | admin |
| Hospitals | `/dashboard/utrmc/hospitals` | Update hospital | `updateHospital(id, data)` | PATCH `/api/hospitals/{id}/` | admin |
| Hospitals | `/dashboard/utrmc/hospitals` | Delete hospital | `deleteHospital(id)` | DELETE `/api/hospitals/{id}/` | admin |
| Hospitals | `/dashboard/utrmc/hospitals` | View depts | `userbaseApi.hospitals.getDepartments(id)` | GET `/api/hospitals/{id}/departments/` | all |
| Departments | `/dashboard/utrmc/departments` | List departments | `getDepartments()` / `userbaseApi.departments.list()` | GET `/api/departments/` | all |
| Departments | `/dashboard/utrmc/departments` | Create dept | `createDepartment(data)` | POST `/api/departments/` | admin |
| Departments | `/dashboard/utrmc/departments` | Update dept | `updateDepartment(id, data)` | PATCH `/api/departments/{id}/` | admin |
| Departments | `/dashboard/utrmc/departments` | Delete dept | `deleteDepartment(id)` | DELETE `/api/departments/{id}/` | admin |
| Departments | `/dashboard/utrmc/departments` | View roster | `userbaseApi.departments.getRoster(id)` | GET `/api/departments/{id}/roster/` | admin, utrmc_admin, utrmc_user, supervisor |
| Matrix | `/dashboard/utrmc/matrix` | List matrix | `getHospitalDepartments()` / `userbaseApi.hospitalDepartments.list()` | GET `/api/hospital-departments/` | all |
| Matrix | `/dashboard/utrmc/matrix` | Add entry | `createHospitalDepartment(data)` | POST `/api/hospital-departments/` | admin, utrmc_admin |
| Matrix | `/dashboard/utrmc/matrix` | Remove entry | `deleteHospitalDepartment(id)` | DELETE `/api/hospital-departments/{id}/` | admin, utrmc_admin |
| Users | `/dashboard/utrmc/users` | List users | `userbaseApi.users.list(params)` | GET `/api/users/` | admin, utrmc_admin, utrmc_user |
| Users | `/dashboard/utrmc/users` | Create user | `userbaseApi.users.create(payload)` | POST `/api/users/` | admin, utrmc_admin |
| Users | `/dashboard/utrmc/users` | Edit user | `userbaseApi.users.update(id, payload)` | PATCH `/api/users/{id}/` | admin, utrmc_admin |
| Users | `/dashboard/utrmc/users` | Assign to dept | `userbaseApi.memberships.create(payload)` | POST `/api/department-memberships/` | admin, utrmc_admin |
| Users | `/dashboard/utrmc/users` | Assign to hospital | `userbaseApi.hospitalAssignments.create(payload)` | POST `/api/hospital-assignments/` | admin, utrmc_admin |
| Supervision | `/dashboard/utrmc/supervision` | List links | `userbaseApi.supervisionLinks.list()` | GET `/api/supervision-links/` | admin, utrmc_admin |
| Supervision | `/dashboard/utrmc/supervision` | Create link | `userbaseApi.supervisionLinks.create(payload)` | POST `/api/supervision-links/` | admin, utrmc_admin |
| HOD | `/dashboard/utrmc/hod` | List assignments | `userbaseApi.hodAssignments.list()` | GET `/api/hod-assignments/` | admin, utrmc_admin |
| HOD | `/dashboard/utrmc/hod` | Create assignment | `userbaseApi.hodAssignments.create(payload)` | POST `/api/hod-assignments/` | admin, utrmc_admin |
| Programs | `/dashboard/utrmc/programs` | List programs | `trainingApi.listPrograms()` | GET `/api/programs/` | all |
| Programs | `/dashboard/utrmc/programs` | Create program | `trainingApi.createProgram(data)` | POST `/api/programs/` | admin, utrmc_admin |
| Programs | `/dashboard/utrmc/programs` | Edit program | `trainingApi.updateProgram(id, data)` | PUT `/api/programs/{id}/` | admin, utrmc_admin |
| Programs | `/dashboard/utrmc/programs` | Edit policy | `trainingApi.updateProgramPolicy(id, data)` | PUT `/api/programs/{id}/policy/` | admin, utrmc_admin |
| Programs | `/dashboard/utrmc/programs` | Add milestone | `trainingApi.createProgramMilestone(id, data)` | POST `/api/programs/{id}/milestones/` | admin, utrmc_admin |
| Eligibility | `/dashboard/utrmc/eligibility` | View matrix | `trainingApi.getMilestoneEligibility()` | GET `/api/utrmc/eligibility/` | admin, utrmc_admin, utrmc_user |
| Rotation Approvals | `/dashboard/utrmc` | Inbox | (rotation approval inbox) | GET `/api/utrmc/approvals/rotations/` | admin, utrmc_admin, utrmc_user |
| Leave Approvals | `/dashboard/utrmc` | Inbox | (leave approval inbox) | GET `/api/utrmc/approvals/leaves/` | admin, utrmc_admin, utrmc_user |

---

## Global Components (All Pages)

| Component | Action | Frontend Function | API Endpoint | Roles |
|-----------|--------|-------------------|-------------|-------|
| Notification Bell | Load unread count | `notificationApi.getUnreadCount()` | GET `/api/notifications/unread-count/` | All |
| Notification Drawer | List notifications | `notificationApi.list(params)` | GET `/api/notifications/` | All |
| Notification Drawer | Mark as read | `notificationApi.markRead(ids)` | POST `/api/notifications/mark-read/` | All |
| Profile Menu | Update profile | `updateProfile(data)` | PATCH `/api/auth/profile/update/` | All |
| Profile Menu | Change password | `changePassword(data)` | POST `/api/auth/change-password/` | All |

---

## Admin-Only Pages

| Page | Route | Action | Frontend Function | API Endpoint | Roles |
|------|-------|--------|-------------------|-------------|-------|
| Audit Logs | `/dashboard/admin/audit` | List activities | `auditApi.listActivities(params)` | GET `/api/audit/activity/` | admin |
| Audit Logs | `/dashboard/admin/audit` | List reports | `auditApi.listReports(params)` | GET `/api/audit/reports/` | admin |
| Audit Logs | `/dashboard/admin/audit` | Create report | `auditApi.createReport(data)` | POST `/api/audit/reports/` | admin |
| Bulk Import | `/dashboard/utrmc/bulk` | Import trainees | `bulkApi.importTrainees(formData)` | POST `/api/bulk/import-trainees/` | admin, utrmc_admin |
| Bulk Import | `/dashboard/utrmc/bulk` | Import supervisors | `bulkApi.importSupervisors(formData)` | POST `/api/bulk/import-supervisors/` | admin, utrmc_admin |
| Bulk Import | `/dashboard/utrmc/bulk` | Import residents | `bulkApi.importResidents(formData)` | POST `/api/bulk/import-residents/` | admin, utrmc_admin |
| Bulk Import | `/dashboard/utrmc/bulk` | Bulk assign | `bulkApi.bulkAssign(data)` | POST `/api/bulk/assignment/` | admin, utrmc_admin |
| Bulk Export | `/dashboard/utrmc/bulk` | Export data | `bulkApi.export(resource, format)` | GET `/api/bulk/exports/{resource}/` | admin, utrmc_admin, utrmc_user |
