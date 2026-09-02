# Remaining Backend Gaps - 2026-04-24

## Uncovered Logic Hotspots

### 1. Training State Transitions (~400 lines)
- `RotationAssignmentViewSet`: Edge cases for `return-to-draft`, `extension`, and `re-assignment` logic.
- `LeaveRequestViewSet`: Rejection reason handling and HOD vs Admin approval branches.

### 2. Bulk Engine Edge Cases (~400 lines)
- `sims/bulk/services.py`: Handlers for malformed Excel files (OpenPyXL specific errors).
- `sims/bulk/userbase_engine.py`: Complex HOD assignment conflict resolution logic.

### 3. Analytics & Reporting (~200 lines)
- `sims/users/views.py`: Dashboard widget aggregations and trend computation.

### 4. Shared Utilities
- `sims/audit/utils.py`: (0% coverage) Audit trail generation logic.
- `sims/notifications/services.py`: (0% coverage) Email dispatch and WebSocket notification integration.

## Recommendations
- Next sprint should prioritize `sims/audit` and `sims/notifications` which are currently at near 0% coverage.
- Add negative tests for file uploads in bulk services (wrong format, missing headers).
- Mock external email/service dependencies to test notification dispatch logic.
