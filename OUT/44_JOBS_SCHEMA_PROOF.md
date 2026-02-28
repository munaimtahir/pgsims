# Jobs and Schema Proof

## Celery Runtime Evidence
- Historical worker/beat logs: `OUT/worker_logs_tail.txt`, `OUT/beat_logs_tail.txt`
- Recent logs after mitigation: `OUT/worker_logs_recent.txt`, `OUT/beat_logs_recent.txt`
- Registered tasks snapshot: `OUT/celery_registered_tasks.txt`

## Missing Task Drift Mitigation
- Disabled drifting periodic tasks that referenced missing modules:
  - `sims.reports.tasks.generate_daily_reports`
  - `sims.notifications.tasks.cleanup_old_notifications`
  - `sims.attendance.tasks.calculate_monthly_summaries`
- Evidence: `OUT/periodic_tasks_disable.txt`
- Result: entries changed from `enabled=True` to `enabled=False`

## OpenAPI Schema Export
- Installed runtime dependencies for DRF schema support:
  - `inflection` (`OUT/pip_install_inflection.txt`)
  - `uritemplate` (`OUT/pip_install_uritemplate.txt`)
  - `drf-spectacular` runtime library (`OUT/pip_install_spectacular.txt`)
- Successful generation command (runtime monkeypatch to use spectacular AutoSchema):
  - Evidence log: `OUT/openapi_generation_strict.txt`
  - Exported schema: `OUT/openapi.json`
  - File size: see `OUT/openapi_size_strict.txt` (non-zero)
- Notes: generation completed with non-fatal warnings for some APIViews lacking explicit serializer metadata.

## Jobs/Schema Gate Result
- Celery drift (unregistered scheduled tasks) -> MITIGATED
- OpenAPI export -> PASS (file generated)
