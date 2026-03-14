# API Contract (v1) — PGSIMS (Simplified Names)

## Auth
- JWT Bearer token
- Client sends: `Authorization: Bearer <token>`

## Roles (locked)
- `pg`
- `supervisor`
- `admin` (technical)
- `utrmc_user` (read-only oversight dashboards/logs/reports/stats)
- `utrmc_admin` (UTRMC super-admin: can configure + approve overrides)

## LogbookEntry (Phase-1)
Required fields in PG-facing responses:
- `id`
- `status`
- `supervisor_feedback` (nullable)
- `feedback` (alias of supervisor_feedback)
- `submitted_to_supervisor_at` (nullable)
- `submitted_at` (alias of submitted_to_supervisor_at)
- `verified_at` (nullable)

Status enum (backend):
- `draft`, `pending`(UI=Submitted), `returned`, `rejected`, `approved`, `archived`

Edit rule:
- PG can edit only when status in `draft`, `returned`

Verify:
- PATCH `/api/logbook/<id>/verify/`
- Payload: `action` (approved/returned/rejected), `feedback` (preferred), `supervisor_feedback` (alias)

## Rotation (next phase)
Rotation summary response must include:
- `id`
- `start_date`, `end_date`
- `status`
- `department`: { id, name, code }
- `hospital`: { id, name, code }
- Optional: `source_department`, `source_hospital`
- `requires_utrmc_approval` (bool)
- `override_reason` (nullable)
- `approved_by`, `approved_at` (nullable)

## Userbase + Org Graph (v1)

### Roles
- Canonical role semantics supported by API:
  - `admin`, `utrmc_admin`, `utrmc_user`, `supervisor`, `faculty`, `resident`
- Backward compatibility:
  - `pg` remains accepted as resident-equivalent for legacy flows.

### Auth
- `GET /api/auth/me/` returns current authenticated user payload.

### Master Data
- Hospitals:
  - `GET/POST /api/hospitals/`
  - `GET/PATCH /api/hospitals/{id}/`
  - Fields: `id, name, code, active, created_at, updated_at`
- Departments:
  - `GET/POST /api/departments/`
  - `GET/PATCH /api/departments/{id}/`
  - Fields: `id, name, code, description, active, created_at, updated_at`
- HospitalDepartment matrix:
  - `GET/POST /api/hospital-departments/`
  - `GET/PATCH /api/hospital-departments/{id}/`
  - Fields: `id, hospital, department, active, created_at, updated_at`

### Users + Profiles
- Users:
  - `GET/POST /api/users/`
  - `GET/PATCH /api/users/{id}/`
  - Filters: `role`, `department`, `active`, `search`
- Resident profiles:
  - `GET/PATCH /api/residents/{user_id}/`
- Staff profiles:
  - `GET/PATCH /api/staff/{user_id}/`

### Memberships + Assignments
- Department memberships:
  - `GET/POST /api/department-memberships/`
  - `PATCH/DELETE /api/department-memberships/{id}/` (`DELETE` = soft deactivate)
- Hospital assignments:
  - `GET/POST /api/hospital-assignments/`
  - `PATCH/DELETE /api/hospital-assignments/{id}/` (`DELETE` = soft deactivate)

### Linking
- Supervisor links:
  - `GET/POST /api/supervision-links/`
  - `PATCH /api/supervision-links/{id}/`
- HOD assignments:
  - `GET/POST /api/hod-assignments/`
  - `PATCH /api/hod-assignments/{id}/`

### Rosters
- `GET /api/departments/{id}/roster/`
  - Response includes:
    - `department`
    - `hod` (nullable)
    - `faculty[]`
    - `supervisors[]`
    - `residents[]`
- `GET /api/hospitals/{id}/departments/`

## Analytics (v1)
Base: `/api/analytics/`

Read endpoints:
- `GET /v1/filters/`
- `GET /v1/tabs/{tab}/` where tab in:
  - `overview`, `adoption`, `logbook`, `review-sla`, `departments`,
    `rotations`, `research`, `data-ops`, `system`, `security`, `live`
- `GET /v1/tabs/{tab}/export/` (CSV)
- `GET /v1/live/`
- `GET /events/live`
- `GET /v1/quality/`

Ingest:
- `POST /events/` for UI events (flag-gated)
  - accepted inbound: `page.view`, `feature.used`, `ui.page.view`, `ui.feature.used`
  - normalized storage: `ui.page.view`, `ui.feature.used`

Query params (where applicable):
- `start_date` (YYYY-MM-DD; default last 14 days)
- `end_date` (YYYY-MM-DD)
- `department_id` (optional)
- `hospital_id` (optional)
- `role` (optional)
- `limit` (live endpoint, max 200)
- `cursor` (`occurred_at|id`, live endpoint)
- `event_type_prefix` (live endpoint)
- `entity_type` (live endpoint)

Response shape for tab endpoints:
- `title`
- `date_range` { `start_date`, `end_date` }
- `cards` [ { `key`, `title`, `value` } ]
- `table` { `columns`, `rows` }
- `series` [object]

Response shape for `GET /events/live`:
- `date_range` { `start_date`, `end_date` }
- `cursor` (nullable)
- `events` [ { `id`, `occurred_at`, `event_type`, `actor_role`, `department_id`, `hospital_id`, `entity_type`, `entity_id`, `drilldown_url`, `metadata` } ]

---

## Phase 6 — Academic Core (2026-03-01)

### Program Policy
- `GET /api/programs/{id}/policy/` — get policy (admin/utrmc_admin only)
- `PUT /api/programs/{id}/policy/` — update policy

### Program Milestones
- `GET /api/programs/{id}/milestones/` — list milestones
- `POST /api/programs/{id}/milestones/` — create milestone

### Resident Research Project
- `GET /api/my/research/` — get own research project
- `POST /api/my/research/` — create research project (resident)
- `PATCH /api/my/research/` — update draft project
- `POST /api/my/research/action/{action}/` — state transition; actions: `submit-to-supervisor`, `supervisor-approve`, `supervisor-return`, `submit-to-university`, `accept-by-university`, `return-to-draft`
  - `supervisor-approve` payload: `{ "project_id": int, "feedback": str }`
  - `supervisor-return` payload: `{ "project_id": int, "feedback": str }`
  - `return-to-draft` is retained as a backward-compatible alias for supervisor return.

### Supervisor Research Approvals
- `GET /api/supervisor/research-approvals/` — list residents' projects (supervisor/faculty/hod)
  - Response rows include `resident_name` for display.

### Thesis
- `GET /api/my/thesis/` — get own thesis record
- `POST /api/my/thesis/` — create thesis record
- `POST /api/my/thesis/submit/` — submit thesis

### Workshop Completions
- `GET /api/my/workshops/` — list completions (paginated: count, results)
- `POST /api/my/workshops/` — record manual completion; payload: `{ workshop, completed_at, notes? }`
- `GET /api/my/workshops/{id}/` — detail
- `DELETE /api/my/workshops/{id}/` — remove

### Eligibility
- `GET /api/my/eligibility/` — resident's eligibility snapshots (triggers recompute)
  - Response shape:
    - `{ resident_training_record, program: {id, code, name}, current_month_index, eligibilities: MilestoneEligibility[] }`
  - `MilestoneEligibility` item shape:
    - `{ id, resident_training_record, resident_name, milestone, milestone_code, milestone_name, status, status_display, reasons: string[], computed_at }`
- `GET /api/utrmc/eligibility/` — all records; query params: `status`, `program`, `department`
  - Response shape: `{ count, results: MilestoneEligibility[] }`

### System Settings
- `GET /api/system/settings/` — returns `{ WORKSHOP_MANAGEMENT_ENABLED: bool, ... }`

### Eligibility Status Values
- `NOT_READY` — all requirements unmet
- `PARTIALLY_READY` — some requirements met
- `ELIGIBLE` — all requirements met

---

## Phase 7 — Rotation & Leave Workflow (2026-03-07)

### Auth Profile (Canonical)

> **Note:** `/api/auth/profile/` is the canonical current-user endpoint used by the frontend. `/api/auth/me/` returns a richer management payload (includes `home_department`, `home_hospital`, `supervisor`, `departments` memberships) and is used by admin tooling.

- `GET /api/auth/profile/` — current authenticated user (canonical)
  - Response: `{ id, username, email, first_name, last_name, full_name, display_name, role, specialty, year, registration_number, phone_number, date_joined, is_active }`
  - Auth: any authenticated user
- `PATCH /api/auth/profile/` — update own profile fields
- `POST /api/auth/change-password/` — change own password; payload: `{ old_password, new_password }`
- `POST /api/auth/password-reset/` — request password reset email; payload: `{ email }`
- `POST /api/auth/password-reset/confirm/` — confirm reset; payload: `{ uid, token, new_password, new_password2 }`

### Rotation Assignments

- `GET /api/rotations/` — list rotations; query params: `pg`, `department`, `hospital`, `status`
  - Roles: admin, utrmc_admin, utrmc_user, supervisor (own residents), pg (own only)
- `POST /api/rotations/` — create rotation assignment
  - Payload: `{ pg: int, department: int, hospital: int, start_date: str, end_date: str, override_reason?: str }`
  - Roles: admin, utrmc_admin
- `GET /api/rotations/{id}/` — retrieve single rotation
- `PATCH /api/rotations/{id}/` — update rotation fields (admin/utrmc_admin only)
- `DELETE /api/rotations/{id}/` — delete rotation (admin only)
- `POST /api/rotations/{id}/submit/` — resident submits for approval; Roles: pg/resident
- `POST /api/rotations/{id}/hod-approve/` — HOD or admin approves; Roles: supervisor (HOD), admin
- `POST /api/rotations/{id}/utrmc-approve/` — UTRMC admin approves override; Roles: admin, utrmc_admin
  - Payload (optional): `{ override_reason?: str }`
- `POST /api/rotations/{id}/activate/` — admin activates approved rotation; Roles: admin, utrmc_admin
- `POST /api/rotations/{id}/complete/` — admin marks rotation complete; Roles: admin, utrmc_admin
- `POST /api/rotations/{id}/returned/` — return to draft for correction; Roles: admin, utrmc_admin, supervisor
- `POST /api/rotations/{id}/reject/` — reject rotation; Roles: admin, utrmc_admin

### My Rotations (Resident)

- `GET /api/my/rotations/` — resident's own rotations; Roles: pg/resident

### Supervisor Rotations

- `GET /api/supervisor/rotations/pending/` — pending rotations for supervisor's residents; Roles: supervisor

### UTRMC Approval Inboxes

- `GET /api/utrmc/approvals/rotations/` — rotations awaiting UTRMC approval; Roles: admin, utrmc_admin
- `GET /api/utrmc/approvals/leaves/` — leaves awaiting UTRMC review; Roles: admin, utrmc_admin

### Leave Requests

- `GET /api/leaves/` — list leave requests
  - Roles: admin, utrmc_admin, utrmc_user, supervisor (own residents), pg (own only)
- `POST /api/leaves/` — create leave request
  - Payload: `{ leave_type: str, start_date: str, end_date: str, reason?: str }`
  - Roles: pg/resident
- `GET /api/leaves/{id}/` — retrieve single leave
- `PATCH /api/leaves/{id}/` — update draft leave; Roles: pg (own, draft only)
- `DELETE /api/leaves/{id}/` — delete draft leave; Roles: pg (own, draft only)
- `POST /api/leaves/{id}/submit/` — submit for approval; Roles: pg/resident
- `POST /api/leaves/{id}/approve/` — approve leave; Roles: supervisor, admin
- `POST /api/leaves/{id}/reject/` — reject leave; payload: `{ reason?: str }`; Roles: supervisor, admin

### My Leaves (Resident)

- `GET /api/my/leaves/` — resident's own leave requests; Roles: pg/resident

### Deputation Postings

- `GET /api/postings/` — list postings; Roles: admin, utrmc_admin, utrmc_user
- `POST /api/postings/` — create posting; payload: `{ pg: int, institution: str, start_date: str, end_date: str, purpose?: str }`; Roles: admin, utrmc_admin
- `GET /api/postings/{id}/` — detail
- `PATCH /api/postings/{id}/` — update; Roles: admin, utrmc_admin
- `DELETE /api/postings/{id}/` — delete; Roles: admin
- `POST /api/postings/{id}/approve/` — approve posting; Roles: admin, utrmc_admin
- `POST /api/postings/{id}/reject/` — reject posting; Roles: admin, utrmc_admin
- `POST /api/postings/{id}/complete/` — mark complete; Roles: admin, utrmc_admin

---

## Phase 8 — Summary & Reporting (2026-03-07)

### Resident Dashboard Summary

- `GET /api/residents/me/summary/` — dashboard summary for resident
  - Roles: pg/resident
  - Response: `{ training_record, rotation: { current, next }, schedule, leaves, postings, research, thesis, workshops, eligibility: { IMM, FINAL } }`

### Supervisor Dashboard Summary

- `GET /api/supervisors/me/summary/` — dashboard summary for supervisor
  - Roles: supervisor
  - Response: `{ pending: { rotation_approvals, leave_approvals, research_approvals }, residents: [...] }`

### Resident Progress (Supervisor view)

- `GET /api/supervisors/residents/{id}/progress/` — progress snapshot for a specific resident
  - Roles: supervisor (own residents), admin, utrmc_admin
  - Response: `{ resident, training_record, current_rotation, research, thesis, workshops, eligibility }`

### Audit Reports

- `GET /api/audit/reports/` — list audit report entries; query params: `entity_type`, `start`, `end`, `user`
  - Roles: admin (is_staff)
  - Response (paginated): `{ count, results: [{ id, timestamp, actor, action, entity_type, entity_id, changes }] }`
