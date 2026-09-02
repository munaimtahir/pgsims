# Bulk Setup Import/Export Contract (Active UTRMC Surface)

Authoritative scope:
- active UTRMC admin surface only
- no legacy logbook/cases/reporting reactivation
- no new route family; workspace lives inside `/dashboard/utrmc`

## UI Surface

- Route: `/dashboard/utrmc`
- Visibility: `admin`, `utrmc_admin`
- Hidden for: `utrmc_user`, `supervisor`, `faculty`, `resident`, `pg`
- Workflow order:
  1. Hospitals
  2. Departments
  3. Hospital-Department Matrix
  4. Faculty & Supervisors
  5. Residents
  6. Supervision Links
  7. HOD Assignments

## Endpoints

- `GET /api/bulk/templates/{resource}/`
  - Returns CSV template for the requested resource
  - Allowed resources:
    - `hospitals`
    - `departments`
    - `matrix`
    - `faculty-supervisors`
    - `residents`
    - `supervision-links`
    - `hod-assignments`
- `POST /api/bulk/import/{entity}/dry-run/`
  - Validates the uploaded CSV/XLSX and returns row-level successes/failures without DB writes
- `POST /api/bulk/import/{entity}/apply/`
  - Applies row-level upserts to the canonical active models
- `GET /api/bulk/exports/{resource}/?file_format=csv|xlsx`
  - Exports the current active-surface dataset in import-compatible column order

## Permission Rules

- Import/template/export:
  - allowed: `admin`, `utrmc_admin`
  - denied: `utrmc_user`, `supervisor`, `faculty`, `resident`, `pg`

## Response Shape

Successful dry-run or apply response:

```json
{
  "operation": "import",
  "status": "completed",
  "success_count": 1,
  "failure_count": 0,
  "details": {
    "successes": [],
    "failures": []
  },
  "dry_run": true
}
```

Notes:
- `successes` and `failures` are row-oriented and intended for admin reconciliation.
- Generated temporary passwords may appear in apply results when a new user row omits `password`.

## Entity Contracts

### Hospitals

Columns:
- `hospital_code` required
- `hospital_name` required
- `address` optional
- `phone` optional
- `email` optional
- `active` optional

Writes:
- upserts `rotations.Hospital`

### Departments

Columns:
- `department_code` required
- `department_name` required
- `description` optional
- `active` optional

Writes:
- upserts canonical `academics.Department`
- does not create matrix rows implicitly

### Matrix

Columns:
- `hospital_code` required
- `department_code` required
- `active` optional

Writes:
- upserts `rotations.HospitalDepartment`
- requires referenced hospital and department to already exist

### Faculty & Supervisors

Columns:
- `email` required
- `full_name` required
- `phone_number` optional
- `role` required: `faculty` or `supervisor`
- `specialty` optional
- `department_code` optional
- `hospital_code` optional
- `designation` optional
- `registration_number` optional
- `username` optional
- `password` optional
- `active` optional
- `start_date` optional

Writes:
- upserts `users.User`
- upserts `users.StaffProfile`
- if `department_code` present: upserts active primary `users.DepartmentMembership`
- if `hospital_code` and `department_code` present: upserts active `users.HospitalAssignment` with `faculty_site`

### Residents

Columns:
- `email` required
- `full_name` required
- `phone_number` optional
- `role` optional: `resident` or `pg` (defaults to `resident`)
- `specialty` required
- `year` required
- `pgr_id` optional
- `training_start` required
- `training_end` optional
- `training_level` optional
- `department_code` optional
- `hospital_code` optional
- `supervisor_email` optional
- `username` optional
- `password` optional
- `active` optional

Writes:
- upserts `users.User`
- upserts `users.ResidentProfile`
- if `department_code` present: upserts active primary `users.DepartmentMembership`
- if `hospital_code` and `department_code` present: upserts active `users.HospitalAssignment` with `primary_training`
- if `supervisor_email` present: sets `users.User.supervisor`

### Supervision Links

Columns:
- `supervisor_email` required
- `resident_email` required
- `department_code` optional
- `start_date` required
- `end_date` optional
- `active` optional

Writes:
- upserts `users.SupervisorResidentLink`
- supervisor must be `faculty` or `supervisor`
- resident must be `resident` or `pg`

### HOD Assignments

Columns:
- `department_code` required
- `hod_email` required
- `start_date` required
- `end_date` optional
- `active` optional

Writes:
- upserts the active `users.HODAssignment` for the target department
- HOD user must be `faculty` or `supervisor`

## Export Truth

- Export columns match the import templates for the same resource.
- Export is intended for reconciliation and round-trip correction, not for legacy reporting.
