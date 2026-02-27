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
