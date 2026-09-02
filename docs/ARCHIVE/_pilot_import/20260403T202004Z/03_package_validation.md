# 03 Package Validation

## Canonical Package Validated

Path: `pilot_data/first_pilot_run/`

### Presence & Readability

All required files present and readable:

1. `final_supervisors_list.csv`
2. `final_residents_list.csv`
3. `final_supervision_links.csv`
4. `final_training_programs.csv`
5. `final_resident_training_records.csv`
6. `final_pilot_workbook.xlsx`

File type check showed CSV ASCII text and valid Excel workbook.

### Structural Validation

- CSV headers present and parseable with UTF-8/UTF-8-SIG readers.
- No broken CSV shape detected during dict parsing.
- Counts from canonical package:
  - supervisors: 4
  - residents: 18
  - supervision links: 18
  - training programs: 2
  - resident training records: 18

### Referential Validation

Validated from canonical CSV values:

- every supervision link resident email exists in residents CSV
- every supervision link supervisor email exists in supervisors CSV
- every training record resident email exists in residents CSV
- every training record program code exists in training programs CSV

All referential checks passed.

### Duplicate Validation

- No duplicate-by-key conflicts were found in canonical source for:
  - supervisors by email
  - residents by email
  - supervision links by (supervisor_email, resident_email, department_code)

### Enum / Controlled Values Observed

- `hospital_code`: `UTRMC`
- `department_code`: `SURG`
- roles: `supervisor`, `resident`
- specialty: `urology`
- program codes: `MS-UROLOGY`, `FCPS-UROLOGY`
- resident years in canonical residents file: `1,2,3,4,5`
- resident `training_level` and training record `current_level` appeared as numeric strings (`1..5`) in source.

### Importer Compatibility Result (direct canonical)

Direct strict import against runtime importer failed on required fields:

1. residents import: `training_start is required`
2. supervision links import: `start_date is required`
3. resident training records import: `Missing resident_email, program_code, or start_date`

These were data-shape compatibility issues (not identity/assignment issues), resolved via deterministic transformed copies documented in later phases.

