# Evidence Log

## Commands Run

### Route and code inspection

```bash
rg --files frontend/app/dashboard | sort
sed -n '1,260p' frontend/lib/navRegistry.ts
sed -n '1,260p' frontend/lib/rbac.ts
sed -n '1,260p' backend/sims_project/urls.py
sed -n '1,320p' backend/sims/training/urls.py
sed -n '1,320p' backend/sims/users/userbase_urls.py
find backend/sims -maxdepth 2 -type d | sort
rg -n "include\\(\"sims\\._legacy|_legacy" backend/sims_project backend/sims -g'*.py'
```

### Frontend gates

```bash
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
cd frontend && npm test -- --watch=false
cd frontend && npm run build
```

Results:

- `npm run lint`: passed
- `npx tsc --noEmit`: passed
- `npm test -- --watch=false`: passed, but emitted a Jest haste naming collision with `.next/standalone/package.json`
- `npm run build`: passed, but build output showed:
  - `Skipping validation of types`
  - `Skipping linting`
  - warnings around `--localstorage-file`

### Backend gates

```bash
cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q
SECRET_KEY=test-secret python3 backend/manage.py check
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -v
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret pytest sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -v
cd backend && SECRET_KEY=test-secret pytest sims/rotations/test_canonical_migration_gate.py -v
cd backend && SECRET_KEY=test-secret pytest sims/_devtools/tests/test_drift_guards.py -v
```

Results:

- `pytest sims -q`: `195 passed`
- `manage.py check`: passed
- research return drift test: passed
- eligibility drift tests: passed
- canonical migration gate: passed
- drift guards: passed

### Browser/runtime verification

Fresh runtime started on non-conflicting ports to avoid relying on pre-existing listeners:

```bash
cd backend && SECRET_KEY=test-secret python3 manage.py seed_e2e
cd frontend && npx playwright install chromium
cd backend && SECRET_KEY=test-secret python3 manage.py runserver 127.0.0.1:8100 --noreload
cd frontend && PORT=3101 INTERNAL_API_URL=http://127.0.0.1:8100 NEXT_PUBLIC_API_URL=/api npm run start:next
cd frontend && E2E_BASE_URL=http://127.0.0.1:3101 E2E_API_URL=http://127.0.0.1:8100 npx playwright test --project=workflow-gate
```

Results:

- `seed_e2e`: passed
- workflow gate: `6 passed (2.2m)`

## Routes Inspected

### Frontend

- `/dashboard/resident`
- `/dashboard/resident/schedule`
- `/dashboard/resident/progress`
- `/dashboard/resident/research`
- `/dashboard/resident/thesis`
- `/dashboard/resident/workshops`
- `/dashboard/resident/postings`
- `/dashboard/supervisor`
- `/dashboard/supervisor/research-approvals`
- `/dashboard/supervisor/residents/[id]/progress`
- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/postings`
- `/dashboard/utrmc/eligibility-monitoring`
- `/forgot-password`
- `/register`

### Backend

- `/api/auth/*`
- `/api/hospitals/`
- `/api/departments/`
- `/api/hospital-departments/`
- `/api/users/`
- `/api/supervision-links/`
- `/api/hod-assignments/`
- `/api/programs/`
- `/api/program-templates/`
- `/api/rotations/`
- `/api/leaves/`
- `/api/postings/`
- `/api/my/research/`
- `/api/my/thesis/`
- `/api/my/workshops/`
- `/api/my/eligibility/`
- `/api/residents/me/summary/`
- `/api/supervisors/me/summary/`
- `/api/utrmc/eligibility/`

## Tests Reviewed

- `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts`
- `frontend/e2e/workflows/utrmc-management.spec.ts`
- `frontend/e2e/workflows/supervisor-review.spec.ts`
- `frontend/e2e/regression/utrmc_readonly_dashboard.spec.ts`

## Files Reviewed

### Authority docs

- `README.md`
- `docs/contracts/TRUTH_TESTS.md`
- `docs/contracts/ROUTES.md`
- `docs/_recovery/20260402T122809Z/01-active-surface-map.md`
- `docs/_milestones/20260402T133945Z-rotation-postings-closure/00-executive-summary.md`

### Frontend implementation

- `frontend/components/auth/ProtectedRoute.tsx`
- `frontend/lib/navRegistry.ts`
- `frontend/lib/rbac.ts`
- `frontend/app/dashboard/resident/page.tsx`
- `frontend/app/dashboard/resident/schedule/page.tsx`
- `frontend/app/dashboard/resident/progress/page.tsx`
- `frontend/app/dashboard/resident/research/page.tsx`
- `frontend/app/dashboard/resident/thesis/page.tsx`
- `frontend/app/dashboard/resident/workshops/page.tsx`
- `frontend/app/dashboard/resident/postings/page.tsx`
- `frontend/app/dashboard/supervisor/page.tsx`
- `frontend/app/dashboard/supervisor/research-approvals/page.tsx`
- `frontend/app/dashboard/utrmc/page.tsx`
- `frontend/app/dashboard/utrmc/hospitals/page.tsx`
- `frontend/app/dashboard/utrmc/departments/page.tsx`
- `frontend/app/dashboard/utrmc/users/page.tsx`
- `frontend/app/dashboard/utrmc/matrix/page.tsx`
- `frontend/app/dashboard/utrmc/supervision/page.tsx`
- `frontend/app/dashboard/utrmc/hod/page.tsx`
- `frontend/app/dashboard/utrmc/programs/page.tsx`
- `frontend/app/dashboard/utrmc/postings/page.tsx`
- `frontend/app/dashboard/utrmc/eligibility-monitoring/page.tsx`
- `frontend/app/register/page.tsx`
- `frontend/next.config.mjs`
- `frontend/package.json`

### Backend implementation

- `backend/sims_project/urls.py`
- `backend/sims/training/urls.py`
- `backend/sims/users/userbase_urls.py`

## Important Observations

1. `_legacy` modules are on disk but not in the live Django include set.
2. The active Next.js route tree contains no logbook, cases, certificate, or search surfaces.
3. README still overclaims active readiness for certificates, analytics/reporting, search, and broad export.
4. `docs/contracts/ROUTES.md` still references `/dashboard/utrmc/users/new` and `/dashboard/utrmc/users/[id]`, but those routes do not exist in the current route tree.
5. `frontend/e2e/regression/utrmc_readonly_dashboard.spec.ts` is stale:
   - expects test ids not present in current UTRMC overview
   - references pending logbook queue text from a deferred surface
6. The fresh current-tree workflow gate passed fully.
7. The browser gate also surfaced auth throttling sensitivity:
   - repeated login attempts triggered a transient `429`
   - the suite still completed successfully
