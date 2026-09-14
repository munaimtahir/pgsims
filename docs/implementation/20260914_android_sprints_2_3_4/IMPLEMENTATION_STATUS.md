# Android Sprints 2–4 — Combined Delivery Status

## Implemented foundation

- The canonical Django notification API now has recipient-scoped `POST
  /api/notifications/mark-unread/` alongside mark-read.
- Notification responses expose `target` only when `metadata.target` matches the supported
  typed contract: `leave`, `evaluation`, `logbook`, `rotation`, `research`, or
  `resident_progress`, with an optional positive numeric `id`.
- `NotificationService` preserves only valid typed targets; arbitrary metadata is never promoted
  to Android navigation.
- Android has an authenticated Inbox navigation item, notification list, read/unread controls,
  and safe target routing. Legacy/invalid targets remain display-only.
- Android retains failed leave and logbook creations as encrypted app-private drafts. Each request
  receives a client UUID; leave persists it in a unique backend field and logbook persists it in
  canonical `extra_data`. Repeated mobile creates return the original resource.
- A unique WorkManager job runs with a network constraint (the Android minimum periodic interval
  is 15 minutes) and removes a draft only after the server accepts it. Failed jobs retry with
  WorkManager backoff.
- The Android Progress tab renders read-only resident training, posting, rotation, logbook,
  evaluation/WBA, research, and workshop summaries from already scoped APIs.

## Deliberately outstanding

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

## Local verification

- `python3 -m py_compile` passed for the changed notification backend modules.
- `./gradlew :app-companion:compileDebugKotlin` passed after encrypted upload queue changes.
- Django is not installed in this checkout, so migration/check/test verification remains a VPS
  gate after commit and synchronisation. This is not production approval.
