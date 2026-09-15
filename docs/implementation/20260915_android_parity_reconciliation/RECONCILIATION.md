# Android parity reconciliation — 2026-09-15

Source parents: parity `d8e2ce6` and released main `aef3bd2`.
Original parity is retained at `checkpoint/android-parity-before-reconciliation`.
This is a branch integration candidate, not a production release verdict.

## Resolution decisions

- Keep release token refresh mutex, checked token persistence, recovery/logout coordination,
  encrypted file fsync and metadata commit, owner checks and explicit retry replacement.
- Keep parity identity/onboarding/account screens, administrative users, workflow detail/actions,
  canonical progress endpoints and backend-owned post-auth routing.
- Keep release Inbox scrolling and awaited refresh/error handling; adapt supervisor test to its
  added password-change callback.
- Keep release permission-first leave idempotency and immutable training/key behavior; remove
  duplicate serializer declaration introduced by automatic merge.
- Use the release shared Locale.ROOT logbook classifier. Show loaded counts and canonical server
  totals under distinct labels, preserving both parity reporting and the released count fix.
- Reserve candidate version 1.1.10/code10, above the installed released 1.1.9/code9.
- Preserve canonical 1.1.9 release evidence; archive the parity parent's reports alongside this
  report rather than overwriting historical release conclusions.

## Verification

Candidate source `800f7ac`; `9364d37` adds fetched-ref support to the isolated backend helper.

- Android build, lint, debug APK and test APK: PASS.
- Android unit tests: 41, zero failures/errors/skips.
- Emulator `pgsims`: Inbox, ownership and staging checks — 7 tests PASS, 9.438s.
- Host process-death harness: post-ack, pre-ack, in-flight upload, source failure,
  reconciliation race and metadata failure PASS.
- Update 0 identity cleanup gate: PASS.
- Disposable PostgreSQL simultaneous leave replay: 1 test PASS, 0.863s.
- Disposable SQLite full backend suite: 929 tests PASS, 89.097s, one PostgreSQL-only skip
  (passed separately above); migration drift, migrate from zero and Django check PASS.

Evidence is in `evidence/`. Backend command on VPS uses
`VERIFY_REF=origin/feature/android-parity-stages-1-6 bash /tmp/verify-parity-backend.sh
sha256:7fe0b71e2c2d5e87e7e36e1ded9deaeab9f74995b9ae965497c3547dba8401e3 [postgres]`;
the helper is extracted with `git show` from the fetched candidate. Container settings use only
temporary SQLite or isolated PostgreSQL, not production settings/data/volumes.

Authenticated parity workflow matrix, remaining roadmap rows, signing and physical-device
acceptance remain subsequent work. None of the historical four-role release evidence is being
claimed as acceptance of the broader parity candidate.

No production service, database, Caddy, FCM or Play changes are part of this integration.

## Integration verdict

GO for branch reconciliation. The candidate is not yet release-certified: authenticated four-role
parity workflows and remaining roadmap rows stay open in `pendingwork.md`. Production main stays
at `aef3bd2`; the combined branch was fetched and tested without switching the VPS checkout.
