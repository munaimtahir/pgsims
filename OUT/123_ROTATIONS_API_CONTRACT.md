# OUT/123 — Rotations API Contract

Generated: 2026-03-01

## Base URL
All endpoints prefixed with `/api/` (same-origin, Caddy proxies to backend:8014).

## Authentication
JWT Bearer token via `POST /api/auth/login/`

---

## Training Programs

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/programs/` | all authenticated | List programs |
| POST | `/api/programs/` | admin, utrmc_admin | Create program |
| GET | `/api/programs/{id}/` | all authenticated | Get program |
| PATCH | `/api/programs/{id}/` | admin, utrmc_admin | Update program |

### Program payload
```json
{
  "id": 1,
  "name": "Internal Medicine",
  "code": "INTMED",
  "duration_months": 36,
  "description": "",
  "active": true
}
```

---

## Rotation Templates

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/program-templates/` | all authenticated | List templates |
| POST | `/api/program-templates/` | admin, utrmc_admin | Create template |
| PATCH | `/api/program-templates/{id}/` | admin, utrmc_admin | Update template |

### Template payload
```json
{
  "id": 1,
  "program": 1,
  "program_name": "Internal Medicine",
  "name": "Medicine Block A",
  "department": 5,
  "department_name": "Internal Medicine",
  "duration_weeks": 8,
  "required": true,
  "sequence_order": null,
  "active": true
}
```

---

## Resident Training Records

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/resident-training/` | admin, utrmc_admin see all; resident sees own | List records |
| POST | `/api/resident-training/` | admin, utrmc_admin | Create record |
| PATCH | `/api/resident-training/{id}/` | admin, utrmc_admin | Update record |

### Resident Training Record payload
```json
{
  "id": 1,
  "resident_user": 27,
  "resident_name": "Dr. John Smith",
  "program": 1,
  "program_name": "Internal Medicine",
  "program_code": "INTMED",
  "start_date": "2026-01-01",
  "expected_end_date": null,
  "current_level": "Y1",
  "active": true
}
```

---

## Rotation Assignments

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/rotations/` | scoped by role | List assignments |
| POST | `/api/rotations/` | admin, utrmc_admin | Create draft |
| PATCH | `/api/rotations/{id}/` | admin, utrmc_admin (DRAFT/RETURNED only) | Update |
| POST | `/api/rotations/{id}/submit/` | admin, utrmc_admin, owner | Submit |
| POST | `/api/rotations/{id}/hod-approve/` | supervisor, faculty, admin | HOD approve |
| POST | `/api/rotations/{id}/utrmc-approve/` | admin, utrmc_admin | UTRMC final approve |
| POST | `/api/rotations/{id}/activate/` | admin, utrmc_admin | Activate |
| POST | `/api/rotations/{id}/complete/` | admin, utrmc_admin | Complete |
| POST | `/api/rotations/{id}/return/` | supervisor, admin | Return with reason |
| POST | `/api/rotations/{id}/reject/` | admin, utrmc_admin | Reject |

### RotationAssignment payload
```json
{
  "id": 1,
  "resident_training": 1,
  "resident_name": "Dr. John Smith",
  "hospital_department": 56,
  "hospital_name": "UTRMC Main Hospital",
  "department_name": "Internal Medicine",
  "template": null,
  "start_date": "2027-01-01",
  "end_date": "2027-04-01",
  "status": "APPROVED",
  "requested_by": 27,
  "approved_by_hod": 5,
  "approved_by_utrmc": 25,
  "submitted_at": "2026-03-01T05:14:00Z",
  "approved_at": "2026-03-01T05:16:00Z",
  "completed_at": null,
  "return_reason": ""
}
```

### Status state machine
```
DRAFT → SUBMITTED → APPROVED (via hod-approve) → APPROVED (via utrmc-approve) → ACTIVE → COMPLETED
                  ↓
               RETURNED (via return/)
               REJECTED (via reject/)
```

---

## Leave Requests

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/leaves/` | scoped by role | List leaves |
| POST | `/api/leaves/` | resident, admin, utrmc_admin | Create draft |
| PATCH | `/api/leaves/{id}/` | owner or admin | Update draft |
| POST | `/api/leaves/{id}/submit/` | resident owner or admin | Submit |
| POST | `/api/leaves/{id}/approve/` | supervisor, admin, utrmc_admin | Approve |
| POST | `/api/leaves/{id}/reject/` | supervisor, admin, utrmc_admin | Reject |

### LeaveRequest payload
```json
{
  "id": 1,
  "resident_training": 1,
  "resident_name": "Dr. John Smith",
  "leave_type": "annual",
  "start_date": "2027-05-01",
  "end_date": "2027-05-07",
  "reason": "Annual vacation",
  "status": "APPROVED",
  "approved_by": 25,
  "approved_at": "2026-03-01T06:00:00Z",
  "reject_reason": ""
}
```

### Leave types: `annual`, `sick`, `casual`, `study`, `maternity`, `other`

---

## Deputation / Off-Service Postings

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/postings/` | scoped by role | List postings |
| POST | `/api/postings/` | resident, admin, utrmc_admin | Create |
| PATCH | `/api/postings/{id}/` | owner or admin | Update |
| POST | `/api/postings/{id}/approve/` | admin, utrmc_admin | Approve |
| POST | `/api/postings/{id}/reject/` | admin, utrmc_admin | Reject |
| POST | `/api/postings/{id}/complete/` | admin, utrmc_admin | Complete |

---

## Approval Inboxes (Read-only)

| Method | Endpoint | Roles | Description |
|--------|----------|-------|-------------|
| GET | `/api/utrmc/approvals/rotations/` | admin, utrmc_admin | Pending rotations |
| GET | `/api/utrmc/approvals/leaves/` | admin, utrmc_admin, supervisor | Pending leaves |
| GET | `/api/my/rotations/` | resident | Own rotation schedule |
| GET | `/api/my/leaves/` | resident | Own leave requests |
| GET | `/api/supervisor/rotations/pending/` | supervisor, faculty | Dept pending rotations |

---

## Bulk Import (reuses existing bulk engine)

| Method | Endpoint | Entity Slug | Description |
|--------|----------|-------------|-------------|
| POST | `/api/bulk/import/training-programs/dry-run/` | training-programs | Validate CSV |
| POST | `/api/bulk/import/training-programs/apply/` | training-programs | Import programs |
| POST | `/api/bulk/import/rotation-templates/dry-run/` | rotation-templates | Validate CSV |
| POST | `/api/bulk/import/rotation-templates/apply/` | rotation-templates | Import templates |
| POST | `/api/bulk/import/resident-training-records/dry-run/` | resident-training-records | Validate CSV |
| POST | `/api/bulk/import/resident-training-records/apply/` | resident-training-records | Import records |
| GET | `/api/bulk/exports/training_programs/` | training-programs | Export all programs |
| GET | `/api/bulk/exports/rotation_templates/` | rotation-templates | Export all templates |
| GET | `/api/bulk/exports/resident_training_records/` | resident-training-records | Export all records |

---

## Error responses
- `400 Bad Request`: Validation error (e.g. overlap, status transition)
- `401 Unauthorized`: No token
- `403 Forbidden`: Role not allowed
- `404 Not Found`: Object not found or out of scope (queryset-filtered)
