# Backend Coverage Gap Map - 2026-04-24

Total Backend Line Coverage: 60.87%
Required for GO: 95.00%

## High Priority Targets

| File Path | Current % | Missing Lines | Purpose | Priority | Planned Test File |
|-----------|-----------|---------------|---------|----------|-------------------|
| `sims/training/views.py` | 62.58% | ~506 lines | Core training & logbook viewsets | High | `sims/tests/test_training_views_extended.py` |
| `sims/bulk/services.py` | 36.41% | ~568 lines | Bulk import/export logic | High | `sims/tests/test_bulk_services_extended.py` |
| `sims/users/views.py` | 56.49% | ~190 lines | User profile & dashboard views | High | `sims/tests/test_users_views_extended.py` |
| `sims/bulk/views.py` | 53.88% | ~86 lines | API endpoints for bulk actions | High | `sims/tests/test_bulk_views.py` |
| `sims/training/eligibility.py` | 62.50% | ~36 lines | Eligibility computation logic | Medium | `sims/tests/test_eligibility_extended.py` |
| `sims/users/decorators.py` | 70.00% | ~23 lines | RBAC guards | Medium | `sims/tests/test_decorators_extended.py` |
| `sims/common_permissions.py` | 66.21% | ~47 lines | Shared permission classes | Medium | `sims/tests/test_common_permissions_extended.py` |
| `sims/users/models.py` | 72.52% | ~52 lines | User & Membership models | Medium | `sims/tests/test_users_models_extended.py` |

## Analysis of Missing Coverage

### 1. Training Views (`sims/training/views.py`)
- Missing large chunks of action logic in `LogbookEntryViewSet`, `RotationAssignmentViewSet`, and `LeaveRequestViewSet`.
- State machine transitions (approvals, returns, rejections) are only partially tested.
- Dashboard query logic for various roles has gaps.

### 2. Bulk Services (`sims/bulk/services.py`)
- Many `_parse_*_rows` helpers and specific entity import logic branches are untested.
- Error handling paths for malformed files are largely missing.
- Excel-specific parsing logic is untested.

### 3. User Views (`sims/users/views.py`)
- Many traditional Django views (not just APIViews) are untested.
- Profile update edge cases and error messages are missing.

### 4. Eligibility (`sims/training/eligibility.py`)
- Specific milestone requirement checks for research and workshops have untested edge cases.

## Sprint Plan
1. **Target 1**: `sims/bulk/services.py` - Add exhaustive tests for each import method with valid and invalid data.
2. **Target 2**: `sims/training/views.py` - Add functional tests for all `@action` methods in viewsets.
3. **Target 3**: `sims/users/views.py` - Cover remaining Django views and profile actions.
4. **Target 4**: `sims/common_permissions.py` - Cover all role check branches.
