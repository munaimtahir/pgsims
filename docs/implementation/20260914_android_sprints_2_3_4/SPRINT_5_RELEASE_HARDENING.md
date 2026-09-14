# Android Sprints 1–5 — Final Release Verification

**CONDITIONAL GO — 2026-09-15.** The verification pass is complete; release acceptance is not.
The canonical results and reproducible commands are in [TEST_RESULTS.md](TEST_RESULTS.md).

- Isolated VPS SQLite suite: 922 tests, zero failures/errors, three explicit repository-file skips,
  59.308s. Test container removed; production health and FCM-disabled state rechecked.
- SUPPORT_STAFF device routing/sign-out, resident/supervisor sessions and forced refresh pass.
- Logbook offline restart/replay, encrypted upload normal restart/explicit discard, and logout
  purge with real queued material pass within the documented test boundaries.
- Mandatory failures: resident Inbox crash; absent supervisor Inbox; leave replay duplicates;
  inconsistent logbook counts. Abrupt-exit upload metadata loss remains a documented recovery failure
  requiring repaired-candidate verification. Full write-action regression is not certified.
- Owner-authorized synthetic records remain unsubmitted drafts: leave 17/18/19; logbook 31.
- Tests cover APK hashes recorded in the canonical report. Later work on
  `feature/android-parity-stages-1-6` and signed release artifacts require separate certification.

This pass adds opt-in device verification tooling and evidence, not application fixes or a deployment.
No FCM enablement, Caddy changes, unrelated workflow changes, or legacy-folder changes were made.
Do not mark GO until every failed or unverified mandatory gate has fresh evidence on the final candidate.

## Feature-candidate closure

`feature/android-parity-stages-1-6` repairs the source failures retained above: all-role Inbox and
exact targets, persisted leave retry IDs with server deduplication, normalized logbook counts, and
synchronous owner-bound upload metadata/orphan cleanup. Migration drift is reconciled and applies
from zero. Automated candidate gates pass; authenticated four-role and release-signing acceptance
remain outstanding, so the verdict remains CONDITIONAL GO.
