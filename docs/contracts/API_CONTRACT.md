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
- `POST /api/my/research/action/{action}/` — state transition; actions: `submit-to-supervisor`, `supervisor-approve`, `submit-to-university`, `accept-by-university`, `return-to-draft`
  - `supervisor-approve` payload: `{ "project_id": int, "feedback": str }`

### Supervisor Research Approvals
- `GET /api/supervisor/research-approvals/` — list residents' projects (supervisor/faculty/hod)

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
- `GET /api/utrmc/eligibility/` — all records; query params: `status`, `program`, `department`

### System Settings
- `GET /api/system/settings/` — returns `{ WORKSHOP_MANAGEMENT_ENABLED: bool, ... }`

### Eligibility Status Values
- `NOT_READY` — all requirements unmet
- `PARTIALLY_READY` — some requirements met
- `ELIGIBLE` — all requirements met
