# Model Audit

## Verified Apps and Models

The cleanup command was built from the actual Django models in the repository, not guessed names.

### Hospitals and Departments

- `backend/sims/rotations/models.py`
  - `Hospital`
  - `HospitalDepartment`
- `backend/sims/academics/models.py`
  - `Department`

### Users and Staffing

- `backend/sims/users/models.py`
  - `User`
  - `StaffProfile`
  - `ResidentProfile`
  - `DepartmentMembership`
  - `HospitalAssignment`
  - `SupervisorResidentLink`
  - `HODAssignment`
  - `DataCorrectionAudit`

### Training and Operational Records

- `backend/sims/training/models.py`
  - `TrainingProgram`
  - `ProgramPolicy`
  - `ProgramMilestone`
  - `ProgramMilestoneResearchRequirement`
  - `ProgramMilestoneWorkshopRequirement`
  - `ProgramMilestoneLogbookRequirement`
  - `ProgramRotationRequirement`
  - `ProgramRotationTemplate`
  - `LogbookThresholdConfig`
  - `ResidentTrainingRecord`
  - `RotationAssignment`
  - `RotationCompletion`
  - `RotationCertificate`
  - `LeaveRequest`
  - `DeputationPosting`
  - `ResidentResearchProject`
  - `ResidentThesis`
  - `ResidentWorkshopCompletion`
  - `ResidentMilestoneEligibility`
  - `LogbookEntry`
  - `LogbookReview`
  - `LogbookThresholdSnapshot`
  - `SubmissionRequirementTemplate`
  - `ResidentSubmission`
  - `SubmissionDocument`
  - `SubmissionReview`
  - `SubmissionCertificate`
  - `Workshop`
  - `WorkshopBlock`
  - `WorkshopRun`

### Audit and Bulk Tables

- `backend/sims/audit/models.py`
  - `ActivityLog`
  - `AuditReport`
- `backend/sims/bulk/models.py`
  - `BulkOperation`

### Notifications

- `backend/sims/notifications/models.py`
  - `Notification`
  - `NotificationPreference`

## Seed Commands Found

- `backend/sims/users/management/commands/seed_org_data.py`
- `backend/sims/users/management/commands/seed_e2e.py`
- `backend/sims/users/management/commands/seed_active_surface_baseline.py`
- `backend/sims/users/management/commands/seed_demo_data.py`
- `backend/sims/users/management/commands/cleanup_pilot_runtime.py`

## Canonical Records Preserved

- Hospitals:
  - Allied Hospital
  - DHQ Hospital
  - Govt General Hospital Ghulam Muhammadabad
  - UTRMC Teaching Hospital
- Departments:
  - Anaesthesia
  - Cardiology
  - Dermatology
  - ENT
  - Emergency Medicine
  - Gastroenterology
  - Gynecology & Obstetrics
  - Intensive Care Unit
  - Medicine
  - Nephrology
  - Neurology
  - Oncology
  - Ophthalmology
  - Orthopedics
  - Pathology
  - Pediatrics
  - Psychiatry
  - Pulmonology
  - Radiology
  - Surgery

