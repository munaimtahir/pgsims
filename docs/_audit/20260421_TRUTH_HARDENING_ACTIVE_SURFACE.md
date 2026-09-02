# Truth-Hardening Active Surface Audit

Date (UTC): 2026-04-21

## Evidence
- Backend: `cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q` -> `217 passed`
- Frontend: Jest, lint, typecheck, and build passed
- Active E2E: `cd frontend && npm run test:e2e:active-surface:local` -> `7 passed`
- Static diff hygiene: `git diff --check` -> clean

## Contract Decision
- Active release surface is limited to auth, resident dashboard, leave flow, supervisor dashboard, UTRMC dashboard/read-only boundary, supervisor self-scoped user read, and logbook workflow.
- Rotations phase-1, synopsis, thesis, and resident postings remain deferred and hidden from active navigation.
