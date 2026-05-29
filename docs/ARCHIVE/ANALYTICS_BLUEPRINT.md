# Analytics Blueprint (Design + Implementation Delta)

## 1) Repo Discovery Summary

### Existing analytics assets found
- Backend module: `backend/sims/analytics/` with legacy endpoints:
  - `GET /api/analytics/trends/`
  - `GET /api/analytics/comparative/`
  - `GET /api/analytics/performance/`
  - `GET /api/analytics/dashboard/overview/`
  - `GET /api/analytics/dashboard/trends/`
  - `GET /api/analytics/dashboard/compliance/`
- Frontend page: `frontend/app/dashboard/admin/analytics/page.tsx` (legacy 3-tab UI)
- Frontend client: `frontend/lib/api/analytics.ts` (legacy method set)

### Gaps/conflicts identified
- `analytics/models.py` was a placeholder with no storage schema.
- No canonical event tracking helper (allowlist, dedupe, metadata privacy guard).
- No event ingest endpoint for UI (`POST /api/analytics/events`).
- Legacy analytics RBAC was generic authenticated access, not admin-only by default.
- No request-id based dedupe support.
- No analytics docs set (`ANALYTICS_BLUEPRINT`, `ANALYTICS_OPENAPI`, `ANALYTICS_UI_SPEC`, architecture note).
- Existing frontend did not implement required tabs/filter bar/live polling.

## 2) Final Taxonomy + Event Catalog

Naming convention: `verb.noun.action` (lowercase dot-separated).

### Auth & RBAC
- `auth.login.succeeded`
- `auth.login.failed`
- `auth.rbac.denied`

### Logbook Workflow
- `logbook.case.created`
- `logbook.case.submitted`
- `logbook.case.sent_back`
- `logbook.case.resubmitted`
- `logbook.case.verified`
- `logbook.case.rejected`
- `logbook.status.transitioned` (`status_from`, `status_to` required)

### Import/Export
- `data.import.started`
- `data.import.completed`
- `data.import.failed`
- `data.export.started`
- `data.export.completed`
- `data.export.failed`

### System
- `system.job.started`
- `system.job.completed`
- `system.job.failed`
- `system.api.error` (sampled via `ANALYTICS_REQUEST_SAMPLING`)

### UI
- Inbound accepted: `page.view`, `feature.used`
- Stored normalized: `ui.page.view`, `ui.feature.used`

## 3) Dimensions + Privacy Rules

Mandatory dimensions retained:
- `hospital_id` (kept even in single-hospital mode)
- `department_id`

Other dimensions:
- `actor_user_id` (nullable), `actor_role`
- `entity_type`, `entity_id`
- `status_from`, `status_to`
- `request_id`, `event_key` (dedupe key)

Privacy controls:
- No names/emails/phones/password/token fields stored in event payload
- Metadata allowlist enforced in tracker helper
- Optional `ip_hash` only (salted hash), never raw IP
- Display name resolution deferred to query layer (not stored in event)

## 4) Endpoint Inventory + Delta Plan

### Legacy endpoints kept (compatibility)
- `/api/analytics/trends/`
- `/api/analytics/comparative/`
- `/api/analytics/performance/`
- `/api/analytics/dashboard/overview/`
- `/api/analytics/dashboard/trends/`
- `/api/analytics/dashboard/compliance/`

### New v1 endpoints added
- `GET /api/analytics/v1/filters/`
- `GET /api/analytics/v1/tabs/{tab}/`
- `GET /api/analytics/v1/tabs/{tab}/export/`
- `GET /api/analytics/v1/live/`
- `POST /api/analytics/events/`

### RBAC policy
- Admin-only by default
- Supervisor access only when `ANALYTICS_SUPERVISOR_ACCESS_ENABLED=true` (legacy alias supported)

## 5) Storage/Schema Plan

Implemented entities:
- `AnalyticsEvent`
  - includes dedupe constraint: `(request_id, event_type, event_key)` when request_id/event_key present
  - required indexes for occurrence/time and dimension slicing
- `AnalyticsDailyRollup`
  - day/event_type/department/hospital aggregate table
  - unique daily scope constraint for stable rollup updates

## 6) Feature Flags
- `ANALYTICS_ENABLED`
- `ANALYTICS_UI_INGEST_ENABLED`
- `ANALYTICS_REQUEST_SAMPLING` (`0.0..1.0`)
- `ANALYTICS_SUPERVISOR_ACCESS_ENABLED` (legacy alias: `ANALYTICS_ALLOW_SUPERVISOR_ACCESS`)
- `ANALYTICS_CACHE_TTL`
- `ANALYTICS_UI_INGEST_RATE`

## 7) Dashboard Widget Wiring
Detailed mapping is in `docs/ANALYTICS_UI_SPEC.md` (widget → category → events → aggregation → endpoint → component).

## 8) Related Docs
- `docs/ANALYTICS_OPENAPI.md`
- `docs/ANALYTICS_UI_SPEC.md`
- `docs/ARCHITECTURE/ANALYTICS.md`

---

## TODO checklist
- [x] Repo discovery summary
- [x] Final taxonomy + event catalog
- [x] Endpoint inventory + delta plan
- [x] OpenAPI-like contract docs written
- [x] UI spec written with widget→endpoint mapping
- [x] Feature flags documented
- [x] Security/privacy rules documented
