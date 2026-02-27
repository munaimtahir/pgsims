# Analytics API Contract (v1, OpenAPI-style)

Base path: `/api/analytics/`

Auth: JWT Bearer  
Default RBAC: `admin` only (`supervisor` allowed only when `ANALYTICS_SUPERVISOR_ACCESS_ENABLED=true`; legacy alias supported).

Feature flags:
- `ANALYTICS_ENABLED` (global kill switch)
- `ANALYTICS_UI_INGEST_ENABLED` (POST ingest)
- `ANALYTICS_REQUEST_SAMPLING` (sampled error events)

## GET `/v1/filters/`
Returns options for global filter bar.

Response `200`:
```json
{
  "roles": ["pg", "supervisor", "admin", "utrmc_user", "utrmc_admin"],
  "departments": [{"id": 1, "name": "Surgery"}],
  "hospitals": [{"id": 1, "name": "Teaching Hospital"}]
}
```

## GET `/v1/tabs/{tab}/`
Supported `tab`:
`overview|adoption|logbook|review-sla|departments|rotations|research|data-ops|system|security|live`

Query params:
- `start_date` (YYYY-MM-DD, default: now-13d)
- `end_date` (YYYY-MM-DD, default: today)
- `department_id` (optional)
- `hospital_id` (optional)
- `role` (optional: pg|supervisor|admin|utrmc_user|utrmc_admin)

Response `200`:
```json
{
  "title": "Overview",
  "date_range": {
    "start_date": "2026-02-13",
    "end_date": "2026-02-26"
  },
  "cards": [
    {"key": "total_events", "title": "Total Events", "value": 120}
  ],
  "table": {
    "columns": ["event_type", "count"],
    "rows": [{"event_type": "auth.login.succeeded", "count": 20}]
  },
  "series": [
    {"day": "2026-02-25", "event_type": "auth.login.succeeded", "count": 8}
  ]
}
```

Errors:
- `403` unauthorized role
- `404` invalid tab
- `503` analytics disabled

## GET `/v1/tabs/{tab}/export/`
Same query params as tab endpoint.  
Returns CSV (`text/csv`) for current tab table.

## GET `/v1/live/`
Same filter params as tab endpoint +:
- `limit` (default 200, max 200)
- `cursor` (`occurred_at|id`, optional)
- `event_type_prefix` (optional)
- `entity_type` (optional)

Response `200`:
```json
{
  "date_range": {"start_date": "2026-02-13", "end_date": "2026-02-26"},
  "events": [
    {
      "id": "uuid",
      "occurred_at": "2026-02-26T22:10:00Z",
      "event_type": "ui.page.view",
      "actor_role": "admin",
      "department_id": 1,
      "hospital_id": 1,
      "entity_type": "logbook_entry",
      "entity_id": "10",
      "status_from": "returned",
      "status_to": "pending",
      "metadata": {"source": "ui_ingest"}
    }
  ]
}
```

## GET `/events/live`
Cursor live feed endpoint used by frontend polling, same payload shape as `/v1/live/`.

## GET `/v1/quality/`
Admin governance endpoint:
- anomaly summary (spike/drop/stable)
- top rejected events
- missing dimensions
- schema drift keys

## POST `/events/`
UI ingest endpoint (flag-gated).

Request:
```json
{
  "event_type": "page.view",
  "metadata": {"feature": "analytics_filters"},
  "department_id": 1,
  "hospital_id": 1,
  "entity_type": "dashboard_tab",
  "entity_id": "overview",
  "event_key": "admin-analytics-tab-overview",
  "occurred_at": "2026-02-26T22:10:00Z"
}
```

Validation:
- Allowed inbound types: `page.view`, `feature.used`, `ui.page.view`, `ui.feature.used`
- Stored normalized types: `ui.page.view`, `ui.feature.used`
- Metadata allowlisted and PII-stripped

Response `202`:
```json
{"accepted": true, "event_id": "uuid-or-null"}
```
