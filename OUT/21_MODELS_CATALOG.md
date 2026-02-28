# Models Catalog

Total models: 62

## academics

### academics.Batch
- **DB Table**: `academics_batch`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `program` | CharField | False | False | False | False | True |  |
| `department` | ForeignKey | False | False | False | False | False | academics.Department |
| `start_date` | DateField | False | False | False | False | False |  |
| `end_date` | DateField | False | False | False | False | False |  |
| `coordinator` | ForeignKey | True | True | False | False | False | users.User |
| `capacity` | IntegerField | False | False | False | False | False |  |
| `active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `department` (ForeignKey) -> `academics.Department` (related_name=batches)
  - `coordinator` (ForeignKey) -> `users.User` (related_name=coordinated_batches)

### academics.Department
- **DB Table**: `academics_department`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `code` | CharField | False | False | False | True | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `head` | ForeignKey | True | True | False | False | False | users.User |
| `active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `head` (ForeignKey) -> `users.User` (related_name=headed_departments)

### academics.StudentProfile
- **DB Table**: `academics_studentprofile`
- **Status/State Fields**: `status`, `status_updated_at`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `user` | OneToOneField | False | False | False | True | False | users.User |
| `batch` | ForeignKey | False | False | False | False | False | academics.Batch |
| `roll_number` | CharField | False | False | False | True | False |  |
| `admission_date` | DateField | False | False | False | False | False |  |
| `expected_graduation_date` | DateField | True | True | False | False | False |  |
| `actual_graduation_date` | DateField | True | True | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `status_updated_at` | DateTimeField | False | False | False | False | False |  |
| `cgpa` | DecimalField | True | True | False | False | False |  |
| `previous_institution` | CharField | False | True | False | False | False |  |
| `previous_qualification` | CharField | False | True | False | False | False |  |
| `emergency_contact_name` | CharField | False | True | False | False | False |  |
| `emergency_contact_phone` | CharField | False | True | False | False | False |  |
| `emergency_contact_relation` | CharField | False | True | False | False | False |  |
| `remarks` | TextField | False | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `user` (OneToOneField) -> `users.User` (related_name=student_profile)
  - `batch` (ForeignKey) -> `academics.Batch` (related_name=student_profiles)

## admin

### admin.LogEntry
- **DB Table**: `django_admin_log`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `action_time` | DateTimeField | False | False | False | False | False |  |
| `user` | ForeignKey | False | False | False | False | False | users.User |
| `content_type` | ForeignKey | True | True | False | False | False | contenttypes.ContentType |
| `object_id` | TextField | True | True | False | False | False |  |
| `object_repr` | CharField | False | False | False | False | False |  |
| `action_flag` | PositiveSmallIntegerField | False | False | False | False | True |  |
| `change_message` | TextField | False | True | False | False | False |  |

- **Relations**:
  - `user` (ForeignKey) -> `users.User` (related_name=None)
  - `content_type` (ForeignKey) -> `contenttypes.ContentType` (related_name=None)

## analytics

### analytics.AnalyticsDailyRollup
- **DB Table**: `analytics_analyticsdailyrollup`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `day` | DateField | False | False | False | False | False |  |
| `event_type` | CharField | False | False | False | False | False |  |
| `department` | ForeignKey | True | True | False | False | False | academics.Department |
| `hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `count` | PositiveIntegerField | False | False | False | False | False |  |
| `extra` | JSONField | False | True | False | False | False |  |

- **Relations**:
  - `department` (ForeignKey) -> `academics.Department` (related_name=analytics_daily_rollups)
  - `hospital` (ForeignKey) -> `rotations.Hospital` (related_name=analytics_daily_rollups)

### analytics.AnalyticsEvent
- **DB Table**: `analytics_analyticsevent`
- **Status/State Fields**: `status_from`, `status_to`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | UUIDField | False | False | True | True | False |  |
| `occurred_at` | DateTimeField | False | False | False | False | False |  |
| `event_type` | CharField | False | False | False | False | False |  |
| `actor_user` | ForeignKey | True | True | False | False | False | users.User |
| `actor_role` | CharField | False | True | False | False | False |  |
| `department` | ForeignKey | True | True | False | False | False | academics.Department |
| `hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `entity_type` | CharField | True | True | False | False | False |  |
| `entity_id` | CharField | True | True | False | False | False |  |
| `status_from` | CharField | True | True | False | False | False |  |
| `status_to` | CharField | True | True | False | False | False |  |
| `request_id` | CharField | True | True | False | False | False |  |
| `event_key` | CharField | True | True | False | False | False |  |
| `metadata` | JSONField | False | True | False | False | False |  |

- **Relations**:
  - `actor_user` (ForeignKey) -> `users.User` (related_name=analytics_events)
  - `department` (ForeignKey) -> `academics.Department` (related_name=analytics_events)
  - `hospital` (ForeignKey) -> `rotations.Hospital` (related_name=analytics_events)

### analytics.AnalyticsValidationRejection
- **DB Table**: `analytics_analyticsvalidationrejection`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `source` | CharField | False | False | False | False | False |  |
| `event_type` | CharField | False | True | False | False | False |  |
| `reason` | CharField | False | False | False | False | False |  |
| `actor_role` | CharField | False | True | False | False | False |  |
| `department_id` | IntegerField | True | True | False | False | False |  |
| `hospital_id` | IntegerField | True | True | False | False | False |  |
| `metadata_keys` | JSONField | False | True | False | False | False |  |

## attendance

### attendance.AttendanceRecord
- **DB Table**: `attendance_attendancerecord`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `user` | ForeignKey | False | False | False | False | False | users.User |
| `session` | ForeignKey | False | False | False | False | False | attendance.Session |
| `status` | CharField | False | False | False | False | True |  |
| `check_in_time` | DateTimeField | True | True | False | False | False |  |
| `remarks` | TextField | False | True | False | False | False |  |
| `recorded_by` | ForeignKey | True | True | False | False | False | users.User |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `user` (ForeignKey) -> `users.User` (related_name=attendance_records)
  - `session` (ForeignKey) -> `attendance.Session` (related_name=attendance_records)
  - `recorded_by` (ForeignKey) -> `users.User` (related_name=recorded_attendance)

### attendance.EligibilitySummary
- **DB Table**: `attendance_eligibilitysummary`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `user` | ForeignKey | False | False | False | False | False | users.User |
| `period` | CharField | False | False | False | False | True |  |
| `start_date` | DateField | False | False | False | False | False |  |
| `end_date` | DateField | False | False | False | False | False |  |
| `total_sessions` | IntegerField | False | False | False | False | False |  |
| `attended_sessions` | IntegerField | False | False | False | False | False |  |
| `percentage_present` | FloatField | False | False | False | False | False |  |
| `is_eligible` | BooleanField | False | False | False | False | False |  |
| `threshold_percentage` | FloatField | False | False | False | False | False |  |
| `remarks` | TextField | False | True | False | False | False |  |
| `generated_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `user` (ForeignKey) -> `users.User` (related_name=eligibility_summaries)

### attendance.Session
- **DB Table**: `attendance_session`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `title` | CharField | False | False | False | False | False |  |
| `session_type` | CharField | False | False | False | False | True |  |
| `date` | DateField | False | False | False | False | False |  |
| `start_time` | TimeField | False | False | False | False | False |  |
| `end_time` | TimeField | False | False | False | False | False |  |
| `rotation` | ForeignKey | True | True | False | False | False | rotations.Rotation |
| `module_name` | CharField | False | True | False | False | False |  |
| `location` | CharField | False | True | False | False | False |  |
| `instructor` | ForeignKey | True | True | False | False | False | users.User |
| `status` | CharField | False | False | False | False | True |  |
| `notes` | TextField | False | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `rotation` (ForeignKey) -> `rotations.Rotation` (related_name=sessions)
  - `instructor` (ForeignKey) -> `users.User` (related_name=taught_sessions)

## audit

### audit.ActivityLog
- **DB Table**: `audit_activitylog`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `actor` | ForeignKey | True | True | False | False | False | users.User |
| `action` | CharField | False | False | False | False | True |  |
| `verb` | CharField | False | False | False | False | False |  |
| `target_content_type` | ForeignKey | True | False | False | False | False | contenttypes.ContentType |
| `target_object_id` | CharField | False | True | False | False | False |  |
| `target_repr` | CharField | False | True | False | False | False |  |
| `metadata` | JSONField | False | True | False | False | False |  |
| `ip_address` | GenericIPAddressField | True | True | False | False | False |  |
| `is_sensitive` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | False | False | False | False |  |

- **Relations**:
  - `actor` (ForeignKey) -> `users.User` (related_name=activity_logs)
  - `target_content_type` (ForeignKey) -> `contenttypes.ContentType` (related_name=None)

### audit.AuditReport
- **DB Table**: `audit_auditreport`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `start` | DateTimeField | False | False | False | False | False |  |
| `end` | DateTimeField | False | False | False | False | False |  |
| `generated_at` | DateTimeField | False | True | False | False | False |  |
| `payload` | JSONField | False | False | False | False | False |  |

- **Relations**:
  - `created_by` (ForeignKey) -> `users.User` (related_name=audit_reports)

### audit.HistoricalAuditReport
- **DB Table**: `audit_historicalauditreport`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `start` | DateTimeField | False | False | False | False | False |  |
| `end` | DateTimeField | False | False | False | False | False |  |
| `generated_at` | DateTimeField | False | True | False | False | False |  |
| `payload` | JSONField | False | False | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `created_by` (ForeignKey) -> `users.User` (related_name=+)
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

## auth

### auth.Group
- **DB Table**: `auth_group`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `permissions` | ManyToManyField | False | True | False | False | False | auth.Permission |

- **Relations**:
  - `permissions` (ManyToManyField) -> `auth.Permission` (related_name=None)

### auth.Permission
- **DB Table**: `auth_permission`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `content_type` | ForeignKey | False | False | False | False | False | contenttypes.ContentType |
| `codename` | CharField | False | False | False | False | False |  |

- **Relations**:
  - `content_type` (ForeignKey) -> `contenttypes.ContentType` (related_name=None)

## bulk

### bulk.BulkOperation
- **DB Table**: `bulk_bulkoperation`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `user` | ForeignKey | False | False | False | False | False | users.User |
| `operation` | CharField | False | False | False | False | True |  |
| `status` | CharField | False | False | False | False | True |  |
| `total_items` | PositiveIntegerField | False | False | False | False | False |  |
| `success_count` | PositiveIntegerField | False | False | False | False | False |  |
| `failure_count` | PositiveIntegerField | False | False | False | False | False |  |
| `details` | JSONField | False | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `completed_at` | DateTimeField | True | True | False | False | False |  |

- **Relations**:
  - `user` (ForeignKey) -> `users.User` (related_name=bulk_operations)

## cases

### cases.CaseCategory
- **DB Table**: `cases_casecategory`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `color_code` | CharField | False | False | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `sort_order` | PositiveIntegerField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

### cases.CaseReview
- **DB Table**: `cases_casereview`
- **Status/State Fields**: `reviewer`, `status`, `review_date`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `case` | ForeignKey | False | False | False | False | False | cases.ClinicalCase |
| `reviewer` | ForeignKey | False | False | False | False | False | users.User |
| `status` | CharField | False | False | False | False | True |  |
| `review_date` | DateField | False | False | False | False | False |  |
| `overall_feedback` | TextField | False | False | False | False | False |  |
| `clinical_reasoning_feedback` | TextField | False | True | False | False | False |  |
| `documentation_feedback` | TextField | False | True | False | False | False |  |
| `learning_points_feedback` | TextField | False | True | False | False | False |  |
| `strengths_identified` | TextField | False | True | False | False | False |  |
| `areas_for_improvement` | TextField | False | True | False | False | False |  |
| `recommendations` | TextField | False | True | False | False | False |  |
| `follow_up_required` | BooleanField | False | False | False | False | False |  |
| `clinical_knowledge_score` | PositiveIntegerField | True | True | False | False | False |  |
| `clinical_reasoning_score` | PositiveIntegerField | True | True | False | False | False |  |
| `documentation_score` | PositiveIntegerField | True | True | False | False | False |  |
| `overall_score` | PositiveIntegerField | True | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `case` (ForeignKey) -> `cases.ClinicalCase` (related_name=reviews)
  - `reviewer` (ForeignKey) -> `users.User` (related_name=case_reviews)

### cases.CaseStatistics
- **DB Table**: `cases_casestatistics`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | OneToOneField | False | False | False | True | False | users.User |
| `total_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `approved_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `pending_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `draft_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `simple_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `moderate_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `complex_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `highly_complex_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `average_self_score` | FloatField | False | False | False | False | False |  |
| `average_supervisor_score` | FloatField | False | False | False | False | False |  |
| `completion_rate` | FloatField | False | False | False | False | False |  |
| `average_submission_time` | FloatField | False | False | False | False | False |  |
| `overdue_cases` | PositiveIntegerField | False | False | False | False | False |  |
| `last_updated` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `pg` (OneToOneField) -> `users.User` (related_name=case_statistics)

### cases.ClinicalCase
- **DB Table**: `cases_clinicalcase`
- **Status/State Fields**: `literature_review`, `status`, `reviewed_by`, `reviewed_at`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | ForeignKey | False | False | False | False | False | users.User |
| `case_title` | CharField | False | False | False | False | False |  |
| `category` | ForeignKey | True | False | False | False | False | cases.CaseCategory |
| `date_encountered` | DateField | False | False | False | False | False |  |
| `rotation` | ForeignKey | True | True | False | False | False | rotations.Rotation |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `patient_age` | PositiveIntegerField | False | False | False | False | False |  |
| `patient_gender` | CharField | False | False | False | False | True |  |
| `complexity` | CharField | False | False | False | False | True |  |
| `chief_complaint` | TextField | False | False | False | False | False |  |
| `history_of_present_illness` | TextField | False | False | False | False | False |  |
| `past_medical_history` | TextField | False | True | False | False | False |  |
| `family_history` | TextField | False | True | False | False | False |  |
| `social_history` | TextField | False | True | False | False | False |  |
| `physical_examination` | TextField | False | False | False | False | False |  |
| `investigations` | TextField | False | True | False | False | False |  |
| `primary_diagnosis` | ForeignKey | True | False | False | False | False | logbook.Diagnosis |
| `differential_diagnosis` | TextField | False | True | False | False | False |  |
| `management_plan` | TextField | False | False | False | False | False |  |
| `learning_objectives` | TextField | False | True | False | False | False |  |
| `clinical_reasoning` | TextField | False | False | False | False | False |  |
| `learning_points` | TextField | False | False | False | False | False |  |
| `challenges_faced` | TextField | False | True | False | False | False |  |
| `literature_review` | TextField | False | True | False | False | False |  |
| `outcome` | TextField | False | True | False | False | False |  |
| `follow_up_plan` | TextField | False | True | False | False | False |  |
| `supervisor_feedback` | TextField | False | True | False | False | False |  |
| `self_assessment_score` | PositiveIntegerField | True | True | False | False | False |  |
| `supervisor_assessment_score` | PositiveIntegerField | True | True | False | False | False |  |
| `case_files` | FileField | True | True | False | False | False |  |
| `case_images` | ImageField | True | True | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `is_featured` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `reviewed_by` | ForeignKey | True | True | False | False | False | users.User |
| `reviewed_at` | DateTimeField | True | True | False | False | False |  |
| `secondary_diagnoses` | ManyToManyField | False | True | False | False | False | logbook.Diagnosis |
| `procedures_performed` | ManyToManyField | False | True | False | False | False | logbook.Procedure |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=clinical_cases)
  - `category` (ForeignKey) -> `cases.CaseCategory` (related_name=cases)
  - `rotation` (ForeignKey) -> `rotations.Rotation` (related_name=clinical_cases)
  - `supervisor` (ForeignKey) -> `users.User` (related_name=supervised_cases)
  - `primary_diagnosis` (ForeignKey) -> `logbook.Diagnosis` (related_name=primary_cases)
  - `created_by` (ForeignKey) -> `users.User` (related_name=created_cases)
  - `reviewed_by` (ForeignKey) -> `users.User` (related_name=reviewed_cases)
  - `secondary_diagnoses` (ManyToManyField) -> `logbook.Diagnosis` (related_name=secondary_cases)
  - `procedures_performed` (ManyToManyField) -> `logbook.Procedure` (related_name=clinical_cases)

### cases.HistoricalCaseCategory
- **DB Table**: `cases_historicalcasecategory`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `color_code` | CharField | False | False | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `sort_order` | PositiveIntegerField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### cases.HistoricalClinicalCase
- **DB Table**: `cases_historicalclinicalcase`
- **Status/State Fields**: `literature_review`, `status`, `reviewed_at`, `reviewed_by`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `case_title` | CharField | False | False | False | False | False |  |
| `date_encountered` | DateField | False | False | False | False | False |  |
| `patient_age` | PositiveIntegerField | False | False | False | False | False |  |
| `patient_gender` | CharField | False | False | False | False | True |  |
| `complexity` | CharField | False | False | False | False | True |  |
| `chief_complaint` | TextField | False | False | False | False | False |  |
| `history_of_present_illness` | TextField | False | False | False | False | False |  |
| `past_medical_history` | TextField | False | True | False | False | False |  |
| `family_history` | TextField | False | True | False | False | False |  |
| `social_history` | TextField | False | True | False | False | False |  |
| `physical_examination` | TextField | False | False | False | False | False |  |
| `investigations` | TextField | False | True | False | False | False |  |
| `differential_diagnosis` | TextField | False | True | False | False | False |  |
| `management_plan` | TextField | False | False | False | False | False |  |
| `learning_objectives` | TextField | False | True | False | False | False |  |
| `clinical_reasoning` | TextField | False | False | False | False | False |  |
| `learning_points` | TextField | False | False | False | False | False |  |
| `challenges_faced` | TextField | False | True | False | False | False |  |
| `literature_review` | TextField | False | True | False | False | False |  |
| `outcome` | TextField | False | True | False | False | False |  |
| `follow_up_plan` | TextField | False | True | False | False | False |  |
| `supervisor_feedback` | TextField | False | True | False | False | False |  |
| `self_assessment_score` | PositiveIntegerField | True | True | False | False | False |  |
| `supervisor_assessment_score` | PositiveIntegerField | True | True | False | False | False |  |
| `case_files` | TextField | True | True | False | False | False |  |
| `case_images` | TextField | True | True | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `is_featured` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `reviewed_at` | DateTimeField | True | True | False | False | False |  |
| `pg` | ForeignKey | True | True | False | False | False | users.User |
| `category` | ForeignKey | True | True | False | False | False | cases.CaseCategory |
| `rotation` | ForeignKey | True | True | False | False | False | rotations.Rotation |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `primary_diagnosis` | ForeignKey | True | True | False | False | False | logbook.Diagnosis |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `reviewed_by` | ForeignKey | True | True | False | False | False | users.User |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=+)
  - `category` (ForeignKey) -> `cases.CaseCategory` (related_name=+)
  - `rotation` (ForeignKey) -> `rotations.Rotation` (related_name=+)
  - `supervisor` (ForeignKey) -> `users.User` (related_name=+)
  - `primary_diagnosis` (ForeignKey) -> `logbook.Diagnosis` (related_name=+)
  - `created_by` (ForeignKey) -> `users.User` (related_name=+)
  - `reviewed_by` (ForeignKey) -> `users.User` (related_name=+)
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

## certificates

### certificates.Certificate
- **DB Table**: `certificates_certificate`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | ForeignKey | False | False | False | False | False | users.User |
| `certificate_type` | ForeignKey | False | False | False | False | False | certificates.CertificateType |
| `title` | CharField | False | False | False | False | False |  |
| `certificate_number` | CharField | False | True | False | False | False |  |
| `issuing_organization` | CharField | False | False | False | False | False |  |
| `issue_date` | DateField | False | False | False | False | False |  |
| `expiry_date` | DateField | True | True | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `skills_acquired` | TextField | False | True | False | False | False |  |
| `cme_points_earned` | PositiveIntegerField | False | False | False | False | False |  |
| `cpd_credits_earned` | PositiveIntegerField | False | False | False | False | False |  |
| `certificate_file` | FileField | False | False | False | False | False |  |
| `additional_documents` | FileField | True | True | False | False | False |  |
| `verification_url` | URLField | False | True | False | False | False |  |
| `verification_code` | CharField | False | True | False | False | False |  |
| `is_verified` | BooleanField | False | False | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `verified_by` | ForeignKey | True | True | False | False | False | users.User |
| `verified_at` | DateTimeField | True | True | False | False | False |  |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=certificates)
  - `certificate_type` (ForeignKey) -> `certificates.CertificateType` (related_name=certificates)
  - `created_by` (ForeignKey) -> `users.User` (related_name=certificates_created)
  - `verified_by` (ForeignKey) -> `users.User` (related_name=certificates_verified)

### certificates.CertificateReview
- **DB Table**: `certificates_certificatereview`
- **Status/State Fields**: `reviewer`, `status`, `review_date`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `certificate` | ForeignKey | False | False | False | False | False | certificates.Certificate |
| `reviewer` | ForeignKey | False | False | False | False | False | users.User |
| `status` | CharField | False | False | False | False | True |  |
| `comments` | TextField | False | True | False | False | False |  |
| `recommendations` | TextField | False | True | False | False | False |  |
| `required_changes` | TextField | False | True | False | False | False |  |
| `review_date` | DateField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `certificate` (ForeignKey) -> `certificates.Certificate` (related_name=reviews)
  - `reviewer` (ForeignKey) -> `users.User` (related_name=certificate_reviews_given)

### certificates.CertificateStatistics
- **DB Table**: `certificates_certificatestatistics`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | OneToOneField | False | False | False | True | False | users.User |
| `total_certificates` | PositiveIntegerField | False | False | False | False | False |  |
| `approved_certificates` | PositiveIntegerField | False | False | False | False | False |  |
| `pending_certificates` | PositiveIntegerField | False | False | False | False | False |  |
| `expired_certificates` | PositiveIntegerField | False | False | False | False | False |  |
| `total_cme_points` | PositiveIntegerField | False | False | False | False | False |  |
| `total_cpd_credits` | PositiveIntegerField | False | False | False | False | False |  |
| `last_certificate_date` | DateField | True | True | False | False | False |  |
| `compliance_rate` | FloatField | False | False | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `pg` (OneToOneField) -> `users.User` (related_name=certificate_stats)

### certificates.CertificateType
- **DB Table**: `certificates_certificatetype`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `is_required` | BooleanField | False | False | False | False | False |  |
| `validity_period_months` | PositiveIntegerField | True | True | False | False | False |  |
| `cme_points` | PositiveIntegerField | False | False | False | False | False |  |
| `cpd_credits` | PositiveIntegerField | False | False | False | False | False |  |
| `prerequisites` | TextField | False | True | False | False | False |  |
| `requirements` | TextField | False | True | False | False | False |  |
| `verification_guidelines` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

### certificates.HistoricalCertificate
- **DB Table**: `certificates_historicalcertificate`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `title` | CharField | False | False | False | False | False |  |
| `certificate_number` | CharField | False | True | False | False | False |  |
| `issuing_organization` | CharField | False | False | False | False | False |  |
| `issue_date` | DateField | False | False | False | False | False |  |
| `expiry_date` | DateField | True | True | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `skills_acquired` | TextField | False | True | False | False | False |  |
| `cme_points_earned` | PositiveIntegerField | False | False | False | False | False |  |
| `cpd_credits_earned` | PositiveIntegerField | False | False | False | False | False |  |
| `certificate_file` | TextField | False | False | False | False | False |  |
| `additional_documents` | TextField | True | True | False | False | False |  |
| `verification_url` | URLField | False | True | False | False | False |  |
| `verification_code` | CharField | False | True | False | False | False |  |
| `is_verified` | BooleanField | False | False | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `verified_at` | DateTimeField | True | True | False | False | False |  |
| `pg` | ForeignKey | True | True | False | False | False | users.User |
| `certificate_type` | ForeignKey | True | True | False | False | False | certificates.CertificateType |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `verified_by` | ForeignKey | True | True | False | False | False | users.User |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=+)
  - `certificate_type` (ForeignKey) -> `certificates.CertificateType` (related_name=+)
  - `created_by` (ForeignKey) -> `users.User` (related_name=+)
  - `verified_by` (ForeignKey) -> `users.User` (related_name=+)
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### certificates.HistoricalCertificateType
- **DB Table**: `certificates_historicalcertificatetype`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `is_required` | BooleanField | False | False | False | False | False |  |
| `validity_period_months` | PositiveIntegerField | True | True | False | False | False |  |
| `cme_points` | PositiveIntegerField | False | False | False | False | False |  |
| `cpd_credits` | PositiveIntegerField | False | False | False | False | False |  |
| `prerequisites` | TextField | False | True | False | False | False |  |
| `requirements` | TextField | False | True | False | False | False |  |
| `verification_guidelines` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

## contenttypes

### contenttypes.ContentType
- **DB Table**: `django_content_type`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `app_label` | CharField | False | False | False | False | False |  |
| `model` | CharField | False | False | False | False | False |  |

## django_celery_beat

### django_celery_beat.ClockedSchedule
- **DB Table**: `django_celery_beat_clockedschedule`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `clocked_time` | DateTimeField | False | False | False | False | False |  |

### django_celery_beat.CrontabSchedule
- **DB Table**: `django_celery_beat_crontabschedule`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `minute` | CharField | False | False | False | False | False |  |
| `hour` | CharField | False | False | False | False | False |  |
| `day_of_month` | CharField | False | False | False | False | False |  |
| `month_of_year` | CharField | False | False | False | False | False |  |
| `day_of_week` | CharField | False | False | False | False | False |  |
| `timezone` | TimeZoneField | False | False | False | False | True |  |

### django_celery_beat.IntervalSchedule
- **DB Table**: `django_celery_beat_intervalschedule`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `every` | IntegerField | False | False | False | False | False |  |
| `period` | CharField | False | False | False | False | True |  |

### django_celery_beat.PeriodicTask
- **DB Table**: `django_celery_beat_periodictask`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `task` | CharField | False | False | False | False | False |  |
| `interval` | ForeignKey | True | True | False | False | False | django_celery_beat.IntervalSchedule |
| `crontab` | ForeignKey | True | True | False | False | False | django_celery_beat.CrontabSchedule |
| `solar` | ForeignKey | True | True | False | False | False | django_celery_beat.SolarSchedule |
| `clocked` | ForeignKey | True | True | False | False | False | django_celery_beat.ClockedSchedule |
| `args` | TextField | False | True | False | False | False |  |
| `kwargs` | TextField | False | True | False | False | False |  |
| `queue` | CharField | True | True | False | False | False |  |
| `exchange` | CharField | True | True | False | False | False |  |
| `routing_key` | CharField | True | True | False | False | False |  |
| `headers` | TextField | False | True | False | False | False |  |
| `priority` | PositiveIntegerField | True | True | False | False | False |  |
| `expires` | DateTimeField | True | True | False | False | False |  |
| `expire_seconds` | PositiveIntegerField | True | True | False | False | False |  |
| `one_off` | BooleanField | False | False | False | False | False |  |
| `start_time` | DateTimeField | True | True | False | False | False |  |
| `enabled` | BooleanField | False | False | False | False | False |  |
| `last_run_at` | DateTimeField | True | True | False | False | False |  |
| `total_run_count` | PositiveIntegerField | False | False | False | False | False |  |
| `date_changed` | DateTimeField | False | True | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |

- **Relations**:
  - `interval` (ForeignKey) -> `django_celery_beat.IntervalSchedule` (related_name=None)
  - `crontab` (ForeignKey) -> `django_celery_beat.CrontabSchedule` (related_name=None)
  - `solar` (ForeignKey) -> `django_celery_beat.SolarSchedule` (related_name=None)
  - `clocked` (ForeignKey) -> `django_celery_beat.ClockedSchedule` (related_name=None)

### django_celery_beat.PeriodicTasks
- **DB Table**: `django_celery_beat_periodictasks`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `ident` | SmallIntegerField | False | False | True | True | False |  |
| `last_update` | DateTimeField | False | False | False | False | False |  |

### django_celery_beat.SolarSchedule
- **DB Table**: `django_celery_beat_solarschedule`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | AutoField | False | True | True | True | False |  |
| `event` | CharField | False | False | False | False | True |  |
| `latitude` | DecimalField | False | False | False | False | False |  |
| `longitude` | DecimalField | False | False | False | False | False |  |

## logbook

### logbook.Diagnosis
- **DB Table**: `logbook_diagnosis`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `icd_code` | CharField | False | True | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `typical_presentation` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `common_procedures` | ManyToManyField | False | True | False | False | False | logbook.Procedure |

- **Relations**:
  - `common_procedures` (ManyToManyField) -> `logbook.Procedure` (related_name=common_diagnoses)

### logbook.HistoricalLogbookReview
- **DB Table**: `logbook_historicallogbookreview`
- **Status/State Fields**: `status`, `review_date`, `reviewer`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `review_date` | DateField | False | False | False | False | False |  |
| `feedback` | TextField | False | False | False | False | False |  |
| `strengths_identified` | TextField | False | True | False | False | False |  |
| `areas_for_improvement` | TextField | False | True | False | False | False |  |
| `recommendations` | TextField | False | True | False | False | False |  |
| `follow_up_required` | BooleanField | False | False | False | False | False |  |
| `clinical_knowledge_score` | PositiveIntegerField | True | True | False | False | False |  |
| `clinical_skills_score` | PositiveIntegerField | True | True | False | False | False |  |
| `professionalism_score` | PositiveIntegerField | True | True | False | False | False |  |
| `overall_score` | PositiveIntegerField | True | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `logbook_entry` | ForeignKey | True | True | False | False | False | logbook.LogbookEntry |
| `reviewer` | ForeignKey | True | True | False | False | False | users.User |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `logbook_entry` (ForeignKey) -> `logbook.LogbookEntry` (related_name=+)
  - `reviewer` (ForeignKey) -> `users.User` (related_name=+)
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### logbook.HistoricalProcedure
- **DB Table**: `logbook_historicalprocedure`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `difficulty_level` | PositiveIntegerField | False | False | False | False | False |  |
| `duration_minutes` | PositiveIntegerField | True | True | False | False | False |  |
| `cme_points` | PositiveIntegerField | False | False | False | False | False |  |
| `learning_objectives` | TextField | False | True | False | False | False |  |
| `prerequisites` | TextField | False | True | False | False | False |  |
| `assessment_criteria` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### logbook.HistoricalSkill
- **DB Table**: `logbook_historicalskill`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `level` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `competency_requirements` | TextField | False | True | False | False | False |  |
| `assessment_methods` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### logbook.LogbookEntry
- **DB Table**: `logbook_logbookentry`
- **Status/State Fields**: `status`, `submitted_to_supervisor_at`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | ForeignKey | False | False | False | False | False | users.User |
| `case_title` | CharField | False | False | False | False | False |  |
| `date` | DateField | False | False | False | False | False |  |
| `location_of_activity` | CharField | False | False | False | False | False |  |
| `patient_history_summary` | TextField | False | False | False | False | False |  |
| `management_action` | TextField | False | False | False | False | False |  |
| `topic_subtopic` | CharField | False | False | False | False | False |  |
| `rotation` | ForeignKey | True | True | False | False | False | rotations.Rotation |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `template` | ForeignKey | True | True | False | False | False | logbook.LogbookTemplate |
| `patient_age` | PositiveIntegerField | True | True | False | False | False |  |
| `patient_gender` | CharField | True | True | False | False | True |  |
| `patient_chief_complaint` | TextField | False | True | False | False | False |  |
| `primary_diagnosis` | ForeignKey | True | True | False | False | False | logbook.Diagnosis |
| `investigations_ordered` | TextField | False | True | False | False | False |  |
| `clinical_reasoning` | TextField | False | True | False | False | False |  |
| `learning_points` | TextField | False | True | False | False | False |  |
| `challenges_faced` | TextField | False | True | False | False | False |  |
| `follow_up_required` | TextField | False | True | False | False | False |  |
| `supervisor_feedback` | TextField | False | True | False | False | False |  |
| `self_assessment_score` | PositiveIntegerField | True | True | False | False | False |  |
| `supervisor_assessment_score` | PositiveIntegerField | True | True | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `submitted_to_supervisor_at` | DateTimeField | True | True | False | False | False |  |
| `supervisor_action_at` | DateTimeField | True | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `verified_by` | ForeignKey | True | True | False | False | False | users.User |
| `verified_at` | DateTimeField | True | True | False | False | False |  |
| `secondary_diagnoses` | ManyToManyField | False | True | False | False | False | logbook.Diagnosis |
| `procedures` | ManyToManyField | False | True | False | False | False | logbook.Procedure |
| `skills` | ManyToManyField | False | True | False | False | False | logbook.Skill |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=logbook_entries)
  - `rotation` (ForeignKey) -> `rotations.Rotation` (related_name=logbook_entries)
  - `supervisor` (ForeignKey) -> `users.User` (related_name=supervised_entries)
  - `template` (ForeignKey) -> `logbook.LogbookTemplate` (related_name=logbook_entries)
  - `primary_diagnosis` (ForeignKey) -> `logbook.Diagnosis` (related_name=primary_entries)
  - `created_by` (ForeignKey) -> `users.User` (related_name=created_logbook_entries)
  - `verified_by` (ForeignKey) -> `users.User` (related_name=verified_logbook_entries)
  - `secondary_diagnoses` (ManyToManyField) -> `logbook.Diagnosis` (related_name=secondary_entries)
  - `procedures` (ManyToManyField) -> `logbook.Procedure` (related_name=logbook_entries)
  - `skills` (ManyToManyField) -> `logbook.Skill` (related_name=logbook_entries)

### logbook.LogbookReview
- **DB Table**: `logbook_logbookreview`
- **Status/State Fields**: `reviewer`, `status`, `review_date`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `logbook_entry` | ForeignKey | False | False | False | False | False | logbook.LogbookEntry |
| `reviewer` | ForeignKey | False | False | False | False | False | users.User |
| `status` | CharField | False | False | False | False | True |  |
| `review_date` | DateField | False | False | False | False | False |  |
| `feedback` | TextField | False | False | False | False | False |  |
| `strengths_identified` | TextField | False | True | False | False | False |  |
| `areas_for_improvement` | TextField | False | True | False | False | False |  |
| `recommendations` | TextField | False | True | False | False | False |  |
| `follow_up_required` | BooleanField | False | False | False | False | False |  |
| `clinical_knowledge_score` | PositiveIntegerField | True | True | False | False | False |  |
| `clinical_skills_score` | PositiveIntegerField | True | True | False | False | False |  |
| `professionalism_score` | PositiveIntegerField | True | True | False | False | False |  |
| `overall_score` | PositiveIntegerField | True | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `logbook_entry` (ForeignKey) -> `logbook.LogbookEntry` (related_name=reviews)
  - `reviewer` (ForeignKey) -> `users.User` (related_name=logbook_reviews_given)

### logbook.LogbookStatistics
- **DB Table**: `logbook_logbookstatistics`
- **Status/State Fields**: `submitted_entries`, `average_review_score`, `average_review_time`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | OneToOneField | False | False | False | True | False | users.User |
| `total_entries` | PositiveIntegerField | False | False | False | False | False |  |
| `draft_entries` | PositiveIntegerField | False | False | False | False | False |  |
| `submitted_entries` | PositiveIntegerField | False | False | False | False | False |  |
| `approved_entries` | PositiveIntegerField | False | False | False | False | False |  |
| `revision_entries` | PositiveIntegerField | False | False | False | False | False |  |
| `total_procedures` | PositiveIntegerField | False | False | False | False | False |  |
| `unique_procedures` | PositiveIntegerField | False | False | False | False | False |  |
| `total_skills` | PositiveIntegerField | False | False | False | False | False |  |
| `unique_skills` | PositiveIntegerField | False | False | False | False | False |  |
| `average_self_score` | FloatField | True | True | False | False | False |  |
| `average_supervisor_score` | FloatField | True | True | False | False | False |  |
| `average_review_score` | FloatField | True | True | False | False | False |  |
| `total_cme_points` | PositiveIntegerField | False | False | False | False | False |  |
| `completion_rate` | FloatField | False | False | False | False | False |  |
| `average_review_time` | FloatField | True | True | False | False | False |  |
| `last_entry_date` | DateField | True | True | False | False | False |  |
| `most_active_month` | CharField | False | True | False | False | False |  |
| `entries_needing_revision_rate` | FloatField | False | False | False | False | False |  |
| `on_time_submission_rate` | FloatField | False | False | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `pg` (OneToOneField) -> `users.User` (related_name=logbook_stats)

### logbook.LogbookTemplate
- **DB Table**: `logbook_logbooktemplate`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `template_type` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `template_structure` | JSONField | False | False | False | False | False |  |
| `required_fields` | JSONField | False | False | False | False | False |  |
| `completion_guidelines` | TextField | False | True | False | False | False |  |
| `example_entries` | TextField | False | True | False | False | False |  |
| `is_default` | BooleanField | False | False | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `created_by` (ForeignKey) -> `users.User` (related_name=created_templates)

### logbook.Procedure
- **DB Table**: `logbook_procedure`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | True | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `difficulty_level` | PositiveIntegerField | False | False | False | False | False |  |
| `duration_minutes` | PositiveIntegerField | True | True | False | False | False |  |
| `cme_points` | PositiveIntegerField | False | False | False | False | False |  |
| `learning_objectives` | TextField | False | True | False | False | False |  |
| `prerequisites` | TextField | False | True | False | False | False |  |
| `assessment_criteria` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `required_skills` | ManyToManyField | False | True | False | False | False | logbook.Skill |

- **Relations**:
  - `required_skills` (ManyToManyField) -> `logbook.Skill` (related_name=required_for_procedures)

### logbook.Skill
- **DB Table**: `logbook_skill`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `category` | CharField | False | False | False | False | True |  |
| `level` | CharField | False | False | False | False | True |  |
| `description` | TextField | False | True | False | False | False |  |
| `competency_requirements` | TextField | False | True | False | False | False |  |
| `assessment_methods` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

## notifications

### notifications.Notification
- **DB Table**: `notifications_notification`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `recipient` | ForeignKey | False | False | False | False | False | users.User |
| `actor` | ForeignKey | True | True | False | False | False | users.User |
| `verb` | CharField | False | False | False | False | False |  |
| `title` | CharField | False | False | False | False | False |  |
| `body` | TextField | False | False | False | False | False |  |
| `channel` | CharField | False | False | False | False | True |  |
| `metadata` | JSONField | False | True | False | False | False |  |
| `read_at` | DateTimeField | True | True | False | False | False |  |
| `scheduled_for` | DateTimeField | True | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `recipient` (ForeignKey) -> `users.User` (related_name=notifications)
  - `actor` (ForeignKey) -> `users.User` (related_name=notifications_sent)

### notifications.NotificationPreference
- **DB Table**: `notifications_notificationpreference`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `user` | OneToOneField | False | False | False | True | False | users.User |
| `email_enabled` | BooleanField | False | False | False | False | False |  |
| `in_app_enabled` | BooleanField | False | False | False | False | False |  |
| `quiet_hours_start` | TimeField | True | True | False | False | False |  |
| `quiet_hours_end` | TimeField | True | True | False | False | False |  |

- **Relations**:
  - `user` (OneToOneField) -> `users.User` (related_name=notification_preferences)

## reports

### reports.ReportTemplate
- **DB Table**: `reports_reporttemplate`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `slug` | SlugField | False | False | False | True | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `template_name` | CharField | False | False | False | False | False |  |
| `default_params` | JSONField | False | True | False | False | False |  |

### reports.ScheduledReport
- **DB Table**: `reports_scheduledreport`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `template` | ForeignKey | False | False | False | False | False | reports.ReportTemplate |
| `created_by` | ForeignKey | False | False | False | False | False | users.User |
| `email_to` | CharField | False | False | False | False | False |  |
| `params` | JSONField | False | True | False | False | False |  |
| `cron` | CharField | False | False | False | False | False |  |
| `last_run_at` | DateTimeField | True | True | False | False | False |  |
| `next_run_at` | DateTimeField | True | True | False | False | False |  |
| `last_result` | JSONField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `template` (ForeignKey) -> `reports.ReportTemplate` (related_name=schedules)
  - `created_by` (ForeignKey) -> `users.User` (related_name=scheduled_reports)

## results

### results.Exam
- **DB Table**: `results_exam`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `title` | CharField | False | False | False | False | False |  |
| `exam_type` | CharField | False | False | False | False | True |  |
| `rotation` | ForeignKey | True | True | False | False | False | rotations.Rotation |
| `module_name` | CharField | False | True | False | False | False |  |
| `date` | DateField | False | False | False | False | False |  |
| `start_time` | TimeField | True | True | False | False | False |  |
| `duration_minutes` | IntegerField | True | True | False | False | False |  |
| `max_marks` | DecimalField | False | False | False | False | False |  |
| `passing_marks` | DecimalField | False | False | False | False | False |  |
| `requires_eligibility` | BooleanField | False | False | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `conducted_by` | ForeignKey | True | True | False | False | False | users.User |
| `instructions` | TextField | False | True | False | False | False |  |
| `remarks` | TextField | False | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `rotation` (ForeignKey) -> `rotations.Rotation` (related_name=exams)
  - `conducted_by` (ForeignKey) -> `users.User` (related_name=conducted_exams)

### results.Score
- **DB Table**: `results_score`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `exam` | ForeignKey | False | False | False | False | False | results.Exam |
| `student` | ForeignKey | False | False | False | False | False | users.User |
| `marks_obtained` | DecimalField | False | False | False | False | False |  |
| `percentage` | DecimalField | True | True | False | False | False |  |
| `grade` | CharField | False | True | False | False | True |  |
| `is_passing` | BooleanField | False | False | False | False | False |  |
| `is_eligible` | BooleanField | False | False | False | False | False |  |
| `ineligibility_reason` | CharField | False | True | False | False | False |  |
| `remarks` | TextField | False | True | False | False | False |  |
| `entered_by` | ForeignKey | True | True | False | False | False | users.User |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `exam` (ForeignKey) -> `results.Exam` (related_name=scores)
  - `student` (ForeignKey) -> `users.User` (related_name=exam_scores)
  - `entered_by` (ForeignKey) -> `users.User` (related_name=entered_scores)

## rotations

### rotations.HistoricalHospital
- **DB Table**: `rotations_historicalhospital`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `code` | CharField | True | True | False | False | False |  |
| `address` | TextField | False | True | False | False | False |  |
| `phone` | CharField | False | True | False | False | False |  |
| `email` | EmailField | False | True | False | False | False |  |
| `website` | URLField | False | True | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `facilities` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### rotations.HistoricalRotation
- **DB Table**: `rotations_historicalrotation`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `start_date` | DateField | False | False | False | False | False |  |
| `end_date` | DateField | False | False | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `objectives` | TextField | False | True | False | False | False |  |
| `learning_outcomes` | TextField | False | True | False | False | False |  |
| `requirements` | TextField | False | True | False | False | False |  |
| `completion_certificate` | TextField | True | True | False | False | False |  |
| `feedback` | TextField | False | True | False | False | False |  |
| `notes` | TextField | False | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `approved_at` | DateTimeField | True | True | False | False | False |  |
| `override_reason` | TextField | True | True | False | False | False |  |
| `utrmc_approved_at` | DateTimeField | True | True | False | False | False |  |
| `pg` | ForeignKey | True | True | False | False | False | users.User |
| `department` | ForeignKey | True | True | False | False | False | academics.Department |
| `hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `approved_by` | ForeignKey | True | True | False | False | False | users.User |
| `source_hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `source_department` | ForeignKey | True | True | False | False | False | academics.Department |
| `utrmc_approved_by` | ForeignKey | True | True | False | False | False | users.User |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=+)
  - `department` (ForeignKey) -> `academics.Department` (related_name=+)
  - `hospital` (ForeignKey) -> `rotations.Hospital` (related_name=+)
  - `supervisor` (ForeignKey) -> `users.User` (related_name=+)
  - `created_by` (ForeignKey) -> `users.User` (related_name=+)
  - `approved_by` (ForeignKey) -> `users.User` (related_name=+)
  - `source_hospital` (ForeignKey) -> `rotations.Hospital` (related_name=+)
  - `source_department` (ForeignKey) -> `academics.Department` (related_name=+)
  - `utrmc_approved_by` (ForeignKey) -> `users.User` (related_name=+)
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### rotations.Hospital
- **DB Table**: `rotations_hospital`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `name` | CharField | False | False | False | False | False |  |
| `code` | CharField | True | True | False | True | False |  |
| `address` | TextField | False | True | False | False | False |  |
| `phone` | CharField | False | True | False | False | False |  |
| `email` | EmailField | False | True | False | False | False |  |
| `website` | URLField | False | True | False | False | False |  |
| `description` | TextField | False | True | False | False | False |  |
| `facilities` | TextField | False | True | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

### rotations.HospitalDepartment
- **DB Table**: `rotations_hospitaldepartment`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `hospital` | ForeignKey | False | False | False | False | False | rotations.Hospital |
| `department` | ForeignKey | False | False | False | False | False | academics.Department |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `hospital` (ForeignKey) -> `rotations.Hospital` (related_name=hospital_departments)
  - `department` (ForeignKey) -> `academics.Department` (related_name=hospital_departments)

### rotations.Rotation
- **DB Table**: `rotations_rotation`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `pg` | ForeignKey | False | False | False | False | False | users.User |
| `department` | ForeignKey | False | False | False | False | False | academics.Department |
| `hospital` | ForeignKey | False | False | False | False | False | rotations.Hospital |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `start_date` | DateField | False | False | False | False | False |  |
| `end_date` | DateField | False | False | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `objectives` | TextField | False | True | False | False | False |  |
| `learning_outcomes` | TextField | False | True | False | False | False |  |
| `requirements` | TextField | False | True | False | False | False |  |
| `completion_certificate` | FileField | True | True | False | False | False |  |
| `feedback` | TextField | False | True | False | False | False |  |
| `notes` | TextField | False | True | False | False | False |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `approved_by` | ForeignKey | True | True | False | False | False | users.User |
| `approved_at` | DateTimeField | True | True | False | False | False |  |
| `source_hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `source_department` | ForeignKey | True | True | False | False | False | academics.Department |
| `override_reason` | TextField | True | True | False | False | False |  |
| `utrmc_approved_by` | ForeignKey | True | True | False | False | False | users.User |
| `utrmc_approved_at` | DateTimeField | True | True | False | False | False |  |

- **Relations**:
  - `pg` (ForeignKey) -> `users.User` (related_name=rotations)
  - `department` (ForeignKey) -> `academics.Department` (related_name=rotations)
  - `hospital` (ForeignKey) -> `rotations.Hospital` (related_name=rotations)
  - `supervisor` (ForeignKey) -> `users.User` (related_name=supervised_rotations)
  - `created_by` (ForeignKey) -> `users.User` (related_name=rotations_created)
  - `approved_by` (ForeignKey) -> `users.User` (related_name=rotations_approved)
  - `source_hospital` (ForeignKey) -> `rotations.Hospital` (related_name=rotations_source_hospital)
  - `source_department` (ForeignKey) -> `academics.Department` (related_name=rotations_source_department)
  - `utrmc_approved_by` (ForeignKey) -> `users.User` (related_name=rotations_utrmc_approved)

### rotations.RotationEvaluation
- **DB Table**: `rotations_rotationevaluation`
- **Status/State Fields**: `status`

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `rotation` | ForeignKey | False | False | False | False | False | rotations.Rotation |
| `evaluator` | ForeignKey | False | False | False | False | False | users.User |
| `evaluation_type` | CharField | False | False | False | False | True |  |
| `score` | IntegerField | True | True | False | False | False |  |
| `comments` | TextField | False | True | False | False | False |  |
| `recommendations` | TextField | False | True | False | False | False |  |
| `status` | CharField | False | False | False | False | True |  |
| `created_at` | DateTimeField | False | True | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

- **Relations**:
  - `rotation` (ForeignKey) -> `rotations.Rotation` (related_name=evaluations)
  - `evaluator` (ForeignKey) -> `users.User` (related_name=evaluations_given)

## search

### search.SavedSearchSuggestion
- **DB Table**: `search_savedsearchsuggestion`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `label` | CharField | False | False | False | True | False |  |
| `payload` | JSONField | False | True | False | False | False |  |
| `usage_count` | PositiveIntegerField | False | False | False | False | False |  |
| `updated_at` | DateTimeField | False | True | False | False | False |  |

### search.SearchQueryLog
- **DB Table**: `search_searchquerylog`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `user` | ForeignKey | False | False | False | False | False | users.User |
| `query` | CharField | False | False | False | False | False |  |
| `filters` | JSONField | False | True | False | False | False |  |
| `result_count` | PositiveIntegerField | False | False | False | False | False |  |
| `duration_ms` | PositiveIntegerField | False | False | False | False | False |  |
| `created_at` | DateTimeField | False | False | False | False | False |  |

- **Relations**:
  - `user` (ForeignKey) -> `users.User` (related_name=search_queries)

## sessions

### sessions.Session
- **DB Table**: `django_session`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `session_key` | CharField | False | False | True | True | False |  |
| `session_data` | TextField | False | False | False | False | False |  |
| `expire_date` | DateTimeField | False | False | False | False | False |  |

## users

### users.HistoricalUser
- **DB Table**: `users_historicaluser`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigIntegerField | False | True | False | False | False |  |
| `password` | CharField | False | False | False | False | False |  |
| `last_login` | DateTimeField | True | True | False | False | False |  |
| `is_superuser` | BooleanField | False | False | False | False | False |  |
| `username` | CharField | False | False | False | False | False |  |
| `first_name` | CharField | False | True | False | False | False |  |
| `last_name` | CharField | False | True | False | False | False |  |
| `email` | EmailField | False | True | False | False | False |  |
| `is_staff` | BooleanField | False | False | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `date_joined` | DateTimeField | False | False | False | False | False |  |
| `role` | CharField | False | False | False | False | True |  |
| `specialty` | CharField | True | True | False | False | True |  |
| `year` | CharField | True | True | False | False | True |  |
| `registration_number` | CharField | True | True | False | False | False |  |
| `phone_number` | CharField | True | True | False | False | False |  |
| `last_login_ip` | GenericIPAddressField | True | True | False | False | False |  |
| `is_archived` | BooleanField | False | False | False | False | False |  |
| `archived_date` | DateTimeField | True | True | False | False | False |  |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `home_hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `home_department` | ForeignKey | True | True | False | False | False | academics.Department |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `modified_by` | ForeignKey | True | True | False | False | False | users.User |
| `history_id` | AutoField | False | True | True | True | False |  |
| `history_date` | DateTimeField | False | False | False | False | False |  |
| `history_change_reason` | CharField | True | False | False | False | False |  |
| `history_type` | CharField | False | False | False | False | True |  |
| `history_user` | ForeignKey | True | False | False | False | False | users.User |

- **Relations**:
  - `supervisor` (ForeignKey) -> `users.User` (related_name=+)
  - `home_hospital` (ForeignKey) -> `rotations.Hospital` (related_name=+)
  - `home_department` (ForeignKey) -> `academics.Department` (related_name=+)
  - `created_by` (ForeignKey) -> `users.User` (related_name=+)
  - `modified_by` (ForeignKey) -> `users.User` (related_name=+)
  - `history_user` (ForeignKey) -> `users.User` (related_name=+)

### users.User
- **DB Table**: `users_user`
- **Status/State Fields**: None detected

| Field | Type | Null | Blank | PK | Unique | Choices | Relation |
|---|---|---:|---:|---:|---:|---:|---|
| `id` | BigAutoField | False | True | True | True | False |  |
| `password` | CharField | False | False | False | False | False |  |
| `last_login` | DateTimeField | True | True | False | False | False |  |
| `is_superuser` | BooleanField | False | False | False | False | False |  |
| `username` | CharField | False | False | False | True | False |  |
| `first_name` | CharField | False | True | False | False | False |  |
| `last_name` | CharField | False | True | False | False | False |  |
| `email` | EmailField | False | True | False | False | False |  |
| `is_staff` | BooleanField | False | False | False | False | False |  |
| `is_active` | BooleanField | False | False | False | False | False |  |
| `date_joined` | DateTimeField | False | False | False | False | False |  |
| `role` | CharField | False | False | False | False | True |  |
| `specialty` | CharField | True | True | False | False | True |  |
| `year` | CharField | True | True | False | False | True |  |
| `supervisor` | ForeignKey | True | True | False | False | False | users.User |
| `home_hospital` | ForeignKey | True | True | False | False | False | rotations.Hospital |
| `home_department` | ForeignKey | True | True | False | False | False | academics.Department |
| `registration_number` | CharField | True | True | False | False | False |  |
| `phone_number` | CharField | True | True | False | False | False |  |
| `created_by` | ForeignKey | True | True | False | False | False | users.User |
| `modified_by` | ForeignKey | True | True | False | False | False | users.User |
| `last_login_ip` | GenericIPAddressField | True | True | False | False | False |  |
| `is_archived` | BooleanField | False | False | False | False | False |  |
| `archived_date` | DateTimeField | True | True | False | False | False |  |
| `groups` | ManyToManyField | False | True | False | False | False | auth.Group |
| `user_permissions` | ManyToManyField | False | True | False | False | False | auth.Permission |

- **Relations**:
  - `supervisor` (ForeignKey) -> `users.User` (related_name=assigned_pgs)
  - `home_hospital` (ForeignKey) -> `rotations.Hospital` (related_name=home_pgs)
  - `home_department` (ForeignKey) -> `academics.Department` (related_name=home_pgs)
  - `created_by` (ForeignKey) -> `users.User` (related_name=users_created)
  - `modified_by` (ForeignKey) -> `users.User` (related_name=users_modified)
  - `groups` (ManyToManyField) -> `auth.Group` (related_name=user_set)
  - `user_permissions` (ManyToManyField) -> `auth.Permission` (related_name=user_set)

