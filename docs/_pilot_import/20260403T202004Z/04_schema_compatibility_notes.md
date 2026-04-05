# 04 Schema Compatibility Notes

## Year=5 Compatibility Investigation

### Findings

- `users.User.year` originally allowed only `1..4` (`YEAR_CHOICES` in `backend/sims/users/models.py`).
- Active userbase importer validates resident year through `YEAR_CHOICES` (`backend/sims/bulk/userbase_engine.py::_normalize_year`).
- Training module already supports `y5` (`backend/sims/training/models.py`, `ResidentTrainingRecord.LEVEL_CHOICES` includes `y5`).

### Action Taken

To safely support real pilot data containing year=5:

1. Extended `YEAR_CHOICES` to include `("5","Year 5")` in `backend/sims/users/models.py`.
2. Updated `import_pilot_bundle` normalizer to preserve/derive up to year 5 (`backend/sims/users/management/commands/import_pilot_bundle.py`).
3. Generated/applied migration:
   - `backend/sims/users/migrations/0003_alter_historicaluser_year_alter_user_year.py`

### Verdict

- **Year=5 is now supported end-to-end** for this go-live:
  - User model validation
  - userbase resident import validation
  - resident training record level (`y5`)
  - persisted runtime data (validated via post-import counts and samples)

## Placeholder Values

- Placeholder emails existed in canonical source package.
- They were preserved unchanged (no identity fabrication/remapping).
- They imported successfully and remain traceable in runtime.

## Import Surface Compatibility

- Runtime now includes required commands/modules (`import_pilot_bundle`, `cleanup_pilot_runtime`, userbase engine).
- Import path used active userbase engine + bulk services in dependency order.

