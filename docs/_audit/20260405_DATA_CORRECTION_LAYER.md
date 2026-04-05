# 2026-04-05 — Data Correction + Admin Control Layer (Additive)

## Scope
- Added a non-breaking data quality control layer on top of existing userbase/training surfaces.
- Preserved existing routes and APIs; added admin-only endpoints and flags.

## Backend changes
- **Model additions**:
  - `users.User`:
    - `is_complete_profile` (bool)
    - `has_placeholder_email` (bool)
    - `data_issues` (JSON list)
  - `users.SupervisorResidentLink`:
    - `has_default_dates` (bool)
  - `training.ResidentTrainingRecord`:
    - `has_default_dates` (bool)
  - `users.DataCorrectionAudit`:
    - actor/entity/field old→new audit trail
- **Migration**:
  - `sims/users/migrations/0004_data_correction_flags.py`
  - Adds new fields/table and backfills flags from current records.
- **Service**:
  - `sims/users/data_quality.py`
  - `scan_user_profile`, `scan_training_record`, `recompute_flags_for_user`, `recompute_all`, `log_data_correction`
- **Admin endpoints** (admin + utrmc_admin only):
  - `GET /api/admin/data-quality/summary`
  - `GET /api/admin/data-quality/users`
  - `POST /api/admin/data-quality/recompute`
  - `GET /api/admin/data-quality/audit`
- **Edit audit hooks**:
  - `PATCH /api/users/{id}/` now logs changed `email`/`year` and recomputes flags.
  - `PATCH /api/residents/{user_id}/` now logs changed training profile fields and recomputes flags.
- **Bulk correction command**:
  - `python manage.py import_corrections_csv <csv> [--apply --confirm --actor-username ...]`
  - Dry-run default, apply mode requires explicit `--confirm`.
  - Validates email/year/date values and logs each applied change to `DataCorrectionAudit`.
- **Feature flag**:
  - `ENABLE_DATA_CORRECTION_LAYER` in settings (env-backed, default true).

## Frontend changes
- Added UTRMC admin page:
  - `/dashboard/utrmc/data-quality`
  - Shows summary cards, resident correction table, issue badges, filter chips, edit modal, and correction audit feed.
- Added API client bindings in `frontend/lib/api/userbase.ts`:
  - `dataQuality.summary/users/recompute/audit`
  - `residents.update` helper for profile correction.
- Added overview entry point card on `/dashboard/utrmc` linking to the Data Quality page.

## Operational notes
- Changes are additive and backward-compatible.
- No existing API route was removed or made incompatible.
- Correction operations are auditable and recompute-based.

## Command CSV format
```csv
resident_email,field_name,new_value
resident.one@example.com,email,resident.one@hospital.org
resident.one@example.com,year,5
resident.one@example.com,training_start,2026-02-01
```
