# Android Sprints 1–5 — Final Release Verification

**GO — 2026-09-15 PKT, focused five-defect release.**

Resident Inbox scrolling, supervisor Inbox, leave UUID idempotency, logbook counts and encrypted
upload durability are repaired and verified. The final signed 1.1.9/code9 APK passed production
recovery: real offline draft creation, process restart, exactly-once persistence/replay, real document
picker/retry, replacement discard and populated-queue logout purge. Session/refresh and role gates pass.

- Deployed backend image: full SQLite 928 tests, zero failures/errors, 87.707s; one PostgreSQL-only
  skip passes separately in 0.794s. Migration drift/from-zero checks pass.
- Android 33 unit tests, lint/debug/release builds, final 5-test Inbox/ownership suite and host-controlled
  process-death/fault/race tests pass. APK/AAB signatures match the prior certificate.
- PR #17 and PR #18 merged to main. Tested backend/worker/beat deployed with verified backup and rollback
  tags. Only the document-upload directory chain required a scoped group/SGID permission correction.
- Production database/cache/Celery healthy, frontend/API HTTP 200, FCM disabled. No Caddy, Play,
  unrelated workflow/service, identity-role or legacy-folder changes.

Exact artifacts, hashes, commands, production fixture IDs, retained rollback material and evidence:
[RELEASE_CLOSURE.md](RELEASE_CLOSURE.md). Earlier failures remain historical in
[TEST_RESULTS.md](TEST_RESULTS.md). Broader parity, full workflow-action/physical-device/accessibility/
performance certification and Play publication are outside this five-defect closure.
