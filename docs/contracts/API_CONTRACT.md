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
