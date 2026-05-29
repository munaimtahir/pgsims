# PGSIMS Admin Model Relevance Report
**Date**: 2026-05-29
**Auditor**: Antigravity (AI Agent)

## 1. Executive Summary
During the controlled pilot deployment phase, the PGSIMS system restricts its scope to a postgraduate resident-focused training workflow. This audit was conducted on the Django admin panel and the underlying database schema to classify registered models as active or legacy. The goal is to clean up the admin interface, remove clutter from legacy undergraduate structures, and ensure strict alignment with the postgraduate terminology (favoring "Resident" over "Student").

To maintain database schema stability and avoid migration complications, **no database tables or migrations are deleted**. Legacy models are simply hidden from the Django admin interface.

---

## 2. Model Classification & Inventory
The table below details all models defined in the active Django apps (`sims.users`, `sims.academics`, `sims.rotations`, `sims.audit`, `sims.bulk`, `sims.notifications`, `sims.training`), their table names, database row counts (queried from the live PostgreSQL docker runtime container), status classification, and cleanup decisions.

| Django App | Model Name | Database Table | Row Count (PG) | Classification | Admin Status / Decision | Notes & Dependencies |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **academics** | `Department` | `academics_department` | 20 | Active Core | Keep / Visible | Represents the canonical Department entity. Referenced by users and training records. |
| **academics** | `Batch` | `academics_batch` | 0 | Legacy | **Hide from Admin** | Leftover undergraduate student cohort grouping. |
| **academics** | `StudentProfile` | `academics_studentprofile` | 0 | Legacy | **Hide from Admin** | Leftover undergraduate student metadata. |
| **users** | `User` | `users_user` | 17 | Active Core | Keep / Visible | Main custom user model supporting role-based access. |
| **users** | `StaffProfile` | `users_staffprofile` | 0 | Active Extension | Keep / Visible | Profile details for faculty and supervisors; used by userbase engine. |
| **users** | `ResidentProfile` | `users_residentprofile` | 0 | Active Extension | Keep / Visible | Profile details for residents/postgraduates; used by userbase engine. |
| **users** | `DepartmentMembership` | `users_departmentmembership` | 5 | Active Core | Keep / Visible | Maps users (faculty/residents/supervisors) to Departments. |
| **users** | `HospitalAssignment` | `users_hospitalassignment` | 0 | Active Core | Keep / Visible | Maps users to Hospital Departments. |
| **users** | `SupervisorResidentLink` | `users_supervisorresidentlink` | 4 | Active Core | Keep / Visible | Maps residents to supervisors for training oversight. |
| **users** | `HODAssignment` | `users_hodassignment` | 1 | Active Core | Keep / Visible | Maps department heads to departments. |
| **users** | `DataCorrectionAudit` | `users_datacorrectionaudit` | 0 | Active Extension | Keep / Visible | Auditing flags for user profile data corrections. |
| **rotations** | `Hospital` | `rotations_hospital` | 4 | Active Core | Keep / Visible | Canonical Hospital entity representing training sites. |
| **rotations** | `HospitalDepartment` | `rotations_hospitaldepartment` | 50 | Active Core | Keep / Visible | Junction table linking Hospitals to hosted Departments. |
| **audit** | `ActivityLog` | `audit_activitylog` | 491 | Active Core | Keep / Visible (API) | Logs user actions. Note: Managed via APIs/Separate views, not registered in admin. |
| **audit** | `AuditReport` | `audit_auditreport` | 0 | Active Core | Keep / Visible (API) | Holds generated audit reports. Not registered in admin. |
| **bulk** | `BulkOperation` | `bulk_bulkoperation` | 2 | Active Core | Keep / Visible (API) | Logs bulk Excel/CSV operations. Not registered in admin. |
| **notifications**| `Notification` | `notifications_notification` | 0 | Active Core | Keep / Visible (API) | Internal app notifications. Not registered in admin. |
| **notifications**| `NotificationPreference` | `notifications_notificationpreference` | 0 | Active Core | Keep / Visible (API) | User notification settings. Not registered in admin. |
| **training** | `TrainingProgram` | `training_trainingprogram` | 3 | Active Core | Keep / Visible | Core postgraduate program metadata. |
| **training** | `ProgramRotationTemplate` | `training_programrotationtemplate` | 0 | Active Core | Keep / Visible | Template configuration for program rotations. |
| **training** | `ResidentTrainingRecord` | `training_residenttrainingrecord` | 7 | Active Core | Keep / Visible | Core resident registration in training program. |
| **training** | `RotationAssignment` | `training_rotationassignment` | 0 | Active Core | Keep / Visible | Roster assignment for resident rotations. |
| **training** | `LeaveRequest` | `training_leaverequest` | 0 | Active Core | Keep / Visible | Leave requests submitted by residents. |
| **training** | `DeputationPosting` | `training_deputationposting` | 0 | Active Core | Keep / Visible | External/deputation posting for residents. |
| **training** | `ProgramPolicy` | `training_programpolicy` | 0 | Active Core | Keep / Visible | Policies associated with programs. |
| **training** | `ProgramMilestone` | `training_programmilestone` | 2 | Active Core | Keep / Visible | Milestones (e.g. IMM, Intermediate, Final) for training. |
| **training** | `ProgramMilestoneResearchRequirement` | `training_programmilestoneresearchrequirement` | 2 | Active Core | Keep / Visible | Research requirements for milestones. |
| **training** | `ProgramMilestoneWorkshopRequirement` | `training_programmilestoneworkshoprequirement` | 0 | Active Core | Keep / Visible | Workshop requirements for milestones. |
| **training** | `ProgramMilestoneLogbookRequirement` | `training_programmilestonelogbookrequirement` | 0 | Active Core | Keep / Visible | Logbook entry count requirements for milestones. |
| **training** | `Workshop` | `training_workshop` | 0 | Active Core | Keep / Visible | Available workshops. |
| **training** | `WorkshopBlock` | `training_workshopblock` | 0 | Active Core | Keep / Visible | Calendar blocks for workshops. |
| **training** | `WorkshopRun` | `training_workshoprun` | 0 | Active Core | Keep / Visible | Instances of workshop executions. |
| **training** | `ResidentResearchProject` | `training_residentresearchproject` | 1 | Active Core | Keep / Visible | Resident research project tracking. |
| **training** | `ResidentThesis` | `training_residentthesis` | 0 | Active Core | Keep / Visible | Resident thesis tracking. |
| **training** | `ResidentWorkshopCompletion`| `training_residentworkshopcompletion` | 0 | Active Core | Keep / Visible | Workshop completion records for residents. |
| **training** | `ResidentMilestoneEligibility`| `training_residentmilestoneeligibility` | 6 | Active Core | Keep / Visible | Eligibility checklists for milestone attempts. |
| **training** | `LogbookThresholdConfig`| `training_logbookthresholdconfig` | 2 | Active Core | Keep / Visible | Logbook compliance configuration. |
| **training** | `LogbookEntry` | `training_logbookentry` | 0 | Active Core | Keep / Visible | Patient procedure entries. |
| **training** | `LogbookReview` | `training_logbookreview` | 0 | Active Core | Keep / Visible | Supervisor sign-offs on logbook entries. |
| **training** | `LogbookThresholdSnapshot`| `training_logbookthresholdsnapshot` | 2 | Active Core | Keep / Visible | Snapshot of compliance records. |
| **training** | `SubmissionRequirementTemplate`| `training_submissionrequirementtemplate` | 4 | Active Core | Keep / Visible | Checklists for document submissions. |
| **training** | `ResidentSubmission` | `training_residentsubmission` | 0 | Active Core | Keep / Visible | Portals for resident document uploads. |
| **training** | `SubmissionDocument` | `training_submissiondocument` | 0 | Active Core | Keep / Visible | Actual uploaded files. |
| **training** | `SubmissionReview` | `training_submissionreview` | 0 | Active Core | Keep / Visible | Supervisor audits of uploaded files. |
| **training** | `SubmissionCertificate`| `training_submissioncertificate` | 0 | Active Core | Keep / Visible | Generated certificates. |
| **training** | `ProgramRotationRequirement`| `training_programrotationrequirement` | 1 | Active Core | Keep / Visible | Rotation-specific requirements. |
| **training** | `RotationCompletion` | `training_rotationcompletion` | 0 | Active Core | Keep / Visible | End-of-rotation completion validation. |
| **training** | `RotationCertificate` | `training_rotationcertificate` | 0 | Active Core | Keep / Visible | Rotation completion certificates. |

---

## 3. Findings & Decisions

### 3.1. Hiding Legacy Academics Models
- **`academics.Batch`** (0 rows) and **`academics.StudentProfile`** (0 rows) are remnants of an undergraduate system structure. They are completely unused by active postgraduate training workflows or APIs in the frontend.
- **Decision**: Remove their registrations from `sims/academics/admin.py` to hide them from the Admin portal.
- **Data Integrity**: Their database tables and existing schema are left intact to ensure no breaking changes in legacy dependencies or database consistency.

### 3.2. Preserving User Profiles
- **`users.StaffProfile`** (0 rows) and **`users.ResidentProfile`** (0 rows) represent the active profiles for supervisors/faculty and residents respectively. They are linked to the custom User model and used in the bulk user base import engine, serializers, and views.
- **Decision**: Keep them registered in the admin panel as they are active extensions of the postgraduate core model.

### 3.3. Terminology & UI Review
- Alignment check: Ensure that labels, badges, and headers in custom admin views and standard models use "Resident" or "Postgraduate (PG)" instead of general "Student" where appropriate.
- Note: Under custom user admin creation and change forms, user roles are listed as "Postgraduate" (`pg`) and "Resident" (`resident`), aligning perfectly with the pilot specifications.

---

## 4. Validation
All tests will be run following changes to verify that hiding the models from Django admin does not cause regressions or contract violations.
