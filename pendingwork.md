# PGSIMS Android — Pending Work & Sprint Roadmap

Last updated: 2026-09-12 (Asia/Karachi) — implementation and verification pass
Repository HEAD: 500f95ef6a4d07170d9dafca7923fa909950d43b
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

Status: [ ] CONDITIONAL — implementation complete; final signed-release and authenticated-emulator gates remain

### 1. Role Routing and Mobile Access Safety

- [~] Recognise RESIDENT explicitly
- [~] Recognise SUPERVISOR explicitly
- [~] Recognise ADMIN explicitly
- [~] Recognise SUPPORT_STAFF explicitly
- [~] Handle unknown/unsupported roles safely
- [~] Prevent ADMIN from entering resident UI
- [~] Prevent SUPPORT_STAFF from entering resident UI
- [~] Add restricted-mobile screen for unsupported mobile roles
- [ ] Verify fresh login routing
- [ ] Verify restored-session routing
- [ ] Verify token-refresh routing
- [ ] Verify logout/re-login routing

### 2. Resident Leave Workflow

- [~] Discover and document canonical leave API contract
- [~] Leave request list
- [~] Leave request detail
- [~] New leave request
- [~] Draft support using the backend draft status
- [~] Submit leave request
- [~] Display supervisor decision
- [~] Display return/rejection reason
- [~] Edit/resubmit where backend permits
- [~] Error/validation handling
- [ ] End-to-end resident → supervisor → resident verification

### 3. Resident Evaluations / WBA

- [~] Discover canonical evaluation/WBA API contract
- [~] Evaluation list
- [~] Evaluation detail
- [~] Pending/in-progress/completed state presentation
- [~] Supervisor feedback display
- [~] Resident actions where backend explicitly supports them
- [~] Error and empty-state handling
- [ ] Real-backend verification

### 4. Supervisor Evaluation Review

- [~] Pending evaluation count reconciled with backend
- [~] Evaluation queue
- [~] Evaluation detail
- [~] Resident/context information
- [~] Supervisor review actions supported by backend
- [~] Remarks/comments where required
- [~] Approve action
- [~] Return action
- [~] Reject action
- [~] Queue refresh after action
- [ ] Resident sees resulting state

### 5. Workflow State Consistency

- [~] Audit canonical backend states
- [~] Shared Android workflow-state mapping
- [~] Eliminate contradictory Android status labels
- [~] Ensure lists/details/dashboard counts agree
- [~] Ensure allowed actions derive from backend state

### 6. Regression Verification

Resident:

- [ ] Authentication
- [ ] Profile
- [ ] Onboarding
- [ ] Dashboard
- [ ] Training programme
- [ ] Current posting
- [ ] Rotation history
- [ ] Supervisor assignment
- [ ] Logbook create/edit/submit
- [ ] Research status
- [ ] Workshop status
- [ ] Document upload/replacement

Supervisor:

- [ ] Resident list
- [ ] Resident progress/detail
- [ ] Logbook approval
- [ ] Leave approval
- [ ] Rotation approval
- [ ] Research approval
- [ ] Evaluation approval/review

### 7. Documentation

- [ ] Update Android API integration documentation
- [ ] Update resident capability matrix
- [ ] Update supervisor capability matrix
- [ ] Correct stale read-only supervisor documentation
- [ ] Update test/runbook documentation
- [ ] Add Sprint 1 implementation report

### 8. Sprint 1 Release Gates

- [ ] Android debug build PASS
- [ ] Android release compilation PASS
- [ ] Unit tests PASS
- [ ] Relevant instrumentation/UI tests PASS
- [ ] Backend/API checks PASS
- [ ] Real authenticated resident workflow PASS
- [ ] Real authenticated supervisor workflow PASS
- [ ] No role-routing regression
- [ ] Existing Android workflows regression-tested
- [ ] Evidence captured
- [ ] Sprint report completed

## Sprint 2 — Mobile Workflow Inbox & Notifications

Status: [ ] PENDING — do not implement in Sprint 1

- [ ] Unified Action Required inbox
- [ ] Resident workflow notifications
- [ ] Supervisor pending-action notifications
- [ ] Notification list
- [ ] Unread count/badge
- [ ] Mark read/unread
- [ ] Deep-link notification → relevant workflow
- [ ] Notification preferences
- [ ] Background refresh strategy
- [ ] Evaluate push-notification architecture
- [ ] Implement push only after infrastructure/design approval
- [ ] Notification API regression tests
- [ ] Sprint 2 documentation and evidence

## Sprint 3 — Mobile Resilience & Offline Drafts

Status: [ ] PENDING — do not implement in Sprint 1

- [ ] Connectivity-state handling
- [ ] Logbook offline draft
- [ ] Leave offline draft
- [ ] Secure local draft storage
- [ ] Draft recovery after process restart
- [ ] Safe synchronization
- [ ] Conflict handling
- [ ] Failed submission retry
- [ ] Document upload retry
- [ ] Upload progress
- [ ] Interrupted upload handling
- [ ] Security review of cached sensitive information
- [ ] Sprint 3 tests/documentation/evidence

## Sprint 4 — Mobile Reporting & Resident Progress

Status: [ ] PENDING — do not implement in Sprint 1

- [ ] Resident progress overview
- [ ] Training milestone summary
- [ ] Rotation completion summary
- [ ] Logbook completion metrics
- [ ] Evaluation/WBA progress
- [ ] Research progress
- [ ] Workshop/compliance status
- [ ] Supervisor resident-progress summary
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
- Live resident leave create → submit → supervisor approve → resident `APPROVED`.
- Live resident evaluation create → submit → supervisor approve → resident `APPROVED`.
- VPS backend checks and full 921-test suite pass.
- Android debug build, release compilation, lint, unit tests, and emulator cold-launch pass.

Remaining mandatory gates:
- [ ] Authenticated Android emulator walkthrough for resident and supervisor.
- [ ] Owner-supplied signed release APK/AAB verification.
