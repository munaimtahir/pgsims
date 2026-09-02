# RBAC and Active Workflow Final Check

## RBAC

- Unauthenticated access: confirmed
- Resident access: confirmed
- Supervisor access: confirmed
- UTRMC access: confirmed

## Workflows

- Resident schedule: confirmed
- Resident logbook create/submit: confirmed
- Supervisor logbook review/return/approve: confirmed
- Resident leave submit: confirmed
- Supervisor leave approve: confirmed
- UTRMC management access: confirmed
- Bulk dry-run/import preview: confirmed

## Result

- `test:e2e:auth`: 10 passed, 0 failed, 0 skipped
- `test:e2e:rbac`: 20 passed, 0 failed, 0 skipped
- `test:e2e:dashboard`: 18 passed, 0 failed, 0 skipped
- `test:e2e:workflows`: 22 passed, 1 failed, 1 skipped

## Note

The only workflow failure was the deferred research notice assertion in an excluded research path, which is outside the active pilot scope.
