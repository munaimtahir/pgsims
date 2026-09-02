# RBAC and Capability Alignment

## Summary

RBAC is aligned for the current active surfaces.

| Role | Feature | UI Visibility | Backend Permission | Runtime Result | Status |
|---|---|---|---|---|---|
| pg | resident dashboard / schedule / logbook | visible | allowed on resident surface only | PASS | aligned |
| supervisor | supervisor dashboard / review queue | visible | allowed on supervisor surface only | PASS | aligned |
| utrmc_user | read-only UTRMC overview | visible | no admin mutation controls | PASS | aligned |
| utrmc_admin | UTRMC admin pages | visible | allowed on UTRMC management pages | PASS | aligned |
| admin | canonical UTRMC landing | visible | mapped to `/dashboard/utrmc` | PASS | aligned |
| admin legacy route | `/dashboard/admin` | not in app | not implemented | FAIL | stale test surface |

## Evidence

- `npm run test:e2e:active-surface:local` passed 7/7.
- `npm run test:e2e:smoke:local` passed 17/17.
- `npm run test:e2e` rerun passed all active RBAC/navigation/dashboard cases.

## Notes

- Cross-role URL blocking works for unauthenticated access and restricted role access.
- The remaining failures are not RBAC mismatches on the active routes; they are legacy admin route expectations.
