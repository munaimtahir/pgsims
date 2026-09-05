# Android current state

As of 2026-09-06.

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

`versionName 1.1.0`, `versionCode 2`. The app keeps the offline **Personal Workspace** (profile,
training records, documents, milestones, reminders) exactly as approved, and adds an **optional
Institutional Workspace** on a fifth tab.

The launch path is unchanged: the app opens into the personal profile flow, and the Institution tab
is one of five peers in the bottom bar. No institutional account is required to reach, use or keep
using any part of the approved baseline. This was verified on a device, offline, from the signed
release build — see `ANDROID_RELEASE_VERIFICATION.md`.

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

## Store-listing consequence of 1.1.0

1.0.0's in-app copy stated the app has "no account, advertising, analytics, cloud sync, or
institutional connection". With an optional institutional connection present that sentence would be
false, so it was rewritten rather than left to drift. **The Play Data Safety declaration must be
updated before this version is rolled out** — see `PGR_SIMS_ANDROID_API_INTEGRATION.md` for exactly
what is now collected and transmitted.
