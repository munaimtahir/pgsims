# 74 — API Contract Summary (Userbase)

## Auth
- `GET /api/auth/me/`
  - returns current user management payload (`id, username, email, role, specialty, year, departments[]`, etc.).

## Master Data Payloads
- Hospital:
  - request/response core: `name, code, active`
- Department:
  - request/response core: `name, code, description, active`
- HospitalDepartment:
  - request: `hospital_id, department_id, active`
  - response: nested `hospital`, nested `department`, plus `active`

## User Payload
- `POST /api/users/`
  - core: `username, email, password, first_name, last_name, role, specialty?, year?`
  - optional nested:
    - `resident_profile { training_start, training_end?, training_level?, pgr_id? }`
    - `staff_profile { designation?, phone?, active? }`
- `GET /api/users/` supports filters:
  - `role`, `department`, `active`, `search`

## Profiles
- `PATCH /api/residents/{user_id}/`:
  - `pgr_id, training_start, training_end, training_level, active`
- `PATCH /api/staff/{user_id}/`:
  - `designation, phone, active`

## Memberships/Assignments
- `POST /api/department-memberships/`
  - `user_id, department_id, member_type, is_primary, start_date, end_date?, active`
- `POST /api/hospital-assignments/`
  - `user_id, hospital_department_id, assignment_type, start_date, end_date?, active`

## Linking
- `POST /api/supervision-links/`
  - `supervisor_user_id, resident_user_id, department_id?, start_date, end_date?, active`
- `POST /api/hod-assignments/`
  - `department_id, hod_user_id, start_date, end_date?, active`

## Roster Response
- `GET /api/departments/{id}/roster/`:
```json
{
  "department": {"id": 1, "name": "Medicine", "code": "MED", "active": true},
  "hod": {"id": 2, "username": "faculty_x", "full_name": "Faculty X", "start_date": "2026-01-01", "end_date": null},
  "faculty": [{"id": 2, "username": "faculty_x", "role": "faculty"}],
  "supervisors": [{"id": 3, "username": "sup_x", "role": "supervisor"}],
  "residents": [{"id": 4, "username": "res_x", "role": "resident"}]
}
```

## OpenAPI Export
- Regenerated file: `OUT/openapi.json`
- Includes all required userbase endpoints and schemas.
