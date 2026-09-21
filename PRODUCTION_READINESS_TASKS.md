# Production Readiness Task List

Created: 2026-09-21

Source: production-readiness review of the environment context, repository source,
recent verification records, and read-only checks on the live VPS.

Audit verdict: **BLOCKED for unrestricted production use.** Core functionality is
substantially implemented. Uploaded-document privacy is the immediate priority;
a controlled pilot remains conditional on fixing that issue and defining the
approved pilot scope.

This document records follow-up work; it does not claim that any task below has
been completed or authorize production mutations. An item is complete only when
its acceptance condition is demonstrated and evidence is recorded. When an
implementation sprint starts, maintain its active scope and progress in
`SPRINT_STATE.md` according to `AGENTS.md`.

## P0 — Production blockers

- [ ] **Secure resident document access.** Replace public file serving with
  authenticated, ownership-checked access. Verify anonymous requests and unrelated
  users cannot retrieve documents.
- [ ] **Address previously exposed document URLs and caching.** Remove public
  caching for private files and assess existing exposure; document any required
  remediation.
- [ ] **Resolve committed secret material.** Remove the archived credential file
  from the tracked tree, establish whether affected credentials remain active,
  rotate affected credentials, and verify services still work. Do not record secret
  values in evidence.
- [ ] **Establish recoverable production backups.** Verify scheduled database and
  media backups, persistent storage, retention, and failure reporting.
- [ ] **Demonstrate disaster recovery.** Restore a recent backup into an isolated
  environment and verify login, records, and uploaded files.

## P1 — Fix incomplete production features

- [ ] **Enable production email delivery.** Configure the application and background
  workers; verify password-reset and notification delivery.
- [ ] **Reconcile the two logbook models.** Establish the canonical source and safely
  align imports, eligibility calculations, and existing records.
- [ ] **Verify eligibility accuracy.** Demonstrate that verified resident logbook
  entries correctly affect thresholds and milestone eligibility.
- [ ] **Complete web notifications.** Add a working inbox, read/unread actions,
  preferences, and navigation to related records.
- [ ] **Correct API schema generation.** Resolve conflicting serializer names and
  missing endpoint descriptions; regenerate and validate the schema.

## P1 — Complete web acceptance testing

Use disposable staging identities for all four roles: `ADMIN`, `RESIDENT`,
`SUPERVISOR`, and `SUPPORT_STAFF`.

- [ ] **Restore reproducible browser-test fixtures.** Resolve baseline-admin
  authentication failures and complete the smoke suite.
- [ ] **Verify universal identity creation.** Test all four roles, linked profiles,
  transaction rollback, audit events, and backend permissions.
- [ ] **Verify dynamic onboarding.** Test forced password change, newly required
  fields, declaration persistence, document completion, and next-login routing.
- [ ] **Verify document workflows.** Test upload, replacement, review, rejection,
  resubmission, authorized download, and access isolation.
- [ ] **Verify supervision workflows.** Test assignment creation, ending,
  primary-supervisor changes, pending-link resolution, and permissions. Verify
  currently available interfaces; the missing web change-primary action has a
  separate scope decision below.
- [ ] **Verify rotation lifecycle.** Test each supported transition, invalid
  transitions, and role restrictions.
- [ ] **Verify leave lifecycle.** Test submission, permitted editing,
  approval/rejection, and supported resubmission.
- [ ] **Verify evaluations and logbook review.** Test draft, submission, return,
  editing, resubmission, approval/verification, and rejection.
- [ ] **Verify reports and exports.** Check totals, filters, pagination, CSV contents,
  and resident/supervisor data isolation.
- [ ] **Verify bulk imports.** Test standard and flexible imports, mapping presets,
  dry-run/apply consistency, validation failures, and duplicate handling.
- [ ] **Verify a reproducible frontend build.** Resolve checkout build-permission
  problems if still present and build the intended release successfully.

## P1 — Complete Android release readiness

- [ ] Complete resident progress/report detail and filtering.
- [ ] Complete supervisor review-queue/workload parity and refresh behavior.
- [ ] Verify returned evaluation editing/resubmission and permitted leave editing.
- [ ] Run authenticated acceptance for all four roles against isolated staging
  fixtures.
- [ ] Verify notification isolation, preferences, pagination, and target navigation.
- [ ] Verify forced onboarding, expired sessions, refresh failure, and restart
  behavior.
- [ ] Verify offline retries, duplicate prevention, account switching, logout
  cleanup, and upload recovery.
- [ ] Complete physical-device accessibility, lifecycle, and performance checks.
- [ ] Rebuild the final release and verify version, signatures, and artifact hashes.
  The current sprint targets `1.1.9` / code `9`; verify Play availability before
  publication.
- [ ] Complete Play publication and post-publication verification through the
  approved release workflow.

## P2 — Decide scope before building deferred features

For each item, explicitly choose **required for launch**, **later release**, or
**backend-only**. Existing backend support does not establish a complete
user-facing workflow. These entries are scope decisions, not authorization to
implement excluded features.

- [ ] Research project management.
- [ ] Thesis/synopsis submission and review.
- [ ] Workshop participation and completion.
- [ ] Deputation/postings and resident scheduling.
- [ ] General admin audit-log/report viewer.
- [ ] Web action for changing a resident's primary supervisor.
- [ ] Android FCM push delivery.

## Final production gate

- [ ] Reconcile local, VPS, and running-image revisions; record the exact release.
- [ ] Update stale architecture, feature-status, and verification documents.
- [ ] Confirm all P0 tasks are closed.
- [ ] Confirm launch-required P1 tasks pass their acceptance checks.
- [ ] Record deferred features and operational limitations.
- [ ] Issue a fresh **GO / CONDITIONAL GO / BLOCKED** verdict with supporting
  evidence.

Core identity, directories, master data, and academic setup need verification,
not redevelopment. HOD as a separate role or dashboard remains intentionally
excluded.

## Audit baseline and evidence limits

- Local checkout reviewed:
  `/media/munaim/shared1/Documents/github/pgsims`, commit `5329019`.
- VPS checkout reviewed: `/home/munaim/srv/apps/pgsims`, commit `eee60ba`.
  The VPS was three commits ahead with additional onboarding changes; selected
  running backend files matched its checkout. This was not a complete image
  provenance verification.
- Live checks found 70 users, zero missing correct role profiles, zero profiles
  attached to the wrong role, and zero pending migrations.
- An unauthenticated HEAD request to an existing resident PDF returned HTTP 200
  with `Cache-Control: public, max-age=604800`. The document was not downloaded.
- Production used `django.core.mail.backends.console.EmailBackend`.
- The production Backup Center had no backup or restore job records. This does
  not prove that external backups are absent.
- Academic navigation and disaster-backup directory creation were already fixed
  in reviewed source; do not reopen those older findings without new evidence.
- Earlier test results are supporting evidence, not a fresh full acceptance run.
  Browser fixture failures and guarded Android test skips remain verification
  gaps rather than confirmed product failures.
- The audit changed no application code, deployment configuration, or production
  records. This checklist does not mark implementation work complete.

## References

- [Project operating rules](AGENTS.md)
- [Environment and deployed architecture context](docs/PROJECT_ENVIRONMENT_CONTEXT.md)
- [Canonical source of truth](docs/CANONICAL_SOURCE_OF_TRUTH.md)
- [Active sprint ledger](SPRINT_STATE.md)
- [Consolidated pending-work register](pendingwork.md)
- [Android gap-closure verification](docs/implementation/20260920_android_gap_closure/TEST_RESULTS.md)
- [Earlier web discovery audit](docs/discovery/WEBAPP_DISCOVERY_REPORT.md)
  — historical findings require reconciliation with current source.
