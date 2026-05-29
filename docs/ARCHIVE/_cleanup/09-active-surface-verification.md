# Active-Surface Verification

Date (UTC): 2026-04-21

## Focused Release Gate
Command:

```bash
cd frontend && npm run test:e2e:active-surface:local
```

Result:
- `7 passed (32.4s)` after rebuilding and restarting the Docker `frontend` service from the current tree.

Covered:
- role login and dashboard reachability
- resident dashboard
- resident logbook draft/submit
- supervisor logbook return/approve
- resident resubmit
- resident blocked from supervisor/UTRMC surfaces
- unauthenticated dashboard redirect
- supervisor cannot review unrelated resident logbook entry
- UTRMC staff read-only controls hidden

## Backend Gate
Command:

```bash
cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q
```

Result:
- `217 passed`

## Frontend Gates
Commands and results:
- `npm test -- --watch=false` -> `3 passed`, `5 tests passed`
- `npm run lint` -> passed
- `npm run typecheck` -> passed
- `npm run build` -> passed

## Notes
- `SECRET_KEY=test-secret python3 manage.py check` passed.
- `git diff --check` passed.
- Running `pytest backend/sims -q` from the repository root incorrectly collects archived `_legacy` tests; the canonical backend gate is `cd backend && pytest sims -q`.
- Inactive-depth Playwright tests remain separate and do not affect the active release verdict.
