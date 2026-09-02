# 2026-05-14 Demo Data Cleanup and Baseline Initialization

## Summary

This session removed fake E2E/workflow/pilot/demo data from the live PGSIMS database and then re-seeded only the minimum canonical master data needed for safe manual entry.

## Evidence

- Cleanup command added: `backend/sims/users/management/commands/reset_demo_data.py`
- Baseline command added: `backend/sims/users/management/commands/initialize_pgsims_baseline.py`
- Cleanup tests added: `backend/sims/users/test_demo_data_reset.py`
- Frontend smoke test added: `frontend/e2e/smoke/cleanup_baseline_routes.spec.ts`
- Evidence bundle: `docs/_implementation/20260514_1404_demo_data_cleanup_baseline_initialization/`
- Stale internal wording standardized in `backend/sims/users/management/commands/seed_active_surface_baseline.py`

## Verification

- Dry-run cleanup completed successfully.
- Confirmed cleanup completed successfully.
- Baseline initialization completed successfully.
- Backend tests passed.
- Frontend smoke test passed.
