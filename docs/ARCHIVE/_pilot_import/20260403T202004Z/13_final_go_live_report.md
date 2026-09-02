# 13 Final Go-Live Report

## A) Canonical Source Used

Confirmed canonical source package:

- `pilot_data/first_pilot_run/`

Inventory used/validated:

1. `final_supervisors_list.csv`
2. `final_residents_list.csv`
3. `final_supervision_links.csv`
4. `final_training_programs.csv`
5. `final_resident_training_records.csv`
6. `final_pilot_workbook.xlsx`

## B) Validation Summary

### Passed

- file presence/readability
- CSV structural parse
- referential integrity across links and training records
- duplicates check (no blocking duplicates)
- controlled values parse

### Required Compatibility Handling

1. **Year=5 compatibility**
   - user year schema/import path initially limited to `1..4`
   - updated to include year `5` and migrated
2. **Required date fields**
   - canonical package had blanks for:
     - resident `training_start`
     - supervision link `start_date`
     - training record `start_date`
   - transformed copies set deterministic default `2026-01-01`
3. **Level normalization**
   - numeric training levels normalized to importer/model-compatible forms:
     - residents: `Y1..Y5`
     - training records: `y1..y5`

### Year=5 Verdict

- **Supported and imported unchanged semantically** (4 residents at year=5; 4 training records at y5).

### Placeholder Handling Verdict

- Placeholder emails preserved as-is from canonical source.
- They do not block import or core pilot workflows.

## C) Import Summary

Final applied import (post-transform compatibility package):

- training programs imported: **2** (created 0, updated 2, skipped 0)
- supervisors imported: **4** (created 0, updated 4, skipped 0)
- residents imported: **18** (created 18, updated 0, skipped 0)
- supervision links imported: **18** (created 18, updated 0, skipped 0)
- resident training records imported: **18** (created 18, updated 0, skipped 0)

Warnings/notes:

- Direct canonical apply failed strict required-date validations; transformed-copy import used for compatibility.
- Placeholder emails present by canonical design.

## D) Deployment Status

- services rebuilt/restarted with explicit env-file binding
- runtime verified on compose stack from `docker/docker-compose.yml`
- backend health: healthy (database/cache/celery OK)
- frontend HTTP endpoint healthy (`200 OK`)
- no demo reseed observed post-import

## E) Final Verdict

**PASS WITH CAUTIONS**

System is usable now for first pilot run; cautions are operational/documentary (not launch blockers).

## F) Blockers

- **None blocking go-live.**

## G) Final Row Counts

```json
{
  "users_total": 23,
  "users_admin": 1,
  "users_supervisor": 4,
  "users_resident": 18,
  "year5_users": 4,
  "departments": 5,
  "hospitals": 1,
  "hospital_departments": 5,
  "supervision_links": 18,
  "resident_profiles": 18,
  "department_memberships": 22,
  "hospital_assignments": 22,
  "training_programs": 2,
  "resident_training_records": 18,
  "training_level_y5_records": 4,
  "placeholder_emails": 11
}
```

---

## Key Evidence References

- Pre-import backup: `docs/_pilot_import/20260403T202004Z/pre_import_db_backup.sql`
- Pre-import state: `01_pre_import_runtime_state.md`
- Validation: `03_package_validation.md`, `04_schema_compatibility_notes.md`
- Transform docs: `05_transformation_plan.md`, `06_transformation_execution.md`
- Import docs: `07_import_execution.md`, `08_import_results.md`
- Deploy/health docs: `09_deploy_actions.md`, `10_runtime_health.md`
- Functional validation: `11_functional_validation.md`

