# Analytics Performance

## Index Audit
Added/confirmed indexes on `AnalyticsEvent`:
- `occurred_at` (db index)
- `(event_type, occurred_at)`
- `(department_id, occurred_at)`
- `(hospital_id, occurred_at)`
- `(request_id, event_type)`
- `(request_id, event_type, entity_id)`

## Rollups
Model: `AnalyticsDailyRollup`
- Dimensions: `day`, `event_type`, `department_id`, `hospital_id`
- Metric: `count`
- Uniqueness: `(day, event_type, department_id, hospital_id)`

## Query Strategy
- Date range `<= ANALYTICS_ROLLUP_RANGE_DAYS` (default 60): use raw events.
- Date range `> ANALYTICS_ROLLUP_RANGE_DAYS`: use rollup table for aggregate counts/series when role filter is not applied.

## Caching
- Tab payload cache key now includes:
  - tab
  - filter tuple (`start/end/department/hospital/role`)
  - user scope (`user:<id>:role:<role>`)
- TTL uses `ANALYTICS_CACHE_TTL` (default 60s).

## Operational Notes
- Rollup command is idempotent (`update_or_create`).
- Recommended schedule: daily run for yesterday + ad-hoc backfill for historical ranges.
