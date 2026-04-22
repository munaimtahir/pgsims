# Canonical Data Model (Locked, Simplified Names)

## Canonical entities

### Department (single canonical list)
- One university-wide list: Department A/B/C/D...
- Unique key: `code` (preferred) or normalized `name`.
- This is the ONLY Department model.
- Canonical table: `academics.Department`.

### Hospital (university sites)
- Multiple hospitals exist under the same university.
- Unique key: `code`.
- Canonical table stays as the existing `rotations.Hospital` model (class name: `Hospital`).

### HospitalDepartment (matrix)
- Represents which departments are hosted in which hospitals.
- (hospital, department) unique.

## Trainee home affiliation (stable until graduation)
For `User` with role=pg:
- `home_department` (FK Department)
- `home_hospital` (FK Hospital)

Home affiliation does not change during rotations.

## Rotation (posting)
A rotation is a time-bounded placement in a (Hospital, Department) pair.

Fields (simple names):
- `pg`
- `department` (FK Department)          # destination department
- `hospital` (FK Hospital)              # destination hospital
- Optional snapshots (audit isolation):
  - `source_department` (FK Department)
  - `source_hospital` (FK Hospital)
- `start_date`, `end_date`
- `status` (planned/ongoing/completed/cancelled/pending_approval)
- `approved_by`, `approved_at`

### Inter-hospital policy rule
If `hospital != home_hospital`:
- Allowed if the destination department is NOT available in the home hospital (missing HospitalDepartment row), OR
- Requires:
  - `override_reason`
  - approval by `utrmc_admin`

If `department == home_department` AND `hospital != home_hospital`:
- Always requires override_reason + `utrmc_admin` approval (rare exception).

## Feature Layer Runtime Entities

### Logbook Domain
- `training.LogbookEntry`
  - Resident-owned open-form clinical entry
  - Statuses: `DRAFT -> SUBMITTED -> RETURNED -> APPROVED`
  - Supports `rotation_assignment` link for per-rotation threshold checks
- `training.LogbookReview`
  - Reviewer action history (`RETURNED`, `APPROVED`) with comments
- `training.LogbookThresholdConfig`
  - Configurable threshold mode: `PER_ROTATION` or `PER_PERIOD`
  - Scoped by optional `program` and `department`
- `training.LogbookThresholdSnapshot`
  - Computed progress snapshots used by resident/supervisor/UTRMC readiness views

### Synopsis/Thesis Completeness Domain
- `training.SubmissionRequirementTemplate`
  - Admin/HOD/UTRMC-managed required-document checklist
  - Scoped by `submission_type` + optional `program`/`department`
- `training.ResidentSubmission`
  - Resident workflow entity for `SYNOPSIS` and `THESIS`
  - Statuses: `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `RETURNED`, `VERIFIED`, `CERTIFICATE_ISSUED`
- `training.SubmissionDocument`
  - Uploaded resident files, optionally linked to checklist item
- `training.SubmissionReview`
  - Explicit review history rows for each state transition
- `training.SubmissionCertificate`
  - One certificate per verified submission, with issue/verify metadata

### Rotation Phase-1 Structured Domain
- `training.ProgramRotationRequirement`
  - Program-level required rotation department map with duration + sequence
- `training.RotationCompletion`
  - One completion record per `RotationAssignment`
  - Statuses: `CONFIRMED_BY_DEPARTMENT`, `PENDING_UTRMC_VERIFICATION`, `VERIFIED`
- `training.RotationCertificate`
  - One certificate per verified completion with issuance traceability

### Readiness Hooks
- Eligibility/readiness now includes verifiable hooks for:
  - logbook threshold progress,
  - synopsis certificate issuance,
  - thesis certificate issuance,
  - rotation completion verification counts.
