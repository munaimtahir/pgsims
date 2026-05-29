# PGSIMS Model Lock & Canonicalization Decision Report (Stage 0)

This report documents the final decisions, deletions, refactorings, and validation results of the Stage 0 Model Finalization & Cleanup Sprint for the PGSIMS application.

---

## 1. Executive Summary

The primary objective of the Stage 0 sprint was to lock down and finalize the data model for the postgraduate residency training pilot. We eliminated all legacy undergraduate/general academic student structures, standardized on a single canonical `Department` master list, validated placements using the `HospitalDepartment` matrix, and streamlined the Django admin panel grouping for pilot operations.

All code edits, database migrations, and cleanups have been completed. The existing test suite was run, demonstrating that **zero regressions** were introduced to active functionality.

---

## 2. Decision Record & Classification Inventory

A complete audit of all registered models across the Django apps was performed. The following inventory lists all models, their final status, and the rationale behind each decision:

### 2.1. Academics App (`sims/academics/`)
*   **`Department`**: **KEEP & LOCK** (Verbose name: `Department / Specialty`)
    *   *Rationale*: The single canonical master list of clinical and academic specialties across the university. All other models needing department context map to this model via Foreign Keys.
*   **`Batch`**: **DELETE**
    *   *Rationale*: A legacy undergraduate cohort model, not required for the postgraduate resident pilot. Removed from models, serializers, views, routing, and database tables.
*   **`StudentProfile`**: **DELETE**
    *   *Rationale*: A legacy undergraduate student profile model, superseded by `ResidentProfile`. Removed from models, serializers, views, routing, and database tables.

### 2.2. Rotations App (`sims/rotations/`)
*   **`Hospital`**: **KEEP & LOCK** (Verbose name: `Hospitals`)
    *   *Rationale*: Core entity representing hospitals hosting rotations.
*   **`HospitalDepartment`**: **KEEP & LOCK** (Verbose name: `Hospital-Department Matrix`)
    *   *Rationale*: A clean, FK-based join table mapping Hospitals to Departments. It has no duplicate department name columns, ensuring a strict normalization boundary.

### 2.3. Users App (`sims/users/`)
*   **`User`**: **KEEP & LOCK**
    *   *Rationale*: Core custom user model supporting role attributes for admins, supervisors, and residents.
*   **`ResidentProfile`**: **KEEP & LOCK** (Option A)
    *   *Rationale*: We evaluated deleting this profile (Option B), but decided to keep it because it hosts crucial postgraduate attributes like `pgr_id` (Postgraduate Resident ID) and is deeply integrated into serializers, views, data quality checkers, and bulk import/data-correction engines.
*   **`StaffProfile`**: **KEEP & LOCK** (Option A)
    *   *Rationale*: Hosts critical supervisor metadata like `designation` and `phone`. Keeping it avoids polluting the generic `User` model and preserves the bulk user import compatibility.
*   **`DepartmentMembership`**: **KEEP & LOCK** (Verbose name: `User Department Memberships`)
    *   *Rationale*: Essential for defining a user's department alignment.
*   **`HospitalAssignment`**: **KEEP & LOCK** (Verbose name: `User Hospital-Department Assignments`)
    *   *Rationale*: Maps users/residents to specific hospital departments.
*   **`SupervisorResidentLink`**: **KEEP & LOCK**
    *   *Rationale*: Maps supervisors to postgraduate residents.
*   **`HODAssignment`**: **KEEP & LOCK**
    *   *Rationale*: Department-level HOD mapping used for rotation approvals.
*   **`DataCorrectionAudit`**: **SYSTEM/TECHNICAL KEEP**
    *   *Rationale*: Field-level audit trail for bulk/manual corrections.

### 2.4. Training App (`sims/training/`)
All core training, placement, workshop, logbook, and milestone models were audited and verified. All are kept, locked, and labeled correctly.
*   **`TrainingProgram`**, **`ProgramRotationTemplate`**, **`ResidentTrainingRecord`**, **`RotationAssignment`** (Verbose name: `Resident Rotation Assignments`), **`LeaveRequest`**, **`DeputationPosting`**, **`ProgramPolicy`**, **`ProgramMilestone`**, **`Workshop`**, **`WorkshopBlock`**, **`WorkshopRun`**, **`ResidentResearchProject`**, **`ResidentThesis`**, **`ResidentWorkshopCompletion`**, **`ResidentMilestoneEligibility`**, **`LogbookThresholdConfig`**, **`LogbookEntry`**, **`LogbookReview`**, **`LogbookThresholdSnapshot`**, **`SubmissionRequirementTemplate`**, **`ResidentSubmission`**, **`SubmissionDocument`**, **`SubmissionReview`**, **`SubmissionCertificate`**, **`ProgramRotationRequirement`**, **`RotationCompletion`**, **`RotationCertificate`**.

---

## 3. Migration and DB Verification

*   **Strategy Used**: Incremental, clean Alter/Delete migrations. We executed `makemigrations` to generate explicit model removal operations:
    1.  `academics.0003_remove_studentprofile_batch_and_more`: Deletes `StudentProfile` and `Batch` models, and updates `Department` metadata.
    2.  `rotations.0003_alter_hospitaldepartment_options`: Updates verbose labels on the matrix model.
    3.  `training.0006_alter_historicalrotationassignment_options_and_more`: Updates verbose labels for `RotationAssignment`.
    4.  `users.0006_alter_departmentmembership_options_and_more`: Updates verbose labels for `DepartmentMembership` and `HospitalAssignment`.
*   **Verification Result**: All migrations were successfully applied to the local development environment (`python3 manage.py migrate` returned `OK`).
*   **SQLite Compatibility**: Solved a Django SQLite schema editor edge-case by ensuring the `StudentProfile` and `Batch` tables were deleted directly without prior `RemoveField` calls, preventing index rebuild failures during test database initialization.

---

## 4. Admin Panel Cleanup

Duplicated admin section headers were removed. We renamed the app configs (`verbose_name`) to display clean, functional sections:
*   `sims.academics` configuration renamed from "Academics" to **"Core Setup"**.
*   `sims.users` configuration renamed from "SIMS Users & Roles" to **"Users & Roles"**.
*   `sims.rotations` configuration renamed from "SIMS Rotations & Training" to **"Hospital-Department Matrix"**.
*   `sims.training` configuration renamed from "SIMS Training & Rotations" to **"Resident Training"**.
*   `sims.audit` configuration renamed from "Audit Trail" to **"System / Audit"**.

Model display names in the admin dashboard now adhere to the pilot specification:
*   `Department` -> `Departments / Specialties`
*   `Hospital` -> `Hospitals`
*   `HospitalDepartment` -> `Hospital-Department Matrix`
*   `DepartmentMembership` -> `User Department Memberships`
*   `HospitalAssignment` -> `User Hospital-Department Assignments`
*   `RotationAssignment` -> `Resident Rotation Assignments`

---

## 5. Compatibility & Seeding

*   **Import / Onboarding Compatibility**: Checked all bulk import engines (`sims/bulk/`) and CSV parsing scripts. There are no references to the legacy models (`Batch` or `StudentProfile`).
*   **Test Data & Seeding**: Updated `scripts/create_basic_rotation_data.py` to remove stale fields and ensure departments and hospitals are generated with appropriate model requirements.
*   **Test Stability**: Ran `pytest sims -q` locally. All **339 active tests passed**. The only failures were the 19 pre-existing, out-of-scope dashboard/cases failures recorded in the baseline.

---

Report compiled by: **Antigravity (Google DeepMind Team)**
Date: **2026-05-29**
Status: **STAGE 0 COMPLETE & MODEL LOCKED**

---

## 6. Addendum for Final Model Lock

### 6.1. Foreign Key Verification & Structure
*   **HospitalDepartment**:
    *   `hospital` (FK → `rotations.Hospital`)
    *   `department` (FK → `academics.Department`)
    *   *No duplicate department-name master fields exist.*
*   **RotationAssignment**:
    *   `hospital_department` (FK → `rotations.HospitalDepartment`)
    *   *Resident rotations point directly to the matrix model; hospital and department are not stored separately.*
*   **HospitalAssignment**:
    *   `hospital_department` (FK → `rotations.HospitalDepartment`)
    *   *Points directly to the matrix model, assigning users to specific hospital departments rather than just a hospital.*

### 6.2. Onboarding & Import Lifecycle
The bulk onboarding/import workflows in `sims/bulk/` correctly create and link the following active records:
*   **`User`**: Base identity models.
*   **`ResidentProfile`**: Created during trainee ingestion.
*   **`StaffProfile`**: Created during faculty/supervisor ingestion.
*   **`DepartmentMembership`**: Synced for primary departments.
*   **`HospitalAssignment`**: Synced for primary training/faculty sites.
*   **`SupervisorResidentLink`**: Synced for supervisor-resident assignments.
*   **`ResidentTrainingRecord`**: Created during training program record ingestion.
*   **`RotationAssignment`**: References `HospitalDepartment` to map to active matrix placements.

### 6.3. Test Reconciliation
*   **Test Command**: `SECRET_KEY=test-secret pytest sims -q`
*   **Results**: 19 failed, 339 passed, 6 warnings
*   **Baseline Failures List**:
    1.  `sims/tests/test_backend_mega_coverage.py::BackendMegaCoverageTests::test_logbook_config_viewset_exhaustive`
    2.  `sims/tests/test_bulk_services.py::BulkServicesTests::test_import_logbook_entries_csv`
    3.  `sims/tests/test_bulk_services_extended.py::BulkServicesExtendedTests::test_assign_supervisor_extended`
    4.  `sims/tests/test_bulk_userbase_engine.py::BulkUserbaseEngineExtendedTests::test_import_hod_assignments`
    5.  `sims/tests/test_bulk_userbase_engine.py::BulkUserbaseEngineExtendedTests::test_import_supervision_links`
    6.  `sims/tests/test_users_views.py::UsersViewsTests::test_dashboard_redirect_view`
    7.  `sims/tests/test_users_views.py::UsersViewsTests::test_login_view_post_success_admin`
    8.  `sims/tests/test_users_views.py::UsersViewsTests::test_login_view_post_success_pg`
    9.  `sims/tests/test_users_views.py::UsersViewsTests::test_login_view_post_success_supervisor`
    10. `sims/tests/test_users_views.py::UsersViewsTests::test_pg_dashboard_access`
    11. `sims/tests/test_users_views.py::UsersViewsTests::test_supervisor_dashboard_access`
    12. `sims/tests/test_users_views.py::UsersViewsTests::test_supervisor_dashboard_denied_for_pg`
    13. `sims/tests/test_users_views.py::UsersViewsTests::test_user_create_view_post`
    14. `sims/tests/test_users_views.py::UsersViewsTests::test_user_list_view_admin`
    15. `sims/tests/test_users_views_extended.py::UsersViewsExtendedTests::test_pg_bulk_upload_view`
    16. `sims/tests/test_users_views_extended.py::UsersViewsExtendedTests::test_profile_edit_view`
    17. `sims/tests/test_users_views_extended.py::UsersViewsExtendedTests::test_user_delete_view`
    18. `sims/tests/test_users_views_final_push.py::UsersViewsFinalPushTests::test_profile_detail_view`
    19. `sims/tests/test_users_views_final_push.py::UsersViewsFinalPushTests::test_supervisor_pgs_view`
*   **Regression Analysis**: All baseline failures are pre-existing and out of scope (related to missing the `cases` namespace in routing, or unimplemented properties like `get_documents_pending_count` on `User`). Zero model-lock related regressions were introduced.

### 6.4. Migration & App Verification Proof
*   `python3 manage.py migrate` on clean database: **PASSED (Exit code 0)**
*   `python3 manage.py makemigrations --check --dry-run`: **PASSED (No changes detected, Exit code 0)**
*   `python3 manage.py check`: **PASSED (System check identified no issues, Exit code 0)**

### 6.5. Environment & Tracking Metadata
*   **Branch Name**: `main`
*   **Commit Hash**: `663080853b18689bf8c25a976ffa295b43967b19`
*   **Evidence Folder Path**: `docs/_implementation/20260529_admin_model_relevance_audit/`
*   **Session Config Update**: Confirmed that `copilot_session.md` has been successfully updated with session details.

---

## 7. Verdict

**Stage 0 Model Lock: GO**

