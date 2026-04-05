# Data Correction Admin Guide

## 1) Open Data Quality Dashboard
- Go to: `/dashboard/utrmc/data-quality`
- Required role: `admin` or `utrmc_admin`

## 2) Identify issues quickly
- Review summary cards:
  - total residents
  - incomplete profiles
  - placeholder emails
  - missing dates
- Use filters:
  - incomplete profile
  - placeholder email
  - missing dates
  - missing email

## 3) Fix a resident inline (UI)
- In resident table, click **Edit**.
- Update fields as needed:
  - email
  - training year (1–5)
  - training start/end
  - training level
- Save.
- Flags are recomputed automatically and change is audit-logged.

## 4) Bulk fix via CSV command
- Prepare CSV headers exactly:
  - `resident_email,field_name,new_value`
- Dry-run first:
```bash
cd backend
python manage.py import_corrections_csv ../pilot_data/first_pilot_run/corrections_sample.csv
```
- Apply with confirmation:
```bash
cd backend
python manage.py import_corrections_csv ../pilot_data/first_pilot_run/corrections_sample.csv --apply --confirm --actor-username admin
```

## 5) Verify completion
- Click **Recompute Flags** in dashboard.
- Confirm resident row becomes **Complete** when no issues remain.
- Check **Recent Correction Audit** for field-level traceability.
