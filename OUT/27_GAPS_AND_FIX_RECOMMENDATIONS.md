# Gaps and Fix Recommendations

## A) Admin Visibility Gaps
Source: `OUT/admin_registry_models.txt`, `OUT/admin_models_gap.txt`, `OUT/admin_files_audit.txt`.

### Models not registered in admin (selected operational gaps)
- `audit.ActivityLog`, `audit.AuditReport`
- `bulk.BulkOperation`
- `notifications.Notification`, `notifications.NotificationPreference`
- `reports.ReportTemplate`, `reports.ScheduledReport`
- `search.SavedSearchSuggestion`, `search.SearchQueryLog`

### admin.py missing/empty/no-op
- Missing: `sims/audit/admin.py`, `sims/search/admin.py`
- Exists but no registrations: `sims/bulk/admin.py`

**Recommendation**
- Add minimal admin registrations only for operational verification targets (audit, bulk operations, notification, scheduled report), with read-only fields for immutable audit data.

---

## B) API / Routing Gaps
Source: `OUT/24_API_ENDPOINTS_CATALOG.md`, `OUT/api_endpoints.json`.

1. Several function-based API endpoints are surfaced with `ANY` and no explicit DRF permission metadata in introspection output.
   - Recommendation: add explicit `@permission_classes` on all function-based API views to reduce ambiguity.

2. Certificates API is mostly PG list/download; status transitions are model/admin-driven rather than explicit DRF workflow endpoints.
   - Recommendation: introduce explicit certificate review API endpoints if frontend needs full workflow control.

---

## C) Background Job Wiring Gaps
Source: `OUT/grep_jobs.txt`, `backend/sims_project/celery.py`.

1. Celery beat references tasks:
   - `sims.reports.tasks.generate_daily_reports`
   - `sims.notifications.tasks.cleanup_old_notifications`
   - `sims.attendance.tasks.calculate_monthly_summaries`

   but no `backend/sims/**/tasks.py` files were discovered.

**Recommendation**
- Implement the referenced task modules/functions or remove/replace stale beat entries.

---

## D) Notification Architecture Drift Risk
Source: `OUT/grep_notifications.txt`, `backend/sims/notifications/services.py`.

- Canonical `NotificationService` exists and uses `recipient/verb/body/metadata` schema.
- Direct `Notification.objects.create(...)` calls still exist in app/admin code (logbook/certificates).

**Recommendation**
- Route all notification writes through `NotificationService` for consistent channel handling, preferences, and drift prevention.

---

## E) Schema Generation Tooling Gaps
Source: `OUT/28_VERIFICATION_EVIDENCE_LOG.md`.

- `manage.py spectacular` unavailable (`Unknown command: spectacular`).
- DRF fallback openapi generation failed due missing `inflection` package.

**Recommendation**
- Add/standardize schema generation tooling (e.g., drf-spectacular or DRF OpenAPI dependencies) in backend runtime for canonical contract export.

---

## F) Runtime/Verification Observations
1. Requested service alias `backend` is not present in compose profile; runtime service is `web` (`OUT/docker_ps.txt`).
2. Migrations are fully applied (`OUT/showmigrations_plan.txt`).
3. Tests passed: `286` tests, `OK` (`OUT/28_VERIFICATION_EVIDENCE_LOG.md`).
4. External health endpoint:
   - `/healthz/` responds to `GET` (HEAD returns `405`, which is expected for HEAD if not implemented).

---

## Priority Fix Order (Low-risk)
1. Wire/repair Celery task modules referenced by beat.
2. Add explicit permission decorators for function-based API endpoints reporting as `ANY`.
3. Register selected operational models in admin (audit, bulk, notifications, reports).
4. Standardize OpenAPI generation tooling in deploy/runtime image.
