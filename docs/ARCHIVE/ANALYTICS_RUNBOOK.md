# Analytics Runbook

## Feature Flags
- `ANALYTICS_ENABLED`
- `ANALYTICS_UI_INGEST_ENABLED`
- `ANALYTICS_REQUEST_SAMPLING` (`0..1`)
- `ANALYTICS_SUPERVISOR_ACCESS_ENABLED` (optional, default false)
- Legacy alias supported: `ANALYTICS_ALLOW_SUPERVISOR_ACCESS`

## Rollup Jobs
### Daily (yesterday)
```bash
cd backend
../.venv/bin/python manage.py rebuild_analytics_rollups --yesterday
```

### Backfill Range
```bash
cd backend
../.venv/bin/python manage.py rebuild_analytics_rollups --start-date 2025-01-01 --end-date 2025-12-31
```

## Validation Rejection Monitoring
- Endpoint: `GET /api/analytics/v1/quality/`
- Admin can inspect:
  - anomaly status (spike/drop/stable)
  - top validation rejections
  - missing dimensions
  - schema drift keys

## Debug Checklist
1. Confirm `ANALYTICS_ENABLED=true`.
2. Check ingest gate: `ANALYTICS_UI_INGEST_ENABLED`.
3. Query rejections in Django admin (`AnalyticsValidationRejection`) or quality endpoint.
4. Run rollup rebuild command for affected date range.
5. Clear cache if stale payload suspected.

## Cache Invalidation
```bash
cd backend
../.venv/bin/python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('cache cleared')"
```
