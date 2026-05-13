# E2E Test Results

## Completed suites

| Command | Result |
|---|---|
| `npm run test:e2e:smoke:local` | 17/17 passed |
| `npm run test:e2e:active-surface:local` | 7/7 passed |
| `npm run test:e2e:critical` | partial; 2 legacy admin failures, 1 skipped legacy live-feed test |

## Observed full-suite state

During `npm run test:e2e`, the following surfaces passed:

- smoke
- workflow-gate
- active-surface
- auth
- rbac
- navigation
- dashboard
- negative

Observed problems:

| Test | Result | Classification |
|---|---|---|
| `e2e/workflows/resident-training.spec.ts:102` research wizard | fail | stale assertion against deferred research page |
| `e2e/critical/admin_critical.spec.ts:3` admin dashboard | fail | legacy route not implemented |
| `e2e/critical/admin_critical.spec.ts:10` admin reports | fail | legacy route not implemented |
| `e2e/critical/admin_analytics_live_feed.spec.ts` | skipped | legacy/outside baseline |

## Important note

The full-suite rerun was intentionally stopped once the remaining gap was clear. The active release surface is green; the remaining failures are legacy/admin or deferred-workflow related.
