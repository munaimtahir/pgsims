# PGSIMS Production Gate Handoff - 2026-04-22

## Current Verdict
NO-GO.

The latest fixing sprint improved the harness and added targeted active-scope tests, but it did not reach the mandatory GO thresholds. Another agent should continue from the new evidence pack, not restart discovery from zero.

## Authoritative Evidence To Load First
- `docs/_prod_gate/20260422T211654Z/`
- `OUT/prod_gate_summary.md`
- `OUT/prod_gate_results.json`
- `OUT/prod_gate_code_coverage.json`
- `OUT/prod_gate_scope_coverage.json`
- `OUT/prod_gate_role_matrix.json`
- `OUT/prod_gate_artifacts/20260422T211654Z/`

Prior baseline evidence remains useful for comparison:
- `docs/_prod_gate/20260421T233708Z/`

## What Was Fixed In The Last Pass
- Wired drf-spectacular into Django settings.
- Added `/api/schema/`.
- Added schema endpoint smoke test at `backend/sims/test_schema_gate.py`.
- Stabilized Jest coverage by ignoring `.next/` module/watch paths.
- Fixed E2E bring-up and seed environment drift:
  - `scripts/e2e_up.sh` now uses `.env`.
  - default E2E DB password matches `.env`.
  - E2E `ALLOWED_HOSTS` includes `backend`.
  - `scripts/e2e_seed.sh` waits for backend readiness instead of rerunning migrations during startup.
- Added backend UTRMC org graph tests:
  - roster route
  - hospital-department matrix route
  - HOD assignment create
  - UTRMC read-only mutation denials
- Added backend invalid transition tests:
  - logbook invalid review/action/resubmit paths
  - leave invalid submit/approve/reject paths
- Added frontend mounted-surface tests:
  - UTRMC HOD page CTA and read-only state
  - UTRMC hospital-department matrix toggle and read-only state

## Key Files Changed In The Last Pass
Backend:
- `backend/sims_project/settings.py`
- `backend/sims_project/urls.py`
- `backend/sims_project/tests.py`
- `backend/sims/test_schema_gate.py`
- `backend/sims/users/test_userbase_api.py`
- `backend/sims/training/test_feature_layer_ops.py`

Frontend:
- `frontend/jest.config.js`
- `frontend/app/dashboard/utrmc/hod/page.test.tsx`
- `frontend/app/dashboard/utrmc/matrix/page.test.tsx`

Runtime harness:
- `scripts/e2e_up.sh`
- `scripts/e2e_seed.sh`

Docs/evidence:
- `docs/_prod_gate/20260422T211654Z/00_closure_map.md`
- `docs/_prod_gate/20260422T211654Z/01_schema_gate.md`
- `docs/_prod_gate/20260422T211654Z/02_harness_stabilization.md`
- `docs/_prod_gate/20260422T211654Z/03_scope_coverage_report.md`
- `docs/_prod_gate/20260422T211654Z/04_code_coverage_report.md`
- `docs/_prod_gate/20260422T211654Z/05_role_route_action_matrix.md`
- `docs/_prod_gate/20260422T211654Z/06_endpoint_coverage_report.md`
- `docs/_prod_gate/20260422T211654Z/07_cta_coverage_report.md`
- `docs/_prod_gate/20260422T211654Z/08_transition_coverage_report.md`
- `docs/_prod_gate/20260422T211654Z/09_fixes_applied.md`
- `docs/_prod_gate/20260422T211654Z/10_remaining_gaps.md`
- `docs/_prod_gate/20260422T211654Z/11_final_verdict.md`

## Verification Results From Last Pass
Dry-run:
- Backend tests: `222 passed`.
- Backend coverage: 54.38% line, 28.69% branch.
- Frontend lint: passed.
- Frontend typecheck: passed.
- Frontend unit/coverage: 5 suites passed, 9 tests passed.
- Frontend coverage: 8.71% line, 7.56% branch.
- Frontend build: passed.
- Django check: passed.
- Strict schema gate: failed.

Runtime:
- Docker stack bring-up: passed after harness fixes.
- Seed baseline: passed after harness fixes.
- Same-origin API proxy: passed after allowing `backend` in `ALLOWED_HOSTS`.
- Active-surface E2E: 4 passed, 3 failed.

## Current Blocking Failures
GO is still forbidden because:
- Backend line coverage is 54.38%, below required 95%.
- Backend branch coverage is 28.69%, below required 90%.
- Frontend line coverage is 8.71%, below required 90%.
- Frontend branch coverage is 7.56%, below required 85%.
- Strict OpenAPI schema command fails under `--fail-on-warn`.
- Active-surface E2E resident dashboard fails to render `My Training Dashboard`.
- Active-surface E2E logbook workflow fails after clicking `Save Logbook Draft`.
- 100% active route/API/CTA/transition/unauthorized coverage was not achieved.
- Mounted UTRMC admin cluster is only partially covered.

## Exact Failing Runtime Commands
Run active-surface E2E after stack/seed:

```bash
E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npm run test:e2e:active-surface
```

Observed result:
- 4 passed.
- 3 failed:
  - `e2e/feature-layer/auth-and-smoke.spec.ts`
  - resident dashboard expected heading not found.
  - `e2e/feature-layer/logbook.spec.ts`
  - logbook draft save confirmation not found.

Artifacts:
- `OUT/prod_gate_artifacts/20260422T211654Z/playwright/results/`
- `OUT/prod_gate_artifacts/20260422T211654Z/playwright/report/index.html`

## Strict Schema Gate Command
```bash
SECRET_KEY=test-secret python3 manage.py spectacular --file ../OUT/prod_gate_artifacts/20260422T211654Z/schema/openapi.yaml --validate --fail-on-warn
```

Observed result:
- Fails with 49 warnings and 315 schema generation errors.
- Main causes include unannotated APIViews, serializer method fields without schema hints, duplicate schema component names, and operationId collisions.

## Commands That Passed
Backend:
```bash
SECRET_KEY=test-secret python3 -m pytest sims -q
```

Frontend:
```bash
npm run lint
npm run typecheck
npm test -- --watch=false --coverage --coverageReporters=json-summary --coverageReporters=text --coverageDirectory=../OUT/prod_gate_artifacts/20260422T211654Z/coverage/frontend
npm run build
```

Runtime harness:
```bash
docker compose --env-file .env -f docker/docker-compose.yml down -v
./scripts/e2e_up.sh
./scripts/e2e_seed.sh
```

## Recommended Next Work Order
1. Fix the active-surface E2E resident dashboard failure first.
   - The page shows `Failed to load dashboard. Please refresh.`
   - Direct backend API for `GET /api/residents/me/summary/` returned 200.
   - Same-origin proxy returned 200 after `backend` host fix.
   - Next agent should inspect browser network errors from Playwright traces.

2. Fix the logbook runtime workflow failure.
   - Page renders and form fills.
   - Click on `Save Logbook Draft` does not produce `Logbook draft saved.`
   - Determine whether this is frontend handler, API payload, proxy/auth, or backend validation.

3. Make strict schema gate pass.
   - Add `@extend_schema`, serializers, and schema fields for active APIViews first.
   - Resolve duplicate `Department` component naming.
   - Do not silence warnings globally if active contract remains ambiguous.

4. Continue meaningful coverage expansion.
   - Backend priority: permissions, workflow transitions, active viewsets/actions, serializers, UTRMC admin APIs.
   - Frontend priority: mounted dashboard pages, UTRMC admin pages, role nav, CTA behavior, active API utilities, error/empty/loading states.
   - Do not exclude active files to inflate percentages.

5. Recompute scope coverage only after active E2E passes.
   - Current `OUT/prod_gate_scope_coverage.json` intentionally marks some values `null` because 100% was not achieved and exact recomputation would be misleading.

## Important Constraints For Next Agent
- Do not expand product scope.
- Do not reactivate deferred rotations/synopsis/thesis surfaces just to satisfy tests.
- Do not remove mounted controls unless current truth docs prove they are out of scope.
- Do not fake coverage by excluding active files.
- Contracts under `docs/contracts/` remain authoritative.
- If payload shapes change, update contracts in the same run.
- Respect canonical Department/Hospital model rules from `AGENTS.md`.

## Final Current State
The repository is improved and more reproducible than the previous NO-GO, but it is still not production-ready for the active scope.

Verdict to carry forward:

**NO-GO — 100% active-scope coverage and/or required coverage thresholds were not achieved.**
