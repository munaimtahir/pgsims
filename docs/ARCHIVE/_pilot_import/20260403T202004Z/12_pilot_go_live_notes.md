# 12 Pilot Go-Live Notes

## Canonical Source Assurance

- Real populated package under `pilot_data/first_pilot_run/` was treated as source-of-truth.
- No canonical file was overwritten.

## Compatibility Adjustments Applied

- Added year=5 support for users/import validation and migrated schema.
- Deterministic transformed copies were used only to satisfy strict required-date/level formatting constraints.

## Operational Guidance

1. Keep transformed package as import artifact trace (`pilot_data/first_pilot_run_transformed/`).
2. Re-runs should use idempotent import sequence in same order.
3. If rollback needed, restore `pre_import_db_backup.sql` first, then recreate runtime with `--env-file .env`.

## Caution Flags (Non-Blocking)

- Placeholder emails remain in production pilot data by design/canonical source.
- Link/training defaults used deterministic `2026-01-01` where source required dates were blank.

