# 2026-04-02 Bulk Setup Import/Export Audit

## Scope

Close the active-surface UTRMC prerequisite setup workflow for:

- hospitals
- departments
- hospital-department matrix
- faculty/supervisors
- residents
- supervision links
- HOD assignments

This pass keeps the UI inside the existing `/dashboard/utrmc` route to preserve the frozen route/navigation surface.

## Contract / Surface Decision

- Route shape unchanged.
- New admin-only in-page workspace added to the existing UTRMC overview.
- New canonical contract doc added: `docs/contracts/BULK_SETUP_IMPORT_EXPORT.md`
- Export payloads now match the same active-surface schemas used by the downloadable templates and imports.

## Files Changed

Backend:
- `backend/sims/bulk/userbase_engine.py`
- `backend/sims/bulk/services.py`
- `backend/sims/bulk/views.py`
- `backend/sims/bulk/urls.py`
- `backend/sims/bulk/tests.py`

Frontend:
- `frontend/lib/api/bulk.ts`
- `frontend/components/ui/ImportExportPanel.tsx`
- `frontend/components/utrmc/BulkSetupWorkspace.tsx`
- `frontend/app/dashboard/utrmc/page.tsx`
- `frontend/e2e/helpers/auth.ts`
- `frontend/e2e/workflow-gate/bulk-setup.spec.ts`
- `frontend/e2e/workflows/utrmc-management.spec.ts`

Contracts / Docs:
- `docs/contracts/BULK_SETUP_IMPORT_EXPORT.md`
- `docs/contracts/API_CONTRACT.md`
- `docs/contracts/ROUTES.md`
- `docs/contracts/TERMINOLOGY.md`
- `docs/README.md`

## Verification Commands

Backend / frontend gates:

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd frontend && npm test -- --watch=false
cd frontend && npm run build
cd backend && SECRET_KEY=test-secret pytest sims/bulk/tests.py -q
cd backend && SECRET_KEY=test-secret pytest sims/tests/test_role_workflows.py::TestBulkOperations -q
cd backend && SECRET_KEY=test-secret pytest sims -q
cd backend && SECRET_KEY=test-secret python3 manage.py check
```

Contract drift / migration gates:

```bash
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -v
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret pytest sims/rotations/test_canonical_migration_gate.py -v
cd backend && SECRET_KEY=test-secret pytest sims/_devtools/tests/test_drift_guards.py -v
```

Runtime setup and browser verification:

```bash
cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e
cd backend && SECRET_KEY=test-secret python3 manage.py runserver 127.0.0.1:8100
cd frontend && PORT=3101 INTERNAL_API_URL=http://127.0.0.1:8100 NEXT_PUBLIC_API_URL=/api npm run start:next
cd frontend && E2E_BASE_URL=http://127.0.0.1:3101 E2E_API_URL=http://127.0.0.1:8100 npx playwright test e2e/workflow-gate/bulk-setup.spec.ts --project=workflow-gate
cd frontend && E2E_BASE_URL=http://127.0.0.1:3101 E2E_API_URL=http://127.0.0.1:8100 npx playwright test --project=workflow-gate
```

## Outcomes

- Active admin users can dry-run/apply prerequisite-aware imports from the UTRMC overview page.
- Every import surface exposes its expected columns in UI and a downloadable CSV template.
- Exports now return active-surface truth for the same canonical resources.
- Resident/faculty/supervisor/hospital/department setup can be established without reactivating deferred legacy modules.

## Results

Passed:

- `cd frontend && npm run lint`
- `cd frontend && npx tsc --noEmit`
- `cd frontend && npm test -- --watch=false`
- `cd frontend && npm run build`
- `cd backend && SECRET_KEY=test-secret pytest sims/bulk/tests.py -q` (`9 passed`)
- `cd backend && SECRET_KEY=test-secret pytest sims/tests/test_role_workflows.py::TestBulkOperations -q` (`6 passed`)
- `cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field sims/rotations/test_canonical_migration_gate.py sims/_devtools/tests/test_drift_guards.py -v` (`7 passed`)
- `cd backend && SECRET_KEY=test-secret pytest sims -q` (`200 passed`)
- `cd backend && SECRET_KEY=test-secret python3 manage.py check`
- `cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e`
- `cd frontend && E2E_BASE_URL=http://127.0.0.1:3102 E2E_API_URL=http://127.0.0.1:8100 npx playwright test e2e/workflow-gate/bulk-setup.spec.ts --project=workflow-gate` (`1 passed`)
- `cd frontend && E2E_BASE_URL=http://127.0.0.1:3102 E2E_API_URL=http://127.0.0.1:8100 npx playwright test --project=workflow-gate` (`7 passed`)

Observed warnings / caveats:

- `next build` still reports that build-time lint/type validation is skipped by Next.js configuration. Separate lint/type gates passed, but the build command itself does not enforce them.
- `next start` warns that `output: standalone` prefers `node .next/standalone/server.js`. The runtime still served correctly for this verification pass.

## Runtime Caveat Addressed

The first browser pass hit auth throttling because multiple Playwright suites were run against the same local runtime concurrently. This audit pass moved the new bulk browser proof into a focused workflow-gate spec and added JWT reuse in `frontend/e2e/helpers/auth.ts` so deterministic gate runs do not spam `/api/auth/login/`.

## Deferred Boundaries Preserved

No logbook, cases, or legacy analytics routes were reintroduced.
