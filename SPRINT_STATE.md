# Android focused release closure

## Scope
Five defects: resident Inbox scrolling, supervisor Inbox, leave idempotency,
logbook status counts, durable encrypted upload recovery. User authorized paused
handoff, focused implementation and production backend + signed APK/AAB release;
no Play publication. Preserve parity branch at d8e2ce6. Work directly in this
checkout on fix/android-release-closure from main 436053a.

## Completed Work
- Paused handoff confirmed; parity changes committed and preserved at d8e2ce6.
- Read AGENTS.md/environment context; production and laptop are separate checkouts.
- Focused source checkpoint 431e09d pushed/fetched on VPS; no production runtime changes.
- Android 32 unit tests, lint, debug/test APK PASS. Inbox + owner/logout race
  instrumentation OK (4 tests). Host-kill post/pre-ack and in-flight upload
  recovery, source/reconcile/metadata fault tests PASS. SUPPORT_STAFF UI PASS.
- Backend 431e09d: isolated SQLite 928 tests/0 failures/0 errors, 102.644s, one
  PostgreSQL-only skip; separate PostgreSQL race test PASS (0.878s). Drift check,
  migrate-from-zero and Django check PASS. Containers/PG tmpfs/network removed.
  VPS logs: /home/munaim/srv/apps/pgsims-verification/closure-{sqlite,postgres}.log.

## Pending Work
1. Reconcile sanitized backend evidence into canonical reports; backend gates complete.
2. Fix resident/supervisor Inbox and shared count classifier in Android baseline.
3. Make encrypted staging durable, owner-bound and race-safe; stream retries and
   cancel recovery before logout purge; add process-death/fault tests.
4. Run Android tests/lint and emulator acceptance with authorized labeled fixtures;
   run full isolated VPS SQLite suite and separate disposable PostgreSQL races.
5. Freeze/build signed 1.1.9/code9 APK/AAB; verify signature/hash; merge/push main,
   verify VPS source; backup and scoped backend deployment only after gates pass.
6. Reconcile evidence into pendingwork.md and canonical Sprint 1–5 reports; recheck
   production health. GO requires all mandatory evidence committed on main.

## Verdict
CONDITIONAL GO; repairs and candidate acceptance pending. Never log credentials.
