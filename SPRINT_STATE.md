# Android parity — merged signed 1.1.9/code9 candidate

## Scope
Parity is merged directly to `main`. The owner confirmed Play has not received versionCode 9, so
the final parity candidate retains 1.1.9/code9. Production remains on source commit `aef3bd2`.

## Completed Work
- Merge `800f7ac` preserves both `d8e2ce6` parity and released safeguards; original parity is retained at `checkpoint/android-parity-before-reconciliation`.
- Candidate `9364d37` pushed/fetched on VPS: Android build/lint, 41 unit tests, 7 emulator tests and process-death harness PASS.
- Disposable backend: 929 tests PASS (89.097s; one PG-only skip), separate PostgreSQL concurrency PASS (0.863s), schema/migrate/check and identity gate PASS.
- Evidence: `docs/implementation/20260915_android_parity_reconciliation/RECONCILIATION.md`. No production changes.
- Repeated fetched-candidate VPS isolation PASS: 929 SQLite tests plus the separate PostgreSQL
  concurrency test; no production database, environment or volume was used.
- Owner-signed parity 1.1.9/code9 APK and AAB produced; signatures and upload certificate match the
  established release identity. New local artifacts are under `builds/companion/1.1.9-parity-main/`;
  the earlier 1.1.9 and superseded 1.1.10 artifacts remain preserved separately.

- Authenticated resident/supervisor refresh, initial gated-session restoration/logout, four-role profile completion and backend identity/notification isolation checks recorded in parity acceptance report.
- Final authenticated ADMIN/RESIDENT/SUPERVISOR/SUPPORT_STAFF Home, Inbox, Profile, restoration and
  logout matrix PASS. ADMIN Users/create-dialog reachability PASS without creating a user.
- Owner-signed parity 1.1.9/code9 APK/AAB verification and prior upload certificate match PASS.
- Rebuilt code9 debug and test APKs installed on emulator `pgsims` with the explicit downgrade flag
  from superseded code10; final package metadata verified and default instrumentation PASS (29 tests).

- Authenticated recovery/logbook correction cycle: seven device methods PASS; leave21/logbook33
  exactly once, document2 byte hash matches, explicit discard/offline logout purge and server zero
  purge-record checks PASS. Runtime unchanged; demo fixtures retained and app signed out.
- Resident workflow implementation increment: draft/returned leave edit dialog and draft/returned
  evaluation response/comment editor now call the canonical PATCH endpoints and preserve record IDs.
  Android unit tests, lint and debug build pass; authenticated UI transition acceptance remains open.
- Supervisor workload and admin overview increment: supervisor home now renders canonical assigned
  resident/training/review totals; admin home renders the backend academic workflow overview cards.
  Android unit tests, lint and debug build pass.
- Admin reporting increment: added a Reports tab backed by data-quality, logbook, evaluation, and
  supervisor-workload endpoints with safe summary rendering. Android unit tests, lint and debug
  build pass.
- Returned workflow contract coverage: repository tests assert leave and evaluation PATCH paths,
  payload fields, response values and leave idempotency-key preservation (`e211118`).
- Admin CSV export: Reports now calls the four authenticated `export.csv` endpoints and shares
  generated CSV text; MockWebServer coverage verifies authorization and path selection (`b42a465`).
- Signed release verification: debug unit tests, lint, `assembleRelease`, and `bundleRelease` pass
  with the owner-controlled signing properties. Current artifact hashes are recorded in the release
  handoff; Play upload remains intentionally unperformed.
- Admin setup workspace: added authenticated, error-safe views for document requirements,
  supervision assignments, training records, academic periods/templates/categories, and review queue
  data (`abc804a`).

## Pending Work
1. Implement remaining unchecked `android.md` rows: role directories,
   document/supervision administration and complete pagination. Authenticated
   device acceptance is still required for the returned evaluation/leave editors; repository
   contract coverage is now present.
2. Complete evaluation/review payload and transition tests, full UI workflow forms, notification
   target/read/unread matrix and expired-session lifecycle cases; run isolated password/schema-state
   cases. See `docs/implementation/20260915_android_parity_acceptance/RECOVERY_WORKFLOW_RESULTS.md`.
3. Physical-device and Play Console upload/publication remain separate release gates. FCM and
   production deployment remain outside current scope.

## Verdict
GO for merge and signed-candidate handoff; CONDITIONAL GO for broader parity release pending the
explicit workflow, physical-device and Play gates above.
