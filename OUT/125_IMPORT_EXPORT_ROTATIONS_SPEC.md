# OUT/125 — Import/Export Rotations Spec

Generated: 2026-03-01

## Overview
The bulk import engine (`sims/bulk/`) was extended with 3 new entity types for the training module.
All imports use the same endpoint pattern: `POST /api/bulk/import/{entity}/{action}/`
where `action` is `dry-run` or `apply`.

---

## Entities

### 1. Training Programs (`training-programs`)

**Template**: `/templates/training_programs.csv`

| Column | Required | Type | Notes |
|--------|----------|------|-------|
| `program_code` | ✅ | string (≤20 chars) | Must be unique |
| `program_name` | ✅ | string (≤200 chars) | |
| `duration_months` | ✅ | integer (>0) | Duration in months |
| `active` | | boolean (true/false) | Default: true |
| `description` | | string | Optional description |

**Validation rules**:
- `program_code` must be unique (dry-run checks; apply upserts by code)
- `duration_months` must be a positive integer
- Missing required fields → row failure

**Sample CSV**:
```csv
program_code,program_name,duration_months,active
INTMED,Internal Medicine,36,true
SURG,General Surgery,60,true
OBGYN,Obstetrics & Gynaecology,48,true
```

---

### 2. Rotation Templates (`rotation-templates`)

**Template**: `/templates/rotation_templates.csv`

| Column | Required | Type | Notes |
|--------|----------|------|-------|
| `program_code` | ✅ | string | Must match existing TrainingProgram.code |
| `template_name` | ✅ | string (≤200 chars) | |
| `department_code` | ✅ | string | Must match existing Department.code |
| `duration_weeks` | ✅ | integer (>0) | Duration in weeks |
| `required` | | boolean | Default: true |
| `sequence_order` | | integer | Sort order within program |
| `active` | | boolean | Default: true |

**Validation rules**:
- `program_code` must resolve to existing `TrainingProgram`
- `department_code` must resolve to existing `Department`
- Upsert by (program_code + template_name) — updates if exists

**Sample CSV**:
```csv
program_code,template_name,department_code,duration_weeks,required,sequence_order
INTMED,Medicine Rotation Block 1,INTMED,8,true,1
INTMED,Cardiology Block,CARDIO,4,false,2
SURG,General Surgery Core,SURG,12,true,1
```

---

### 3. Resident Training Records (`resident-training-records`)

**Template**: `/templates/resident_training_records.csv`

| Column | Required | Type | Notes |
|--------|----------|------|-------|
| `resident_email` | ✅ | email | Must match existing User with role pg/resident |
| `program_code` | ✅ | string | Must match existing TrainingProgram.code |
| `start_date` | ✅ | date (YYYY-MM-DD) | |
| `expected_end_date` | | date (YYYY-MM-DD) | |
| `current_level` | | string (≤20 chars) | e.g. Y1, Y2, Y3 |
| `active` | | boolean | Default: true |

**Validation rules**:
- `resident_email` must resolve to User with role in `[pg, resident]`
- `program_code` must resolve to existing `TrainingProgram`
- `start_date` must be valid date
- If `expected_end_date` provided: must be after `start_date`
- Existing active record for same resident+program → updates if found

**Sample CSV**:
```csv
resident_email,program_code,start_date,expected_end_date,current_level,active
john.doe@utrmc.pk,INTMED,2025-01-01,2028-01-01,Y1,true
jane.smith@utrmc.pk,SURG,2024-07-01,2029-07-01,Y2,true
```

---

## API Response Format

All import responses follow the `BulkOperation` schema:

```json
{
  "operation": "import",
  "status": "completed",
  "success_count": 3,
  "failure_count": 1,
  "details": {
    "successes": [
      {"row": 2, "code": "INTMED"},
      {"row": 3, "code": "SURG"}
    ],
    "failures": [
      {"row": 4, "error": "program_code 'UNKNOWN' not found"}
    ]
  },
  "created_at": "2026-03-01T05:00:00Z",
  "completed_at": "2026-03-01T05:00:01Z",
  "dry_run": true
}
```

---

## Export Endpoints

| Resource | Endpoint |
|----------|----------|
| Export Training Programs | GET `/api/bulk/exports/training_programs/` |
| Export Rotation Templates | GET `/api/bulk/exports/rotation_templates/` |
| Export Resident Training Records | GET `/api/bulk/exports/resident_training_records/` |

Response: CSV file download (`Content-Type: text/csv`)

---

## UI Location
Data Admin pages accessible at:
- `/dashboard/utrmc/data-admin/training-programs`
- `/dashboard/utrmc/data-admin/rotation-templates`
- `/dashboard/utrmc/data-admin/resident-training-records`

CSV template download links in `/dashboard/utrmc/data-admin/templates`

---

## Backend Implementation
- Service: `sims/bulk/services.py` — methods `import_training_programs()`, `import_rotation_templates()`, `import_resident_training_records()`
- View: `sims/bulk/views.py` — `_ENTITY_METHOD_MAP` extended with 3 training slugs
- All methods support `dry_run=True` mode (no DB writes)
- Error rows collected and returned; success rows committed (or skipped in dry-run)
