# Android parity — merged signed 1.1.10 candidate

## Scope
Parity is merged directly to `main`. Production remains on verified 1.1.9 (`aef3bd2`); signed
candidate is 1.1.10/code10.

## Completed Work
- Merge `800f7ac` preserves both `d8e2ce6` parity and released safeguards; original parity is retained at `checkpoint/android-parity-before-reconciliation`.
- Candidate `9364d37` pushed/fetched on VPS: Android build/lint, 41 unit tests, 7 emulator tests and process-death harness PASS.
- Disposable backend: 929 tests PASS (89.097s; one PG-only skip), separate PostgreSQL concurrency PASS (0.863s), schema/migrate/check and identity gate PASS.
- Evidence: `docs/implementation/20260915_android_parity_reconciliation/RECONCILIATION.md`. No production changes.
- Repeated fetched-candidate VPS isolation PASS: 929 SQLite tests plus the separate PostgreSQL
  concurrency test; no production database, environment or volume was used.
- Owner-signed 1.1.10/code10 APK and AAB produced; signatures and upload certificate match verified
  1.1.9. Local artifacts are under `builds/companion/1.1.10/`.

- Authenticated resident/supervisor refresh, initial gated-session restoration/logout, four-role profile completion and backend identity/notification isolation checks recorded in parity acceptance report.
- Final authenticated ADMIN/RESIDENT/SUPERVISOR/SUPPORT_STAFF Home, Inbox, Profile, restoration and
  logout matrix PASS. ADMIN Users/create-dialog reachability PASS without creating a user.
- Owner-signed 1.1.10 APK/AAB verification and prior Play upload certificate match PASS.

## Pending Work
1. Implement remaining unchecked `android.md` rows: returned evaluation/leave edits, supervisor
   queues/workload, role directories, document/supervision administration, reports/CSV and pagination.
2. Run authenticated workflow-transition/offline-upload matrix and isolated password/schema-state
   cases; the shell/session matrix is complete.
3. Physical-device and Play Console upload/publication remain separate release gates. FCM and
   production deployment remain outside current scope.

## Verdict
GO for merge and signed-candidate handoff; CONDITIONAL GO for broader parity release pending the
explicit workflow, physical-device and Play gates above.
