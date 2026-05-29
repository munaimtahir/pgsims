# Backend–Frontend Truth Map

**Generated:** 2026-03-07  
**Status:** CURRENT — reflects verified integration as of this date  
**Test Coverage:** 103/103 role-based workflow tests passing

This is the single authoritative document linking every frontend feature to its backend implementation.

---

## Feature: Authentication

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/login`, `/register`, `/forgot-password` |
| **Frontend Module** | `frontend/lib/api/auth.ts` |
| **Frontend Functions** | `login()`, `register()`, `logout()`, `getCurrentUser()`, `refreshToken()`, `updateProfile()`, `requestPasswordReset()`, `confirmPasswordReset()`, `changePassword()` |
| **Backend View** | `CustomTokenObtainPairView`, `register_view`, `logout_view`, `user_profile_view`, `update_profile_view`, `password_reset_*` |
| **Backend Source** | `sims/users/api_views.py`, `sims/users/api_urls.py` |
| **Endpoints** | POST `/api/auth/login/`, POST `/api/auth/register/`, POST `/api/auth/logout/`, GET `/api/auth/profile/`, PATCH `/api/auth/profile/update/`, POST `/api/auth/refresh/`, POST `/api/auth/change-password/`, POST `/api/auth/password-reset/`, POST `/api/auth/password-reset/confirm/` |
| **Roles** | All (public for login/register/reset; authenticated for profile) |
| **Token Mechanism** | JWT via `djangorestframework-simplejwt`; access + refresh tokens; auto-refresh on 401 via axios interceptor |
| **Known Issues** | `/api/auth/me/` and `/api/auth/profile/` both exist — frontend uses profile; me/ is redundant |

---

## Feature: Organisation Graph — Hospitals

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/hospitals` |
| **Frontend Modules** | `frontend/lib/api/hospitals.ts`, `frontend/lib/api/userbase.ts` |
| **Backend ViewSet** | `HospitalViewSet` |
| **Backend Source** | `sims/users/userbase_views.py`, `sims/users/userbase_urls.py` |
| **Endpoints** | GET/POST `/api/hospitals/`, GET/PATCH/DELETE `/api/hospitals/{id}/`, GET `/api/hospitals/{id}/departments/` |
| **Write Roles** | admin only (`IsTechAdmin`) |
| **Read Roles** | All authenticated |
| **Request Shape (create)** | `{ name, code, city?, is_active? }` |
| **Response Shape** | `{ id, name, code, city, is_active }` |

---

## Feature: Organisation Graph — Departments

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/departments` |
| **Frontend Modules** | `frontend/lib/api/departments.ts`, `frontend/lib/api/userbase.ts` |
| **Backend ViewSet** | `DepartmentViewSet` |
| **Backend Source** | `sims/users/userbase_views.py` |
| **Endpoints** | GET/POST `/api/departments/`, GET/PATCH/DELETE `/api/departments/{id}/`, GET `/api/departments/{id}/roster/` |
| **Write Roles** | admin only (`IsTechAdmin`) |
| **Read Roles** | All authenticated |
| **Canonical Model** | `sims.academics.Department` — ONE canonical Department entity |

---

## Feature: Hospital–Department Matrix

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/matrix` |
| **Frontend Modules** | `frontend/lib/api/departments.ts`, `frontend/lib/api/userbase.ts` |
| **Backend ViewSet** | `HospitalDepartmentViewSet` |
| **Backend Source** | `sims/users/userbase_views.py` |
| **Endpoints** | GET/POST `/api/hospital-departments/`, PATCH/DELETE `/api/hospital-departments/{id}/` |
| **Write Roles** | admin, utrmc_admin (`IsManager`) |
| **Read Roles** | All authenticated |
| **Request Shape (create)** | `{ hospital: id, department: id, is_active?: bool }` |

---

## Feature: User Management

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/users` |
| **Frontend Modules** | `frontend/lib/api/users.ts`, `frontend/lib/api/userbase.ts` |
| **Backend Views** | `UserListCreateView`, `UserRetrieveUpdateView`, `AssignedPGsView` |
| **Backend Source** | `sims/users/api_user_urls.py` |
| **Endpoints** | GET/POST `/api/users/`, GET/PATCH `/api/users/{id}/`, GET `/api/users/assigned-pgs/` |
| **Write Roles** | admin, utrmc_admin |
| **Read Roles** | admin, utrmc_admin, utrmc_user, supervisor |
| **Special** | `/api/users/assigned-pgs/` is supervisor-only |

---

## Feature: Supervision Links

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/supervision` |
| **Frontend Module** | `frontend/lib/api/userbase.ts` |
| **Backend ViewSet** | `SupervisionLinkViewSet` |
| **Backend Source** | `sims/users/userbase_views.py` |
| **Endpoints** | GET/POST `/api/supervision-links/`, PATCH `/api/supervision-links/{id}/` |
| **Roles** | admin, utrmc_admin only (`IsManager`) |
| **Required Fields** | `supervisor`, `resident`, `start_date` |
| **⚠️ Mismatch** | `departments.ts` calls `/api/supervisor-resident-links/` (wrong URL) — see MISMATCH-001 |

---

## Feature: HOD Assignments

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/hod` |
| **Frontend Module** | `frontend/lib/api/userbase.ts`, `frontend/lib/api/departments.ts` |
| **Backend ViewSet** | `HODAssignmentViewSet` |
| **Endpoints** | GET/POST `/api/hod-assignments/`, PATCH `/api/hod-assignments/{id}/` |
| **Roles** | admin, utrmc_admin (`IsManager`) |
| **Required Fields** | `user`, `department`, `hospital`, `start_date` |

---

## Feature: Training Programs

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/utrmc/programs` |
| **Frontend Module** | `frontend/lib/api/training.ts` (trainingApi) |
| **Backend ViewSet** | `TrainingProgramViewSet`, `ProgramPolicyView`, `ProgramMilestoneViewSet` |
| **Backend Source** | `sims/training/views.py` |
| **Endpoints** | GET/POST `/api/programs/`, GET/PUT `/api/programs/{id}/`, GET/PUT `/api/programs/{id}/policy/`, GET/POST `/api/programs/{id}/milestones/` |
| **Write Roles** | admin, utrmc_admin |
| **Read Roles** | All authenticated |
| **degree_type Values** | `"FCPS"`, `"MD"`, `"MS"`, `"Diploma"`, `"Other"` (UPPERCASE) |

---

## Feature: Rotation Assignment Workflow

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/pg/schedule`, `/dashboard/utrmc`, `/dashboard/supervisor` |
| **Frontend Module** | `frontend/lib/api/training.ts` |
| **Backend ViewSet** | `RotationAssignmentViewSet` |
| **Backend Source** | `sims/training/views.py`, `sims/training/urls.py` |
| **Endpoints** | See Rotation endpoints in API_ENDPOINT_CATALOG.md |
| **State Machine** | `draft → submitted → approved → active → completed` / `→ returned → draft` / `→ rejected` |
| **PG Actions** | create (draft), submit |
| **Admin/UTRMC Actions** | hod-approve, utrmc-approve, activate, complete, returned, reject |
| **Resident View** | `GET /api/my/rotations/` |
| **Admin Inbox** | `GET /api/utrmc/approvals/rotations/` |
| **Supervisor View** | `GET /api/supervisor/rotations/pending/` |
| **Error Handling** | 409 for invalid state transition |

---

## Feature: Leave Requests

| Property | Value |
|----------|-------|
| **Frontend Module** | `frontend/lib/api/training.ts` |
| **Backend ViewSet** | `LeaveRequestViewSet` |
| **Endpoints** | GET/POST `/api/leaves/`, POST `/api/leaves/{id}/submit/`, POST `/api/leaves/{id}/approve/`, POST `/api/leaves/{id}/reject/`, GET `/api/my/leaves/` |
| **State Machine** | `draft → submitted → approved` / `→ rejected` |
| **PG Actions** | create, submit |
| **Admin/UTRMC Actions** | approve, reject |
| **UTRMC Inbox** | `GET /api/utrmc/approvals/leaves/` |

---

## Feature: Research Project

| Property | Value |
|----------|-------|
| **Frontend Pages** | `/dashboard/resident/research` |
| **Frontend Module** | `frontend/lib/api/training.ts` |
| **Backend Views** | `ResidentResearchProjectView`, `ResearchProjectActionView`, `SupervisorResearchApprovalsView` |
| **Endpoints** | GET/POST/PATCH `/api/my/research/`, POST `/api/my/research/action/{action}/`, GET `/api/supervisor/research-approvals/` |
| **State Machine** | `draft → submitted_to_supervisor → synopsis_approved → submitted_to_university → accepted` / `→ supervisor_returned` |
| **PG Actions** | create, update, submit to supervisor, submit to university |
| **Supervisor Actions** | approve synopsis, return synopsis |
| **File Upload** | PATCH with multipart FormData for `synopsis_file` |

---

## Feature: Thesis

| Property | Value |
|----------|-------|
| **Frontend Module** | `frontend/lib/api/training.ts` |
| **Backend Views** | `ResidentThesisView`, `ThesisSubmitView` |
| **Endpoints** | GET/POST `/api/my/thesis/`, POST `/api/my/thesis/submit/` |
| **Roles** | pg only |
| **Page Status** | ⚠️ No page found in `frontend/app/` — see MISSING_IMPLEMENTATIONS |

---

## Feature: Workshops

| Property | Value |
|----------|-------|
| **Frontend Module** | `frontend/lib/api/training.ts` |
| **Backend ViewSet/Views** | `WorkshopViewSet`, `MyWorkshopCompletionsView`, `MyWorkshopCompletionDetailView` |
| **Endpoints** | GET `/api/workshops/`, GET/POST `/api/my/workshops/`, DELETE `/api/my/workshops/{id}/` |
| **Roles** | read: all; create/delete completions: pg only |
| **Page Status** | ⚠️ No page found in `frontend/app/` — see MISSING_IMPLEMENTATIONS |

---

## Feature: Eligibility

| Property | Value |
|----------|-------|
| **Frontend Module** | `frontend/lib/api/training.ts` |
| **Backend Views** | `MyEligibilityView`, `UTRMCEligibilityView` |
| **Endpoints** | GET `/api/my/eligibility/`, GET `/api/utrmc/eligibility/` |
| **PG View** | Own milestone eligibility status |
| **UTRMC View** | All residents' eligibility matrix |

---

## Feature: Notifications

| Property | Value |
|----------|-------|
| **Frontend Component** | Global notification bell/drawer |
| **Frontend Module** | `frontend/lib/api/notifications.ts` |
| **Backend ViewSet/View** | `NotificationViewSet`, `NotificationPreferencesView` |
| **Backend Source** | `sims/notifications/` |
| **Endpoints** | GET `/api/notifications/`, GET `/api/notifications/unread-count/`, POST `/api/notifications/mark-read/`, GET/PATCH `/api/notifications/preferences/` |
| **Roles** | All authenticated |
| **Schema** | `recipient`, `verb`, `body`, `metadata` — NO legacy keys |
| **Unread Count Field** | `{ "unread": N }` — NOT `"count"` or `"unread_count"` |
| **Mark Read Payload** | `{ "notification_ids": [id1, id2] }` — NOT `"ids"` |

---

## Feature: Audit Logs

| Property | Value |
|----------|-------|
| **Frontend Module** | `frontend/lib/api/audit.ts` |
| **Backend ViewSets** | `ActivityLogViewSet`, `AuditReportViewSet` |
| **Endpoints** | GET/POST `/api/audit/activity/`, GET/POST `/api/audit/reports/` |
| **Roles** | admin only (`IsAdminUser` — requires `is_staff=True`) |

---

## Feature: Bulk Operations

| Property | Value |
|----------|-------|
| **Frontend Module** | `frontend/lib/api/bulk.ts` |
| **Backend Views** | `BulkImportView`, `BulkAssignmentView`, `BulkReviewView`, `BulkExportView` |
| **Endpoints** | POST `/api/bulk/import/`, POST `/api/bulk/import-{type}/`, POST `/api/bulk/assignment/`, POST `/api/bulk/review/`, GET `/api/bulk/exports/{resource}/` |
| **Write Roles** | admin, utrmc_admin |
| **Read/Export Roles** | admin, utrmc_admin, utrmc_user |
| **⚠️ Needs Verification** | Specialised import endpoints (`/import-trainees/` etc.) need backend URL verification |

---

## Verified Integration Checkpoints

The following integration points are verified by the role-based test suite (`sims/tests/test_role_workflows.py`, 103/103 passing):

| Checkpoint | Status |
|------------|--------|
| Login → JWT token → profile retrieval | ✓ Verified |
| Hospital CRUD: admin can create, utrmc_admin cannot | ✓ Verified |
| Department CRUD: admin can create, utrmc_admin cannot | ✓ Verified |
| HospitalDepartment: admin + utrmc_admin can manage | ✓ Verified |
| SupervisionLink: admin + utrmc_admin only | ✓ Verified |
| HODAssignment: admin + utrmc_admin only | ✓ Verified |
| Training program: admin + utrmc_admin can write | ✓ Verified |
| Rotation workflow: pg submits → admin approves | ✓ Verified |
| Leave workflow: pg submits → admin approves | ✓ Verified |
| Notification mark-read (notification_ids field) | ✓ Verified |
| Notification unread count (unread field) | ✓ Verified |
| Audit log: admin only | ✓ Verified |
| Supervisor sees only assigned residents | ✓ Verified |
| PG my-views: my/rotations, my/leaves | ✓ Verified |
