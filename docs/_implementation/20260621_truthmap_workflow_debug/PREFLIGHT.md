# Preflight

- Branch: `fix/frontend-backend-truthmap-workflows`
- Baseline commit: `3599a67f4956fa31a1e9f4ce1a359a9bf776140b`
- Evidence folder: `docs/_implementation/20260621_truthmap_workflow_debug/`

## Reported live issues

1. Users page could not safely support supervisor onboarding or account operations.
2. Supervision Links saved with a generic failure and rendered blank names in the table.
3. HOD Assignments saved with a generic failure and exposed the wrong candidate pool.
4. Resident programme/course assignment had no dedicated page.
5. Dashboard was too operational and not scoped as a monitoring page.
6. The UI truth map had frontend actions without a clear backend link and backend endpoints without visible frontend exposure.

## Validation notes

- Backend workflow slice targeted for this sprint:
  - `python3 manage.py test sims.users.test_userbase_api sims.users.test_resident_onboarding`
- Frontend workflow slice targeted for this sprint:
  - `npm run typecheck`
  - `npm test -- --runInBand --runTestsByPath app/dashboard/utrmc/page.test.tsx app/dashboard/utrmc/users/page.test.tsx app/dashboard/utrmc/hod/page.test.tsx app/dashboard/utrmc/supervision/page.test.tsx app/dashboard/utrmc/resident-training/page.test.tsx components/layout/Sidebar.test.tsx lib/api/userbase.test.ts lib/api/training.test.ts`

## Screenshot status

- No browser screenshot artifacts were captured in this environment.
- Runtime verification was performed through targeted unit tests and backend test execution.
