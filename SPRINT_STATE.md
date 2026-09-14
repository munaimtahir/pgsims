# SPRINT_STATE.md — Android Sprints 1–5 release verification

## Scope

Verify the `13f1bb7` baseline without production infrastructure changes. Final result: CONDITIONAL GO.
Canonical evidence: `docs/implementation/20260914_android_sprints_2_3_4/TEST_RESULTS.md`.

## Completed Work

- Reconciled inherited four-role API-login and ADMIN restricted-device evidence without repeating standalone API logins.
- Isolated current VPS image: SQLite suite 922 tests, 0 failures/errors, 3 repository-file skips, 59.308s; container removed and health/FCM-disabled state verified.
- SUPPORT_STAFF restricted routing/sign-out; RESIDENT/SUPERVISOR login, restore, forced refresh, logout; baseline Android build, 30 unit tests and lint pass.
- Offline drafts survive restart; logbook deduplicates to ID 31. Normal encrypted upload restart/explicit discard and populated-queue logout purge pass.
- Captured mandatory failures with reproducible device/server evidence; no production code/config deployment, no unrelated workflow changes.

## Pending Work

1. Fix `InstitutionalScreen.kt` / `NotificationCenter.kt` nested scrolling and add Supervisor Inbox; rerun both role Inbox/read-unread/target checks on a frozen artifact.
2. Fix `LeaveRequestSerializer` / `LeaveRequestViewSet` key persistence; test new labeled keys for exactly one server record. Existing test leave IDs 17/18/19 are unsubmitted duplicate drafts; logbook ID 31 is the single synthetic draft.
3. Normalize logbook state counts in `ResidentWorkflowScreens.kt`; verify Approved count agrees with list/detail/Progress.
4. Reproduce and fix immediate-process-death upload metadata loss; assert retained upload count and orphan handling. Normal restart/explicit discard/logout purge already pass.
5. Complete unverified write-action regression and document-upload integration using dedicated fixtures; retain the three repository-dependent SQLite skips explicitly.
6. Freeze and separately verify any later `feature/android-parity-stages-1-6` changes and signed candidate; this report certifies only its recorded debug APK hashes. No GO or deployment until required gates pass.

## Environment

Laptop physical checkout `/media/munaim/shared1/Documents/github/pgsims`; VPS `ssh test`, repo
`/home/munaim/srv/apps/pgsims`. A concurrent session owns the feature branch/worktree; evidence is
committed on main separately without merging its edits. Credentials and tokens are not in evidence.
FCM remains false; Caddy, production volumes, unrelated services and legacy folders are unchanged.
