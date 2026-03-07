# COMPLETE BACKEND API ENDPOINT CATALOG
## PGSIMS - Django REST Framework Project

**Project Location:** `/home/munaim/srv/apps/pgsims/backend`
**Main URL Router:** `/home/munaim/srv/apps/pgsims/backend/sims_project/urls.py`

---

## 1. AUTHENTICATION API ENDPOINTS
**URL Prefix:** `/api/auth/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/users/api_urls.py`
**App:** `sims.users`

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/auth/login/` | POST | `CustomTokenObtainPairView` | AllowAny | JWT token obtain (with rate throttle) |
| `/api/auth/refresh/` | POST | `TokenRefreshView` | AllowAny | JWT token refresh |
| `/api/auth/logout/` | POST | `logout_view` | IsAuthenticated | User logout |
| `/api/auth/register/` | POST | `register_view` | AllowAny | User registration |
| `/api/auth/me/` | GET | `AuthMeView` | IsAuthenticated | Get current user profile |
| `/api/auth/profile/` | GET | `user_profile_view` | IsAuthenticated | Get user profile details |
| `/api/auth/profile/update/` | PUT, PATCH | `update_profile_view` | IsAuthenticated | Update user profile |
| `/api/auth/password-reset/` | POST | `password_reset_request_view` | AllowAny | Request password reset |
| `/api/auth/password-reset/confirm/` | POST | `password_reset_confirm_view` | AllowAny | Confirm password reset |
| `/api/auth/change-password/` | POST | `change_password_view` | IsAuthenticated | Change password for authenticated user |

---

## 2. USER MANAGEMENT API (Organizational Graph)
**URL Prefix:** `/api/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/users/userbase_urls.py`
**App:** `sims.users`
**ViewSet Router:** DefaultRouter

### 2.1 Hospitals ViewSet
**Base Route:** `/api/hospitals/`
**View Class:** `HospitalViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/hospitals/` | GET | list | List all hospitals |
| `/api/hospitals/` | POST | create | Create new hospital |
| `/api/hospitals/{id}/` | GET | retrieve | Get hospital details |
| `/api/hospitals/{id}/` | PUT, PATCH | update | Update hospital |
| `/api/hospitals/{id}/` | DELETE | destroy | Delete hospital |
| `/api/hospitals/{id}/departments/` | GET | `@action departments` | Get departments in hospital |

### 2.2 Departments ViewSet
**Base Route:** `/api/departments/`
**View Class:** `DepartmentViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/departments/` | GET | list | List all departments |
| `/api/departments/` | POST | create | Create new department |
| `/api/departments/{id}/` | GET | retrieve | Get department details |
| `/api/departments/{id}/` | PUT, PATCH | update | Update department |
| `/api/departments/{id}/` | DELETE | destroy | Delete department |
| `/api/departments/{id}/roster/` | GET | `@action roster` | Get department roster/members |

### 2.3 Hospital Departments ViewSet
**Base Route:** `/api/hospital-departments/`
**View Class:** `HospitalDepartmentViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/hospital-departments/` | GET | list | List all hospital-department mappings |
| `/api/hospital-departments/` | POST | create | Create hospital-department mapping |
| `/api/hospital-departments/{id}/` | GET | retrieve | Get mapping details |
| `/api/hospital-departments/{id}/` | PUT, PATCH | update | Update mapping |
| `/api/hospital-departments/{id}/` | DELETE | destroy | Delete mapping |

### 2.4 Residents ViewSet
**Base Route:** `/api/residents/`
**View Class:** `ResidentProfileViewSet` (BaseManagedModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/residents/` | GET | list | List all resident profiles |
| `/api/residents/` | POST | create | Create resident profile |
| `/api/residents/{id}/` | GET | retrieve | Get resident profile |
| `/api/residents/{id}/` | PUT, PATCH | update | Update resident profile |
| `/api/residents/{id}/` | DELETE | destroy | Delete resident profile |

### 2.5 Staff ViewSet
**Base Route:** `/api/staff/`
**View Class:** `StaffProfileViewSet` (BaseManagedModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/staff/` | GET | list | List all staff profiles |
| `/api/staff/` | POST | create | Create staff profile |
| `/api/staff/{id}/` | GET | retrieve | Get staff profile |
| `/api/staff/{id}/` | PUT, PATCH | update | Update staff profile |
| `/api/staff/{id}/` | DELETE | destroy | Delete staff profile |

### 2.6 Department Memberships ViewSet
**Base Route:** `/api/department-memberships/`
**View Class:** `DepartmentMembershipViewSet` (BaseManagedModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/department-memberships/` | GET | list | List memberships |
| `/api/department-memberships/` | POST | create | Create membership |
| `/api/department-memberships/{id}/` | GET | retrieve | Get membership |
| `/api/department-memberships/{id}/` | PUT, PATCH | update | Update membership |
| `/api/department-memberships/{id}/` | DELETE | destroy | Delete membership |

### 2.7 Hospital Assignments ViewSet
**Base Route:** `/api/hospital-assignments/`
**View Class:** `HospitalAssignmentViewSet` (BaseManagedModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/hospital-assignments/` | GET | list | List hospital assignments |
| `/api/hospital-assignments/` | POST | create | Create hospital assignment |
| `/api/hospital-assignments/{id}/` | GET | retrieve | Get assignment |
| `/api/hospital-assignments/{id}/` | PUT, PATCH | update | Update assignment |
| `/api/hospital-assignments/{id}/` | DELETE | destroy | Delete assignment |

### 2.8 Supervision Links ViewSet
**Base Route:** `/api/supervision-links/`
**View Class:** `SupervisionLinkViewSet` (BaseManagedModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/supervision-links/` | GET | list | List supervision links |
| `/api/supervision-links/` | POST | create | Create supervision link |
| `/api/supervision-links/{id}/` | GET | retrieve | Get supervision link |
| `/api/supervision-links/{id}/` | PUT, PATCH | update | Update supervision link |
| `/api/supervision-links/{id}/` | DELETE | destroy | Delete supervision link |

### 2.9 HOD Assignments ViewSet
**Base Route:** `/api/hod-assignments/`
**View Class:** `HODAssignmentViewSet` (BaseManagedModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/hod-assignments/` | GET | list | List HOD assignments |
| `/api/hod-assignments/` | POST | create | Create HOD assignment |
| `/api/hod-assignments/{id}/` | GET | retrieve | Get assignment |
| `/api/hod-assignments/{id}/` | PUT, PATCH | update | Update assignment |
| `/api/hod-assignments/{id}/` | DELETE | destroy | Delete assignment |

---

## 3. USERS API (Extended)
**URL Prefix:** `/api/users/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/users/api_user_urls.py`
**App:** `sims.users`

### 3.1 Users ViewSet
**Base Route:** `/api/users/`
**View Class:** `UserViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/users/` | GET | list | List all users |
| `/api/users/` | POST | create | Create user |
| `/api/users/{id}/` | GET | retrieve | Get user details |
| `/api/users/{id}/` | PUT, PATCH | update | Update user |
| `/api/users/{id}/` | DELETE | destroy | Delete user |

### 3.2 Supervisor-specific Endpoint
| URL Path | HTTP Methods | View Class | Purpose |
|----------|--------------|-----------|---------|
| `/api/users/assigned-pgs/` | GET | `SupervisorAssignedPGsView` | Get PGs assigned to supervisor |
| | | **Permissions:** IsAuthenticated, IsSupervisor | |

---

## 4. TRAINING & ROTATIONS API
**URL Prefix:** `/api/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/training/urls.py`
**App:** `sims.training`

### 4.1 Training Programs ViewSet
**Base Route:** `/api/programs/`
**View Class:** `TrainingProgramViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`
**Write Permissions:** Admin or UTRMC Admin only

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/programs/` | GET | list | List training programs (filters: active) |
| `/api/programs/` | POST | create | Create program (admin/utrmc_admin only) |
| `/api/programs/{id}/` | GET | retrieve | Get program details |
| `/api/programs/{id}/` | PUT, PATCH | update | Update program (admin/utrmc_admin only) |
| `/api/programs/{id}/` | DELETE | destroy | Delete program (admin/utrmc_admin only) |
| `/api/programs/{id}/policy/` | GET | non-router | Get program policy |

### 4.2 Program Rotation Templates ViewSet
**Base Route:** `/api/program-templates/`
**View Class:** `ProgramRotationTemplateViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`
**Write Permissions:** Admin or UTRMC Admin only

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/program-templates/` | GET | list | List rotation templates (filters: program, required, active) |
| `/api/program-templates/` | POST | create | Create template (admin/utrmc_admin only) |
| `/api/program-templates/{id}/` | GET | retrieve | Get template details |
| `/api/program-templates/{id}/` | PUT, PATCH | update | Update template (admin/utrmc_admin only) |
| `/api/program-templates/{id}/` | DELETE | destroy | Delete template (admin/utrmc_admin only) |

### 4.3 Resident Training Records ViewSet
**Base Route:** `/api/resident-training/`
**View Class:** `ResidentTrainingRecordViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/resident-training/` | GET | list | List training records |
| `/api/resident-training/` | POST | create | Create training record |
| `/api/resident-training/{id}/` | GET | retrieve | Get record details |
| `/api/resident-training/{id}/` | PUT, PATCH | update | Update record |
| `/api/resident-training/{id}/` | DELETE | destroy | Delete record |

### 4.4 Rotation Assignments ViewSet
**Base Route:** `/api/rotations/`
**View Class:** `RotationAssignmentViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

#### Standard CRUD Operations:
| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/rotations/` | GET | list | List rotation assignments |
| `/api/rotations/` | POST | create | Create rotation assignment |
| `/api/rotations/{id}/` | GET | retrieve | Get rotation details |
| `/api/rotations/{id}/` | PUT, PATCH | update | Update rotation |
| `/api/rotations/{id}/` | DELETE | destroy | Delete rotation |

#### Custom Actions (State Machine):
| URL Path | HTTP Methods | Action | Permissions | Purpose |
|----------|--------------|--------|-------------|---------|
| `/api/rotations/{id}/submit/` | POST | `@action submit` | Resident or Admin/UTRMC Admin | Submit rotation for approval |
| `/api/rotations/{id}/hod-approve/` | POST | `@action hod_approve` | Supervisor/Faculty or Admin/UTRMC Admin | HOD approves rotation |
| `/api/rotations/{id}/utrmc-approve/` | POST | `@action utrmc_approve` | Admin/UTRMC Admin only | UTRMC approves rotation |
| `/api/rotations/{id}/activate/` | POST | `@action activate` | Admin/UTRMC Admin | Activate approved rotation |
| `/api/rotations/{id}/complete/` | POST | `@action complete` | Admin/UTRMC Admin | Mark rotation as completed |
| `/api/rotations/{id}/returned/` | POST | `@action returned` | Supervisor/Faculty or Admin/UTRMC Admin | Return rotation (requires reason) |
| `/api/rotations/{id}/reject/` | POST | `@action reject` | Supervisor/Faculty or Admin/UTRMC Admin | Reject rotation (requires reason) |

### 4.5 Leave Requests ViewSet
**Base Route:** `/api/leaves/`
**View Class:** `LeaveRequestViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

#### Standard CRUD Operations:
| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/leaves/` | GET | list | List leave requests |
| `/api/leaves/` | POST | create | Create leave request |
| `/api/leaves/{id}/` | GET | retrieve | Get leave request |
| `/api/leaves/{id}/` | PUT, PATCH | update | Update leave |
| `/api/leaves/{id}/` | DELETE | destroy | Delete leave |

#### Custom Actions:
| URL Path | HTTP Methods | Action | Permissions | Purpose |
|----------|--------------|--------|-------------|---------|
| `/api/leaves/{id}/submit/` | POST | `@action submit` | Resident/PG or Admin/UTRMC Admin | Submit leave for approval |
| `/api/leaves/{id}/approve/` | POST | `@action approve` | Supervisor/Faculty or Admin/UTRMC Admin | Approve leave request |
| `/api/leaves/{id}/reject/` | POST | `@action reject` | Supervisor/Faculty or Admin/UTRMC Admin | Reject leave request |

### 4.6 Deputation Postings ViewSet
**Base Route:** `/api/postings/`
**View Class:** `DeputationPostingViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

#### Standard CRUD Operations:
| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/postings/` | GET | list | List deputation postings |
| `/api/postings/` | POST | create | Create posting |
| `/api/postings/{id}/` | GET | retrieve | Get posting details |
| `/api/postings/{id}/` | PUT, PATCH | update | Update posting |
| `/api/postings/{id}/` | DELETE | destroy | Delete posting |

#### Custom Actions:
| URL Path | HTTP Methods | Action | Permissions | Purpose |
|----------|--------------|--------|-------------|---------|
| `/api/postings/{id}/approve/` | POST | `@action approve` | Supervisor/Faculty or Admin/UTRMC Admin | Approve posting |
| `/api/postings/{id}/reject/` | POST | `@action reject` | Supervisor/Faculty or Admin/UTRMC Admin | Reject posting |
| `/api/postings/{id}/complete/` | POST | `@action complete` | Admin/UTRMC Admin | Mark posting as completed |

### 4.7 Program Milestones ViewSet
**Base Route:** `/api/programs/{program_id}/milestones/`
**View Class:** `ProgramMilestoneViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/programs/{program_id}/milestones/` | GET | list | List milestones for program |
| `/api/programs/{program_id}/milestones/` | POST | create | Create milestone |
| `/api/programs/{program_id}/milestones/{id}/` | GET | retrieve | Get milestone details |
| `/api/programs/{program_id}/milestones/{id}/` | PUT, PATCH | update | Update milestone |
| `/api/programs/{program_id}/milestones/{id}/` | DELETE | destroy | Delete milestone |

### 4.8 Workshops ViewSet
**Base Route:** `/api/workshops/`
**View Class:** `WorkshopViewSet` (ReadOnlyModelViewSet)
**Permissions:** `IsAuthenticated`
**Note:** Read-only; no create/update/delete

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/workshops/` | GET | list | List workshops |
| `/api/workshops/{id}/` | GET | retrieve | Get workshop details |

### 4.9 Non-Router Training Endpoints

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/programs/{program_id}/policy/` | GET | `ProgramPolicyView` | IsAuthenticated | Get program policy details |
| `/api/milestones/{milestone_id}/requirements/research/` | GET | `MilestoneResearchRequirementView` | IsAuthenticated | Get research requirements for milestone |
| `/api/utrmc/approvals/rotations/` | GET | `RotationApprovalInboxView` | IsAuthenticated | Get pending rotation approvals (UTRMC inbox) |
| `/api/utrmc/approvals/leaves/` | GET | `LeaveApprovalInboxView` | IsAuthenticated | Get pending leave approvals (UTRMC inbox) |
| `/api/utrmc/eligibility/` | GET | `UTRMCEligibilityView` | IsAuthenticated | Get UTRMC eligibility status |
| `/api/my/rotations/` | GET | `MyRotationsView` | IsAuthenticated | Get current user's rotations |
| `/api/my/leaves/` | GET | `MyLeavesView` | IsAuthenticated | Get current user's leaves |
| `/api/my/research/` | GET, POST | `ResidentResearchProjectView` | IsAuthenticated | Get/create research project |
| `/api/my/research/action/{action}/` | POST | `ResearchProjectActionView` | IsAuthenticated | Perform action on research project (submit/withdraw) |
| `/api/my/thesis/` | GET, POST | `ResidentThesisView` | IsAuthenticated | Get/manage thesis |
| `/api/my/thesis/submit/` | POST | `ThesisSubmitView` | IsAuthenticated | Submit thesis |
| `/api/my/workshops/` | GET | `MyWorkshopCompletionsView` | IsAuthenticated | Get user's workshop completions |
| `/api/my/workshops/{id}/` | GET | `MyWorkshopCompletionDetailView` | IsAuthenticated | Get workshop completion details |
| `/api/my/eligibility/` | GET | `MyEligibilityView` | IsAuthenticated | Get resident's eligibility status |
| `/api/supervisor/rotations/pending/` | GET | `SupervisorPendingRotationsView` | IsAuthenticated | Get supervisor's pending rotation approvals |
| `/api/supervisor/research-approvals/` | GET | `SupervisorResearchApprovalsView` | IsAuthenticated | Get supervisor's research approvals |
| `/api/residents/me/summary/` | GET | `ResidentSummaryView` | IsAuthenticated | Get resident's training summary |
| `/api/supervisors/me/summary/` | GET | `SupervisorSummaryView` | IsAuthenticated | Get supervisor's overview |
| `/api/supervisors/residents/{resident_id}/progress/` | GET | `SupervisorResidentProgressView` | IsAuthenticated | Get resident's progress (supervisor view) |
| `/api/system/settings/` | GET, PUT, PATCH | `SystemSettingsView` | IsAuthenticated | Get/update system settings |

---

## 5. AUDIT API
**URL Prefix:** `/api/audit/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/audit/urls.py`
**App:** `sims.audit`

### 5.1 Activity Log ViewSet
**Base Route:** `/api/audit/activity/`
**View Class:** `ActivityLogViewSet` (ReadOnlyModelViewSet)
**Permissions:** `IsAdminUser`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/audit/activity/` | GET | list | List activity logs |
| `/api/audit/activity/{id}/` | GET | retrieve | Get activity log detail |
| `/api/audit/activity/export/` | GET | `@action export` | Export activity logs |

### 5.2 Audit Reports ViewSet
**Base Route:** `/api/audit/reports/`
**View Class:** `AuditReportViewSet` (CreateModelMixin + ListModelMixin)
**Permissions:** `IsAdminUser`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/audit/reports/` | GET | list | List audit reports |
| `/api/audit/reports/` | POST | create | Create new audit report |
| `/api/audit/reports/latest/` | GET | `@action latest` | Get latest audit report |

---

## 6. BULK OPERATIONS API
**URL Prefix:** `/api/bulk/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/bulk/urls.py`
**App:** `sims.bulk`

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/bulk/review/` | POST | `BulkReviewView` | IsAuthenticated | Review bulk operations |
| `/api/bulk/assignment/` | POST | `BulkAssignmentView` | IsAuthenticated | Bulk assignment operations |
| `/api/bulk/import/` | POST | `BulkImportView` | IsAuthenticated | Generic bulk import |
| `/api/bulk/import-trainees/` | POST | `BulkTraineeImportView` | IsAuthenticated | Bulk import trainees |
| `/api/bulk/import-supervisors/` | POST | `BulkSupervisorImportView` | IsAuthenticated | Bulk import supervisors |
| `/api/bulk/import-residents/` | POST | `BulkResidentImportView` | IsAuthenticated | Bulk import residents |
| `/api/bulk/import-departments/` | POST | `BulkDepartmentImportView` | IsAuthenticated | Bulk import departments |
| `/api/bulk/exports/{resource}/` | GET | `BulkExportView` | IsAuthenticated | Export resource (trainees/supervisors/residents) |
| `/api/bulk/import/{entity}/{action}/` | POST | `BulkImportEntityView` | IsAuthenticated | Unified import endpoint (entity: type, action: create/update) |

---

## 7. NOTIFICATIONS API
**URL Prefix:** `/api/notifications/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/notifications/urls.py`
**App:** `sims.notifications`

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/notifications/` | GET | `NotificationListView` | IsAuthenticated | List user's notifications (paginated) |
| `/api/notifications/mark-read/` | POST | `NotificationMarkReadView` | IsAuthenticated | Mark notifications as read |
| `/api/notifications/preferences/` | GET, PUT | `NotificationPreferenceView` | IsAuthenticated | Get/update notification preferences |
| `/api/notifications/unread-count/` | GET | `NotificationUnreadCountView` | IsAuthenticated | Get count of unread notifications |

---

## 8. ACADEMICS API
**URL Prefix:** `/academics/api/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/academics/urls.py`
**App:** `sims.academics`

### 8.1 Departments ViewSet
**Base Route:** `/academics/api/departments/`
**View Class:** `DepartmentViewSet` (ModelViewSet)
**Permissions:** `ReadAnyWriteAdminOnly`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/academics/api/departments/` | GET | list | List departments |
| `/academics/api/departments/` | POST | create | Create department (admin only) |
| `/academics/api/departments/{id}/` | GET | retrieve | Get department |
| `/academics/api/departments/{id}/` | PUT, PATCH | update | Update department (admin only) |
| `/academics/api/departments/{id}/` | DELETE | destroy | Delete department (admin only) |

### 8.2 Batches ViewSet
**Base Route:** `/academics/api/batches/`
**View Class:** `BatchViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/academics/api/batches/` | GET | list | List batches |
| `/academics/api/batches/` | POST | create | Create batch |
| `/academics/api/batches/{id}/` | GET | retrieve | Get batch |
| `/academics/api/batches/{id}/` | PUT, PATCH | update | Update batch |
| `/academics/api/batches/{id}/` | DELETE | destroy | Delete batch |

### 8.3 Student Profiles ViewSet
**Base Route:** `/academics/api/students/`
**View Class:** `StudentProfileViewSet` (ModelViewSet)
**Permissions:** `IsAuthenticated`

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/academics/api/students/` | GET | list | List student profiles |
| `/academics/api/students/` | POST | create | Create student profile |
| `/academics/api/students/{id}/` | GET | retrieve | Get student profile |
| `/academics/api/students/{id}/` | PUT, PATCH | update | Update student profile |
| `/academics/api/students/{id}/` | DELETE | destroy | Delete student profile |

---

## 9. LEGACY CASE MANAGEMENT API
**URL Prefix:** `/api/cases/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/cases/api_urls.py`
**App:** `sims.cases` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/cases/categories/` | GET | `CaseCategoryListView` | IsAuthenticated | List case categories |
| `/api/cases/my/` | GET, POST | `PGCaseListCreateView` | IsAuthenticated | List/create own cases |
| `/api/cases/my/{id}/` | GET, PUT, DELETE | `PGCaseDetailView` | IsAuthenticated | Get/update/delete own case |
| `/api/cases/my/{id}/submit/` | POST | `PGCaseSubmitView` | IsAuthenticated | Submit case for review |
| `/api/cases/pending/` | GET | `PendingCaseListView` | IsAuthenticated | List pending cases for review |
| `/api/cases/{id}/review/` | POST | `CaseReviewActionView` | IsAuthenticated | Review/approve/reject case |
| `/api/cases/statistics/` | GET | `CaseStatisticsView` | IsAuthenticated | Get case statistics |

---

## 10. LEGACY LOGBOOK API
**URL Prefix:** `/api/logbook/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/logbook/api_urls.py`
**App:** `sims.logbook` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/logbook/pending/` | GET | `PendingLogbookEntriesView` | `CanViewPendingLogbookQueue` | Get pending logbook entries for verification |
| `/api/logbook/{id}/verify/` | POST | `VerifyLogbookEntryView` | `CanVerifyLogbookEntry` | Verify/approve logbook entry |
| `/api/logbook/my/` | GET, POST | `PGLogbookEntryListCreateView` | IsAuthenticated, IsPGUser | List/create own entries |
| `/api/logbook/my/{id}/` | GET, PUT, PATCH | `PGLogbookEntryDetailView` | IsAuthenticated, IsPGUser | Get/update own entry |
| `/api/logbook/my/{id}/submit/` | POST | `PGLogbookEntrySubmitView` | IsAuthenticated, IsPGUser | Submit entry for verification |

---

## 11. LEGACY CERTIFICATES API
**URL Prefix:** `/api/certificates/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/certificates/api_urls.py`
**App:** `sims.certificates` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/certificates/my/` | GET | `PGCertificatesListView` | IsAuthenticated, IsPGUser | List own certificates |
| `/api/certificates/my/{id}/download/` | GET | `PGCertificateDownloadView` | IsAuthenticated, IsPGUser | Download certificate file |

---

## 12. LEGACY ANALYTICS API
**URL Prefix:** `/api/analytics/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/analytics/urls.py`
**App:** `sims.analytics` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/analytics/trends/` | GET | `TrendAnalyticsView` | IsAuthenticated | Get trend analytics |
| `/api/analytics/comparative/` | GET | `ComparativeAnalyticsView` | IsAuthenticated | Get comparative analytics |
| `/api/analytics/performance/` | GET | `PerformanceMetricsView` | IsAuthenticated | Get performance metrics |
| `/api/analytics/dashboard/overview/` | GET | `DashboardOverviewView` | IsAuthenticated | Get dashboard overview |
| `/api/analytics/dashboard/trends/` | GET | `DashboardTrendsView` | IsAuthenticated | Get dashboard trends |
| `/api/analytics/dashboard/compliance/` | GET | `DashboardComplianceView` | IsAuthenticated | Get compliance dashboard |
| `/api/analytics/events/` | POST | `AnalyticsEventIngestView` | IsAuthenticated | Ingest analytics events |
| `/api/analytics/events/live` | GET | `AnalyticsLiveView` | IsAuthenticated | Get live events |
| `/api/analytics/v1/filters/` | GET | `AnalyticsFiltersView` | IsAuthenticated, AnalyticsAccessPermission | Get available filters |
| `/api/analytics/v1/tabs/{tab}/` | GET | `AnalyticsTabView` | IsAuthenticated, AnalyticsAccessPermission | Get tab data |
| `/api/analytics/v1/tabs/{tab}/export/` | GET | `AnalyticsTabExportView` | IsAuthenticated | Export tab data |
| `/api/analytics/v1/live/` | GET | `AnalyticsLiveView` | IsAuthenticated | Get live analytics |
| `/api/analytics/v1/quality/` | GET | `AnalyticsQualityView` | IsAuthenticated | Get quality metrics |

---

## 13. LEGACY ATTENDANCE API
**URL Prefix:** `/api/attendance/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/attendance/urls.py`
**App:** `sims.attendance` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/attendance/upload/` | POST | `BulkAttendanceUploadView` | IsAuthenticated | Upload attendance records |
| `/api/attendance/summary/` | GET | `AttendanceSummaryView` | IsAuthenticated | Get attendance summary |

---

## 14. LEGACY REPORTS API
**URL Prefix:** `/api/reports/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/reports/urls.py`
**App:** `sims.reports` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/reports/templates/` | GET | `ReportTemplateListView` | IsAuthenticated | List report templates |
| `/api/reports/catalog/` | GET | `ReportCatalogView` | IsAuthenticated | Get report catalog |
| `/api/reports/run/{key}/` | POST | `ReportRunView` | IsAuthenticated | Run report by key |
| `/api/reports/export/{key}/` | GET | `ReportExportView` | IsAuthenticated | Export report results |
| `/api/reports/generate/` | POST | `ReportGenerateView` | IsAuthenticated | Generate custom report |
| `/api/reports/scheduled/` | GET, POST | `ScheduledReportListCreateView` | IsAuthenticated | List/create scheduled reports |
| `/api/reports/scheduled/{id}/` | GET, PUT, PATCH | `ScheduledReportDetailView` | IsAuthenticated | Get/update scheduled report |

---

## 15. LEGACY RESULTS API
**URL Prefix:** `/api/results/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/results/urls.py`
**App:** `sims.results` (legacy)

### 15.1 Exams ViewSet
**Base Route:** `/api/results/exams/`
**View Class:** `ExamViewSet` (ModelViewSet)

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/results/exams/` | GET | list | List exams |
| `/api/results/exams/` | POST | create | Create exam |
| `/api/results/exams/{id}/` | GET | retrieve | Get exam |
| `/api/results/exams/{id}/` | PUT, PATCH | update | Update exam |
| `/api/results/exams/{id}/` | DELETE | destroy | Delete exam |

### 15.2 Scores ViewSet
**Base Route:** `/api/results/scores/`
**View Class:** `ScoreViewSet` (ModelViewSet)

| URL Path | HTTP Methods | Action | Purpose |
|----------|--------------|--------|---------|
| `/api/results/scores/` | GET | list | List scores |
| `/api/results/scores/` | POST | create | Create score |
| `/api/results/scores/{id}/` | GET | retrieve | Get score |
| `/api/results/scores/{id}/` | PUT, PATCH | update | Update score |
| `/api/results/scores/{id}/` | DELETE | destroy | Delete score |

---

## 16. LEGACY SEARCH API
**URL Prefix:** `/api/search/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/_legacy/search/urls.py`
**App:** `sims.search` (legacy)

| URL Path | HTTP Methods | View Class | Permissions | Purpose |
|----------|--------------|-----------|------------|---------|
| `/api/search/` | GET, POST | `GlobalSearchView` | IsAuthenticated | Global search across system |
| `/api/search/history/` | GET | `SearchHistoryView` | IsAuthenticated | Get search history |
| `/api/search/suggestions/` | GET | `SearchSuggestionsView` | IsAuthenticated | Get search suggestions |

---

## 17. UTILITY ENDPOINTS
**File:** `/home/munaim/srv/apps/pgsims/backend/sims_project/urls.py`

| URL Path | HTTP Methods | View Class | Purpose |
|----------|--------------|-----------|---------|
| `/` | GET, POST | `home_view` | Home/login page |
| `/health/` | GET | `health_check` | Health check |
| `/healthz/` | GET | `healthz` | Kubernetes health |
| `/readiness/` | GET | `readiness` | Readiness probe |
| `/liveness/` | GET | `liveness` | Liveness probe |
| `/robots.txt` | GET | `robots_txt` | SEO robots |
| `/__fingerprint/` | GET | `fingerprint_view` | Admin reset fingerprint |
| `/admin/` | - | Django Admin | Django Admin Panel |

---

## 18. HTML/TEMPLATE ENDPOINTS (Non-REST)
**URL Prefix:** `/users/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/users/urls.py`
**Note:** These are HTML/Django template views, not API endpoints

| URL Path | View Class | Purpose |
|----------|-----------|---------|
| `/users/login/` | LoginView | Login page |
| `/users/logout/` | logout_view | Logout |
| `/users/password-change/` | PasswordChangeView | Change password |
| `/users/password-reset/` | PasswordResetView | Password reset |
| `/users/dashboard/` | DashboardRedirectView | Role-based dashboard redirect |
| `/users/admin-dashboard/` | AdminDashboardView | Admin dashboard |
| `/users/supervisor-dashboard/` | SupervisorDashboardView | Supervisor dashboard |
| `/users/pg-dashboard/` | PGDashboardView | PG/Resident dashboard |
| `/users/profile/` | ProfileView | User profile |
| `/users/list/` | UserListView | User management list |
| `/users/create/` | UserCreateView | Create user |
| `/users/pgs/` | PGListView | PG list management |
| `/users/reports/` | UserReportsView | Reports |

---

## 19. ROTATIONS UTILITY ENDPOINT
**URL Prefix:** `/rotations/`
**File:** `/home/munaim/srv/apps/pgsims/backend/sims/rotations/urls.py`

| URL Path | HTTP Methods | View Function | Purpose |
|----------|--------------|---------------|---------|
| `/rotations/api/departments/{hospital_id}/` | GET | `department_by_hospital_api` | Get departments for hospital (requires login) |

---

## KEY PERMISSION PATTERNS

### Permission Classes Used:
- `IsAuthenticated` - Any logged-in user
- `IsAdminUser` - Django admin users only
- `permissions.IsAuthenticated` - DRF version of IsAuthenticated
- `permissions.IsAdminUser` - DRF admin check
- `AllowAny` - No authentication required
- `IsSupervisor` - Custom: supervisor role
- `IsPGUser` - Custom: PG/resident role
- `ReadAnyWriteAdminOnly` - Read for all authenticated, write for admin
- `IsUTRMCAdmin` - Custom: UTRMC admin role
- `IsTechAdmin` - Custom: tech admin role
- `CanViewPendingLogbookQueue` - Custom: can view pending logbook
- `CanVerifyLogbookEntry` - Custom: can verify entries

### Role-Based Access Control:
- **Admin/UTRMC Admin**: Full access to programs, templates, rotation workflow, all admin endpoints
- **Supervisor/Faculty/HOD**: Can approve rotations/leaves, access their supervisees' data
- **Resident/PG**: Can submit rotations/leaves, see own records, create logbook entries/cases
- **Authenticated Users**: Can read organizational data, access analytics

---

## STATISTICS

**Total Active API Endpoints:** ~120+
**REST ViewSets:** 24 (with ~6 custom @action endpoints per average)
**Non-Router APIView Endpoints:** 40+
**HTML Template Views:** 30+
**Utility Endpoints:** 7

**By App:**
- sims.users: 25 endpoints (API + auth + HTML)
- sims.training: 50+ endpoints (major app)
- sims.audit: 3 endpoints
- sims.bulk: 8 endpoints
- sims.notifications: 4 endpoints
- sims.academics: 3 endpoints (ViewSet)
- sims.cases (legacy): 7 endpoints
- sims.logbook (legacy): 5 endpoints
- sims.certificates (legacy): 2 endpoints
- sims.analytics (legacy): 13 endpoints
- sims.attendance (legacy): 2 endpoints
- sims.reports (legacy): 7 endpoints
- sims.results (legacy): 2 endpoints (ViewSet)
- sims.search (legacy): 3 endpoints
- sims.rotations: 1 utility endpoint
- Utility/Health: 7 endpoints

