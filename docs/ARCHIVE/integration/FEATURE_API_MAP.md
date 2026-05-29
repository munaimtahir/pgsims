# Feature API Map

**Generated:** 2026-03-07  
**Source:** Full scan of `frontend/lib/api/*.ts` and `frontend/app/**/*.tsx`

This document maps every frontend feature to the API functions and backend endpoints it uses.

---

## Feature: Authentication

**Pages:** `/login`, `/register`, `/forgot-password`  
**Module:** `frontend/lib/api/auth.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `login(credentials)` | POST | `/api/auth/login/` | Obtain JWT tokens |
| `register(data)` | POST | `/api/auth/register/` | Create new account |
| `logout()` | POST | `/api/auth/logout/` | Invalidate refresh token |
| `getCurrentUser()` | GET | `/api/auth/profile/` | Get current user data |
| `refreshToken(refreshToken)` | POST | `/api/auth/refresh/` | Refresh access token |
| `updateProfile(data)` | PATCH | `/api/auth/profile/update/` | Update profile fields |
| `requestPasswordReset(email)` | POST | `/api/auth/password-reset/` | Send reset email |
| `confirmPasswordReset(data)` | POST | `/api/auth/password-reset/confirm/` | Set new password |
| `changePassword(data)` | POST | `/api/auth/change-password/` | Change password (authenticated) |

---

## Feature: Organisation Graph — Hospitals

**Pages:** `/dashboard/utrmc/hospitals`  
**Modules:** `frontend/lib/api/hospitals.ts`, `frontend/lib/api/userbase.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `getHospitals()` | GET | `/api/hospitals/` | List all hospitals |
| `createHospital(data)` | POST | `/api/hospitals/` | Create a hospital |
| `updateHospital(id, data)` | PATCH | `/api/hospitals/{id}/` | Update hospital |
| `deleteHospital(id)` | DELETE | `/api/hospitals/{id}/` | Remove hospital |
| `userbaseApi.hospitals.list()` | GET | `/api/hospitals/` | Rich hospital list with metadata |
| `userbaseApi.hospitals.create(payload)` | POST | `/api/hospitals/` | Create hospital (typed) |
| `userbaseApi.hospitals.update(id, payload)` | PATCH | `/api/hospitals/{id}/` | Update hospital (typed) |
| `userbaseApi.hospitals.getDepartments(id)` | GET | `/api/hospitals/{id}/departments/` | Hospital's available departments |

---

## Feature: Organisation Graph — Departments

**Pages:** `/dashboard/utrmc/departments`  
**Modules:** `frontend/lib/api/departments.ts`, `frontend/lib/api/userbase.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `getDepartments()` | GET | `/api/departments/` | List all departments |
| `createDepartment(data)` | POST | `/api/departments/` | Create a department |
| `updateDepartment(id, data)` | PATCH | `/api/departments/{id}/` | Update department |
| `deleteDepartment(id)` | DELETE | `/api/departments/{id}/` | Remove department |
| `getHospitalDepartments()` | GET | `/api/hospital-departments/` | List hospital-dept matrix |
| `createHospitalDepartment(data)` | POST | `/api/hospital-departments/` | Link hospital to dept |
| `deleteHospitalDepartment(id)` | DELETE | `/api/hospital-departments/{id}/` | Unlink hospital from dept |
| `getSupervisorResidentLinks()` | GET | `/api/supervisor-resident-links/` | ⚠ MISMATCH — see below |
| `createSupervisorResidentLink(data)` | POST | `/api/supervisor-resident-links/` | ⚠ MISMATCH — see below |
| `deleteSupervisorResidentLink(id)` | DELETE | `/api/supervisor-resident-links/{id}/` | ⚠ MISMATCH — see below |
| `getHodAssignments()` | GET | `/api/hod-assignments/` | List HOD assignments |
| `createHodAssignment(data)` | POST | `/api/hod-assignments/` | Assign HOD |
| `userbaseApi.departments.list()` | GET | `/api/departments/` | Rich dept list with metadata |
| `userbaseApi.departments.update(id, payload)` | PATCH | `/api/departments/{id}/` | Update department (typed) |
| `userbaseApi.departments.getRoster(id)` | GET | `/api/departments/{id}/roster/` | Department members |
| `userbaseApi.hospitalDepartments.list()` | GET | `/api/hospital-departments/` | Matrix list |
| `userbaseApi.hospitalDepartments.create(payload)` | POST | `/api/hospital-departments/` | Add to matrix |
| `userbaseApi.hospitalDepartments.update(id, payload)` | PATCH | `/api/hospital-departments/{id}/` | Update matrix entry |

---

## Feature: User Management

**Pages:** `/dashboard/utrmc/users`  
**Modules:** `frontend/lib/api/users.ts`, `frontend/lib/api/userbase.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `getAssignedPGs()` | GET | `/api/users/assigned-pgs/` | Supervisor's assigned PGs |
| `userbaseApi.users.list(params)` | GET | `/api/users/` | List users with filters |
| `userbaseApi.users.create(payload)` | POST | `/api/users/` | Create user account |
| `userbaseApi.users.get(id)` | GET | `/api/users/{id}/` | Get user details |
| `userbaseApi.users.update(id, payload)` | PATCH | `/api/users/{id}/` | Update user |
| `userbaseApi.memberships.create(payload)` | POST | `/api/department-memberships/` | Assign user to dept |
| `userbaseApi.memberships.update(id, payload)` | PATCH | `/api/department-memberships/{id}/` | Update membership |
| `userbaseApi.memberships.delete(id)` | DELETE | `/api/department-memberships/{id}/` | Remove membership |
| `userbaseApi.hospitalAssignments.create(payload)` | POST | `/api/hospital-assignments/` | Assign user to hospital |
| `userbaseApi.hospitalAssignments.update(id, payload)` | PATCH | `/api/hospital-assignments/{id}/` | Update assignment |
| `userbaseApi.hospitalAssignments.delete(id)` | DELETE | `/api/hospital-assignments/{id}/` | Remove assignment |
| `userbaseApi.supervisionLinks.list(params)` | GET | `/api/supervision-links/` | List supervisor-resident links |
| `userbaseApi.supervisionLinks.create(payload)` | POST | `/api/supervision-links/` | Create supervision link |
| `userbaseApi.supervisionLinks.update(id, payload)` | PATCH | `/api/supervision-links/{id}/` | Update link |
| `userbaseApi.hodAssignments.list(params)` | GET | `/api/hod-assignments/` | List HOD assignments |
| `userbaseApi.hodAssignments.create(payload)` | POST | `/api/hod-assignments/` | Create HOD assignment |
| `userbaseApi.hodAssignments.update(id, payload)` | PATCH | `/api/hod-assignments/{id}/` | Update HOD assignment |

---

## Feature: Training Programs

**Pages:** `/dashboard/utrmc/programs`  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.listPrograms()` | GET | `/api/programs/` | List training programs |
| `trainingApi.getProgram(id)` | GET | `/api/programs/{id}/` | Get program detail |
| `trainingApi.createProgram(data)` | POST | `/api/programs/` | Create program |
| `trainingApi.updateProgram(id, data)` | PUT | `/api/programs/{id}/` | Update program |
| `trainingApi.getProgramPolicy(programId)` | GET | `/api/programs/{id}/policy/` | Get program policy |
| `trainingApi.updateProgramPolicy(programId, data)` | PUT | `/api/programs/{id}/policy/` | Update program policy |
| `trainingApi.getProgramMilestones(programId)` | GET | `/api/programs/{id}/milestones/` | List milestones |
| `trainingApi.createProgramMilestone(programId, data)` | POST | `/api/programs/{id}/milestones/` | Add milestone |

---

## Feature: Resident Dashboard / Schedule

**Pages:** `/dashboard/pg`, `/dashboard/pg/schedule`, `/dashboard/resident`  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.getResidentSummary()` | GET | `/api/residents/me/summary/` | Resident dashboard summary |
| (rotations via resident-training record) | GET | `/api/my/rotations/` | Resident's own rotations |
| (leaves via my/leaves) | GET | `/api/my/leaves/` | Resident's own leaves |

---

## Feature: Research Project (Resident)

**Pages:** `/dashboard/resident/research`  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.getMyResearch()` | GET | `/api/my/research/` | Get research project |
| `trainingApi.createMyResearch(data)` | POST | `/api/my/research/` | Create research project |
| `trainingApi.updateMyResearch(data)` | PATCH | `/api/my/research/` | Update research project |
| `trainingApi.researchAction(action, data)` | POST | `/api/my/research/action/{action}/` | Trigger research workflow action |
| `trainingApi.approveResearch(data)` | POST | `/api/my/research/action/supervisor-approve/` | Supervisor approve synopsis |
| `trainingApi.returnResearch(data)` | POST | `/api/my/research/action/supervisor-return/` | Supervisor return synopsis |
| (inline in page) | GET | `/api/users/?role=supervisor` | Load supervisor dropdown |
| (inline in page, file upload) | PATCH | `/api/my/research/` (multipart) | Upload synopsis file |
| `trainingApi.getSupervisorResearchApprovals()` | GET | `/api/supervisor/research-approvals/` | Supervisor's pending reviews |

---

## Feature: Thesis (Resident)

**Pages:** `/dashboard/resident/thesis` (assumed)  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.getMyThesis()` | GET | `/api/my/thesis/` | Get thesis record |
| `trainingApi.createMyThesis(data)` | POST | `/api/my/thesis/` | Create thesis record |
| `trainingApi.submitThesis(data)` | POST | `/api/my/thesis/submit/` | Submit thesis |

---

## Feature: Workshops (Resident)

**Pages:** `/dashboard/resident/workshops` (assumed)  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.listWorkshops()` | GET | `/api/workshops/` | List available workshops |
| `trainingApi.getMyWorkshops()` | GET | `/api/my/workshops/` | Get completions |
| `trainingApi.logWorkshopCompletion(data)` | POST | `/api/my/workshops/` | Log completion |
| `trainingApi.deleteWorkshopCompletion(id)` | DELETE | `/api/my/workshops/{id}/` | Remove log entry |

---

## Feature: Eligibility

**Pages:** `/dashboard/utrmc/eligibility`, `/dashboard/pg/eligibility`  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.getMyEligibility()` | GET | `/api/my/eligibility/` | Resident's milestone eligibility |
| `trainingApi.getMilestoneEligibility(programId)` | GET | `/api/utrmc/eligibility/` | UTRMC eligibility overview |

---

## Feature: Supervisor Dashboard

**Pages:** `/dashboard/supervisor`  
**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.getSupervisorSummary()` | GET | `/api/supervisors/me/summary/` | Supervisor dashboard data |
| `trainingApi.getResidentProgress(residentId)` | GET | `/api/supervisors/residents/{id}/progress/` | Resident progress snapshot |

---

## Feature: Notifications

**Pages:** Global (notification bell in header)  
**Module:** `frontend/lib/api/notifications.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `notificationApi.list(params)` | GET | `/api/notifications/` | List notifications |
| `notificationApi.listUnread(params)` | GET | `/api/notifications/` | Unread notifications |
| `notificationApi.getUnreadCount()` | GET | `/api/notifications/unread-count/` | Unread count badge |
| `notificationApi.markRead(ids)` | POST | `/api/notifications/mark-read/` | Mark as read |
| `notificationApi.getPreferences()` | GET | `/api/notifications/preferences/` | Get preferences |
| `notificationApi.updatePreferences(prefs)` | PATCH | `/api/notifications/preferences/` | Update preferences |

---

## Feature: Audit Logs

**Pages:** `/dashboard/admin/audit` (assumed)  
**Module:** `frontend/lib/api/audit.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `auditApi.listActivities(params)` | GET | `/api/audit/activity/` | List activity logs |
| `auditApi.listReports(params)` | GET | `/api/audit/reports/` | List audit reports |
| `auditApi.createReport(data)` | POST | `/api/audit/reports/` | Create audit report |

---

## Feature: Bulk Import/Export

**Pages:** `/dashboard/utrmc/bulk` (assumed)  
**Module:** `frontend/lib/api/bulk.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `bulkApi.import(formData)` | POST | `/api/bulk/import/` | Generic bulk import |
| `bulkApi.importTrainees(formData)` | POST | `/api/bulk/import-trainees/` | Import trainees CSV |
| `bulkApi.importSupervisors(formData)` | POST | `/api/bulk/import-supervisors/` | Import supervisors CSV |
| `bulkApi.importResidents(formData)` | POST | `/api/bulk/import-residents/` | Import residents CSV |
| `bulkApi.importDepartments(formData)` | POST | `/api/bulk/import-departments/` | Import departments CSV |
| `bulkApi.bulkAssign(data)` | POST | `/api/bulk/assignment/` | Bulk assign rotations/leaves |
| `bulkApi.bulkReview(payload)` | POST | `/api/bulk/review/` | Bulk review items |
| `bulkApi.export(resource, format)` | GET | `/api/bulk/exports/{resource}/` | Download export file |

---

## Feature: System Settings

**Module:** `frontend/lib/api/training.ts`

| Function | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| `trainingApi.getSystemSettings()` | GET | `/api/system/settings/` | Get system feature flags |
