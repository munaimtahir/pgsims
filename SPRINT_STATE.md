# SPRINT_STATE.md — Resident-only onboarding access

## Scope

Keep mandatory onboarding enforcement for `RESIDENT` users and disable the
onboarding workflow for `ADMIN`, `SUPERVISOR`, and `SUPPORT_STAFF` users.

## Completed work

- Backend `/api/auth/me/` now routes only residents with incomplete onboarding to `/complete-profile`.
- Non-resident direct visits to `/complete-profile` redirect to their role dashboard.
- Non-resident navigation and dashboard UI no longer advertise onboarding completion.
- Added backend and frontend regression coverage for the resident-only policy.

## Pending work

1. Run frontend and backend targeted tests, then deploy the backend/frontend changes to the VPS checkout.
2. Verify live login routing with available authenticated accounts; confirm resident onboarding remains enforced.

## Closure state

Implementation is complete locally; test and deployment verification remain open.
