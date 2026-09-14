# PGSIMS Android — Pending Work & Sprint Roadmap

Last updated: 2026-09-14 23:36 PKT
Repository HEAD: 921969bbeed29fb897fe57dc32f8614de6ab446b
Branch: remediation/pgsims-final-production-readiness

## Purpose

This document is the canonical tracker for remaining PGSIMS Android development.

Rules:
- [ ] means pending
- [~] means actively being implemented
- [x] means implemented AND verified
- Blocked items remain unchecked and must state the blocker.
- A sprint is checked complete only after all mandatory acceptance gates pass.

## Sprint 1 — Core Resident–Supervisor Workflow Parity

Status: [~] CONDITIONAL GO — core functionality validated on device; remaining gates are session/refresh and full regression coverage.

### 1. Role Routing and Mobile Access Safety

- [x] Recognise RESIDENT explicitly
- [x] Recognise SUPERVISOR explicitly
- [x] Recognise ADMIN explicitly
- [x] Recognise SUPPORT_STAFF explicitly
- [x] Handle unknown/unsupported roles safely
- [x] Prevent ADMIN from entering resident UI
- [x] Prevent SUPPORT_STAFF from entering resident UI
- [x] Add restricted-mobile screen for unsupported mobile roles
- [x] Verify fresh login routing
- [ ] Verify restored-session routing — Blocker: not yet exercised on authenticated restart flow.
- [ ] Verify token-refresh routing — Blocker: not yet exercised during this session.
- [x] Verify logout/re-login routing

### 2. Resident Leave Workflow

- [x] Discover and document canonical leave API contract
- [x] Leave request list
- [x] Leave request detail
- [x] New leave request
- [x] Draft support using the backend draft status
- [x] Submit leave request
- [x] Display supervisor decision
- [x] Display return/rejection reason
- [x] Edit/resubmit where backend permits
- [x] Error/validation handling
- [x] End-to-end resident → supervisor → resident verification

### 3. Resident Evaluations / WBA

- [x] Discover canonical evaluation/WBA API contract
- [x] Evaluation list
- [x] Evaluation detail
- [x] Pending/in-progress/completed state presentation
- [x] Supervisor feedback display
- [x] Resident actions where backend explicitly supports them
- [x] Error and empty-state handling
- [x] Real-backend verification

### 4. Supervisor Evaluation Review

- [x] Pending evaluation count reconciled with backend
- [x] Evaluation queue
- [x] Evaluation detail
- [x] Resident/context information
- [x] Supervisor review actions supported by backend
- [x] Remarks/comments where required
- [x] Approve action
- [x] Return action
- [x] Reject action
- [x] Queue refresh after action
- [x] Resident sees resulting state

### 5. Workflow State Consistency

- [x] Audit canonical backend states
- [x] Shared Android workflow-state mapping
- [x] Eliminate contradictory Android status labels
- [ ] Ensure lists/details/dashboard counts agree — Blocker: not yet validated on non-demo dataset.
- [x] Ensure allowed actions derive from backend state

### 6. Regression Verification

Resident:

- [x] Authentication
- [ ] Profile — Blocker: full regression pass not yet completed in this sequence.
- [ ] Onboarding — Blocker: full regression pass not yet completed in this sequence.
- [ ] Dashboard — Blocker: full regression pass not yet completed in this sequence.
- [ ] Training programme
- [ ] Current posting
- [ ] Rotation history
- [ ] Supervisor assignment
- [ ] Logbook create/edit/submit
- [ ] Research status
- [ ] Workshop status
- [ ] Document upload/replacement

Supervisor:

- [x] Resident list
- [ ] Resident progress/detail
- [ ] Logbook approval
- [ ] Leave approval
- [ ] Rotation approval
- [ ] Research approval
- [x] Evaluation approval/review

### 7. Documentation

- [x] Update Android API integration documentation
- [ ] Update resident capability matrix
- [ ] Update supervisor capability matrix
- [x] Correct stale read-only supervisor documentation
- [x] Update test/runbook documentation
- [x] Add Sprint 1 implementation report

### 8. Sprint 1 Release Gates

- [x] Android debug build PASS
- [x] Android release compilation PASS
- [x] Unit tests PASS
- [ ] Relevant instrumentation/UI tests PASS
- [x] Backend/API checks PASS
- [x] Real authenticated resident workflow PASS
- [x] Real authenticated supervisor workflow PASS
- [ ] No role-routing regression — Blocker: requires a full retained-session test matrix.
- [ ] Existing Android workflows regression-tested — Blocker: broad regression matrix still pending.
- [x] Evidence captured
- [x] Sprint report completed

## Sprint 2 — Mobile Workflow Inbox & Notifications

Status: [ ] PENDING

- [x] Unified Action Required inbox
- [ ] Resident workflow notifications
- [ ] Supervisor pending-action notifications
- [x] Notification list
- [x] Unread count/badge
- [x] Mark read/unread
- [x] Deep-link notification → relevant workflow
- [ ] Notification preferences
- [x] Background refresh strategy
- [ ] Evaluate push-notification architecture
- [ ] Implement push only after infrastructure/design approval
- [ ] Notification API regression tests
- [ ] Sprint 2 documentation and evidence

## Sprint 3 — Mobile Resilience & Offline Drafts

Status: [ ] PENDING

- [x] Connectivity-state handling
- [x] Logbook offline draft
- [x] Leave offline draft
- [x] Secure local draft storage
- [x] Draft recovery after process restart
- [x] Safe synchronization
- [ ] Conflict handling
- [ ] Failed submission retry
- [ ] Document upload retry
- [ ] Upload progress
- [ ] Interrupted upload handling
- [ ] Security review of cached sensitive information
- [ ] Sprint 3 tests/documentation/evidence

## Sprint 4 — Mobile Reporting & Resident Progress

Status: [ ] PENDING

- [x] Resident progress overview
- [x] Training milestone summary
- [x] Rotation completion summary
- [x] Logbook completion metrics
- [x] Evaluation/WBA progress
- [x] Research progress
- [x] Workshop/compliance status
- [x] Supervisor resident-progress summary
- [ ] Appropriate mobile reports
- [ ] Export/share only where justified
- [ ] Sprint 4 tests/documentation/evidence

## Sprint 5 — Mobile UX, Reliability & Release Hardening

Status: [ ] PENDING — do not implement in Sprint 1

- [ ] Cross-screen UX consistency audit
- [ ] Accessibility audit
- [ ] Loading-state consistency
- [ ] Empty-state consistency
- [ ] Error-state consistency
- [ ] Session-expiry behaviour
- [ ] Deep-link verification
- [ ] Performance profiling
- [ ] Network efficiency review
- [ ] Security review
- [ ] Crash-path review
- [ ] Release build verification
- [ ] Emulator/device acceptance suite
- [ ] Play-ready release package
- [ ] Final capability matrix
- [ ] Final release report

## Explicit Web-First / Not Planned for Immediate Android Parity

- Admin user management
- Master-data administration
- Bulk import/export
- Backup/restore
- Full audit-log administration
- Data-quality administration
- Complex institutional reports
- System configuration

These capabilities remain intentionally web-first unless a later product decision establishes a
genuine mobile use case. Android parity means parity for appropriate resident and supervisor
workflows, not duplication of every desktop administrative function.

## Sprint 1 Evidence and Blockers

Implementation evidence and blockers will be recorded in:
`docs/implementation/20260912_android_sprint1_workflow_parity/SPRINT_1_IMPLEMENTATION_REPORT.md`.

Verified evidence:
- Signed release APK installed on `emulator-5554` and launched successfully (`pk.vexel.pgrcompanion`,
  `versionName=1.1.7`, `versionCode=7`).
- Supervisor demo walkthrough (`supervisor` / `supervisor123`):
  - Sign-in, dashboard, evaluation queue, and evaluation detail/action controls validated (`Approve`, `Reject`,
    `Return for revision`, `Cancel`).
- Resident demo walkthrough (`pgrdrmuhammadadeelbas` / `pgfmu123`):
  - Sign-in, resident workspace nav, dashboard, and core screens validated.
- Live backend chain has been validated for leave and evaluation resident→supervisor→resident updates.
- VPS backend checks and full 921-test suite remain passing.
- Android debug build, release compilation, lint, unit tests, and emulator launch pass.

Remaining mandatory gates:
- [x] Authenticated Android emulator walkthrough for resident and supervisor.
- [x] Owner-supplied signed release APK/AAB verification.
  - Signed artifacts:
    - [APK] `app-companion/build/outputs/apk/release/app-companion-release.apk`
    - [AAB] `app-companion/build/outputs/bundle/release/app-companion-release.aab`
- [ ] ADMIN/SUPPORT_STAFF routing smoke checks on device
- [ ] Restored-session and token-refresh routing checks
- [ ] Full resident/supervisor regression matrix for existing feature surfaces
