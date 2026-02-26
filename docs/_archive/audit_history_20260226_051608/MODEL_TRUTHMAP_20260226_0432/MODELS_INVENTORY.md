# Models Inventory

This is a comprehensive inventory of all Django models defined under `backend/sims/**/models.py` relevant to the review domain.

### `sims/users/models.py`
- **User** (extends `AbstractUser`) [line 46]
  - Fields: `role`, `specialty`, `year`, `registration_number`, `phone_number`, `last_login_ip`, `is_archived`, `archived_date`
  - Relations: `supervisor` (FK `self`), `created_by` (FK `self`), `modified_by` (FK `self`)
  - Indexes: `role`, `specialty`, `supervisor`, `is_active`

### `sims/academics/models.py`
- **Department** [line 16]
  - Fields: `name`, `code`, `description`, `active`
  - Relations: `head` (FK `sims.users.User`)
  - Indexes: `code`, `active`
- **Batch** [line 48]
  - Fields: `name`, `program`, `start_date`, `end_date`, `capacity`, `active`
  - Relations: `department` (FK `Department`), `coordinator` (FK `sims.users.User`)
  - Unique/Indexes: unique_together `[name, department, start_date]`
- **StudentProfile** [line 116]
  - Fields: `roll_number`, `admission_date`, `expected_graduation_date`, `actual_graduation_date`, `status`, `status_updated_at`, `cgpa`, etc.
  - Relations: `user` (OneToOne `sims.users.User`), `batch` (FK `Batch`)
  - Indexes: `roll_number`, `status`, `batch`, `admission_date`

### `sims/rotations/models.py`
- **Hospital** [line 18]
  - Fields: `name`, `code`, `address`, `phone`, `email`, `website`, `description`, `facilities`, `is_active`
  - Indexes: `name`, `is_active`
- **Department** [line 83]
  - Fields: `name`, `head_of_department`, `contact_email`, `contact_phone`, `description`, `training_objectives`, `required_skills`, `is_active`
  - Relations: `hospital` (FK `Hospital`)
  - Unique/Indexes: unique_together `[hospital, name]`
- **Rotation** [line 157]
  - Fields: `start_date`, `end_date`, `status`, `objectives`, `learning_outcomes`, `requirements`, `completion_certificate`, `feedback`, `notes`
  - Relations: `pg` (FK `sims.users.User`), `department` (FK `Department`), `hospital` (FK `Hospital`), `supervisor` (FK `sims.users.User`), `created_by` (FK `sims.users.User`), `approved_by` (FK `sims.users.User`)
  - Constraints/Indexes: custom constraint `rotation_end_after_start`. Indexes on pg, status, supervisor, start/end date.
- **RotationEvaluation** [line 462]
  - Relations: `rotation` (FK `Rotation`), `evaluator` (FK `sims.users.User`)
  - Fields: `evaluation_type`, `score`, `comments`, `recommendations`, `status`
  - Unique: unique_together `[rotation, evaluator, evaluation_type]`

### `sims/logbook/models.py`
- **Procedure**, **Diagnosis**, **Skill**, **LogbookTemplate** [lines 29-401]
  - Core domain dictionaries for logging activities.
- **LogbookEntry** [line 403]
  - Fields: `case_title`, `date`, `location_of_activity`, `patient_history_summary`, `management_action`, `patient_age`, `patient_gender`, `status`, etc.
  - Relations: `pg` (FK User), `rotation` (FK `sims.rotations.Rotation`), `supervisor` (FK User), `template` (FK LogbookTemplate), `primary_diagnosis` (FK Diagnosis), `secondary_diagnoses` (M2M Diagnosis), `procedures` (M2M Procedure), `skills` (M2M Skill).

### `sims/cases/models.py`
- **ClinicalCase** [line 65], **CaseReview** [line 451], **CaseStatistics** [line 593]
  - Focuses on clinical reports. `ClinicalCase` links to `Rotation` and `sims.users.User`.

### `sims/attendance/models.py`
- **Session**, **AttendanceRecord**, **EligibilitySummary** [lines 12-241]
  - `Session` conditionally links to `rotations.Rotation` [line 45].
  - `EligibilitySummary` logs % attendance and rules.

### Others
- **sims/audit/models.py**: `ActivityLog`, `AuditReport`
- **sims/bulk/models.py**: `BulkOperation`
- **sims/certificates/models.py**: `Certificate`, `CertificateType`, `CertificateReview`, `CertificateStatistics`
- **sims/notifications/models.py**: `Notification`, `NotificationPreference`
- **sims/reports/models.py**: `ReportTemplate`, `ScheduledReport`
- **sims/results/models.py**: `Exam`, `Score`
- **sims/search/models.py**: `SearchQueryLog`, `SavedSearchSuggestion`
