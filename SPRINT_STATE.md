# SPRINT_STATE.md — Resident-only onboarding access

## Scope

Keep mandatory onboarding enforcement for `RESIDENT` users and disable the
onboarding workflow for `ADMIN`, `SUPERVISOR`, and `SUPPORT_STAFF` users.

## Completed work

- Backend `/api/auth/me/` now routes only residents with incomplete onboarding to `/complete-profile`.
- Non-resident direct visits to `/complete-profile` redirect to their role dashboard.
- Non-resident navigation and dashboard UI no longer advertise onboarding completion.
- Added backend and frontend regression coverage for the resident-only policy.
- Frontend checks passed; backend regression suite passed 15 tests in the VPS container.
- Commit `bdd105b` deployed to the VPS; backend and frontend containers are healthy.

## Pending work

1. Verify live login routing with authenticated resident and non-resident accounts when credentials are available.

## Closure state

Implementation, tests, and deployment are complete; authenticated browser verification remains pending account access.
