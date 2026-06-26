# 2026-06-20 Onboarding Cleanup Audit

Scope:
- Simplified pilot onboarding so resident import is the only visible onboarding workflow.
- Paused the Google Workspace/AdminOps bridge from the visible UI.
- Kept existing bridge code in place, but removed its active navigation entry points.

Cleanup map:
- Keep: `/dashboard/onboarding/residents`, `/dashboard/onboarding/login-sheet`, `/dashboard/onboarding/batches`, `/dashboard/onboarding/incomplete-profiles`, `/dashboard/onboarding`
- Hide / redirect: `/dashboard/utrmc/onboarding`, `/dashboard/onboarding/finalization`
- Remove from visible UI: UTRMC "Open onboarding tools" CTA and the old bulk setup entry point

Developer note:
- Google Workspace/AdminOps bridge intentionally paused for pilot onboarding. Current onboarding issues only PGSIMS local usernames.

Validation:
- Backend: `python3 manage.py test sims.users.test_resident_onboarding -v 2` passed.
- Frontend Jest: resident onboarding, login sheet, batches, incomplete profiles, sidebar, ProtectedRoute, and complete-profile suites passed.
- Frontend lint: `npm run lint` passed.
- Frontend build: `npm run build` passed.

Notes:
- Legacy onboarding routes now redirect to `/dashboard/onboarding/residents`.
- The resident completion flow now refreshes the canonical completeness flag after successful first-login submission.
