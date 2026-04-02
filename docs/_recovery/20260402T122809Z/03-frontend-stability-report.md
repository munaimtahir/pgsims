# Frontend Stability Report

## Commands run

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd frontend && npm test -- --watch=false
cd frontend && npm run build
cd frontend && npx playwright install chromium
cd frontend && E2E_BASE_URL=http://127.0.0.1:3001 E2E_API_URL=http://127.0.0.1:8000 npx playwright test --project=workflow-gate
```

## Results
- `npm run lint`: PASS
- `npx tsc --noEmit`: PASS
- `npm test -- --watch=false`: PASS
- `npm run build`: PASS
- `npx playwright install chromium`: PASS
- Workflow gate Playwright suite: PASS (`4 passed`)

## Major frontend fixes made
- Added live leave workflow wiring to the resident schedule page on the active route instead of leaving the workflow backend-only.
- Added actionable supervisor leave approvals to the supervisor dashboard.
- Corrected resident quick-action routing so leave actions point to the real active workflow page.
- Fixed active UTRMC page typing issues in departments, hospitals, and users screens.
- Fixed regression-spec import drift that was breaking TypeScript analysis of the test tree.
- Added a small test-global shim so repo typecheck passes without requiring ad hoc package install changes in the current environment.

## Route and navigation consistency
- Resident canonical area is `/dashboard/resident/*`.
- `/dashboard/pg` exists only as a compatibility redirect to `/dashboard/resident`.
- Active navigation in `frontend/lib/navRegistry.ts` matches the current route tree for resident, supervisor, and UTRMC areas.
- No active navigation exposes logbook or cases.

## Remaining frontend risks
- Rotation and postings flows are still only partially verified compared with the promoted research/leave/auth workflow gate.
- `frontend/next.config.mjs` still ignores lint and type errors during build. The explicit lint/typecheck commands passed in this recovery pass, but build alone is not a sufficient health signal.
- The workflow gate depends on seeded deterministic data and explicit environment setup; this is good for reproducibility but still narrower than full regression coverage.
