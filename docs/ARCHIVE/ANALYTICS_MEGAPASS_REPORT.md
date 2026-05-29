# Analytics Megapass Report

## Discovery Snapshot (before this pass)
- Existing analytics stack was present under `backend/sims/analytics/` with:
  - `AnalyticsEvent` and `AnalyticsDailyRollup` models.
  - Admin v1 tab endpoints and live endpoint (`/api/analytics/v1/live/`).
  - Cached tab payloads and 7-second frontend refresh on Live tab.
  - Basic UI ingest endpoint and analytics event tracking helpers.
- Existing contract/docs existed (`docs/ANALYTICS_*`, `docs/contracts/API_CONTRACT.md`) but had drift against mission constraints.

## Gaps Found
- No authoritative event catalog module; allowlist/metadata policy lived inline in helper.
- Metadata handling dropped unknown/PII keys silently instead of enforcing rejection.
- No persisted rejection telemetry for governance quality reporting.
- Live feed endpoint did not implement cursor-based incremental polling semantics.
- No `/api/analytics/events/live` endpoint path.
- Supervisor analytics flag used `ANALYTICS_ALLOW_SUPERVISOR_ACCESS`; mission requires `ANALYTICS_SUPERVISOR_ACCESS_ENABLED`.
- Hospital dimension was not guaranteed by explicit resolver contract.
- No rollup management command/backfill runbook entrypoint.
- Index set missed `(request_id, event_type, entity_id)` composite.

## Delta Implemented In This Run
- Added canonical event catalog + metadata schema policy (`backend/sims/analytics/event_catalog.py`).
- Added strict validation + rejection persistence (`AnalyticsValidationRejection`) in tracking and ingest paths.
- Added hospital dimension resolver (`get_current_hospital_id`) and enforced non-null hospital for non-system events.
- Added cursor-based live polling behavior and new endpoint path: `GET /api/analytics/events/live`.
- Added analytics quality endpoint: `GET /api/analytics/v1/quality/`.
- Added rollup rebuild command (`rebuild_analytics_rollups`) with idempotent upsert behavior.
- Added new composite index on analytics events for dedupe/query patterns.
- Updated frontend live tab to use cursor polling + dedupe + cap 200 + prefix/entity filters.
- Added backend tests for validation, PII rejection, cursor behavior, rollup idempotency, quality endpoint.
- Added Playwright live feed workflow spec and evidence artifacts (local-only under `docs/_audit`).

## Key Decisions
- Kept existing `v1` response envelope shape; added fields in backward-compatible way (`cursor`, `drilldown_url`).
- Preserved existing supervisor flag as backward-compatible alias while introducing required flag.
- Kept route/navigation labels unchanged (Frozen UX rule).
- Kept all analytics changes admin-first RBAC with optional supervisor feature flag.
