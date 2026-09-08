# Android current state

> Historical 1.0.2 companion-track record. The current canonical candidate is now
> `android/app-portal` as `pk.vexel.pgrcompanion` version `1.1.3`/code `3`; see
> `SPRINT_STATE.md` and `android/README.md`. Statements below about a single `:app` module and an
> optional institutional tab describe the retired architecture, not the current release track.

As of 2026-09-06.

## Closed-testing baseline (Milestone A)

The Play-approved closed-testing build is preserved by the tag **`play-closed-testing-baseline-1.0.0`**.
That tag already existed when this pass began and was **not** moved or recreated.

| | |
|---|---|
| Commit | `f37469a0697dd07107e3283da6320eb5f84c1808` — *Correct release symbol handoff* |
| Package ID | `pk.vexel.pgrcompanion` |
| versionName / versionCode | `1.0.0` / `1` |
| compileSdk / targetSdk / minSdk | 36 / 36 / 26 |
| Build variant | `release` (R8 + resource shrinking, `signingConfigs.release`) |
| Release artifact status | Signed AAB + APK produced and verified from this source state; `apksigner` reported v2, one signer, RSA 4096 Vexel Consultants certificate. See `docs/android/pgr-companion-1.0.0/VERIFICATION.md`. |

**Provenance and its limit.** The tagged commit is the last commit that touches the Android module
before this work, and the build metadata in its `app/build.gradle.kts` (`versionCode 1`,
`versionName 1.0.0`, package `pk.vexel.pgrcompanion`) matches the artifact recorded in
`docs/android/pgr-companion-1.0.0/VERIFICATION.md`. That is a *source-state* match, not proof of
byte-identity with the AAB in Play Console — no upload receipt or Play-side artifact hash is held in
this repository, and the AAB itself is not committed. Treat the tag as "the verified source state
that produced a 1.0.0 release artifact", which is what it is, and not as a Play upload receipt.

Nothing in this pass rewrites, reverts or re-points that tag, and no commit before it was amended.

## What shipped before this change

The Play baseline is `pk.vexel.pgrcompanion`, `1.0.0`, `versionCode 1` — a standalone, fully
offline "PGR Companion: Residency". It passed Google Play review and is in closed testing. It has
no account, no network calls and no institutional connection. **That baseline is policy-approved
and is not to be broken or hidden behind a login.**

An earlier, richer multi-module architecture (`android/core/*`, `android/feature/*`) was scrapped
in favour of the current single-module app. Those directories still exist but contain only
`.gitkeep` files — no code, and `settings.gradle.kts` includes `:app` only. There is nothing there
to resurrect.

## What this change adds

`versionName 1.0.2`, `versionCode 2`. The app keeps the offline **Personal Workspace** (profile,
training records, documents, milestones, reminders) exactly as approved, and adds an **optional
Institutional Workspace** on a fifth tab.

The launch path is unchanged: the app opens into the personal profile flow, and the Institution tab
is one of five peers in the bottom bar. No institutional account is required to reach, use or keep
using any part of the approved baseline. This was verified on a device, offline, from the signed
release build — see `ANDROID_RELEASE_VERIFICATION.md`.

## Generic-workspace stabilization in this version

- **Reminders are real.** 1.0.0 declared `POST_NOTIFICATIONS`, created a notification channel, and
  then never requested the permission or delivered anything — a declared permission the app could
  not use. Reminders now take a due date from a date picker, schedule an inexact `RTC_WAKEUP` alarm
  for 09:00 that morning, and deliver through a non-exported `ReminderReceiver`. The runtime
  permission is requested the first time the user adds a reminder, never at launch; refusing it
  disables nothing else. `RECEIVE_BOOT_COMPLETED` was added solely to re-arm pending reminders,
  which the platform drops across a reboot, and the app also re-arms on launch.
- Reminders were previously write-only; they can now be completed and deleted, and both actions
  cancel the pending alarm, as does Delete All App Data.
- The selected tab is `rememberSaveable`, so a rotation or process death no longer silently returns
  the user to Home.
- The document vault stored each file as `doc_<millis>` with the extension stripped, leaving every
  copy unopenable and indistinguishable. It now keeps the real filename and extension, titles the
  record from it, and surfaces a copy failure instead of silently doing nothing.
- Delete buttons name what they delete, for screen readers.
- `android:fullBackupContent` now excludes the institutional session on pre-Android-12 devices too,
  matching the Android 12+ extraction rules.

## Known limitation

The app is deliberately light-only: `CompanionTheme` uses a fixed light scheme and the activity
theme matches it, so it renders identically regardless of system dark mode. Adding a dark palette
would mean revisiting the hardcoded card colours throughout, which is a design change rather than
stabilization, so it is deferred rather than half-done.

## Data boundaries

| | Personal Workspace | Institutional Workspace |
|---|---|---|
| Storage | `LocalStore`, plain `SharedPreferences` + app-private files | Server-side; only JWTs are held locally |
| Token storage | none | `EncryptedSharedPreferences`, excluded from backup and D2D transfer |
| Network | none | HTTPS only, to the institution's PGR SIMS server |
| Requires sign-in | no | yes, and only for this tab |
| Effect of sign-out | none | clears the session only |

The two never cross. `InstitutionalRepository` does not read or write `LocalStore`, and nothing in
the personal flow reads institutional state. An institutional failure renders inside the
Institution tab and cannot stop the other four from rendering.

## Credentials and signing

The repository contains no signing key and no production credential. Release signing is supplied
externally through `-PpgrCompanionSigningPropertiesFile`; see `ANDROID_RELEASE_VERIFICATION.md` for
the fingerprint of the key used and what still needs owner confirmation.

## Store-listing consequence of 1.0.2

1.0.0's in-app copy stated the app has "no account, advertising, analytics, cloud sync, or
institutional connection". With an optional institutional connection present that sentence would be
false, so it was rewritten rather than left to drift. **The Play Data Safety declaration must be
updated before this version is rolled out** — see `PGR_SIMS_ANDROID_API_INTEGRATION.md` for exactly
what is now collected and transmitted.
