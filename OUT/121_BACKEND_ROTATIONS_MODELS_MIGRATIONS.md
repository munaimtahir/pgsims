# OUT/121_BACKEND_ROTATIONS_MODELS_MIGRATIONS.md

## New App: sims.training

### Models

| Model | Key Fields | Constraints |
|---|---|---|
| TrainingProgram | name, code(unique), duration_months, active | code unique |
| ProgramRotationTemplate | program(FK), department(FK), duration_weeks, required, sequence_order | M2M allowed_hospitals |
| ResidentTrainingRecord | resident_user(FK), program(FK), start_date, current_level, active | UniqueConstraint(resident_user, program) WHERE active=True |
| RotationAssignment | resident_training(FK), hospital_department(FK), start_date, end_date, status | CheckConstraint end_date > start_date; overlap validation in clean() |
| LeaveRequest | resident_training(FK), leave_type, start_date, end_date, status | CheckConstraint end_date >= start_date |
| DeputationPosting | resident_training(FK), posting_type, institution_name, start_date, end_date, status | CheckConstraint end_date >= start_date |

### Migration

`sims/training/migrations/0001_initial.py` — Applied OK

```
python manage.py makemigrations training  # → 0001_initial.py created
python manage.py migrate --noinput        # → training.0001_initial... OK
```

### System Check

```
python manage.py check  # System check identified no issues (0 silenced).
```

### Audit

All models use `HistoricalRecords()` from `simple_history` for full audit trail.
`requested_by`, `approved_by_hod`, `approved_by_utrmc`, `approved_by`, `created_by` tracked for all state transitions.

### Django Admin

All 6 models registered with `SimpleHistoryAdmin`:
- list_display, list_filter, search_fields, raw_id_fields, date_hierarchy configured
