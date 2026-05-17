# CI follow-up for clean merge

## Scope
- Fixed failing CI gate references and stabilized smoke workflow runtime for PR branch `codex/dead-code-cleanup`.

## Changes
- Updated backend truth gate workflow to run the active logbook flow truth test:
  - `sims/training/test_feature_layer_ops.py::FeatureLayerOperationalFlowTests::test_logbook_submit_return_resubmit_approve_flow`
- Updated smoke workflow to run against local ephemeral runtime instead of live host:
  - install backend deps
  - migrate test DB
  - ensure `admin/admin123` via `create_superadmin --reset-password`
  - seed E2E users/data via `seed_e2e`
  - boot backend (`127.0.0.1:8014`) and frontend (`127.0.0.1:8082`) inside job
  - execute Playwright smoke suite against local URLs
- Repaired unit tests that were failing in CI due mock compatibility and async assertions:
  - `ProtectedRoute.test.tsx`
  - `auth.test.ts`
  - `bulk.test.ts`
  - `userbase.test.ts`
  - resident and UTRMC dashboard tests

## Validation evidence
- `cd backend && python manage.py check` ✅
- `cd backend && pytest -v sims/training/test_feature_layer_ops.py::FeatureLayerOperationalFlowTests::test_logbook_submit_return_resubmit_approve_flow sims/rotations/test_canonical_migration_gate.py sims/_devtools/tests/test_drift_guards.py` ✅
- `cd frontend && npm run lint` ✅
- `cd frontend && npm test -- --runInBand` ✅
- `cd frontend && npm run build` ✅
- `cd frontend && E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npx playwright test --project=smoke e2e/smoke/cleanup_baseline_routes.spec.ts` ✅
