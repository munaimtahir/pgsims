# Backend Gap Killer Map - 2026-04-24

Current Backend Line Coverage: 62.38%
Target: 70%+ (Stretch: 75%+)

## Target Files & Gaps

| File Path | Current % | Uncovered Functions/Logic | Proposed Test Cases | Expected Impact |
|-----------|-----------|---------------------------|---------------------|-----------------|
| `sims/audit/utils.py` | 0% | All functions (1-62) | Test `log_action` with/without request, anonymous users, metadata extraction. | High |
| `sims/notifications/services.py` | 0% | All functions (3-134) | Test `NotificationService.notify`, scoping, unread count, failure safety. | High |
| `sims/bulk/userbase_engine.py` | 62.54% | Conflict resolution, duplicate detection, invalid row handling (154-174, 222-245, etc.) | Test scenarios with existing users, mismatched data, and dry-run vs apply. | High |
| `sims/training/views.py` | 65.93% | Long-tail error paths, invalid transitions, denied role paths (~452 lines) | Targeted functional tests for specific error branches in ViewSets. | Medium |
| `sims/users/views.py` | 62.07% | Long-tail error paths, specific profile actions (~159 lines) | Targeted functional tests for specific error branches in user views. | Medium |

## Execution Plan

1. **Audit Utilities**: Create `sims/tests/test_audit_utils.py` and cover all utility functions.
2. **Notification Services**: Create `sims/tests/test_notification_services.py` and cover the service layer.
3. **Bulk Engine**: Expand `sims/tests/test_bulk_userbase_engine.py` to cover conflict resolution and duplicate detection logic.
4. **Long-tail Branches**: Identify specific line ranges in `training/views.py` and `users/views.py` and add surgical tests to hit those branches.
