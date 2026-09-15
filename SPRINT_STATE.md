# Android parity — acceptance and remaining workflows

## Scope
Continue `feature/android-parity-stages-1-6` after reconciliation with released main `aef3bd2`.
Production remains on verified 1.1.9; parity candidate is 1.1.10/code10.

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

## Pending Work
1. Resume authenticated device matrix after competing MedSIMS automation releases `pgsims`: foreground repeatedly switched to `pk.vexel.medsims/.MainActivity`; owner asked to pause it. All four demo profiles now completed using authorized demo values and two audited demo lookups; ADMIN credentials added privately. See `docs/implementation/20260915_android_parity_acceptance/TEST_RESULTS.md` for exact fixture values and remaining device gates.
2. Implement remaining unchecked `android.md` rows: returned evaluation/leave edits, supervisor queues/workload, role directories, document/supervision administration, reports/CSV and pagination.
3. Physical-device and Play Console upload/publication remain separate release gates. FCM and
   production deployment remain outside current scope.

## Verdict
GO for branch reconciliation; CONDITIONAL GO for broader parity release pending the explicit gates above.
