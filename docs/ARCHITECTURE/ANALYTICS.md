# Analytics Architecture

## Scope
Analytics is event-driven and powers admin dashboards through read-optimized APIs.

## Data Flow
1. Workflow/API action occurs.
2. `track_event(...)` records canonical event row in `AnalyticsEvent`.
3. Optional rollups in `AnalyticsDailyRollup` are used for faster aggregated reads.
4. Dashboard endpoints (`/api/analytics/v1/...`) return tab payloads with cards/table/series.
5. Frontend `/dashboard/admin/analytics` renders tab views with polling-based live feed.

## Key Components
- **Storage**
  - `sims.analytics.models.AnalyticsEvent`
  - `sims.analytics.models.AnalyticsDailyRollup`
- **Tracking helper**
  - `sims.analytics.event_tracking.track_event`
  - event catalog validation, PII key rejection, request-id + event-key dedupe
- **Query layer**
  - `sims.analytics.dashboard_v1`
  - filter resolution, tab payload composition, CSV export
- **API layer**
  - `sims.analytics.views` (`v1` tab/filter/live + ingest endpoints)
- **Frontend**
  - `frontend/app/dashboard/admin/analytics/page.tsx`
  - `frontend/lib/api/analytics.ts`

## RBAC + Flags
- Analytics APIs/UI are admin-only by default.
- Supervisor access requires `ANALYTICS_SUPERVISOR_ACCESS_ENABLED=true` (legacy alias supported).
- `ANALYTICS_ENABLED` can disable all analytics endpoints/tracking.
- `ANALYTICS_UI_INGEST_ENABLED` gates UI event ingest.

## Privacy
- No PII in analytics metadata (`name/email/phone/mobile/mrno/address/cnic/dob/patient/password/token` blocked).
- `actor_user_id` allowed; display names resolved at query/UI time.
- Optional IP is stored only as hash (`ip_hash`).

## Live Updates
- Polling every 7s for live feed; no websocket/SSE in v1.
