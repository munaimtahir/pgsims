# Testing Truth Audit

## Present And Working
- Backend canonical tests: `cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q`
- Frontend lint/type/unit/build: `npm run lint`, `npm run typecheck`, `npm test -- --watch=false`, `npm run build`
- Live active surface: `cd frontend && npm run test:e2e:active-surface:local`
- Live smoke/RBAC/navigation/dashboard/negative projects exist and are runnable.

## Present But Broken Or Drifted
- Backend system Python did not have `coverage`/`pytest-cov`; fixed for this gate with isolated venv under `OUT/prod_gate_artifacts/20260421T233708Z/backend-venv`.
- Old workflow/navigation specs referenced de-scoped research, rotation, posting, and old resident nav labels; repaired to active truth.
- Frontend Jest coverage reports a `.next/standalone/package.json` haste collision warning from prior build output; tests still pass.

## Missing And Required For GO
- Generated OpenAPI/schema endpoint or reproducible schema generation command is not wired despite `drf-spectacular` dependency.
- Code coverage is far below required thresholds.
- Complete active mounted route/API/CTA coverage is not yet proven.

## Missing But Optional
- Formal security certification and load testing are outside this gate.

