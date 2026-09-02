# API Endpoint Catalog

**Generated:** 2026-03-07  
**Source:** Full scan of `backend/sims/` URL files and views  
**Status:** CURRENT — reflects actual implementation

---

## Auth Endpoints — `/api/auth/`

Source: `sims/users/api_urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/auth/login/` | POST | `CustomTokenObtainPairView` | All (public) | ✓ Implemented |
| `/api/auth/refresh/` | POST | `TokenRefreshView` | All (public) | ✓ Implemented |
| `/api/auth/logout/` | POST | `logout_view` | Authenticated | ✓ Implemented |
| `/api/auth/register/` | POST | `register_view` | All (public) | ✓ Implemented |
| `/api/auth/me/` | GET | `AuthMeView` | Authenticated | ✓ Implemented |
| `/api/auth/profile/` | GET | `user_profile_view` | Authenticated | ✓ Implemented |
| `/api/auth/profile/update/` | PATCH | `update_profile_view` | Authenticated | ✓ Implemented |
| `/api/auth/password-reset/` | POST | `password_reset_request_view` | All (public) | ✓ Implemented |
| `/api/auth/password-reset/confirm/` | POST | `password_reset_confirm_view` | All (public) | ✓ Implemented |
| `/api/auth/change-password/` | POST | `change_password_view` | Authenticated | ✓ Implemented |

**Note:** Frontend calls `/api/auth/profile/` via `getCurrentUser()` in `auth.ts`. Both `/api/auth/me/` and `/api/auth/profile/` return user data — `/me/` is via `AuthMeView`, `/profile/` via function-based view. Frontend should standardise on one.

---

## Organisation Graph — `/api/`

Source: `sims/users/userbase_urls.py`

| Endpoint | Method | ViewSet/View | Roles | Status |
|----------|--------|-------------|-------|--------|
| `/api/hospitals/` | GET | `HospitalViewSet.list` | All authenticated | ✓ Implemented |
| `/api/hospitals/` | POST | `HospitalViewSet.create` | admin (IsTechAdmin) | ✓ Implemented |
| `/api/hospitals/{id}/` | GET | `HospitalViewSet.retrieve` | All authenticated | ✓ Implemented |
| `/api/hospitals/{id}/` | PATCH | `HospitalViewSet.partial_update` | admin (IsTechAdmin) | ✓ Implemented |
| `/api/hospitals/{id}/` | DELETE | `HospitalViewSet.destroy` | admin (IsTechAdmin) | ✓ Implemented |
| `/api/hospitals/{id}/departments/` | GET | `HospitalViewSet.departments` (action) | All authenticated | ✓ Implemented |
| `/api/departments/` | GET | `DepartmentViewSet.list` | All authenticated | ✓ Implemented |
| `/api/departments/` | POST | `DepartmentViewSet.create` | admin (IsTechAdmin) | ✓ Implemented |
| `/api/departments/{id}/` | GET | `DepartmentViewSet.retrieve` | All authenticated | ✓ Implemented |
| `/api/departments/{id}/` | PATCH | `DepartmentViewSet.partial_update` | admin (IsTechAdmin) | ✓ Implemented |
| `/api/departments/{id}/` | DELETE | `DepartmentViewSet.destroy` | admin (IsTechAdmin) | ✓ Implemented |
| `/api/departments/{id}/roster/` | GET | `DepartmentViewSet.roster` (action) | admin, utrmc_admin, utrmc_user, supervisor | ✓ Implemented |
| `/api/hospital-departments/` | GET | `HospitalDepartmentViewSet.list` | All authenticated | ✓ Implemented |
| `/api/hospital-departments/` | POST | `HospitalDepartmentViewSet.create` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/hospital-departments/{id}/` | PATCH | `HospitalDepartmentViewSet.partial_update` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/hospital-departments/{id}/` | DELETE | `HospitalDepartmentViewSet.destroy` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/residents/` | GET | `ResidentProfileViewSet.list` | admin, utrmc_admin, utrmc_user, supervisor | ✓ Implemented |
| `/api/residents/` | POST | `ResidentProfileViewSet.create` | admin, utrmc_admin | ✓ Implemented |
| `/api/residents/{user_id}/` | GET | `ResidentProfileViewSet.retrieve` | admin, utrmc_admin, utrmc_user, supervisor | ✓ Implemented |
| `/api/residents/{user_id}/` | PATCH | `ResidentProfileViewSet.partial_update` | admin, utrmc_admin | ✓ Implemented |
| `/api/staff/` | GET | `StaffProfileViewSet.list` | admin, utrmc_admin, utrmc_user | ✓ Implemented |
| `/api/staff/` | POST | `StaffProfileViewSet.create` | admin, utrmc_admin | ✓ Implemented |
| `/api/staff/{user_id}/` | GET/PATCH | `StaffProfileViewSet` | admin, utrmc_admin | ✓ Implemented |
| `/api/department-memberships/` | GET/POST | `DepartmentMembershipViewSet` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/department-memberships/{id}/` | PATCH/DELETE | `DepartmentMembershipViewSet` | admin, utrmc_admin | ✓ Implemented |
| `/api/hospital-assignments/` | GET/POST | `HospitalAssignmentViewSet` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/hospital-assignments/{id}/` | PATCH/DELETE | `HospitalAssignmentViewSet` | admin, utrmc_admin | ✓ Implemented |
| `/api/supervision-links/` | GET | `SupervisionLinkViewSet.list` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/supervision-links/` | POST | `SupervisionLinkViewSet.create` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/supervision-links/{id}/` | PATCH | `SupervisionLinkViewSet.partial_update` | admin, utrmc_admin | ✓ Implemented |
| `/api/hod-assignments/` | GET | `HODAssignmentViewSet.list` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/hod-assignments/` | POST | `HODAssignmentViewSet.create` | admin, utrmc_admin (IsManager) | ✓ Implemented |
| `/api/hod-assignments/{id}/` | PATCH | `HODAssignmentViewSet.partial_update` | admin, utrmc_admin | ✓ Implemented |

---

## User Management — `/api/users/`

Source: `sims/users/api_user_urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/users/` | GET | `UserListCreateView` | admin, utrmc_admin, utrmc_user, supervisor | ✓ Implemented |
| `/api/users/` | POST | `UserListCreateView` | admin, utrmc_admin | ✓ Implemented |
| `/api/users/{id}/` | GET | `UserRetrieveUpdateView` | admin, utrmc_admin, utrmc_user | ✓ Implemented |
| `/api/users/{id}/` | PATCH | `UserRetrieveUpdateView` | admin, utrmc_admin | ✓ Implemented |
| `/api/users/assigned-pgs/` | GET | `AssignedPGsView` | supervisor | ✓ Implemented |

---

## Training Programs — `/api/programs/`

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/programs/` | GET | `TrainingProgramViewSet.list` | All authenticated | ✓ Implemented |
| `/api/programs/` | POST | `TrainingProgramViewSet.create` | admin, utrmc_admin | ✓ Implemented |
| `/api/programs/{id}/` | GET | `TrainingProgramViewSet.retrieve` | All authenticated | ✓ Implemented |
| `/api/programs/{id}/` | PUT | `TrainingProgramViewSet.update` | admin, utrmc_admin | ✓ Implemented |
| `/api/programs/{id}/` | DELETE | `TrainingProgramViewSet.destroy` | admin | ✓ Implemented |
| `/api/programs/{id}/policy/` | GET | `ProgramPolicyView` | All authenticated | ✓ Implemented |
| `/api/programs/{id}/policy/` | PUT | `ProgramPolicyView` | admin, utrmc_admin | ✓ Implemented |
| `/api/programs/{id}/milestones/` | GET | `ProgramMilestoneViewSet.list` | All authenticated | ✓ Implemented |
| `/api/programs/{id}/milestones/` | POST | `ProgramMilestoneViewSet.create` | admin, utrmc_admin | ✓ Implemented |
| `/api/programs/{id}/milestones/{id}/` | GET/PUT/PATCH/DELETE | `ProgramMilestoneViewSet` | admin, utrmc_admin | ✓ Implemented |

---

## Resident Training Records — `/api/resident-training/`

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/resident-training/` | GET | `ResidentTrainingRecordViewSet.list` | admin, utrmc_admin, utrmc_user | ✓ Implemented |
| `/api/resident-training/` | POST | `ResidentTrainingRecordViewSet.create` | admin, utrmc_admin | ✓ Implemented |
| `/api/resident-training/{id}/` | GET | `ResidentTrainingRecordViewSet.retrieve` | admin, utrmc_admin, utrmc_user, pg (own) | ✓ Implemented |
| `/api/resident-training/{id}/` | PATCH | `ResidentTrainingRecordViewSet.partial_update` | admin, utrmc_admin | ✓ Implemented |

---

## Rotations — `/api/rotations/`

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/rotations/` | GET | `RotationAssignmentViewSet.list` | All authenticated (scoped) | ✓ Implemented |
| `/api/rotations/` | POST | `RotationAssignmentViewSet.create` | pg, admin, utrmc_admin | ✓ Implemented |
| `/api/rotations/{id}/` | GET | `RotationAssignmentViewSet.retrieve` | All authenticated (scoped) | ✓ Implemented |
| `/api/rotations/{id}/` | PATCH | `RotationAssignmentViewSet.partial_update` | pg (draft/returned only), admin | ✓ Implemented |
| `/api/rotations/{id}/` | DELETE | `RotationAssignmentViewSet.destroy` | admin | ✓ Implemented |
| `/api/rotations/{id}/submit/` | POST | `RotationAssignmentViewSet.submit` | pg | ✓ Implemented |
| `/api/rotations/{id}/hod-approve/` | POST | `RotationAssignmentViewSet.hod_approve` | admin, utrmc_admin | ✓ Implemented |
| `/api/rotations/{id}/utrmc-approve/` | POST | `RotationAssignmentViewSet.utrmc_approve` | admin, utrmc_admin | ✓ Implemented |
| `/api/rotations/{id}/activate/` | POST | `RotationAssignmentViewSet.activate` | admin, utrmc_admin | ✓ Implemented |
| `/api/rotations/{id}/complete/` | POST | `RotationAssignmentViewSet.complete` | admin, utrmc_admin | ✓ Implemented |
| `/api/rotations/{id}/returned/` | POST | `RotationAssignmentViewSet.returned` | admin, utrmc_admin | ✓ Implemented |
| `/api/rotations/{id}/reject/` | POST | `RotationAssignmentViewSet.reject` | admin, utrmc_admin | ✓ Implemented |
| `/api/my/rotations/` | GET | `MyRotationsView` | pg | ✓ Implemented |
| `/api/utrmc/approvals/rotations/` | GET | `RotationApprovalInboxView` | admin, utrmc_admin, utrmc_user | ✓ Implemented |
| `/api/supervisor/rotations/pending/` | GET | `SupervisorPendingRotationsView` | supervisor | ✓ Implemented |

---

## Leaves — `/api/leaves/`

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/leaves/` | GET | `LeaveRequestViewSet.list` | All authenticated (scoped) | ✓ Implemented |
| `/api/leaves/` | POST | `LeaveRequestViewSet.create` | pg | ✓ Implemented |
| `/api/leaves/{id}/` | GET/PATCH | `LeaveRequestViewSet` | pg (own), admin, utrmc_admin | ✓ Implemented |
| `/api/leaves/{id}/submit/` | POST | `LeaveRequestViewSet.submit` | pg | ✓ Implemented |
| `/api/leaves/{id}/approve/` | POST | `LeaveRequestViewSet.approve` | admin, utrmc_admin | ✓ Implemented |
| `/api/leaves/{id}/reject/` | POST | `LeaveRequestViewSet.reject` | admin, utrmc_admin | ✓ Implemented |
| `/api/my/leaves/` | GET | `MyLeavesView` | pg | ✓ Implemented |
| `/api/utrmc/approvals/leaves/` | GET | `LeaveApprovalInboxView` | admin, utrmc_admin, utrmc_user | ✓ Implemented |

---

## Deputation Postings — `/api/postings/`

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/postings/` | GET/POST | `DeputationPostingViewSet` | admin, utrmc_admin | ✓ Implemented |
| `/api/postings/{id}/` | GET/PATCH/DELETE | `DeputationPostingViewSet` | admin, utrmc_admin | ✓ Implemented |

---

## Research, Thesis, Workshops, Eligibility (Resident Academic)

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/my/research/` | GET | `ResidentResearchProjectView` | pg | ✓ Implemented |
| `/api/my/research/` | POST | `ResidentResearchProjectView` | pg | ✓ Implemented |
| `/api/my/research/` | PATCH | `ResidentResearchProjectView` | pg | ✓ Implemented |
| `/api/my/research/action/{action}/` | POST | `ResearchProjectActionView` | pg | ✓ Implemented |
| `/api/supervisor/research-approvals/` | GET | `SupervisorResearchApprovalsView` | supervisor | ✓ Implemented |
| `/api/my/thesis/` | GET | `ResidentThesisView` | pg | ✓ Implemented |
| `/api/my/thesis/` | POST | `ResidentThesisView` | pg | ✓ Implemented |
| `/api/my/thesis/submit/` | POST | `ThesisSubmitView` | pg | ✓ Implemented |
| `/api/workshops/` | GET | `WorkshopViewSet.list` | All authenticated | ✓ Implemented |
| `/api/my/workshops/` | GET | `MyWorkshopCompletionsView` | pg | ✓ Implemented |
| `/api/my/workshops/` | POST | `MyWorkshopCompletionsView` | pg | ✓ Implemented |
| `/api/my/workshops/{id}/` | DELETE | `MyWorkshopCompletionDetailView` | pg | ✓ Implemented |
| `/api/my/eligibility/` | GET | `MyEligibilityView` | pg | ✓ Implemented |
| `/api/utrmc/eligibility/` | GET | `UTRMCEligibilityView` | admin, utrmc_admin, utrmc_user | ✓ Implemented |
| `/api/milestones/{id}/requirements/research/` | GET | `MilestoneResearchRequirementView` | All authenticated | ✓ Implemented |

---

## Summary Endpoints

Source: `sims/training/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/residents/me/summary/` | GET | `ResidentSummaryView` | pg | ✓ Implemented |
| `/api/supervisors/me/summary/` | GET | `SupervisorSummaryView` | supervisor | ✓ Implemented |
| `/api/supervisors/residents/{id}/progress/` | GET | `SupervisorResidentProgressView` | supervisor | ✓ Implemented |
| `/api/system/settings/` | GET | `SystemSettingsView` | All authenticated | ✓ Implemented |

---

## Notifications — `/api/notifications/`

Source: `sims/notifications/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/notifications/` | GET | `NotificationViewSet.list` | All authenticated | ✓ Implemented |
| `/api/notifications/unread-count/` | GET | `NotificationViewSet.unread_count` | All authenticated | ✓ Implemented |
| `/api/notifications/mark-read/` | POST | `NotificationViewSet.mark_read` | All authenticated | ✓ Implemented |
| `/api/notifications/preferences/` | GET | `NotificationPreferencesView` | All authenticated | ✓ Implemented |
| `/api/notifications/preferences/` | PATCH | `NotificationPreferencesView` | All authenticated | ✓ Implemented |

---

## Audit — `/api/audit/`

Source: `sims/audit/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/audit/activity/` | GET | `ActivityLogViewSet.list` | admin (is_staff) | ✓ Implemented |
| `/api/audit/activity/` | POST | `ActivityLogViewSet.create` | admin (is_staff) | ✓ Implemented |
| `/api/audit/activity/{id}/` | GET/PATCH/DELETE | `ActivityLogViewSet` | admin (is_staff) | ✓ Implemented |
| `/api/audit/reports/` | GET | `AuditReportViewSet.list` | admin (is_staff) | ✓ Implemented |
| `/api/audit/reports/` | POST | `AuditReportViewSet.create` | admin (is_staff) | ✓ Implemented |

---

## Bulk Operations — `/api/bulk/`

Source: `sims/bulk/urls.py`

| Endpoint | Method | View | Roles | Status |
|----------|--------|------|-------|--------|
| `/api/bulk/import/` | POST | `BulkImportView` | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/import-trainees/` | POST | `BulkImportView` (trainees) | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/import-supervisors/` | POST | `BulkImportView` (supervisors) | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/import-residents/` | POST | `BulkImportView` (residents) | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/import-departments/` | POST | `BulkImportView` (departments) | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/assignment/` | POST | `BulkAssignmentView` | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/review/` | POST | `BulkReviewView` | admin, utrmc_admin | ✓ Implemented |
| `/api/bulk/exports/{resource}/` | GET | `BulkExportView` | admin, utrmc_admin, utrmc_user | ✓ Implemented |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Auth endpoints | 10 |
| Org graph endpoints | 28 |
| User management | 5 |
| Training programs | 10 |
| Resident training records | 4 |
| Rotations | 13 |
| Leaves | 8 |
| Postings | 5 |
| Research/Thesis/Workshop/Eligibility | 15 |
| Summary/Settings | 4 |
| Notifications | 5 |
| Audit | 5 |
| Bulk operations | 8 |
| **Total** | **120** |
