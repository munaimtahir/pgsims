# Android focused release closure — pending work

Candidate `e0c98b5`, 1.1.9/code9. **CONDITIONAL GO** until final production acceptance.
See [release closure report](docs/implementation/20260914_android_sprints_2_3_4/RELEASE_CLOSURE.md).
Concurrent parity remains preserved at `d8e2ce6`; it is not part of this release.

## Five original defects

1. Resident Inbox: source, Compose regression and real resident Inbox PASS.
2. Supervisor Inbox: source and Compose navigation PASS; authenticated login/Inbox/restoration/refresh PASS.
3. Leave idempotency: immutable UUID, scope/collision/rollback tests PASS; 928-test SQLite
   suite and PostgreSQL race PASS. Production exactly-once replay awaits deployment.
4. Logbook counts: shared normalized/summed classifier and unit test PASS; final device
   list/Progress comparison pending.
5. Upload durability: host process-death, interrupted upload, failed source/metadata,
   reconciliation race, owner isolation and logout race PASS. Real picker/success recovery pending.

## Actions still required

- Complete authenticated candidate resident/supervisor regression and recovery fixture checks.
- Verify signed APK/AAB; run full suite against newly built backend image.
- Backup, merge verified focused branch to main, verify VPS checkout, deploy only backend/worker/beat.
- Verify labeled production drafts exactly once per key and real document upload/retry/discard/purge.
- Recheck health, commit canonical evidence and release verdict on main.

FCM remains disabled. No Play publication, Caddy changes, unrelated workflows or destructive
resets. Earlier labeled leave 17/18/19 and logbook 31 are retained historical fixtures.
