# Serializers Payload Shapes

## sims.academics.serializers.BatchSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `name` | CharField | True | False | False | False |
| `program` | ChoiceField | True | False | False | False |
| `department` | PrimaryKeyRelatedField | True | False | False | False |
| `department_name` | CharField | False | True | False | False |
| `start_date` | DateField | True | False | False | False |
| `end_date` | DateField | True | False | False | False |
| `coordinator` | PrimaryKeyRelatedField | False | False | False | True |
| `coordinator_name` | CharField | False | True | False | False |
| `capacity` | IntegerField | False | False | False | False |
| `current_strength` | IntegerField | False | True | False | False |
| `is_full` | BooleanField | False | True | False | False |
| `active` | BooleanField | False | False | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "name": "string",
  "program": "choice_value",
  "department": 1,
  "start_date": "2026-01-01",
  "end_date": "2026-01-01",
  "coordinator": 1,
  "capacity": 1,
  "active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "program": "value",
  "department": "value",
  "department_name": "value",
  "start_date": "value",
  "end_date": "value",
  "coordinator": "value",
  "coordinator_name": "value",
  "capacity": "value",
  "current_strength": "value",
  "is_full": "value",
  "active": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.academics.serializers.DepartmentSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `name` | CharField | True | False | False | False |
| `code` | CharField | True | False | False | False |
| `description` | CharField | False | False | False | False |
| `head` | PrimaryKeyRelatedField | False | False | False | True |
| `head_name` | CharField | False | True | False | False |
| `active` | BooleanField | False | False | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "name": "string",
  "code": "string",
  "description": "string",
  "head": 1,
  "active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "code": "value",
  "description": "value",
  "head": "value",
  "head_name": "value",
  "active": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.academics.serializers.StudentProfileSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `user` | PrimaryKeyRelatedField | True | False | False | False |
| `user_name` | CharField | False | True | False | False |
| `user_email` | EmailField | False | True | False | False |
| `batch` | PrimaryKeyRelatedField | True | False | False | False |
| `batch_name` | CharField | False | True | False | False |
| `department_name` | CharField | False | True | False | False |
| `roll_number` | CharField | True | False | False | False |
| `admission_date` | DateField | True | False | False | False |
| `expected_graduation_date` | DateField | False | False | False | True |
| `actual_graduation_date` | DateField | False | False | False | True |
| `status` | ChoiceField | False | False | False | False |
| `status_updated_at` | DateTimeField | False | True | False | False |
| `cgpa` | DecimalField | False | False | False | True |
| `previous_institution` | CharField | False | False | False | False |
| `previous_qualification` | CharField | False | False | False | False |
| `emergency_contact_name` | CharField | False | False | False | False |
| `emergency_contact_phone` | CharField | False | False | False | False |
| `emergency_contact_relation` | CharField | False | False | False | False |
| `remarks` | CharField | False | False | False | False |
| `is_active` | BooleanField | False | True | False | False |
| `duration` | IntegerField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "user": 1,
  "batch": 1,
  "roll_number": "string",
  "admission_date": "2026-01-01",
  "expected_graduation_date": "2026-01-01",
  "actual_graduation_date": "2026-01-01",
  "status": "choice_value",
  "cgpa": "10.00",
  "previous_institution": "string",
  "previous_qualification": "string",
  "emergency_contact_name": "string",
  "emergency_contact_phone": "string",
  "emergency_contact_relation": "string",
  "remarks": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "user": "value",
  "user_name": "value",
  "user_email": "value",
  "batch": "value",
  "batch_name": "value",
  "department_name": "value",
  "roll_number": "value",
  "admission_date": "value",
  "expected_graduation_date": "value",
  "actual_graduation_date": "value",
  "status": "value",
  "status_updated_at": "value",
  "cgpa": "value",
  "previous_institution": "value",
  "previous_qualification": "value",
  "emergency_contact_name": "value",
  "emergency_contact_phone": "value",
  "emergency_contact_relation": "value",
  "remarks": "value",
  "is_active": "value",
  "duration": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.analytics.serializers.AnalyticsCardSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `key` | CharField | True | False | False | False |
| `title` | CharField | True | False | False | False |
| `value` | FloatField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "key": "string",
  "title": "string",
  "value": 1.5
}
```

Example response payload (synthetic):
```json
{
  "key": "value",
  "title": "value",
  "value": "value"
}
```

## sims.analytics.serializers.AnalyticsFilterOptionSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | True | False | False | False |
| `name` | CharField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "id": 1,
  "name": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value"
}
```

## sims.analytics.serializers.AnalyticsFiltersSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `roles` | ListField | True | False | False | False |
| `departments` | ListSerializer | True | False | False | False |
| `hospitals` | ListSerializer | True | False | False | False |

Example request payload (synthetic):
```json
{
  "roles": [],
  "departments": [],
  "hospitals": []
}
```

Example response payload (synthetic):
```json
{
  "roles": "value",
  "departments": "value",
  "hospitals": "value"
}
```

## sims.analytics.serializers.AnalyticsLivePayloadSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `date_range` | DictField | True | False | False | False |
| `cursor` | CharField | False | False | False | True |
| `events` | ListField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "date_range": "value",
  "cursor": "string",
  "events": []
}
```

Example response payload (synthetic):
```json
{
  "date_range": "value",
  "cursor": "value",
  "events": "value"
}
```

## sims.analytics.serializers.AnalyticsTabPayloadSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `title` | CharField | True | False | False | False |
| `date_range` | DictField | True | False | False | False |
| `cards` | ListSerializer | True | False | False | False |
| `table` | AnalyticsTableSerializer | True | False | False | False |
| `series` | ListField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "title": "string",
  "date_range": "value",
  "cards": [],
  "table": {},
  "series": []
}
```

Example response payload (synthetic):
```json
{
  "title": "value",
  "date_range": "value",
  "cards": "value",
  "table": "value",
  "series": "value"
}
```

## sims.analytics.serializers.AnalyticsTableSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `columns` | ListField | True | False | False | False |
| `rows` | ListField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "columns": [],
  "rows": []
}
```

Example response payload (synthetic):
```json
{
  "columns": "value",
  "rows": "value"
}
```

## sims.analytics.serializers.AnalyticsUIEventIngestSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `event_type` | CharField | True | False | False | False |
| `metadata` | DictField | False | False | False | False |
| `department_id` | IntegerField | False | False | False | True |
| `hospital_id` | IntegerField | False | False | False | True |
| `entity_type` | CharField | False | False | False | False |
| `entity_id` | CharField | False | False | False | False |
| `event_key` | CharField | False | False | False | False |
| `occurred_at` | DateTimeField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "event_type": "string",
  "metadata": "value",
  "department_id": 1,
  "hospital_id": 1,
  "entity_type": "string",
  "entity_id": "string",
  "event_key": "string",
  "occurred_at": "2026-01-01T00:00:00Z"
}
```

Example response payload (synthetic):
```json
{
  "event_type": "value",
  "metadata": "value",
  "department_id": "value",
  "hospital_id": "value",
  "entity_type": "value",
  "entity_id": "value",
  "event_key": "value",
  "occurred_at": "value"
}
```

## sims.analytics.serializers.ComparativeGroupSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `value` | FloatField | True | False | False | False |
| `total_entries` | IntegerField | True | False | False | False |
| `approved` | IntegerField | True | False | False | False |
| `average_score` | FloatField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "value": 1.5,
  "total_entries": 1,
  "approved": 1,
  "average_score": 1.5
}
```

Example response payload (synthetic):
```json
{
  "value": "value",
  "total_entries": "value",
  "approved": "value",
  "average_score": "value"
}
```

## sims.analytics.serializers.ComparativeResponseSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `primary` | ComparativeGroupSerializer | True | False | False | False |
| `secondary` | ComparativeGroupSerializer | True | False | False | False |

Example request payload (synthetic):
```json
{
  "primary": {},
  "secondary": {}
}
```

Example response payload (synthetic):
```json
{
  "primary": "value",
  "secondary": "value"
}
```

## sims.analytics.serializers.ComplianceDataSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `rotation_name` | CharField | True | False | False | False |
| `total_logs` | IntegerField | True | False | False | False |
| `verified_logs` | IntegerField | True | False | False | False |
| `verification_percentage` | FloatField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "rotation_name": "string",
  "total_logs": 1,
  "verified_logs": 1,
  "verification_percentage": 1.5
}
```

Example response payload (synthetic):
```json
{
  "rotation_name": "value",
  "total_logs": "value",
  "verified_logs": "value",
  "verification_percentage": "value"
}
```

## sims.analytics.serializers.DashboardComplianceSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `compliance` | ListSerializer | True | False | False | False |

Example request payload (synthetic):
```json
{
  "compliance": []
}
```

Example response payload (synthetic):
```json
{
  "compliance": "value"
}
```

## sims.analytics.serializers.DashboardOverviewSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `total_residents` | IntegerField | True | False | False | False |
| `active_rotations` | IntegerField | True | False | False | False |
| `pending_certificates` | IntegerField | True | False | False | False |
| `last_30d_logs` | IntegerField | True | False | False | False |
| `last_30d_cases` | IntegerField | True | False | False | False |
| `unverified_logs` | IntegerField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "total_residents": 1,
  "active_rotations": 1,
  "pending_certificates": 1,
  "last_30d_logs": 1,
  "last_30d_cases": 1,
  "unverified_logs": 1
}
```

Example response payload (synthetic):
```json
{
  "total_residents": "value",
  "active_rotations": "value",
  "pending_certificates": "value",
  "last_30d_logs": "value",
  "last_30d_cases": "value",
  "unverified_logs": "value"
}
```

## sims.analytics.serializers.DashboardTrendsSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `trends` | ListSerializer | True | False | False | False |

Example request payload (synthetic):
```json
{
  "trends": []
}
```

Example response payload (synthetic):
```json
{
  "trends": "value"
}
```

## sims.analytics.serializers.MonthlyTrendSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `month` | CharField | True | False | False | False |
| `department` | CharField | True | False | False | False |
| `case_count` | IntegerField | True | False | False | False |
| `log_count` | IntegerField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "month": "string",
  "department": "string",
  "case_count": 1,
  "log_count": 1
}
```

Example response payload (synthetic):
```json
{
  "month": "value",
  "department": "value",
  "case_count": "value",
  "log_count": "value"
}
```

## sims.analytics.serializers.PerformanceMetricsSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `total_entries` | FloatField | True | False | False | False |
| `pending` | FloatField | True | False | False | False |
| `approved` | FloatField | True | False | False | False |
| `approval_rate` | FloatField | True | False | False | False |
| `rejection_rate` | FloatField | True | False | False | False |
| `pending_rate` | FloatField | True | False | False | False |
| `average_review_hours` | FloatField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "total_entries": 1.5,
  "pending": 1.5,
  "approved": 1.5,
  "approval_rate": 1.5,
  "rejection_rate": 1.5,
  "pending_rate": 1.5,
  "average_review_hours": 1.5
}
```

Example response payload (synthetic):
```json
{
  "total_entries": "value",
  "pending": "value",
  "approved": "value",
  "approval_rate": "value",
  "rejection_rate": "value",
  "pending_rate": "value",
  "average_review_hours": "value"
}
```

## sims.analytics.serializers.TrendPointSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `date` | DateField | True | False | False | False |
| `count` | IntegerField | True | False | False | False |
| `approved` | IntegerField | True | False | False | False |
| `avg_score` | FloatField | True | False | False | True |
| `moving_average` | FloatField | True | False | False | True |

Example request payload (synthetic):
```json
{
  "date": "2026-01-01",
  "count": 1,
  "approved": 1,
  "avg_score": 1.5,
  "moving_average": 1.5
}
```

Example response payload (synthetic):
```json
{
  "date": "value",
  "count": "value",
  "approved": "value",
  "avg_score": "value",
  "moving_average": "value"
}
```

## sims.analytics.serializers.TrendResponseSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `metric` | CharField | True | False | False | False |
| `window` | IntegerField | True | False | False | False |
| `series` | ListSerializer | True | False | False | False |

Example request payload (synthetic):
```json
{
  "metric": "string",
  "window": 1,
  "series": []
}
```

Example response payload (synthetic):
```json
{
  "metric": "value",
  "window": "value",
  "series": "value"
}
```

## sims.audit.serializers.ActivityLogSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `actor` | PrimaryKeyRelatedField | False | True | False | True |
| `actor_display` | CharField | False | True | False | False |
| `action` | ChoiceField | False | True | False | False |
| `verb` | CharField | False | True | False | False |
| `target_object_id` | CharField | False | True | False | False |
| `target_repr` | CharField | False | True | False | False |
| `metadata` | JSONField | False | True | False | False |
| `ip_address` | IPAddressField | False | True | False | True |
| `is_sensitive` | BooleanField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "actor": "value",
  "actor_display": "value",
  "action": "value",
  "verb": "value",
  "target_object_id": "value",
  "target_repr": "value",
  "metadata": "value",
  "ip_address": "value",
  "is_sensitive": "value",
  "created_at": "value"
}
```

## sims.audit.serializers.AuditReportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `start` | DateTimeField | True | False | False | False |
| `end` | DateTimeField | True | False | False | False |
| `generated_at` | DateTimeField | False | True | False | False |
| `payload` | JSONField | False | True | False | False |
| `created_by` | PrimaryKeyRelatedField | False | True | False | True |

Example request payload (synthetic):
```json
{
  "start": "2026-01-01T00:00:00Z",
  "end": "2026-01-01T00:00:00Z"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "start": "value",
  "end": "value",
  "generated_at": "value",
  "payload": "value",
  "created_by": "value"
}
```

## sims.bulk.serializers.BulkAssignmentSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `entry_ids` | ListField | True | False | False | False |
| `supervisor_id` | IntegerField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "entry_ids": [],
  "supervisor_id": 1
}
```

Example response payload (synthetic):
```json
{
  "entry_ids": "value",
  "supervisor_id": "value"
}
```

## sims.bulk.serializers.BulkImportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `file` | FileField | True | False | False | False |
| `dry_run` | BooleanField | False | False | False | False |
| `allow_partial` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "file": "value",
  "dry_run": true,
  "allow_partial": true
}
```

Example response payload (synthetic):
```json
{
  "file": "value",
  "dry_run": "value",
  "allow_partial": "value"
}
```

## sims.bulk.serializers.BulkReviewSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `entry_ids` | ListField | True | False | False | False |
| `status` | ChoiceField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "entry_ids": [],
  "status": "choice_value"
}
```

Example response payload (synthetic):
```json
{
  "entry_ids": "value",
  "status": "value"
}
```

## sims.bulk.serializers.DepartmentImportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `file` | FileField | True | False | False | False |
| `dry_run` | BooleanField | False | False | False | False |
| `allow_partial` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "file": "value",
  "dry_run": true,
  "allow_partial": true
}
```

Example response payload (synthetic):
```json
{
  "file": "value",
  "dry_run": "value",
  "allow_partial": "value"
}
```

## sims.bulk.serializers.ResidentImportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `file` | FileField | True | False | False | False |
| `dry_run` | BooleanField | False | False | False | False |
| `allow_partial` | BooleanField | False | False | False | False |
| `generate_passwords` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "file": "value",
  "dry_run": true,
  "allow_partial": true,
  "generate_passwords": true
}
```

Example response payload (synthetic):
```json
{
  "file": "value",
  "dry_run": "value",
  "allow_partial": "value",
  "generate_passwords": "value"
}
```

## sims.bulk.serializers.SupervisorImportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `file` | FileField | True | False | False | False |
| `dry_run` | BooleanField | False | False | False | False |
| `allow_partial` | BooleanField | False | False | False | False |
| `generate_passwords` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "file": "value",
  "dry_run": true,
  "allow_partial": true,
  "generate_passwords": true
}
```

Example response payload (synthetic):
```json
{
  "file": "value",
  "dry_run": "value",
  "allow_partial": "value",
  "generate_passwords": "value"
}
```

## sims.bulk.serializers.TraineeImportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `file` | FileField | True | False | False | False |
| `dry_run` | BooleanField | False | False | False | False |
| `allow_partial` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "file": "value",
  "dry_run": true,
  "allow_partial": true
}
```

Example response payload (synthetic):
```json
{
  "file": "value",
  "dry_run": "value",
  "allow_partial": "value"
}
```

## sims.cases.api_serializers.CaseCategorySerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `name` | CharField | True | False | False | False |
| `description` | CharField | False | False | False | False |
| `color_code` | CharField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "name": "string",
  "description": "string",
  "color_code": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "description": "value",
  "color_code": "value"
}
```

## sims.cases.api_serializers.CaseReviewSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `status` | ChoiceField | True | False | False | False |
| `overall_feedback` | CharField | True | False | False | False |
| `clinical_reasoning_feedback` | CharField | False | False | False | False |
| `documentation_feedback` | CharField | False | False | False | False |
| `learning_points_feedback` | CharField | False | False | False | False |
| `strengths_identified` | CharField | False | False | False | False |
| `areas_for_improvement` | CharField | False | False | False | False |
| `recommendations` | CharField | False | False | False | False |
| `follow_up_required` | BooleanField | False | False | False | False |
| `clinical_knowledge_score` | IntegerField | False | False | False | True |
| `clinical_reasoning_score` | IntegerField | False | False | False | True |
| `documentation_score` | IntegerField | False | False | False | True |
| `overall_score` | IntegerField | False | False | False | True |

Example request payload (synthetic):
```json
{
  "status": "choice_value",
  "overall_feedback": "string",
  "clinical_reasoning_feedback": "string",
  "documentation_feedback": "string",
  "learning_points_feedback": "string",
  "strengths_identified": "string",
  "areas_for_improvement": "string",
  "recommendations": "string",
  "follow_up_required": true,
  "clinical_knowledge_score": 1,
  "clinical_reasoning_score": 1,
  "documentation_score": 1,
  "overall_score": 1
}
```

Example response payload (synthetic):
```json
{
  "status": "value",
  "overall_feedback": "value",
  "clinical_reasoning_feedback": "value",
  "documentation_feedback": "value",
  "learning_points_feedback": "value",
  "strengths_identified": "value",
  "areas_for_improvement": "value",
  "recommendations": "value",
  "follow_up_required": "value",
  "clinical_knowledge_score": "value",
  "clinical_reasoning_score": "value",
  "documentation_score": "value",
  "overall_score": "value"
}
```

## sims.cases.api_serializers.ClinicalCaseSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `case_title` | CharField | True | False | False | False |
| `status` | ChoiceField | False | True | False | False |
| `date_encountered` | DateField | True | False | False | False |
| `patient_age` | IntegerField | True | False | False | False |
| `patient_gender` | ChoiceField | True | False | False | False |
| `complexity` | ChoiceField | False | False | False | False |
| `chief_complaint` | CharField | True | False | False | False |
| `history_of_present_illness` | CharField | True | False | False | False |
| `physical_examination` | CharField | True | False | False | False |
| `management_plan` | CharField | True | False | False | False |
| `clinical_reasoning` | CharField | True | False | False | False |
| `learning_points` | CharField | True | False | False | False |
| `supervisor_feedback` | CharField | False | True | False | False |
| `category` | PrimaryKeyRelatedField | False | False | False | True |
| `category_name` | CharField | False | True | False | False |
| `primary_diagnosis` | PrimaryKeyRelatedField | False | False | False | True |
| `rotation` | PrimaryKeyRelatedField | False | False | False | True |
| `pg` | PrimaryKeyRelatedField | False | True | False | False |
| `pg_name` | CharField | False | True | False | False |
| `supervisor` | PrimaryKeyRelatedField | False | True | False | True |
| `supervisor_name` | CharField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |
| `reviewed_at` | DateTimeField | False | True | False | True |

Example request payload (synthetic):
```json
{
  "case_title": "string",
  "date_encountered": "2026-01-01",
  "patient_age": 1,
  "patient_gender": "choice_value",
  "complexity": "choice_value",
  "chief_complaint": "string",
  "history_of_present_illness": "string",
  "physical_examination": "string",
  "management_plan": "string",
  "clinical_reasoning": "string",
  "learning_points": "string",
  "category": 1,
  "primary_diagnosis": 1,
  "rotation": 1
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "case_title": "value",
  "status": "value",
  "date_encountered": "value",
  "patient_age": "value",
  "patient_gender": "value",
  "complexity": "value",
  "chief_complaint": "value",
  "history_of_present_illness": "value",
  "physical_examination": "value",
  "management_plan": "value",
  "clinical_reasoning": "value",
  "learning_points": "value",
  "supervisor_feedback": "value",
  "category": "value",
  "category_name": "value",
  "primary_diagnosis": "value",
  "rotation": "value",
  "pg": "value",
  "pg_name": "value",
  "supervisor": "value",
  "supervisor_name": "value",
  "created_at": "value",
  "updated_at": "value",
  "reviewed_at": "value"
}
```

## sims.certificates.api_serializers.CertificateSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `title` | CharField | True | False | False | False |
| `certificate_type_name` | CharField | False | True | False | False |
| `issue_date` | DateField | True | False | False | False |
| `status` | ChoiceField | False | False | False | False |
| `has_file` | SerializerMethodField | False | True | False | False |
| `file_name` | SerializerMethodField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "title": "string",
  "issue_date": "2026-01-01",
  "status": "choice_value"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "title": "value",
  "certificate_type_name": "value",
  "issue_date": "value",
  "status": "value",
  "has_file": "value",
  "file_name": "value"
}
```

## sims.logbook.api_serializers.PGLogbookEntrySerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `case_title` | CharField | True | False | False | False |
| `date` | DateField | True | False | False | False |
| `location_of_activity` | CharField | False | False | False | False |
| `patient_history_summary` | CharField | False | False | False | False |
| `management_action` | CharField | False | False | False | False |
| `topic_subtopic` | CharField | False | False | False | False |
| `status` | ChoiceField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |
| `supervisor_feedback` | CharField | False | True | False | False |
| `feedback` | CharField | False | True | False | False |
| `submitted_to_supervisor_at` | DateTimeField | False | True | False | True |
| `submitted_at` | DateTimeField | False | True | False | False |
| `verified_at` | DateTimeField | False | True | False | True |

Example request payload (synthetic):
```json
{
  "case_title": "string",
  "date": "2026-01-01",
  "location_of_activity": "string",
  "patient_history_summary": "string",
  "management_action": "string",
  "topic_subtopic": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "case_title": "value",
  "date": "value",
  "location_of_activity": "value",
  "patient_history_summary": "value",
  "management_action": "value",
  "topic_subtopic": "value",
  "status": "value",
  "created_at": "value",
  "updated_at": "value",
  "supervisor_feedback": "value",
  "feedback": "value",
  "submitted_to_supervisor_at": "value",
  "submitted_at": "value",
  "verified_at": "value"
}
```

## sims.logbook.api_serializers.PGLogbookEntryWriteSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `case_title` | CharField | True | False | False | False |
| `date` | DateField | True | False | False | False |
| `location_of_activity` | CharField | False | False | False | False |
| `patient_history_summary` | CharField | False | False | False | False |
| `management_action` | CharField | False | False | False | False |
| `topic_subtopic` | CharField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "case_title": "string",
  "date": "2026-01-01",
  "location_of_activity": "string",
  "patient_history_summary": "string",
  "management_action": "string",
  "topic_subtopic": "string"
}
```

Example response payload (synthetic):
```json
{
  "case_title": "value",
  "date": "value",
  "location_of_activity": "value",
  "patient_history_summary": "value",
  "management_action": "value",
  "topic_subtopic": "value"
}
```

## sims.notifications.serializers.NotificationMarkReadSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `notification_ids` | ListField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "notification_ids": []
}
```

Example response payload (synthetic):
```json
{
  "notification_ids": "value"
}
```

## sims.notifications.serializers.NotificationPreferenceSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `email_enabled` | BooleanField | False | False | False | False |
| `in_app_enabled` | BooleanField | False | False | False | False |
| `quiet_hours_start` | TimeField | False | False | False | True |
| `quiet_hours_end` | TimeField | False | False | False | True |

Example request payload (synthetic):
```json
{
  "email_enabled": true,
  "in_app_enabled": true,
  "quiet_hours_start": "value",
  "quiet_hours_end": "value"
}
```

Example response payload (synthetic):
```json
{
  "email_enabled": "value",
  "in_app_enabled": "value",
  "quiet_hours_start": "value",
  "quiet_hours_end": "value"
}
```

## sims.notifications.serializers.NotificationSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `verb` | CharField | True | False | False | False |
| `title` | CharField | True | False | False | False |
| `body` | CharField | True | False | False | False |
| `channel` | ChoiceField | False | False | False | False |
| `metadata` | JSONField | False | False | False | False |
| `is_read` | ReadOnlyField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "verb": "string",
  "title": "string",
  "body": "string",
  "channel": "choice_value",
  "metadata": "value"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "verb": "value",
  "title": "value",
  "body": "value",
  "channel": "value",
  "metadata": "value",
  "is_read": "value",
  "created_at": "value"
}
```

## sims.reports.serializers.ReportRequestSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `template_slug` | SlugField | True | False | False | False |
| `format` | ChoiceField | True | False | False | False |
| `params` | DictField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "template_slug": "sample-slug",
  "format": "choice_value",
  "params": "value"
}
```

Example response payload (synthetic):
```json
{
  "template_slug": "value",
  "format": "value",
  "params": "value"
}
```

## sims.reports.serializers.ReportTemplateSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `slug` | SlugField | True | False | False | False |
| `name` | CharField | True | False | False | False |
| `description` | CharField | False | False | False | False |
| `template_name` | CharField | True | False | False | False |
| `default_params` | JSONField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "slug": "sample-slug",
  "name": "string",
  "description": "string",
  "template_name": "string",
  "default_params": "value"
}
```

Example response payload (synthetic):
```json
{
  "slug": "value",
  "name": "value",
  "description": "value",
  "template_name": "value",
  "default_params": "value"
}
```

## sims.reports.serializers.ScheduledReportSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `template` | PrimaryKeyRelatedField | True | False | False | False |
| `email_to` | CharField | True | False | False | False |
| `params` | JSONField | False | False | False | False |
| `cron` | CharField | True | False | False | False |
| `last_run_at` | DateTimeField | False | True | False | True |
| `next_run_at` | DateTimeField | False | True | False | True |
| `is_active` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "template": 1,
  "email_to": "string",
  "params": "value",
  "cron": "string",
  "is_active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "template": "value",
  "email_to": "value",
  "params": "value",
  "cron": "value",
  "last_run_at": "value",
  "next_run_at": "value",
  "is_active": "value"
}
```

## sims.results.serializers.ExamSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `title` | CharField | True | False | False | False |
| `exam_type` | ChoiceField | False | False | False | False |
| `rotation` | PrimaryKeyRelatedField | False | False | False | True |
| `rotation_name` | CharField | False | True | False | False |
| `module_name` | CharField | False | False | False | False |
| `date` | DateField | True | False | False | False |
| `start_time` | TimeField | False | False | False | True |
| `duration_minutes` | IntegerField | False | False | False | True |
| `max_marks` | DecimalField | False | False | False | False |
| `passing_marks` | DecimalField | False | False | False | False |
| `requires_eligibility` | BooleanField | False | False | False | False |
| `status` | ChoiceField | False | False | False | False |
| `conducted_by` | PrimaryKeyRelatedField | False | False | False | True |
| `conducted_by_name` | CharField | False | True | False | False |
| `instructions` | CharField | False | False | False | False |
| `remarks` | CharField | False | False | False | False |
| `total_scores` | IntegerField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "title": "string",
  "exam_type": "choice_value",
  "rotation": 1,
  "module_name": "string",
  "date": "2026-01-01",
  "start_time": "value",
  "duration_minutes": 1,
  "max_marks": "10.00",
  "passing_marks": "10.00",
  "requires_eligibility": true,
  "status": "choice_value",
  "conducted_by": 1,
  "instructions": "string",
  "remarks": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "title": "value",
  "exam_type": "value",
  "rotation": "value",
  "rotation_name": "value",
  "module_name": "value",
  "date": "value",
  "start_time": "value",
  "duration_minutes": "value",
  "max_marks": "value",
  "passing_marks": "value",
  "requires_eligibility": "value",
  "status": "value",
  "conducted_by": "value",
  "conducted_by_name": "value",
  "instructions": "value",
  "remarks": "value",
  "total_scores": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.results.serializers.ScoreSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `exam` | PrimaryKeyRelatedField | True | False | False | False |
| `exam_title` | CharField | False | True | False | False |
| `exam_date` | DateField | False | True | False | False |
| `student` | PrimaryKeyRelatedField | True | False | False | False |
| `student_name` | CharField | False | True | False | False |
| `student_roll` | CharField | False | True | False | False |
| `marks_obtained` | DecimalField | True | False | False | False |
| `percentage` | DecimalField | False | True | False | True |
| `grade` | ChoiceField | False | True | False | False |
| `is_passing` | BooleanField | False | True | False | False |
| `is_eligible` | BooleanField | False | False | False | False |
| `ineligibility_reason` | CharField | False | False | False | False |
| `remarks` | CharField | False | False | False | False |
| `entered_by` | PrimaryKeyRelatedField | False | False | False | True |
| `entered_by_name` | CharField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "exam": 1,
  "student": 1,
  "marks_obtained": "10.00",
  "is_eligible": true,
  "ineligibility_reason": "string",
  "remarks": "string",
  "entered_by": 1
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "exam": "value",
  "exam_title": "value",
  "exam_date": "value",
  "student": "value",
  "student_name": "value",
  "student_roll": "value",
  "marks_obtained": "value",
  "percentage": "value",
  "grade": "value",
  "is_passing": "value",
  "is_eligible": "value",
  "ineligibility_reason": "value",
  "remarks": "value",
  "entered_by": "value",
  "entered_by_name": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.rotations.api_serializers.DepartmentRefSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | True | False | False | False |
| `name` | CharField | True | False | False | False |
| `code` | CharField | False | False | False | True |

Example request payload (synthetic):
```json
{
  "id": 1,
  "name": "string",
  "code": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "code": "value"
}
```

## sims.rotations.api_serializers.HospitalDepartmentSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `hospital` | HospitalRefSerializer | False | True | False | False |
| `department` | DepartmentRefSerializer | False | True | False | False |
| `hospital_id` | IntegerField | True | False | True | False |
| `department_id` | IntegerField | True | False | True | False |
| `is_active` | BooleanField | False | False | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "hospital_id": 1,
  "department_id": 1,
  "is_active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "hospital": "value",
  "department": "value",
  "is_active": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.rotations.api_serializers.HospitalRefSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | True | False | False | False |
| `name` | CharField | True | False | False | False |
| `code` | CharField | False | False | False | True |

Example request payload (synthetic):
```json
{
  "id": 1,
  "name": "string",
  "code": "string"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "code": "value"
}
```

## sims.rotations.api_serializers.HospitalSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `name` | CharField | True | False | False | False |
| `code` | CharField | False | False | False | True |
| `address` | CharField | False | False | False | False |
| `phone` | CharField | False | False | False | False |
| `email` | EmailField | False | False | False | False |
| `website` | URLField | False | False | False | False |
| `description` | CharField | False | False | False | False |
| `facilities` | CharField | False | False | False | False |
| `is_active` | BooleanField | False | False | False | False |
| `created_at` | DateTimeField | False | True | False | False |
| `updated_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{
  "name": "string",
  "code": "string",
  "address": "string",
  "phone": "string",
  "email": "user@example.com",
  "website": "https://example.com",
  "description": "string",
  "facilities": "string",
  "is_active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "code": "value",
  "address": "value",
  "phone": "value",
  "email": "value",
  "website": "value",
  "description": "value",
  "facilities": "value",
  "is_active": "value",
  "created_at": "value",
  "updated_at": "value"
}
```

## sims.rotations.api_serializers.RotationSummarySerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `name` | SerializerMethodField | False | True | False | False |
| `department` | SerializerMethodField | False | True | False | False |
| `hospital` | SerializerMethodField | False | True | False | False |
| `start_date` | DateField | True | False | False | False |
| `end_date` | DateField | True | False | False | False |
| `status` | ChoiceField | False | False | False | False |
| `supervisor_name` | SerializerMethodField | False | True | False | False |
| `source_department` | SerializerMethodField | False | True | False | False |
| `source_hospital` | SerializerMethodField | False | True | False | False |
| `requires_utrmc_approval` | SerializerMethodField | False | True | False | False |
| `override_reason` | CharField | False | False | False | True |
| `approved_by` | SerializerMethodField | False | True | False | False |
| `approved_at` | DateTimeField | False | False | False | True |
| `utrmc_approved_by` | PrimaryKeyRelatedField | False | False | False | True |
| `utrmc_approved_at` | DateTimeField | False | False | False | True |

Example request payload (synthetic):
```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-01-01",
  "status": "choice_value",
  "override_reason": "string",
  "approved_at": "2026-01-01T00:00:00Z",
  "utrmc_approved_by": 1,
  "utrmc_approved_at": "2026-01-01T00:00:00Z"
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "name": "value",
  "department": "value",
  "hospital": "value",
  "start_date": "value",
  "end_date": "value",
  "status": "value",
  "supervisor_name": "value",
  "source_department": "value",
  "source_hospital": "value",
  "requires_utrmc_approval": "value",
  "override_reason": "value",
  "approved_by": "value",
  "approved_at": "value",
  "utrmc_approved_by": "value",
  "utrmc_approved_at": "value"
}
```

## sims.search.serializers.SearchQueryLogSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `query` | CharField | False | True | False | False |
| `filters` | JSONField | False | True | False | False |
| `result_count` | IntegerField | False | True | False | False |
| `duration_ms` | IntegerField | False | True | False | False |
| `created_at` | DateTimeField | False | True | False | False |

Example request payload (synthetic):
```json
{}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "query": "value",
  "filters": "value",
  "result_count": "value",
  "duration_ms": "value",
  "created_at": "value"
}
```

## sims.search.serializers.SearchResultSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `module` | CharField | True | False | False | False |
| `object_id` | IntegerField | True | False | False | False |
| `title` | CharField | True | False | False | False |
| `summary` | CharField | True | False | False | False |
| `url` | CharField | True | False | False | False |
| `score` | FloatField | True | False | False | False |

Example request payload (synthetic):
```json
{
  "module": "string",
  "object_id": 1,
  "title": "string",
  "summary": "string",
  "url": "string",
  "score": 1.5
}
```

Example response payload (synthetic):
```json
{
  "module": "value",
  "object_id": "value",
  "title": "value",
  "summary": "value",
  "url": "value",
  "score": "value"
}
```

## sims.users.serializers.AssignedPGSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `username` | CharField | True | False | False | False |
| `full_name` | CharField | False | True | False | False |
| `email` | EmailField | False | False | False | False |
| `specialty` | ChoiceField | False | False | False | True |
| `year` | ChoiceField | False | False | False | True |
| `is_active` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "username": "string",
  "email": "user@example.com",
  "specialty": "choice_value",
  "year": "choice_value",
  "is_active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "username": "value",
  "full_name": "value",
  "email": "value",
  "specialty": "value",
  "year": "value",
  "is_active": "value"
}
```

## sims.users.serializers.UserDetailSerializer
- Introspection error: `Field name `bio` is not valid for model `User` in `sims.users.serializers.UserDetailSerializer`.`

## sims.users.serializers.UserRegistrationSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `username` | CharField | True | False | False | False |
| `email` | EmailField | True | False | False | False |
| `password` | CharField | True | False | True | False |
| `password2` | CharField | True | False | True | False |
| `first_name` | CharField | True | False | False | False |
| `last_name` | CharField | True | False | False | False |
| `role` | ChoiceField | True | False | False | False |
| `specialty` | ChoiceField | False | False | False | True |
| `year` | ChoiceField | False | False | False | True |
| `supervisor` | PrimaryKeyRelatedField | False | False | False | True |
| `registration_number` | CharField | False | False | False | True |
| `phone_number` | CharField | False | False | False | True |

Example request payload (synthetic):
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "password2": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "choice_value",
  "specialty": "choice_value",
  "year": "choice_value",
  "supervisor": 1,
  "registration_number": "string",
  "phone_number": "string"
}
```

Example response payload (synthetic):
```json
{
  "username": "value",
  "email": "value",
  "first_name": "value",
  "last_name": "value",
  "role": "value",
  "specialty": "value",
  "year": "value",
  "supervisor": "value",
  "registration_number": "value",
  "phone_number": "value"
}
```

## sims.users.serializers.UserSerializer
| Field | Type | Required | Read Only | Write Only | Nullable |
|---|---|---:|---:|---:|---:|
| `id` | IntegerField | False | True | False | False |
| `username` | CharField | True | False | False | False |
| `email` | EmailField | False | False | False | False |
| `first_name` | CharField | False | False | False | False |
| `last_name` | CharField | False | False | False | False |
| `full_name` | CharField | False | True | False | False |
| `display_name` | CharField | False | True | False | False |
| `role` | ChoiceField | True | False | False | False |
| `specialty` | ChoiceField | False | False | False | True |
| `year` | ChoiceField | False | False | False | True |
| `registration_number` | CharField | False | False | False | True |
| `phone_number` | CharField | False | False | False | True |
| `date_joined` | DateTimeField | False | True | False | False |
| `is_active` | BooleanField | False | False | False | False |

Example request payload (synthetic):
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "role": "choice_value",
  "specialty": "choice_value",
  "year": "choice_value",
  "registration_number": "string",
  "phone_number": "string",
  "is_active": true
}
```

Example response payload (synthetic):
```json
{
  "id": "value",
  "username": "value",
  "email": "value",
  "first_name": "value",
  "last_name": "value",
  "full_name": "value",
  "display_name": "value",
  "role": "value",
  "specialty": "value",
  "year": "value",
  "registration_number": "value",
  "phone_number": "value",
  "date_joined": "value",
  "is_active": "value"
}
```

