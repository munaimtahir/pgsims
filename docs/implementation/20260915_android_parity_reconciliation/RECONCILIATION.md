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

In progress. Build/unit/lint, synthetic emulator recovery/Inbox and isolated backend suite must
pass before the branch integration is considered verified. Authenticated parity workflow matrix,
remaining roadmap rows, signing and physical-device acceptance remain subsequent work.

No production service, database, Caddy, FCM or Play changes are part of this integration.
