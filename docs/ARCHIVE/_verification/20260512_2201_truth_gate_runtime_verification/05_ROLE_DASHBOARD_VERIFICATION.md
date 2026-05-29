# Role Dashboard Verification

## Evidence

- `npm run test:e2e:smoke:local` — 17/17 passed
- `npm run test:e2e:active-surface:local` — 7/7 passed
- `npm run test:e2e` rerun — all active dashboards passed; only legacy admin and one research workflow gap remained

| Dashboard | Role Used | Loads? | API Errors? | Console Errors? | Screenshot | Status |
|---|---|---:|---:|---:|---|---|
| `/dashboard/utrmc` | `utrmc_admin` / `utrmc_user` | yes | none observed | none observed | `screenshots/` (not captured manually) | PASS |
| `/dashboard/supervisor` | `supervisor` | yes | none observed | none observed | `screenshots/` (not captured manually) | PASS |
| `/dashboard/resident` | `pg` | yes | none observed | none observed | `screenshots/` (not captured manually) | PASS |
| `/dashboard/admin` | `admin` | no | n/a | n/a | n/a | FAIL / legacy route |

## Notes

- The current app route tree implements UTRMC, supervisor, resident, and related subroutes.
- `/dashboard/admin` is only referenced by legacy tests; no app route exists under `frontend/app/dashboard/admin/`.
