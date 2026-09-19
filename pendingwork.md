# Android pending-work register

Updated 2026-09-20. This is the consolidated Android backlog. `android.md` remains the capability
matrix; this file separates current gap closure from next-sprint work and release-only gates.

## Current sprint — gap closure

- [x] Repository pagination traversal for resident snapshot, admin setup, supervisor queues,
  notifications, templates and academic list responses.
- [x] Repository contract test for a multi-page notification response.
- [x] Non-credentialed connected Android suite on `pgsims` API 36: 51 executed, 22 intentional
  skips, 0 failures.
- [x] Inbox UI regression suite: 3/3 tests pass on `pgsims` after query-aware fixtures.
- [x] Synthetic process-death/recovery harness: all six local storage/recovery scenarios pass.
- [ ] Authenticated four-role emulator acceptance for current source.
- [ ] Resident returned evaluation edit/resubmit UI and same-record response preservation.
- [ ] Resident permitted leave edit UI and same-record/idempotency-key preservation.
- [ ] Supervisor review payloads, scoring, comments, return/reject reasons and refresh behavior.
- [ ] Notification recipient isolation, read/unread, preferences, target navigation and paging.
- [ ] Forced password/schema-change onboarding, stale state, restart and back-navigation cases.
- [ ] Expired access token, refresh rotation, failed refresh and no-refresh-loop cases.
- [ ] Offline duplicate-worker, account-switch, retry, logout purge and upload metadata recovery.
- [ ] Runtime verification of current role directory/search/filter/details behavior.
- [ ] Runtime verification of current admin setup, reports and CSV export behavior.

## Next sprint — other Android implementation work

- [ ] Dedicated role directories and detail/profile-management surfaces where canonical APIs support
  them; do not invent archive/reset endpoints.
- [ ] Resident canonical progress/report detail, filters and multi-page totals.
- [ ] Supervisor generic review queue/workload/status parity beyond existing workflow queues.
- [ ] Admin document-requirement management and pending-supervisor resolution/linking.
- [ ] Admin supervision assignment list/detail/create/end/change-primary flows.
- [ ] Admin training records, academic periods, rotation templates, evaluation templates and
  logbook-category authoring.
- [ ] Admin leave/logbook/evaluation workflow actions where the backend exposes canonical contracts.
- [ ] Admin dashboard totals, data-quality/monitoring drilldowns and report detail/filter screens.
- [ ] Resident-progress, supervisor-workload, logbook, evaluation and data-quality report exports
  where canonical APIs and authorization are available.
- [ ] Flexible import header detection, mapping validation, mapping presets, dry-run and apply.
- [ ] Standard master-data/template exports and supervision CSV import.
- [ ] Complete list error recovery, stable ordering, filters and empty/failed page behavior across
  all future directory, academic, report and bulk screens.

## Release gates — after gap closure

- [ ] Physical-device install/upgrade and lifecycle testing.
- [ ] Accessibility, font scale, TalkBack, touch targets, keyboard/date/number input and contrast.
- [ ] Performance, rotation, background, low-memory and process-death checks on a physical device.
- [ ] Final source freeze and rebuild of the existing `1.1.9` / code `9` release artifacts.
- [ ] Verify package metadata, AAB/APK signatures, upload certificate and hashes.
- [ ] Play Console upload/publication and post-upload verification.

## Explicitly deferred / not part of current Android sprint

- [ ] FCM activation or push delivery claims; compile-time FCM remains disabled.
- [ ] Google Drive/cloud-backup integration or connection changes.
- [ ] Android backup/restore UI and destructive restore certification.
- [ ] Production/VPS/Caddy/deployment changes.
- [ ] Resident research, thesis, workshops, postings and other web-deferred workflows without an
  active canonical mobile contract.
- [ ] Academic workflow seed/demo actions; never run them during verification.

## Cross-project web audit pending work retained from the concurrent remote update

These items are not part of the Android gap-closure sprint, but remain documented so the shared
workspace does not lose the web audit backlog:

- [ ] Complete Update 0 identity/onboarding and HOD designation cleanup; preserve only four roles.
- [ ] Remove or explicitly isolate dummy legacy compatibility routes.
- [ ] Verify universal identity creation and dynamic onboarding for all four roles with disposable
  fixtures, transaction rollback, audit events and browser coverage.
- [ ] Complete and browser-verify rotation, leave, logbook and evaluation lifecycle workflows.
- [ ] Verify/harden web document upload/review/resubmission and notification read/preferences flows.
- [ ] Expose and verify approved academic reports/CSV exports and selected bulk import/export paths.
- [ ] Add approved academic/report/monitoring routes to role-aware web navigation.
- [ ] Restore reproducible disposable E2E credentials/database and resolve root-owned `.next` build
  artifacts; re-run full browser verification.
- [ ] Decide eligibility coverage and classify research, synopsis/thesis and workshop workflows as
  required, backend-only, mobile, or deferred before implementation.

Remote web evidence: backend pytest 1,211 passed/9 skipped/82.13% coverage; affected frontend
142/142 passed; full Jest 252/252 passed; typecheck/lint/Django checks passed; prior Playwright
smoke 19/25 passed with six baseline-admin 401 blockers; direct frontend build is blocked by
root-owned `.next/trace-build`.

## Historical records, not active pending work

Older documents mentioning 1.1.3, 1.1.7, 1.1.8 or the superseded 1.1.10 candidate are retained as
provenance. The active release identity remains `pk.vexel.pgrcompanion`, version `1.1.9`, code `9`.
