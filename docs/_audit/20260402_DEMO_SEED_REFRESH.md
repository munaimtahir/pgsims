# 2026-04-02 Demo Seed Refresh

## Scope

- Replaced the stale `seed_demo_data` implementation with a canonical seed that targets active apps only.
- Preserved the hard login rule for `admin / admin123`.
- Added realistic demo data for:
  - 2 hospitals
  - 2 departments
  - 15 total users
  - hospital-department matrix
  - department memberships, hospital assignments, HOD assignments, supervision links
  - training programs, milestones, workshops, resident training records
  - rotations, leave requests, deputation postings, research, thesis, notifications

## Contract Impact

- No API payload shapes changed.
- No route or terminology changes.
- No contract document updates were required.

## Evidence

- Seed command updated: `backend/sims/users/management/commands/seed_demo_data.py`
- Reproducible entrypoint fixed: `Makefile`
- Regression coverage added: `backend/sims/users/test_seed_demo_data.py`

## Verification

Executed locally:

```bash
cd backend
SECRET_KEY=test-secret python3 manage.py seed_demo_data --reset
SECRET_KEY=test-secret pytest sims/users/test_seed_demo_data.py sims/_devtools/tests/test_drift_guards.py sims/rotations/test_canonical_migration_gate.py -q
```

Observed seed summary:

- demo users seeded: 15
- demo hospitals seeded: 2
- demo departments seeded: 2
- hospital-department links: 4
- resident training records: 8
- rotation assignments: 24
- workshop completions: 8

## Notes

- `make seed` now runs `seed_demo_data --reset` so local demo refresh uses the committed canonical command instead of the removed `sims_seed_demo` name.
