# 2026-04-02 Active Surface Hardening Audit

## Scope
- Harden already-exposed active UTRMC administration pages without expanding scope
- Preserve deferred boundaries for logbook, cases, and legacy analytics
- Align nav-visible UTRMC read-only surfaces with backend read permissions
- Convert misleading mutation affordances into truthful read-only behavior for `utrmc_user`

## Active-surface truth addressed
- UTRMC read-only oversight pages were visible in the active nav but some routes were not truthfully usable for `utrmc_user`.
- The frontend exposed mutation affordances on several UTRMC pages even when backend writes were intentionally forbidden.
- Programmes and eligibility monitoring were part of the active UTRMC surface but their backend GET permissions were narrower than the active routing implied.

## Evidence sources
- Frontend route tree: `frontend/app/dashboard/utrmc/*`
- Frontend role helpers: `frontend/lib/rbac.ts`
- Frontend access envelope: `frontend/components/auth/ProtectedRoute.tsx`
- Userbase API enforcement: `backend/sims/users/userbase_views.py`
- Training read/write enforcement: `backend/sims/training/views.py`
- Regression browser coverage: `frontend/e2e/rbac/utrmc_readonly_dashboard.spec.ts`
- Truth baseline and roadmap: `docs/_recovery/20260402T122809Z/`, `docs/_discovery/20260402T215202Z-functionality-categorization/`

## Changes made
- Added a shared readonly banner component: `frontend/components/ReadonlyNotice.tsx`
- Added explicit UTRMC role helpers:
  - `isUtrmcManagerRole`
  - `isUtrmcReadonlyRole`
- Updated active UTRMC pages to hide mutation controls for `utrmc_user` and show explicit read-only messaging:
  - `frontend/app/dashboard/utrmc/hospitals/page.tsx`
  - `frontend/app/dashboard/utrmc/departments/page.tsx`
  - `frontend/app/dashboard/utrmc/users/page.tsx`
  - `frontend/app/dashboard/utrmc/matrix/page.tsx`
  - `frontend/app/dashboard/utrmc/supervision/page.tsx`
  - `frontend/app/dashboard/utrmc/hod/page.tsx`
  - `frontend/app/dashboard/utrmc/programs/page.tsx`
- Expanded read-only backend visibility for nav-exposed oversight pages while preserving manager-only writes:
  - `backend/sims/users/userbase_views.py`
  - `backend/sims/training/views.py`
- Added backend regression coverage for read-only oversight boundaries:
  - `backend/sims/users/tests.py`
  - `backend/sims/training/tests.py`
- Removed stale route assumptions from contracts/docs and active test references:
  - `docs/contracts/ROUTES.md`
  - `README.md`
  - `docs/README.md`
  - `frontend/e2e/helpers/navigation.ts`
  - `frontend/e2e/rbac/access-control.spec.ts`
  - `frontend/e2e/critical/userbase_foundation.spec.ts`
  - `frontend/e2e/critical/phase6_research_eligibility.spec.ts`

## Commands run

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd backend && SECRET_KEY=test-secret pytest sims/users/tests.py sims/training/tests.py -q
cd frontend && npm test -- --watch=false
cd frontend && npm run build

cd backend && SECRET_KEY=test-secret pytest sims -q
cd backend && SECRET_KEY=test-secret python3 manage.py check
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -v
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field -v sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret pytest sims/rotations/test_canonical_migration_gate.py -v
cd backend && SECRET_KEY=test-secret pytest sims/_devtools/tests/test_drift_guards.py -v

cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e
cd frontend && npx playwright install chromium
cd backend && SECRET_KEY=test-secret python3 manage.py runserver 127.0.0.1:8100 --noreload
cd frontend && PORT=3101 INTERNAL_API_URL=http://127.0.0.1:8100 NEXT_PUBLIC_API_URL=/api npm run start:next
cd frontend && E2E_BASE_URL=http://127.0.0.1:3101 E2E_API_URL=http://127.0.0.1:8100 npx playwright test --project=workflow-gate
cd frontend && E2E_BASE_URL=http://127.0.0.1:3101 E2E_API_URL=http://127.0.0.1:8100 npx playwright test e2e/rbac/utrmc_readonly_dashboard.spec.ts --project=rbac
```

## Results
- `npm run lint`: passed
- `npx tsc --noEmit`: passed
- targeted backend read-only regression tests: `29 passed`
- `npm test -- --watch=false`: `2 passed`
- `npm run build`: passed
- `pytest sims -q`: `200 passed`
- `manage.py check`: passed
- contract drift tests: passed
- canonical migration gate: passed
- drift guards: passed
- workflow gate on current tree: `6 passed`
- UTRMC readonly browser regression: `2 passed`

## Runtime notes
- Current-tree runtime verification used backend `127.0.0.1:8100` and frontend `127.0.0.1:3101`.
- `next start` still emits the known standalone warning; it did not block the verification run.
- Django emitted the known staticfiles warning for local runserver; it did not block API/browser verification.

## Outcome summary
- Active UTRMC read-only pages now tell the truth about `utrmc_user` capabilities.
- Nav-visible UTRMC oversight pages are backend-readable for `utrmc_user` where the active surface already implied read-only oversight.
- Mutation actions remain restricted to `admin` and `utrmc_admin`.
- Deferred legacy modules remain deferred and were not reintroduced.

## Remaining boundaries
- This pass did not reactivate or harden deferred logbook, cases, or legacy analytics flows.
- Broader non-critical legacy regression suites remain historical noise unless separately promoted into active gates.
- Frontend build policy still requires explicit lint/type gates because `next build` skips those validations in this setup.
