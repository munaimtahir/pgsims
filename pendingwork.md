# Android release closure — all five items complete

**GO — 1.1.9/code9, 2026-09-15.** Backend deployed; signed APK/AAB ready.

- [x] Resident Inbox crash: fixed; real signed Inbox and exact/missing target checks pass.
- [x] Supervisor Inbox: present; role-scoped signed navigation and session checks pass.
- [x] Leave idempotency: immutable persisted UUID; concurrent PostgreSQL and production HTTPS
  replay pass; leave #20 remains exactly one row per key.
- [x] Logbook counts: shared normalization/summing; list Approved 1 equals Progress verified 1.
- [x] Upload durability: acknowledged encrypted staging survives process death; real picker/retry
  succeeds with matching server hash; replacement discard and populated-queue logout purge pass.

No mandatory gates remain for this five-defect release. Backend 928 tests, Android 33 unit tests,
final device/fault/recovery checks and production health pass; evidence is committed on main.

[Canonical release report](docs/implementation/20260914_android_sprints_2_3_4/RELEASE_CLOSURE.md)
contains artifacts, hashes, commands, fixture IDs, backup and rollback details.

Outside this release scope: the preserved parity branch at `d8e2ce6`, full workflow-action/
physical-device/accessibility/performance certification and Play publication. FCM remains disabled.

## Next sprint — parity integration and acceptance

- [x] Reconciled `feature/android-parity-stages-1-6` with `aef3bd2`; combined Android, emulator,
  recovery and isolated backend gates PASS (see `SPRINT_STATE.md`).
- [x] Authenticated four-role Home/Inbox/Profile/session-restoration/logout matrix passes; ADMIN
  Users and universal-create dialog also render without performing a creation mutation.
- [ ] Complete unchecked parity workflows in `android.md`: directories,
  document/supervision administration and pagination. CSV export is now wired in the Admin Reports tab;
  returned evaluation/leave editors
  are implemented and their PATCH contracts are covered by `e211118`; authenticated transition acceptance remains required.
- [x] Owner-signed parity 1.1.9/code9 APK/AAB signatures and prior Play upload certificate match;
  code9 is still available in Play per owner confirmation.
- [x] Current source builds and signs successfully with the owner-controlled release properties;
  Play upload remains intentionally unperformed.
- [ ] Physical-device checks and Play Console upload/publication remain open.

Authenticated recovery addendum: restart/replay/exactly-once, PDF hash, logbook return/correction/
resubmit and offline discard/logout purge PASS. Full UI/evaluation/expired-session/schema cases
remain open; see `docs/implementation/20260915_android_parity_acceptance/RECOVERY_WORKFLOW_RESULTS.md`.

---

# Web application discovery audit — 2026-09-19

The following unchecked items were identified by the web audit. Discovery does not count as implementation or verification.

## A. Broken existing functionality

- [x] WEB-DISC-001 — Repair admin monitoring Jest mock/API contract. Module/role: admin dashboard/ADMIN. Status: BUILT_WORKING after verification. Frontend: mock `getAdminDashboardMonitoring` and assert response rendering. Backend: none identified. Evidence: `frontend/app/dashboard/utrmc/page.test.tsx`; focused and full Jest runs (252/252). Acceptance met: focused page test and full Jest pass.
- [ ] WEB-DISC-005 — Remove/migrate active HOD/faculty-era role and permission drift. Module/role: identity, rotations, training, contracts/all. Status: BUILT_NEEDS_DEBUG; P0. Frontend: no old role/designation controls. Backend: migrate/constrain old values, remove HOD endpoints/models/references where required, preserve designation text only if approved. Dependencies: AGENTS.md role lock. Evidence: static scan in `docs/discovery/evidence/20260919_command_results.txt`. Acceptance: four roles only; HOD not a role/model/endpoint; migration/RBAC tests pass.
- [ ] WEB-DISC-026 — Remove or explicitly isolate dummy legacy compatibility routes. Module/role: backend routing/all. Status: BUILT_NEEDS_DEBUG; P2. Frontend: none identified. Backend: remove mounted dummy URL modules or document/test approved aliases. Evidence: `backend/sims_project/urls.py`, `backend/sims/users/*dummy_urls.py`, `backend/sims/rotations/urls.py`. Acceptance: no misleading business route returns a generic dashboard redirect; URL tests pass.

## B. Partially built workflows

- [ ] WEB-DISC-002 / WEB-DISC-003 — Verify universal identity creation and dynamic onboarding for all four roles. Module/role: users/onboarding/ADMIN plus new users. Status: BLOCKED_UNVERIFIED; P1. Frontend: exercise `/users/new`, `/complete-profile`, `/change-password`, `/api/auth/me/`. Backend: verify transaction, profile registry/schema versions, audit and rollback. Data: disposable four-role fixture. Dependencies: WEB-DISC-005, WEB-DISC-006. Acceptance: four role/profile pairs, default flags, rollback, next-login missing field and audit actions pass; browser matrix passes.
- [ ] WEB-DISC-008 — Complete and browser-verify rotation lifecycle. Module/role: academics rotations/ADMIN|SUPERVISOR|RESIDENT. Status: PARTIALLY_BUILT; P1. Frontend: list/new/detail/submit/approve/return/complete and refresh. Backend: confirm permissions and assignment scope. Data: resident-supervisor/hospital-department fixture. Acceptance: state persists after reload and unauthorized resident is denied. Regression: API + Playwright.
- [ ] WEB-DISC-009 — Complete and browser-verify leave lifecycle. Module/role: academics leave/ADMIN|SUPERVISOR|RESIDENT. Status: PARTIALLY_BUILT; P1. Frontend/backend analogous to WEB-DISC-008. Acceptance: submit, approve/reject/return, reload and duplicate-click tests.
- [ ] WEB-DISC-010 — Make logbook discoverable and verify draft→submit→review→correction/resubmit. Module/role: academics logbook/RESIDENT|SUPERVISOR|ADMIN. Status: PARTIALLY_BUILT; P1. Frontend: role-aware nav, page tests, status labels. Backend: verify canonical `academics.LogbookEntry` permissions/reviewer assignment. Acceptance: full transition visible to both roles and survives reload.
- [ ] WEB-DISC-011 — Make evaluation workflow discoverable and verify submission/review. Module/role: academics evaluations/RESIDENT|SUPERVISOR|ADMIN. Status: PARTIALLY_BUILT; P1. Frontend: nav/page tests and errors. Backend: validate template/submission permissions. Acceptance: create, submit, review, return, resubmit and cross-user denial.
- [ ] WEB-DISC-015 — Expose and verify academic reports/CSV exports. Module/role: reports/ADMIN|SUPERVISOR|RESIDENT. Status: PARTIALLY_BUILT; P2. Frontend: role-aware navigation/download handling. Backend: confirm report scopes/CSV response. Acceptance: authorized export matches canonical records.

## C. Missing frontend for usable backend

- [ ] WEB-DISC-022 — Confirm requirement and, if approved, build research web workflow. Module/role: training research/RESIDENT|SUPERVISOR. Status: NOT_BUILT; P2. Frontend: edit/submit and supervisor approval. Dependency: scope decision; historically deferred. Acceptance: CRUD/submit/review/resubmit with audit/isolation.
- [ ] WEB-DISC-023 — Confirm requirement and, if approved, build synopsis/thesis web workflow. Module/role: training submissions/RESIDENT|SUPERVISOR. Status: NOT_BUILT; P2. Frontend: documents, submit, review queue/action. Dependency: scope decision. Acceptance: upload/review/correction lifecycle.
- [ ] WEB-DISC-024 — Confirm requirement and, if approved, build workshops web surface. Module/role: training workshops/RESIDENT. Status: NOT_BUILT; P3. Frontend: list/completion/detail. Dependency: scope decision. Acceptance: completion persistence and summary consistency.

## D. Frontend blocked by backend/data/configuration

- [ ] WEB-DISC-018 — Verify/harden web document upload/review/resubmission. Module/role: resident documents/RESIDENT|ADMIN. Status: PARTIALLY_BUILT; P1. Frontend: file errors, reload and download evidence. Backend: content/ownership/status verification. Data: disposable media fixtures. Acceptance: upload, defer, correction, replace and authorized download survive reload.
- [ ] WEB-DISC-020 — Verify notifications read/mark/preferences flow. Module/role: notifications/all. Status: BLOCKED_UNVERIFIED; P2. Frontend: expose list/preferences if required. Backend: confirm NotificationService and scope. Acceptance: unread count, mark-read and refresh consistent.
- [ ] WEB-DISC-021 — Verify selected bulk import/export paths used by web. Module/role: bulk/ADMIN. Status: PARTIALLY_BUILT; P2. Frontend: validation/error/dry-run states. Backend: entity permissions/canonical mappings. Acceptance: disposable CSV dry-run/apply/export.

## E. Navigation/layout/routes/orphans

- [ ] WEB-DISC-028 / WEB-DISC-003 — Add missing academic/report/monitoring routes to role-aware navigation after permission review. Module/role: sidebar/all relevant roles. Status: PARTIALLY_BUILT; P1. Frontend: update `frontend/lib/navRegistry.ts`, dashboard links and return destinations. Backend: none identified. Acceptance: every approved built route has an intentional entry point and deep-link/refresh/back tests.

## F. Verification blockers

- [ ] WEB-DISC-006 / WEB-DISC-029 — Restore reproducible disposable E2E credentials/database and resolve root-owned `.next` build artifacts. Module/role: test/build environment/all. Status: BLOCKED_UNVERIFIED; P1. No product change until environment corrected. Evidence: six 401 smoke failures and EACCES build output. Acceptance: smoke 25/25 or documented exclusions; production build succeeds in isolated workspace; no production mutation.

## G. Confirmed or scope-pending future requirements

- [ ] WEB-DISC-025 — Decide eligibility web coverage and classify required, backend-only, mobile, or deferred. Module/role: training eligibility/ADMIN|RESIDENT. Status: REQUIREMENT_UNCONFIRMED; P3. Acceptance: signed scope decision and matrix/backlog disposition.
