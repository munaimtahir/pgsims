# SPRINT_STATE.md — Supervisor/resident demo identity linkage

## Scope

Repair the `supervisor`/`resident` demo-login accounts so they resolve to real canonical
Urology identities (Prof. Dr. M. Tahir Bashir Malik / Dr. Jawad Saifullah) instead of their own
empty profiles, fix the resulting broken super-admin supervisor detail route, and verify the
resident↔supervisor relationship end-to-end via web + API (Android pending device access).
Full report: `docs/implementation/20260910_urology_institutional_demo/SUPERVISOR_RESIDENT_IDENTITY_LINKAGE.md`.

## Completed work

- Took `/tmp/pgsims_pre_supervisor_link_20260910.dump` before any writes.
- Added idempotent `reconcile_urology_supervisor_profiles` management command: re-points the
  real SupervisorProfile/ResidentProfile (+ ResidentTrainingRecord for residents) onto the
  `supervisor`/`resident` logins via a scratch-user swap (avoids OneToOne unique collision),
  copies the real identity's name, deactivates the now-redundant real-identity login. 9/9 tests
  pass; verified idempotent and correct against production.
- Found and fixed a second, pre-existing bug during verification:
  `ResidentAcademicSummaryView`/`SupervisorAcademicSummaryView` looked profiles up by pk instead
  of `user_id` (inconsistent with `ResidentProfileViewSet`/`SupervisorProfileViewSet` and what
  the frontend actually sends), causing the admin's `/supervisors/{id}` and `/residents/{id}`
  pages to 500/show empty data. Fixed + 2 new regression tests + updated affected fixtures;
  143/143 academics tests pass.
- Verified end-to-end via real HTTP calls and an authenticated browser session against
  production: `supervisor` → M. Tahir Bashir Malik (7 residents, correctly scoped), `resident` →
  Dr. Jawad Saifullah (supervisor = Tahir), admin `/supervisors/63` and `/residents/62` pages
  render correctly, and Dr. Jawad Saifullah's pre-seeded pending logbook/evaluation already
  route to Tahir's review queue with no client-specific logic anywhere in the path.
- `django check`, migration check, and supervision/users/training test suites (45 tests) all
  pass with no regressions.

## Pending work

1. Android emulator verification of the same `resident`/`supervisor` login → My Residents /
   pending-workflow chain — blocked on device/emulator access, not a known backend issue (see
   "Known limitations" in the linked report).
2. Pre-existing onboarding-completeness gaps are documented but intentionally not fixed here
   (out of scope): `supervisor` profile missing phone/email/designation_ref; `resident` profile
   missing academic_session_ref.

## Closure state

Backend identity linkage, the admin-route fix, and web+API verification are complete and
deployed to production. Android-side verification remains pending device availability.
