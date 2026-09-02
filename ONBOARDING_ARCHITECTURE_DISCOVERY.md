# PGR SIMS Resident Onboarding — Architecture Discovery & Current-State Audit

This report documents the strictly read-only architecture discovery focused on the current Resident account creation, onboarding, profile, training, supervisor assignment, document upload, authentication, API, and frontend architecture of the postgraduate management system.

---

## 1. Executive Summary

A comprehensive architectural discovery and state audit of the PGR SIMS repository reveals the following:
* **Universal Identity Layer**: The system has successfully converged on the final four roles: `ADMIN`, `RESIDENT`, `SUPERVISOR`, and `SUPPORT_STAFF`. Universal account creation occurs via the service-layer function [`create_user_with_profile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/services.py#L266).
* **Onboarding & Dynamic Profile Completion**: Dynamic validation is driven by a central registry [`PROFILE_COMPLETION_REQUIREMENTS`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/services.py#L12) on the backend. NextJS route guards (`ProtectedRoute.tsx`) successfully intercept unauthorized dashboard paths and direct incomplete profiles to `/complete-profile`.
* **Data Model Duplications**: High data duplication exists between the core [`User`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L48) model (inheriting fields and defining home hospital/department/specialty/phone) and the specialized [`ResidentProfile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L451). Similarly, supervisors are linked via both `User.supervisor` (direct ForeignKey) and [`ResidentSupervisorAssignment`](file:///home/munaim/srv/apps/pgsims/backend/sims/supervision/models.py#L7).
* **Resident Document Center Gap**: While the backend includes a fully fleshed-out program-specific submission and review architecture for Synopsis/Thesis (`ResidentSubmission`, `SubmissionDocument`, and `SubmissionRequirementTemplate`), **there is no frontend UI for residents to upload documents**, and no generic onboarding document upload model exists.
* **Dashboard Redirect Stubs**: Subpages under the resident dashboard (e.g. `/dashboard/resident/thesis`, `/dashboard/resident/research`) exist but currently operate as NextJS client-side redirect stubs pointing back to the main resident dashboard page.

---

## 2. Repository Architecture

The project is structured as a decoupled NextJS (frontend) and Django (backend) monorepo:
* **Backend Framework & Location**: Django REST Framework located in the [`backend/`](file:///home/munaim/srv/apps/pgsims/backend/) directory.
* **Frontend Framework & Location**: NextJS App Router located in the [`frontend/`](file:///home/munaim/srv/apps/pgsims/frontend/) directory.
* **Authentication**: JWT-based authentication using [`django-rest-framework-simplejwt`](https://django-rest-framework-simplejwt.readthedocs.io/). Client-side auth state is managed in a persisted Zustand store [`authStore.ts`](file:///home/munaim/srv/apps/pgsims/frontend/store/authStore.ts) and synchronized to cookies for NextJS middleware route protection.
* **Database Technology**: SQLite for local development (`db.sqlite3` and `sims_db`).
* **Django Applications**:
  * [`sims.users`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/): Custom `User` model, role-specific profiles, services, and dynamic completion registries.
  * [`sims.training`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/): Postgraduate training records, milestones, workshop completions, logbooks, and synopsis/thesis submissions.
  * [`sims.supervision`](file:///home/munaim/srv/apps/pgsims/backend/sims/supervision/): Supervision assignment and tracking models.
  * [`sims.academics`](file:///home/munaim/srv/apps/pgsims/backend/sims/academics/): Specialties, departments, and academic periods.
  * [`sims.bulk`](file:///home/munaim/srv/apps/pgsims/backend/sims/bulk/): CSV/Excel template and flexible column mapping engines.
  * [`sims._legacy`](file:///home/munaim/srv/apps/pgsims/backend/sims/_legacy/): Old modules (cases, logbook, certificates) whose template views are bypassed via dummy URL redirects to `/dashboard`.

---

## 3. Authentication / User Architecture

The canonical authentication model is the custom [`User`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L48) class:
* **File Path**: [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L48)
* **PrimaryKey**: `id` (Auto-incrementing integer)
* **Username Field**: `username` (alphanumeric string with defaults like `pgr001` or `sup001`)
* **Email Handling**: `email` (standard string field) + `has_placeholder_email` (computed boolean indicator for generated pilot emails)
* **Password Handling**: Hashed storage (`set_password()`). New accounts default to temporary password `pgfmu123` and `must_change_password = True`.
* **Account Status**: `is_active` (boolean) + `is_archived` (boolean) + `archived_date` (datetime)
* **Role Representation**: `role` string field with choices `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`.
* **Profile Completion Fields**:
  * `is_profile_complete`: Boolean indicator indicating if required onboarding profile fields are filled.
  * `is_complete_profile`: Boolean indicator (legacy data quality flag).
  * `data_issues`: JSONField listing computed data quality issue codes.
* **Onboarding Logic**:
  * [`AuthMeView`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py#L586) (`GET /api/auth/me/`) recalculates profile completion state and returns `allowed_next_route` based on constraints.
  * If `must_change_password` is `True` $\to$ returns `/change-password`.
  * If required profile registry fields are missing $\to$ returns `/complete-profile`.
  * If complete $\to$ returns role-specific dashboard URL.
  * On the frontend, NextJS [`ProtectedRoute.tsx`](file:///home/munaim/srv/apps/pgsims/frontend/components/auth/ProtectedRoute.tsx#L16) calls `me()` on mount/navigation and redirects the user if `allowed_next_route` does not match the current path.

---

## 4. Role Architecture

The system supports exactly four roles, defined in [`USER_ROLES`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L8):
```python
USER_ROLES = (
    ("ADMIN", "Admin"),
    ("RESIDENT", "Resident"),
    ("SUPERVISOR", "Supervisor"),
    ("SUPPORT_STAFF", "Support Staff"),
)
```
* **Backend Enforcements**: Profile models ([`AdminProfile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L395), [`ResidentProfile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L451), [`SupervisorProfile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L547), [`SupportStaffProfile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L643)) enforce role matching in their `clean()` validation methods (e.g. `ResidentProfile` errors out if the linked user does not have `RESIDENT` role).
* **Frontend Enforcements**: Zustand store, NextJS middleware, and dynamic sidebar rendering check role strings.
* **Legacy Role Mappings**: Handled dynamically during identity repair (`repair_identity_profiles` command) where old roles are converted:
  * `UTRMC_ADMIN` / `SUPER_ADMIN` / `SYSTEM_ADMIN` $\to$ `ADMIN`
  * `TEACHER` / `FACULTY` $\to$ `SUPERVISOR`
  * `STUDENT` / `PGR` / `TRAINEE` $\to$ `RESIDENT`
  * `CLERK` / `OFFICE_STAFF` / `DATA_ENTRY` $\to$ `SUPPORT_STAFF`

---

## 5. Resident Models

Trainee/resident data is split across three primary models:

### Model A: `users.User`
* **Source File**: [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L48)
* **Purpose**: Credentials, active status, role, phone, and legacy home hospital/department links.
* **Key Fields**: `username`, `email`, `role`, `supervisor`, `home_hospital`, `home_department`, `phone_number`, `registration_number`.

### Model B: `users.ResidentProfile`
* **Source File**: [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L451)
* **Purpose**: Personal and academic metadata linked to the resident identity.
* **Key Fields**: `user` (OneToOne), `registration_no`, `cnic`, `phone`, `email`, `hospital` (FK to Hospital), `department_ref` (FK to Department), `program_ref` (FK to TrainingProgram), `academic_session_ref` (FK to AcademicSession), `specialty_ref` (FK to Specialty), `profile_status` (INCOMPLETE/COMPLETE), `profile_schema_version`, `completed_schema_version`.

### Model C: `training.ResidentTrainingRecord`
* **Source File**: [`backend/sims/training/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L111)
* **Purpose**: Represents the active timeline and container for training progress, rotations, and milestones.
* **Key Fields**: `resident_user` (FK to User), `program` (FK to TrainingProgram), `department` (FK to Department), `training_site` (FK to Hospital), `academic_session` (FK to AcademicSession), `start_date`, `expected_end_date`, `current_level`, `status` (ACTIVE/SUSPENDED/COMPLETED/etc.).

---

## 6. Canonical Resident Analysis

There is no single canonical model representing all resident information; instead, identity, profile metadata, and training container metrics are fragmented.

### Data Duplication Matrix

| Data Field | `User` (Model A) | `ResidentProfile` (Model B) | `ResidentTrainingRecord` (Model C) | Risk & Overlap |
| :--- | :--- | :--- | :--- | :--- |
| **Email** | `user.email` | `profile.email` | — | Sync drift if email updated on only one model. |
| **Phone** | `user.phone_number` | `profile.phone` | — | Sync drift if phone updated on only one model. |
| **Registration Number** | `user.registration_number` | `profile.registration_no` | — | Redundant schema fields; sync mismatches. |
| **Hospital / Site** | `user.home_hospital` | `profile.hospital` | `record.training_site` | Training record represents the active site; user/profile fields may diverge. |
| **Department** | `user.home_department` | `profile.department_ref` | `record.department` | Roster queries read memberships; home fields are duplicative. |
| **Specialty** | `user.specialty` | `profile.specialty_ref` | — | Specialty is duplicated between the account and profile level. |
| **Academic Session** | — | `profile.academic_session_ref` | `record.academic_session` | Conflicting source of truth for current induction cohort. |
| **Supervisor** | `user.supervisor` (FK) | — | Linked via `ResidentSupervisorAssignment` | Direct FK on User bypasses the history and assignment status tracking in the supervision app. |

---

## 7. Training Architecture

* **Training Records**: Contained in [`ResidentTrainingRecord`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L111) which links a resident user to a [`TrainingProgram`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L18), a `Department`, and a `Hospital`.
* **Degree Programs**: Managed by `TrainingProgram` (duration, degree type).
* **Timeline**: `start_date` and `expected_end_date` are tracked on the `ResidentTrainingRecord`.
* **Specialty / Department**: Normalized relationships to `Specialty` and `Department` models from the `sims.academics` app.

---

## 8. Supervisor Architecture

* **Supervisor Profile**: Model [`SupervisorProfile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L547) links to `User` (where `role="SUPERVISOR"`) and holds registration (`pmdc_no`), department, and designation.
* **Supervision Assignments**: Tracked via [`ResidentSupervisorAssignment`](file:///home/munaim/srv/apps/pgsims/backend/sims/supervision/models.py#L7) which links `ResidentProfile` to `SupervisorProfile` with a status (`ACTIVE`, `ENDED`), an assignment type (`PRIMARY`, `CO_SUPERVISOR`), and dates.
* **Duplication**: The core `User` model maintains a direct `supervisor` ForeignKey (pointing to a supervisor user). E2E tests, CSV imports, and database seeds write to `User.supervisor`, while the supervision overview tables read from `ResidentSupervisorAssignment`.

---

## 9. Resident Document Architecture

### Document Upload Models
Postgraduate documents are structured under the synopsis and thesis submission models in [`backend/sims/training/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py):
* [`ResidentSubmission`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L1208): Represents a resident's synopsis or thesis submission container. Tracks status (`DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `RETURNED`, `VERIFIED`, `CERTIFICATE_ISSUED`).
* [`SubmissionDocument`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L1274): Uploaded files attached to a `ResidentSubmission`, mapping to a `SubmissionRequirementTemplate`.
* [`SubmissionReview`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L1323): Action history and remarks for submissions.
* [`SubmissionCertificate`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L1365): Digitally issued/verified credentials once a submission is completed.

### Onboarding / Generic Documents
* **Initial Onboarding Documents**: Documents like MBBS Degree certificates, CNIC files, or PMDC registration certificates **do not have specialized models or file fields**.
* **Model Style**: Currently, the system uses a **mix of structured models** for thesis/synopsis (`ResidentSubmission`) and dummy redirects for legacy certificates (`sims.certificates` is a disabled app).

---

## 10. Document Requirement Architecture

* **Configurable Document Requirements**: Managed via [`SubmissionRequirementTemplate`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py#L1150), which allows defining requirements for `SYNOPSIS` or `THESIS` types, configurable by `program` and `department`.
* **Onboarding Documents**: There is **no configurable model** for defining initial registration or onboarding documents (such as MBBS degree, CNIC copy, etc.).

---

## 11. Current Onboarding Flow

### 1. Account Creation (Administrative)
* Admin creates user via [`/users/new`](file:///home/munaim/srv/apps/pgsims/frontend/app/users/new/page.tsx) page $\to$ POSTs payload to [`/api/users/`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/api_user_urls.py#L15) $\to$ Calls [`create_user_with_profile`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/services.py#L266) service.
* Generates a username prefix (`pgr001`, `sup001`) and sets default password `pgfmu123` with flags `must_change_password = True` and profile status `INCOMPLETE`.

### 2. First Login
* User logs in at `/login` and receives JWT tokens.
* NextJS route guard [`ProtectedRoute.tsx`](file:///home/munaim/srv/apps/pgsims/frontend/components/auth/ProtectedRoute.tsx) calls `/api/auth/me/` to check profile completeness.
* Redirected to `/change-password` (forced password change) if `must_change_password` is True.
* Redirected to `/complete-profile` if any profile completion registry fields are missing.

### 3. Profile Completion
* Form renders fields dynamically based on missing registry requirements (driven by `/api/auth/complete-profile/` GET).
* User fills form $\to$ POSTs data $\to$ [`CompleteProfileView`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py#L639) validates and saves fields, recalculates profile status to `COMPLETE`, sets `is_profile_complete = True`.
* Next login directs user to the correct role dashboard.

---

## 12. Resident Creation & Import Pathways

Three separate pathways exist for resident account creation:

| Pathway | Frontend | Backend/API | Models Written | Current/Legacy |
| :--- | :--- | :--- | :--- | :--- |
| **Manual User Add** | `/users/new` (Role-aware) | `POST /api/users/` | `User` + `ResidentProfile` (Audit logs created, Recalculate completion) | **Current (Canonical)** |
| **Flexible Bulk Import** | `/masters` (Step 7: Residents panel) | `POST /api/bulk/import/residents/apply/` | `User` + `ResidentProfile` + `ResidentTrainingRecord` (Uses `_upsert_resident_user`) | **Current (Canonical)** |
| **Legacy Bulk Resident Upload** | None (Orphaned API) | `POST /api/bulk/import-residents/` | Only `User` (Bypasses profile creation, no training records or audits) | **Legacy (Orphaned)** |

---

## 13. API Inventory

| Method | Path | Backend Handler | Serializer / Schema | Purpose | Frontend Consumer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/auth/login/` | `CustomTokenObtainPairView` | `CustomTokenObtainPairSerializer` | Obtains JWT tokens | [`authApi.login`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/auth.ts#L108) |
| **GET** | `/api/auth/me/` | `AuthMeView` | — | Returns onboarding state & redirect route | [`authApi.me`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/auth.ts#L151) |
| **GET** | `/api/auth/complete-profile/` | `CompleteProfileView` | — | Lists missing dynamic profile fields | [`authApi.getCompleteProfileForm`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/auth.ts#L156) |
| **POST** | `/api/auth/complete-profile/` | `CompleteProfileView` | — | Saves completion data and recalculates state | [`authApi.completeProfile`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/auth.ts#L161) |
| **POST** | `/api/auth/change-password/` | `change_password_view` | — | Updates password and disables forced reset | [`authApi.changePassword`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/auth.ts#L237) |
| **POST** | `/api/users/` | `UserViewSet.create` | `UserManagementSerializer` | Universal identity creation endpoint | [`userbaseApi.users.create`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/userbase.ts#L189) |
| **POST** | `/api/bulk/import/residents/apply/` | `BulkImportEntityView` | — | Flexible CSV resident upsert | [`ImportExportPanel.tsx`](file:///home/munaim/srv/apps/pgsims/frontend/components/ui/ImportExportPanel.tsx#L103) |
| **GET** | `/api/academics/residents/me/summary/` | `MyResidentAcademicSummaryView` | — | Fetches summary training/supervision metrics | [`academicsApi.getMyResidentSummary`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/academics.ts#L331) |

---

## 14. Frontend Inventory

| Route | Component | Purpose | APIs Used | Status |
| :--- | :--- | :--- | :--- | :--- |
| `/login` | `LoginPage` | User login screen | `/api/auth/login/` | **ACTIVE / CANONICAL** |
| `/change-password` | `ChangePasswordPage` | Forced password change screen | `/api/auth/change-password/` | **ACTIVE / CANONICAL** |
| `/complete-profile` | `CompleteProfilePage` | Dynamic dynamic form for missing profile inputs | `/api/auth/complete-profile/` | **ACTIVE / CANONICAL** |
| `/users/new` | `NewUserPage` | Universal user creation page | `/api/auth/identity/options/`, `/api/users/` | **ACTIVE / CANONICAL** |
| `/users` | `UsersPage` | Master roster directory | `/api/users/` | **ACTIVE / CANONICAL** |
| `/residents` | `ResidentsPage` | Lists resident profiles | `/api/users/?role=RESIDENT` | **ACTIVE / CANONICAL** |
| `/residents/[id]` | `ResidentDetailPage` | Detail view of a resident's training summary | `/api/residents/[id]/`, `/api/academics/residents/[id]/summary/` | **ACTIVE / CANONICAL** |
| `/dashboard/resident` | `ResidentHomePage` | Main resident dashboard shell | `/api/academics/residents/me/summary/` | **ACTIVE / CANONICAL** |
| `/dashboard/resident/thesis` | `ResidentThesisRedirect` | Redirect to main resident dashboard | None (Redirect stub) | **MOCKED / STUB** |
| `/dashboard/resident/research` | `ResidentResearchRedirect` | Redirect to main resident dashboard | None (Redirect stub) | **MOCKED / STUB** |
| `/dashboard/resident/workshops` | `ResidentWorkshopsRedirect` | Redirect to main resident dashboard | None (Redirect stub) | **MOCKED / STUB** |
| `/dashboard/resident/schedule` | `ResidentScheduleRedirect` | Redirect to main resident dashboard | None (Redirect stub) | **MOCKED / STUB** |

---

## 15. Navigation Audit

Exposed menu items configured in [`navRegistry.ts`](file:///home/munaim/srv/apps/pgsims/frontend/lib/navRegistry.ts):
* **ADMIN**: Dashboard (`/dashboard/utrmc`), Users (`/users`), Residents (`/residents`), Supervisors (`/supervisors`), Support Staff (`/support-staff`), Admins (`/admins`), Masters (`/masters`), Data Quality, Backup Center, Supervision menu, Academics menu.
* **RESIDENT**: My Dashboard (`/dashboard/resident`), My Training (`/dashboard/resident`), My Supervisor (`/dashboard/resident`), My Academic Summary (`/dashboard/resident`), My Rotations (`/academics/rotation-assignments`), My Leave (`/academics/leave-requests`), My Profile (`/complete-profile`).
* **SUPERVISOR**: My Dashboard, My Residents, Supervision Ledger, Academic Review Queue, Rotation Approvals, Leave Approvals, My Profile.
* **SUPPORT_STAFF**: My Dashboard (`/dashboard`), My Profile (`/complete-profile`).

---

## 16. Backend/Frontend Exposure Gaps

| Capability | Backend Location | API | Missing Frontend |
| :--- | :--- | :--- | :--- |
| **Legacy Resident Import** | `BulkResidentImportView` | `POST /api/bulk/import-residents/` | No page uses this; the frontend uses the unified userbase engine. |
| **Legacy Trainee Import** | `BulkTraineeImportView` | `POST /api/bulk/import-trainees/` | Orphaned backend endpoint. |
| **Legacy Supervisor Import** | `BulkSupervisorImportView` | `POST /api/bulk/import-supervisors/` | Orphaned backend endpoint. |
| **Legacy Department Import** | `BulkDepartmentImportView` | `POST /api/bulk/import-departments/` | Orphaned backend endpoint. |
| **Staff Profile Viewset** | `StaffProfileViewSet` | `PATCH /api/staff/[id]/` | Roster list reads users directly; staff updates are orphaned. |
| **Synopsis/Thesis Submission** | Synopsis/Thesis submit views | `/api/submissions/synopsis/submit/`, `/api/submissions/thesis/submit/` | Residents have no buttons or forms to perform document uploads; resident pages redirect back to dashboard. |

---

## 17. Migration & Lifecycle Findings

* **`SupervisorResidentLink` Deletion**: Migration `0009_delete_supervisorresidentlink.py` deleted the old linking model, replacing it with the robust `ResidentSupervisorAssignment`.
* **Specialty Restructuring**: Migrations `0010_add_specialty_ref.py` to `0013_alter_historicaluser_specialty_alter_user_specialty.py` restructured how specialty is saved on both User and ResidentProfile, moving from text enums to foreign keys.
* **Simple History Integration**: Almost all model changes (profiles, supervision assignments, records) have corresponding historical tracking models.
* **No Post-Save User Signals**: Creating a user does not automatically spawn a profile via post-save signals; instead, profile creation must be triggered explicitly via the service layer ([`services.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/services.py)).

---

## 18. Duplicate Data Analysis

Data duplication between accounts (`User`) and profiles (`ResidentProfile`) introduces significant risk:
* **Mismatch Risk**: Changing phone number or email on the User object (via default Django profile edit) leaves the corresponding `ResidentProfile` phone/email blank or out of sync.
* **Roster Discrepancies**: Roster directories list users using `User.home_department`, but registration forms check `ResidentProfile.department_ref`. If the two are out of sync, residents appear under different departments on different pages.
* **Double Linking**: Residents link to supervisors via `User.supervisor` (which is set during user creation/import) and via `ResidentSupervisorAssignment`. If a supervisor assignment changes, the direct `User.supervisor` foreign key must be manually updated to prevent inconsistencies.

---

## 19. Legacy / Cleanup Candidates

| Item / Model | Type | Path | Overlap | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **`User.supervisor`** | Field | [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L86) | Overlaps with `ResidentSupervisorAssignment` | **DEPRECATE / MERGE** into `ResidentSupervisorAssignment` |
| **`User.home_hospital`** | Field | [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L96) | Overlaps with `ResidentProfile.hospital` | **DEPRECATE / MERGE** into `ResidentProfile.hospital` |
| **`User.home_department`** | Field | [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L105) | Overlaps with `ResidentProfile.department_ref` | **DEPRECATE / MERGE** into `ResidentProfile.department_ref` |
| **`User.registration_number`** | Field | [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L115) | Overlaps with `ResidentProfile.registration_no` | **DEPRECATE / MERGE** into `ResidentProfile.registration_no` |
| **`User.phone_number`** | Field | [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py#L122) | Overlaps with `ResidentProfile.phone` | **DEPRECATE / MERGE** into `ResidentProfile.phone` |
| **`BulkResidentImportView`** | View | [`backend/sims/bulk/views.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/bulk/views.py#L254) | Bypasses `ResidentProfile` creation | **DELETE**; use `BulkImportEntityView` |
| **`StaffProfileViewSet`** | Viewset | [`backend/sims/users/userbase_views.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py#L451) | Overlaps with `SupportStaffProfileViewSet` | **DELETE**; use `SupportStaffProfileViewSet` |

---

## 20. Current Architecture Diagrams

### A. Authentication & Profiles
```text
      [User (AbstractUser)]
        |
        +-- role = "RESIDENT" (ADMIN / SUPERVISOR / SUPPORT_STAFF)
        |
        +-- (OneToOne) ---> [ResidentProfile] (CNIC, registration_no)
        +-- (OneToOne) ---> [SupervisorProfile] (pmdc_no, designation)
        +-- (OneToOne) ---> [AdminProfile] (scope)
        +-- (OneToOne) ---> [SupportStaffProfile] (designation)
```

### B. Postgraduate Training Container
```text
           [User (role=RESIDENT)]
                    |
                    v
       [ResidentTrainingRecord] <---- (links) ---- [TrainingProgram]
                    |
                    +---- (links) ----> [Hospital (training_site)]
                    +---- (links) ----> [Department]
                    +---- (links) ----> [AcademicSession]
```

### C. Supervision Structure
```text
           [ResidentProfile] <--- (links) ---> [SupervisorProfile]
                                     |
                         [ResidentSupervisorAssignment]
                               (PRIMARY / CO)
```

### D. Document Submissions
```text
         [ResidentTrainingRecord]
                    |
                    v (OneToOne)
           [ResidentSubmission] (SYNOPSIS / THESIS)
                    |
                    +-- (ForeignKey) ---> [SubmissionDocument] (Uploaded File)
                    |
                    +-- (ForeignKey) ---> [SubmissionRequirementTemplate] (Scope)
```

---

## 21. Desired Workflow Compatibility

The target onboarding workflow is highly compatible with the core models, but requires several additions:
1. **Generic Onboarding Documents**: Since there is no model for general uploads (MBBS degree, CNIC file), a generic document model or extending the `SubmissionDocument` to support an `ONBOARDING` category is needed.
2. **File Uploads on Complete Profile Form**: The dynamic form on `/complete-profile` must be extended to support file uploads and coordinate multipart requests.
3. **Dashboard Subpage Wiring**: The mocked redirect stubs under `/dashboard/resident/*` must be replaced with pages integrating with `/api/submissions/synopsis/` and `/api/submissions/thesis/` endpoints.

---

## 22. Gap Matrix

| Target Capability | Existing | Partial | Missing | Existing Implementation |
| :--- | :---: | :---: | :---: | :--- |
| **Admin creates account** | Yes | — | — | [`/users/new`](file:///home/munaim/srv/apps/pgsims/frontend/app/users/new/page.tsx) and `/api/users/` viewset. |
| **Temporary password** | Yes | — | — | Defaults to `pgfmu123` via `create_user_with_profile` service. |
| **First-login detection** | Yes | — | — | `must_change_password` checked on user model. |
| **Forced password change** | Yes | — | — | NextJS route redirects to `/change-password` path. |
| **Resident profile** | Yes | — | — | `ResidentProfile` model exists. |
| **Mandatory fields** | Yes | — | — | Defined in backend `PROFILE_COMPLETION_REQUIREMENTS` registry. |
| **Institution-controlled training** | Yes | — | — | Managed via `ResidentTrainingRecord` model. |
| **Resident document center** | — | — | Yes | Frontend UI is completely missing. |
| **Document types** | Yes | — | — | Defined in `SubmissionRequirementTemplate` choices (Synopsis, Thesis). |
| **Configurable requirements** | Yes | — | — | Scoped via `SubmissionRequirementTemplate` model. |
| **Required-now documents** | — | — | Yes | Missing generic onboarding document model. |
| **Required-later documents** | Yes | — | — | Handled by synopsis/thesis submission requirements. |
| **Optional documents** | Yes | — | — | Supported in `SubmissionRequirementTemplate` (`is_required=False`). |
| **Verification workflow** | Yes | — | — | Implemented on the backend via `SubmissionReview`. |
| **Onboarding completion** | Yes | — | — | User.is_profile_complete recalculations during save. |

---

## 23. Architecture Decision Answers

* **Q1: Canonical auth model?**
  * `sims.users.models.User` (AbstractUser subclass).
* **Q2: Canonical resident/profile model?**
  * `sims.users.models.ResidentProfile` linked to `User`.
* **Q3: Canonical training model?**
  * `sims.training.models.ResidentTrainingRecord`.
* **Q4: Canonical resident-supervisor relationship?**
  * `sims.supervision.models.ResidentSupervisorAssignment` (linking the resident profile to the supervisor profile).
* **Q5: Canonical document architecture?**
  * `ResidentSubmission` as the container, and `SubmissionDocument` as the file attachment mapping to `SubmissionRequirementTemplate`.
* **Q6: Is a new generic `ResidentDocument` model necessary?**
  * Yes, to support initial onboarding uploads (e.g. CNIC file, MBBS Degree) which are currently missing.
* **Q7: Does a configurable `DocumentRequirement` model exist?**
  * Yes: `SubmissionRequirementTemplate` (covers Synopsis/Thesis requirements).
* **Q8: What field represents onboarding completion?**
  * `User.is_profile_complete`.
* **Q9: Which first-login mechanisms can be reused?**
  * `User.must_change_password` and `/api/auth/me/`'s return of `allowed_next_route`.
* **Q10: Which resident creation mechanism should become canonical?**
  * Universal user creation service `create_user_with_profile` and userbase flexible bulk imports.
* **Q11: Which pathways overlap?**
  * Legacy `BulkResidentImportView` (`POST /api/bulk/import-residents/`) which bypasses profiles.
* **Q12: Which frontend pages remain canonical?**
  * `/users/new`, `/complete-profile`, `/change-password`, and `/residents/[id]`.
* **Q13: Which pages are cleanup candidates?**
  * The stub redirect pages under `/dashboard/resident/` (e.g. `thesis/page.tsx`, `research/page.tsx`) must be replaced with actual document upload/listing interfaces.
* **Q14: Which backend models are cleanup candidates?**
  * Legacy/orphaned bulk upload view functions and serializers.
* **Q15: Which APIs exist without frontend exposure?**
  * `/api/bulk/import-residents/`, `/api/bulk/import-supervisors/`, `/api/bulk/import-trainees/`, `/api/staff/`.
* **Q16: Which frontend features use legacy APIs/models?**
  * None actively, but E2E tests have leftover references to legacy HOD terminology.
* **Q17: Biggest risks?**
  * Field mismatch due to duplication (e.g. modifying a resident's email on User but not updating profile/training records) and orphaned resident users created without profiles.

---

## 24. Recommended Direction

### **OPTION B — REUSE + SMALL EXTENSION**

**Rationale**:
The database schema and service layers already implement universal user creation (`create_user_with_profile`), dynamic onboarding field checks (`PROFILE_COMPLETION_REQUIREMENTS`), and dynamic front-end completion rendering (`/complete-profile`).
The only extensions required are:
1. Adding a generic `ResidentDocument` model to store initial onboarding file uploads (CNIC, MBBS certificate) linked to the resident.
2. Extending `/api/auth/complete-profile/` POST to accept multipart/form-data for document attachments.
3. Replacing the NextJS resident dashboard redirect stubs with active upload widgets calling the backend submission APIs.

---

## 25. Files Most Relevant to the Next Implementation Session

### Backend
1. [`backend/sims/users/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/models.py): Inspect `User` and `ResidentProfile`.
2. [`backend/sims/users/services.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/services.py): Dynamic requirements registry and user creation service.
3. [`backend/sims/users/userbase_views.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py): Profile completion views and me views.
4. [`backend/sims/training/models.py`](file:///home/munaim/srv/apps/pgsims/backend/sims/training/models.py): Resident training records and submission/document upload paths.

### Frontend
1. [`frontend/components/auth/ProtectedRoute.tsx`](file:///home/munaim/srv/apps/pgsims/frontend/components/auth/ProtectedRoute.tsx): NextJS route guarding logic.
2. [`frontend/app/complete-profile/page.tsx`](file:///home/munaim/srv/apps/pgsims/frontend/app/complete-profile/page.tsx): Profile completion dynamic input fields.
3. [`frontend/lib/api/auth.ts`](file:///home/munaim/srv/apps/pgsims/frontend/lib/api/auth.ts): Authentication API clients.
4. [`frontend/app/dashboard/resident/page.tsx`](file:///home/munaim/srv/apps/pgsims/frontend/app/dashboard/resident/page.tsx): Resident dashboard shell.
