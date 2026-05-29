# 05 Transformation Plan

## Why Transformation Was Required

Canonical source package is authoritative and was preserved intact.  
However, strict runtime importer requires non-empty date fields for some entities where canonical CSV had blanks:

1. residents: `training_start` required
2. supervision links: `start_date` required
3. resident training records: `start_date` required

Additionally, canonical level fields were numeric (`1..5`) while training record enum is `y1..y5`.

## Safety Rules Applied

- **No edits to canonical source files**
- create transformed copies under:
  - `pilot_data/first_pilot_run_transformed/`
- deterministic defaults only
- preserve identities, emails, supervisor assignments, programs, and linkage keys
- document each normalized field

## Deterministic Transformations

1. Default date for missing required starts: `2026-01-01`
2. residents:
   - if missing `training_start` -> set `2026-01-01`
   - normalize `training_level` numeric `N` -> `YN`
3. supervision links:
   - if missing `start_date` -> set `2026-01-01`
4. training records:
   - if missing `start_date` -> set `2026-01-01`
   - normalize `current_level` numeric `N` -> `yN`
5. normalize active flags to lowercase `true|false`

## Non-Transform Rules

- no name/email/user reassignment
- no synthetic supervisor/resident/program creation beyond import behavior
- no mutation of canonical package files

