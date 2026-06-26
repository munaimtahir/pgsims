# Frontend Route / Action Catalog

Scope: routes and visible actions that participate in the truth map or influence it directly.

| Page / route | Visible controls | API client function(s) | Endpoint(s) called | Nav exposure | Backend exists |
| --- | --- | --- | --- | --- | --- |
| `/dashboard/utrmc` | KPI cards, monitoring links, no bulk creation form | `trainingApi.getUTRMCOperationalDashboard`, `userbaseApi.users.list`, `userbaseApi.departments.list`, `userbaseApi.hodAssignments.list`, `userbaseApi.supervisionLinks.list`, `trainingApi.listResidentTrainingRecords`, `userbaseApi.dataQuality.summary` | operational dashboard, users, departments, HOD, supervision, data quality | Yes | Yes |
| `/dashboard/utrmc/users` | Search, role, department, active, supervisor, programme filters; Edit; Reset Password; Deactivate; Delete; Add User | `userbaseApi.users.list/create/update/resetPassword/deactivate/delete`, `trainingApi.listPrograms`, `trainingApi.listResidentTrainingRecords` | `/api/users/`, `/api/users/{id}/reset-password/`, `/api/users/{id}/deactivate/`, `/api/users/{id}/` | Yes | Yes |
| `/dashboard/utrmc/supervision` | Add Link, department selector, validation error display, table with names/dates | `userbaseApi.supervisionLinks.list/create`, `userbaseApi.users.list`, `userbaseApi.departments.list` | `/api/supervision-links/`, `/api/users/`, `/api/departments/` | Yes | Yes |
| `/dashboard/utrmc/hod` | Add HOD, filtered candidate dropdown, empty-state message, validation error display | `userbaseApi.hodAssignments.list/create`, `userbaseApi.users.list`, `userbaseApi.departments.list` | `/api/hod-assignments/`, `/api/users/`, `/api/departments/` | Yes | Yes |
| `/dashboard/utrmc/resident-training` | Add Assignment, resident/programme selectors, edit/delete row actions | `trainingApi.listResidentTrainingRecords/createResidentTrainingRecord/updateResidentTrainingRecord/deleteResidentTrainingRecord`, `trainingApi.listPrograms`, `userbaseApi.users.list` | `/api/resident-training/`, `/api/programs/`, `/api/users/` | Yes | Yes |
| `/dashboard/onboarding/residents` | Upload Excel/CSV, map columns, preview, import, generate logins, export sheet | onboarding client functions | onboarding upload/map/import/login sheet endpoints | Yes | Yes |
| `/dashboard/onboarding/login-sheet` | Export Excel/PDF, mark issued, reset passwords | onboarding client functions | onboarding login sheet endpoints | Yes | Yes |
| `/dashboard/onboarding/batches` | Open batch, view imported residents, generate missing logins, export batch sheet, download error report | onboarding client functions | batch endpoints | Yes | Yes |
| `/dashboard/onboarding/incomplete-profiles` | Edit profile, reset password, mark complete, export list | onboarding client functions | incomplete profile endpoints | Yes | Yes |
| `/resident/complete-profile` | New password, confirm password, mobile, email, CNIC, missing program/year, submit | resident profile completion client functions | `/api/resident/complete-profile/` and profile-status endpoint | Yes | Yes |
| `/dashboard/utrmc/onboarding` | Legacy onboarding entrypoint | legacy component / redirect | mixed legacy onboarding links | No, hidden from nav | Partial / legacy |
| `/dashboard/utrmc/supervisors` | Legacy supervisor management | legacy supervisor component | supervisor admin APIs | No, hidden from nav | Yes |
| `/dashboard/utrmc/backup` | Backup center actions | backup API client functions | `/api/backup_center/*` | Yes for admins | Yes |

## Notes

- The active UTRMC dashboard is now monitoring-only and links out to dedicated workflow pages.
- Users page row actions now have direct backend bindings and no longer rely on hidden operations.
- The resident programme assignment page is the new explicit path for training record assignment.
