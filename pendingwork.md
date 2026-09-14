# Android release closure — all five items complete

**GO — 1.1.9/code9, 2026-09-15.** Backend deployed; signed APK/AAB ready.

- [x] Resident Inbox crash: fixed; real signed Inbox and exact/missing target checks pass.
- [x] Supervisor Inbox: present; role-scoped signed navigation and session checks pass.
- [x] Leave idempotency: immutable persisted UUID; concurrent PostgreSQL and production HTTPS
  replay pass; leave #20 remains exactly one row per key.
- [x] Logbook counts: shared normalization/summing; list Approved 1 equals Progress verified 1.
- [x] Upload durability: acknowledged encrypted staging survives process death; real picker/retry
  succeeds with matching server hash; replacement discard and populated-queue logout purge pass.

No mandatory gates remain for this five-defect release. Backend 928 tests, Android 33 unit tests,
final device/fault/recovery checks and production health pass; evidence is committed on main.

[Canonical release report](docs/implementation/20260914_android_sprints_2_3_4/RELEASE_CLOSURE.md)
contains artifacts, hashes, commands, fixture IDs, backup and rollback details.

Outside this release scope: the preserved parity branch at `d8e2ce6`, full workflow-action/
physical-device/accessibility/performance certification and Play publication. FCM remains disabled.
