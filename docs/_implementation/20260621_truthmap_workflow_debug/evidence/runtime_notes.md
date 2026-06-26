# Runtime Notes

## Environment

- Local frontend server: `http://127.0.0.1:3000`
- Capture tool: Playwright running against the local Next.js app
- Auth seeding:
  - `pgsims_access_token` cookie seeded with a valid JWT-like payload containing the UTRMC admin role
  - `pgsims_user_role` and `pgsims_access_exp` cookies seeded alongside it
  - `auth-storage` localStorage seeded so the client store hydrates immediately

## Workflow verification steps

1. Opened `/dashboard/utrmc/users`.
2. Applied the user filters:
   - role = `resident`
   - department = `Urology`
   - supervisor = `Dr Sana`
   - programme/course = `FCPS-URO`
3. Verified the row action buttons were visible:
   - Edit
   - Reset Password
   - Deactivate
   - Delete
4. Clicked `Reset Password` for the resident row and captured the browser-runtime confirmation overlay showing the request result and the `pgfmu123` password.
5. Opened `/dashboard/utrmc/resident-training` and captured the resident programme assignment workspace with the current assignment table visible.
6. Opened `/dashboard/utrmc/supervision`, created a supervision link, and captured the refreshed table showing supervisor and resident names.
7. Opened `/dashboard/utrmc/hod`, created an HOD assignment, and captured the refreshed table showing department and HOD names.
8. Opened `/dashboard/utrmc` and captured the monitoring-only dashboard layout with KPI cards and quick links.

## Runtime evidence files

- `screenshots/users-filters-row-actions.png`
- `screenshots/users-reset-password.png`
- `screenshots/resident-programme-assignment.png`
- `screenshots/supervision-link-created.png`
- `screenshots/hod-assignment-created.png`
- `screenshots/utrmc-monitoring-dashboard.png`

## Notes

- The capture run used mocked API responses to make the browser behavior deterministic and to prove the UI wiring for the priority workflows.
- The reset-password screenshot includes an evidence overlay because the page action is backend-driven and does not emit a native success toast in the current UI.
