# Midpoint Coverage Rebalance - 2026-04-24

## Status
- **Backend Line Coverage**: 60.00% (from 56.10%)
- **Frontend Line Coverage**: 29.60% (from 12.71%)
- **Strict Schema Gate**: PASS
- **Active-Surface E2E**: 7/7 PASS

## Progress Highlights
1. **Backend**:
   - Added `UsersModelsTests` and `TrainingModelsTests` covering core properties and methods.
   - Added `BulkServicesTests` covering ~23% of `sims/bulk/services.py`.
   - Fixed multiple bugs in `sims/bulk/services.py` related to outdated field names and missing imports.
2. **Frontend**:
   - Added Jest tests for all major dashboard pages (Resident, Supervisor, UTRMC).
   - Added direct unit tests for API client modules (`lib/api/*`).
   - Fixed `document.cookie` mocking in `cookies.test.ts`.
   - Reached ~100% coverage on core UI components (`MetricCard`, `Sidebar`, etc.).

## Remaining Gaps & Rebalance
### Backend (Goal: 95%)
- `sims/training/views.py`: 61.20% -> Need to cover more complex state machine transitions in Logbook and Rotation flows.
- `sims/bulk/services.py`: 23.66% -> Many branches in `import_residents` and `import_supervisors` remain uncovered.
- `sims/users/views.py`: 56.49% -> Traditional Django views need more exhaustive functional tests.

### Frontend (Goal: 90%)
- `app/` subpages: Deep subpages like `/dashboard/utrmc/hod` and `/dashboard/utrmc/matrix` have low unit test coverage.
- `components/utrmc/`: Bulk operation components are not yet tested.

## Strategy for Final Push
- Focus on the "long tail" of backend views.
- Add negative tests (403, 404, 400) for all critical API endpoints.
- Ensure all branches in `sims/training/eligibility.py` are covered.
