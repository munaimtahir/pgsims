# Stage 7: Specific Module Verdicts

## Programs

- Page load: Yes, `200`
- Visible in nav: Yes, `Programmes`
- Create button visible: No
- Edit button visible: No
- Create/edit actions working: No visible create/edit program UI was found on the loaded page

Additional evidence:

- The page is a per-program detail surface.
- After selecting a program, the UI exposes tabs for:
  - overview
  - policy
  - milestones
  - templates

Verdict: program-management frontend is partial. Existing-program detail management is present; program create/edit UI is not.

## Training Programs

- Separate module from Programs: No
- Complete management UI: No
- Policy management from frontend: Yes
- Milestones visible from frontend: Yes
- Program-template/rotation-template management path: Yes
- Create/edit top-level Training Program records: No visible UI

Verdict: “Training Programs” is the same surface as Programs. It is not a complete standalone management UI.

## Workshops

- Visible in nav: No
- Route exists: Yes, `/dashboard/resident/workshops`
- Backend exists: Yes, workshops endpoints returned `200`
- Frontend state on route: deferred notice only
- Completion add/verify from frontend: No active UI
- Runtime workshop seed data available: No, current workshop list count is `0`

Verdict: real frontend gap. Backend exists, but the active frontend workflow is deferred and undiscoverable from nav.

## Logbook

- Resident logbook visible: Yes
- Resident create draft: Yes
- Resident submit: Yes
- Supervisor review UI present: Yes, on supervisor dashboard
- Supervisor review action works: Yes
- Seeded pending entry verified: Yes, created in this run and observed in supervisor review queue

Verdict: resident and supervisor logbook workflow is present and working on fresh runtime.

## Leave

- Resident create draft: Yes, inside resident schedule page
- Resident submit: Yes
- Supervisor approve: Yes, on supervisor dashboard
- Supervisor return/reject: Yes, on supervisor dashboard
- Separate sidebar entries for leave: No

Verdict: workflow exists and works, even though it is embedded rather than exposed as standalone nav modules.

## Supervision Links

- Page load: Yes
- `+ Add Link` opens modal: Yes
- Safe create test via current frontend UI: No
- Result of UI save attempt: `Save failed`
- Backend link API exists: Yes

Fresh root cause:

- frontend posts `supervisor` and `resident`
- backend requires `supervisor_user_id` and `resident_user_id`

Verdict: real frontend-backend contract bug.

## Data Quality

- Page load: Yes
- User-facing data load: No
- Direct backend endpoints fail: No, direct backend calls are `200`
- Frontend proxied endpoints fail: Yes, browser gets `404`
- Cause type: route/proxy mismatch, not feature flag and not permission denial

Failing proxied endpoints:

- `/api/admin/data-quality/summary`
- `/api/admin/data-quality/users`
- `/api/admin/data-quality/audit`

Verdict: real frontend proxy/path configuration issue.

## Bulk

- UI visible: Yes, inside UTRMC overview page
- Dry-run button: Present; endpoint validated and returned expected `400` for empty file
- Template button: Verified working; download received
- Export button: Verified working; download received
- Apply import button: Present, but not executed against canonical data in this audit

Verdict: bulk UI is present and materially wired up. Missing-UI claims from the previous audit are false.
