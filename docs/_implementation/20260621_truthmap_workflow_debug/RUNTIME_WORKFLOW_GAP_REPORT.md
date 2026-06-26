# Runtime Workflow Gap Report

## Reported live gaps and current status

| Gap | Status | Notes |
| --- | --- | --- |
| Cannot add supervisor properly from Users page | Fixed | Users page now exposes the necessary form fields and supports supervisor-aware create/update payloads. |
| Supervision Links save fails with generic error | Fixed | Backend validation details are now surfaced to the UI. |
| Supervision Links table shows blank names | Fixed | Table now uses nested supervisor/resident objects and fallback text. |
| HOD Assignment save fails with generic error | Fixed | UI now shows the backend validation message. |
| HOD dropdown shows inappropriate users | Fixed | Candidate pool excludes admin users and uses supervisor/faculty candidates. |
| Users page missing reset/deactivate/delete and filters | Fixed | Added the requested filters and row actions. |
| No clear programme/course assignment workflow | Fixed | Dedicated Resident Programme Assignment page exists and is linked from Users and nav. |
| Dashboard is too operational | Fixed | Dashboard now serves as a monitoring page with scoped KPI cards and quick links. |
| Duplicate onboarding/import surfaces visible | Mitigated | The nav now exposes only the simplified onboarding path; legacy routes remain hidden/legacy. |

## Notes on verification

- Backend workflow slice passed:
  - `python3 manage.py test sims.users.test_userbase_api sims.users.test_resident_onboarding`
- Frontend workflow slice passed:
  - `npm run typecheck`
  - `npm test -- --runInBand --runTestsByPath app/dashboard/utrmc/page.test.tsx app/dashboard/utrmc/users/page.test.tsx app/dashboard/utrmc/hod/page.test.tsx app/dashboard/utrmc/supervision/page.test.tsx app/dashboard/utrmc/resident-training/page.test.tsx components/layout/Sidebar.test.tsx lib/api/userbase.test.tsx lib/api/training.test.tsx`

## Remaining legacy surfaces

- Some older routes still exist on disk, but they are not in the current sidebar and are not part of the active pilot workflow.
- Google Workspace / AdminOps bridge endpoints remain present in the backend but are intentionally paused for this sprint.
