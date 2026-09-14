# Android Sprints 2–4 — Combined Delivery Status

**Current focused release: GO, signed 1.1.9/code 9.** All five blockers are closed; see
[RELEASE_CLOSURE.md](RELEASE_CLOSURE.md). The sections below also cover historical implementation
and a wider roadmap outside this release scope.

For the current shared runtime/API verification state, read
[`VERIFICATION_LEDGER.md`](VERIFICATION_LEDGER.md) before changing this document or claiming a
release gate is complete.

## Implemented foundation

- The canonical Django notification API now has recipient-scoped `POST
  /api/notifications/mark-unread/` alongside mark-read.
- Notification responses expose `target` only when `metadata.target` matches the supported
  typed contract: `leave`, `evaluation`, `logbook`, `rotation`, `research`, or
  `resident_progress`, with an optional positive numeric `id`.
- `NotificationService` preserves only valid typed targets; arbitrary metadata is never promoted
  to Android navigation.
- Android has a Resident Inbox destination plus notification list, read/unread controls and target
  routing code. Current device verification found two release defects: Supervisor navigation does
  not expose Inbox, and Resident Inbox crashes because it is nested inside another vertical scroll.
  Legacy/invalid targets remain display-only once the screen is reachable.
- Android retains failed leave and logbook creations as encrypted app-private drafts. Each request
  receives a client UUID. Logbook persists it in canonical `extra_data` and deduplicates successfully.
  Leave has a unique model field but its serializer drops the incoming key; repeated creates
  currently duplicate records. See the final verification correction below.
- A unique WorkManager job runs with a network constraint (the Android minimum periodic interval
  is 15 minutes) and removes a draft only after the server accepts it. Failed jobs retry with
  WorkManager backoff.
- The Android Progress tab renders read-only resident training, posting, rotation, logbook,
  evaluation/WBA, research, and workshop summaries from already scoped APIs.

## Implemented recovery foundation with outstanding verification

- Document selections are staged in an `EncryptedFile` under app-private storage before any
  network request.  The queue persists the server document id, filename, MIME type, byte count,
  retry count, opaque local id and error state.  A constrained WorkManager job retries uploads;
  only a successful server response deletes encrypted material.  Logout purges all queued
  institutional drafts and uploads before another account can sign in.
- Supervisor resident progress already uses the scoped on-demand detail screen from Sprint 1;
  no administrative or export reporting is added to mobile.
- FCM registration code remains available, but Android has a compile-time `FCM_ENABLED=false`
  kill switch and Django defaults to `FCM_ENABLED=false`. PGR SIMS owns recipient-scoped device
  registrations and dispatch; no Firebase credential is committed or required for this release.

Final baseline recovery evidence: both drafts survive restart; logbook deduplicates and leave fails
deduplication. Normal upload restart/discard/purge passes; the immediate-exit orphan finding remains
explicit. The 1.1.8/code 8 baseline APK was rebuilt and verified; later feature edits are outside
that result. See `TEST_RESULTS.md`.

## Local verification

- `python3 -m py_compile` passed for the changed notification backend modules.
- `./gradlew :app-companion:compileDebugKotlin` passed after encrypted upload queue changes.
- A later network-isolated VPS container run completed 922 Django tests with zero failures/errors
  and three explicit repository-file skips. This closes the former full-suite lock, while the
  skipped deployment-domain checks and focused affected API checks remain pending. See the canonical
  test report and verification ledger; this is not a GO release verdict.

## Final baseline verification correction — 2026-09-15

The final [canonical report](TEST_RESULTS.md) supersedes earlier pending verification descriptions.
Logbook restart/replay deduplication passes (record 31), but **leave idempotency fails**: its serializer
ignores the non-editable request ID, producing labeled drafts 17/18/19 with null keys. Normal encrypted
upload restart, explicit discard and populated-queue logout purge pass; abrupt-exit metadata loss
remains a recovery finding. The baseline APK was rebuilt and tested; later parity-branch edits are
separate, unverified work. Both Inbox defects and the logbook count mismatch reproduce on that APK.
Verdict: CONDITIONAL GO. No claim that all mobile APIs/workflows are verified follows from the
922-test SQLite pass or from successful authenticated API reads.
