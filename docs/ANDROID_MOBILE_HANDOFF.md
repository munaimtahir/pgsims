# PGR SIMS Android — Development Handoff

## Current locked position

PGR SIMS Android is being introduced now because mobile onboarding is expected to materially improve resident compliance compared with requiring residents to use the web portal for first-time profile completion.

The MVP is therefore deliberately onboarding-first, but the Android application is being architected as a permanent first-class client of PGR SIMS.

The long-term objective is progressive functional parity with the web application.

Both clients must use the same canonical backend, data models, permissions, services and workflows.

## MVP user flow

Administration creates the resident account and issues credentials.

Resident:
1. installs app
2. logs in
3. completes personal and training information
4. selects or declares supervisor
5. uploads required documents or defers eligible documents
6. reviews and submits onboarding
7. waits for administrative review
8. corrects/resubmits if requested
9. sees approved state
10. continues seeing persistent reminders for outstanding documents

After onboarding, the resident receives a lightweight mobile view of current training information, supervisor, documents, workshop status and logbook summary where already available.

Supervisor and staff mobile functionality remains intentionally limited in MVP to basic self-information and resident/onboarding status visibility.

Administrative approval remains web-first in MVP.

## Key architecture lock

Android must not become a parallel system.

Every mobile capability must resolve through:

`UI → API → canonical backend service → canonical data`

The backend remains authoritative for:
- validation
- permissions
- onboarding state
- resident profile
- supervision
- documents
- training status
- logbook/workshop data
- approvals

## Production sequence

1. Initial Android repository scaffold
2. Add authoritative Android documentation
3. M0 — backend/API mobile readiness discovery
4. M1 — canonical mobile API contract
5. M2 — Android platform foundation
6. M3 — authentication/bootstrap
7. M4 — resident onboarding
8. M5 — documents/compliance
9. M6 — resident post-onboarding experience
10. M7 — minimal supervisor/staff views
11. M8 — notifications/compliance
12. M9 — hardening/release

## Status as of 2026-09-03

M0 (API readiness discovery) through M6 (resident post-onboarding experience) are implemented —
see `docs/implementation/20260903_resident_onboarding_android_mvp/FINAL_IMPLEMENTATION_REPORT.md`
for the full account. Login, the complete onboarding wizard (personal info, training/enrollment,
supervisor, documents, review & submit), the pending-review/correction-required/approved states,
and a 4-tab post-approval Home (Home/Training/Documents/Profile) are all real, wired to the
canonical backend — no mock data, no Android-only state machine. `versionCode` is now 2 /
`0.2.0`. A **debug** APK was built and its data flows verified live against the real backend
(login, save/resume, document upload, submit, admin correction, resubmit, admin approval, all
authorization boundaries); on-device/emulator UI verification is still outstanding because this
build environment has no working Android emulator (no KVM) — that must happen on a machine with
a real device or working emulator before a signed release build.

M7 (minimal supervisor/staff views), M8 (notifications), and M9 (release hardening/signed AAB) are
still outstanding — signing happens on a separate machine that holds the release keystore.
