# Post-Runtime Fix Baseline - 2026-04-23

## Status Confirmation
- **Runtime Fix**: Confirmed. `scripts/e2e_up.sh` uses same-origin proxy via `NEXT_PUBLIC_API_URL=/api`.
- **Active-Surface E2E**: 7/7 tests pass.
- **Restart/Reseed**: Verified green.
- **Regression Smoke**: Selector fix for Resident Research page confirmed.

## Current Blocker Status (as of Baseline)
- **Blocker #1 (Schema)**: FAIL (315 errors, 65 unique).
- **Blockers #5 #6 (Coverage)**: FAIL (Backend 54%, Frontend 8%).
- **Active Scope**: 100% completion pending.

## Evidence
`active-surface` E2E run on 2026-04-23 passed all 7 tests in 28.9s.
Schema generation still reports 315 errors.
