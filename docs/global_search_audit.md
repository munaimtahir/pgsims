# Stage B Enhancements

## Global Search
- Cross-module search covering users, rotations, logbooks, certificates and clinical cases.
- PostgreSQL full-text search is used automatically when the site runs on PostgreSQL; SQLite deployments fall back to case-insensitive matching.
- Search requests are logged per-user (query text, applied filters, duration, total hits) to power recent history and suggestions.
- `/api/search/` (GET) returns paginated-style payload with highlights, search history and suggestions. Additional helper endpoints:
  - `/api/search/history/` – recent personal queries.
  - `/api/search/suggestions/` – cached suggestions with 30s cache window.
- Results are capped using `SEARCH_MAX_RESULTS` (default 100) and respect role-based visibility (PGs only see their own records, supervisors see assigned learners, admins see everything).

## Audit Trail
- Added `django-simple-history` to core models (users, rotations, certificates, logbook entries, cases, hospitals, departments).
- Every historical change emits an `ActivityLog` entry; key actions (view, create, update, delete, export, login/logout) can be recorded programmatically.
- `/api/audit/activity/` exposes filterable, CSV-exportable activity logs for admins.
- `/api/audit/reports/` lets admins generate cached summary reports covering a date window; `/latest/` fetches the most recent snapshot.

## Data Validation & Sanitisation
- Centralised validators in `sims/domain/validators.py` cover chronology checks, future-date protection and free-text sanitisation (server-side script blocking).
- Models leverage the shared validators (e.g. rotations, logbook entries) to provide consistent user-facing errors while logging developer context.

## Performance & Ops
- Redis cache support enabled via `REDIS_URL`; local deployments still default to an in-memory cache.
- Static files served via manifest storage for hashed filenames.
- REST API throttling tightened (per-user and search-specific buckets).
- Audit/search APIs use select-related/prefetching to reduce query counts.

## Testing
- Added `tests/test_global_search_feature.py` to exercise global search results, API logging and audit report aggregation.
