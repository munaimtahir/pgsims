# Import / Export, Background Jobs, and Notifications

## Import / Export Entry Points

### A) Bulk API endpoints (`backend/sims/bulk/views.py`)
- `POST /api/bulk/import` → `BulkService.import_logbook_entries(...)`.
- `POST /api/bulk/import-trainees` → `BulkService.import_trainees(...)`.
- `POST /api/bulk/import-supervisors` → `BulkService.import_supervisors(...)`.
- `POST /api/bulk/import-residents` → `BulkService.import_residents(...)`.
- `POST /api/bulk/import-departments` → `BulkService.import_departments(...)`.
- `GET /api/bulk/exports/<resource>` → `BulkService.export_dataset(...)`.

### B) Management commands
- `python manage.py import_trainees <file>` (`backend/sims/users/management/commands/import_trainees.py`).
- `python manage.py preview_trainees <file>` (`.../preview_trainees.py`) for non-destructive validation.
- `python manage.py import_demo_cases --file <csv>` (`.../import_demo_cases.py`) for seeded demo datasets.
- `python manage.py run_scheduled_reports` (`backend/sims/reports/management/commands/run_scheduled_reports.py`).

### C) Web/admin export paths
- Logbook CSV export view: `export_logbook_csv` (`backend/sims/logbook/views.py:1039+`).
- Rotations CSV export view: `export_rotations_csv` (`backend/sims/rotations/views.py:672+`).
- Audit log CSV export action: `ActivityLogViewSet.export_csv` (`backend/sims/audit/views.py:27+`).
- Import-export resources in Django admin for Users/Logbook (`backend/sims/users/admin.py`, `backend/sims/logbook/admin.py`).

## File Formats and Validation
- Bulk import supports CSV/Excel depending on endpoint/service (`.csv`, `.xlsx`, `.xls`; e.g., `users/forms.py:308-309`, `attendance/api_views.py:45-46`).
- Attendance bulk upload is strictly CSV (`backend/sims/attendance/api_views.py:20-49`).
- Export dataset supports `xlsx` and `csv` (`backend/sims/bulk/services.py:1209-1211`).
- Report scheduler output format supports `pdf`/`xlsx` (`backend/sims/reports/serializers.py:18`, `backend/sims/reports/services.py`).

## Idempotency / Transaction Behavior
- Bulk operations are persisted in `bulk.BulkOperation` with status and counts (`backend/sims/bulk/models.py:14-77`).
- Import methods support `dry_run` and `allow_partial` flags.
- When `dry_run=False` and `allow_partial=False`, imports run in `transaction.atomic()` and roll back on aggregated errors (`backend/sims/bulk/services.py:174-186`, `1075-1087`, `1188-1201`).
- Department import uses `update_or_create` for idempotent upsert behavior on `Department` and `HospitalDepartment` mapping (`backend/sims/bulk/services.py:1164-1176`).
- Trainee import updates existing users by username, otherwise creates (`backend/sims/bulk/services.py:1033-1049`).

## Background / Scheduled Jobs

### Celery configuration
- Celery app configured in `backend/sims_project/celery.py` and autodiscovers tasks.
- Beat schedule currently references:
  - `sims.reports.tasks.generate_daily_reports`
  - `sims.notifications.tasks.cleanup_old_notifications`
  - `sims.attendance.tasks.calculate_monthly_summaries`
- Celery settings in `backend/sims_project/settings.py:344-352`.

### Scheduled reports runtime
- `ScheduledReportRunner` executes due rows from `reports.ScheduledReport` where `next_run_at <= now` (`backend/sims/reports/services.py:171-190`).
- `record_run()` stores execution result (`backend/sims/reports/models.py:56-61`).
- Delivery via email attachment in `_email_report` (`backend/sims/reports/services.py:192-203`).

## Notifications System

### Canonical schema (model truth)
- `Notification`: `recipient`, `actor`, `verb`, `title`, `body`, `channel`, `metadata`, `read_at`, `scheduled_for` (`backend/sims/notifications/models.py:24-43`).
- Channel constants: `email`, `in_app` (`backend/sims/notifications/models.py:17-22`).
- Preferences: `NotificationPreference` with quiet hours/channel toggles (`backend/sims/notifications/models.py:63-111`).

### Delivery service
- `NotificationService.send(...)` handles channel preference checks and dispatch (`backend/sims/notifications/services.py:36-64`).
- In-app creation via canonical keys (`recipient`, `verb`, `body`, `metadata`) (`backend/sims/notifications/services.py:66-78`).
- Trigger helpers for logbook status and upcoming rotation deadlines (`backend/sims/notifications/services.py:108-157`).

## Observed Gaps Relevant to Jobs/Imports
- Celery beat references task paths under `sims.<app>.tasks`, but no `tasks.py` files were found in `backend/sims/**/tasks.py` during this audit.
- Some notification creation still occurs directly in app/admin code (`logbook/models.py`, `logbook/admin.py`, `certificates/admin.py`) in addition to centralized `NotificationService`.
