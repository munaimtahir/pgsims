# Android release verification

Baseline: `play-closed-testing-baseline-1.0.0` (`pk.vexel.pgrcompanion`, `1.0.0`, `versionCode 1`).
Candidate: `1.1.0`, `versionCode 2`.

## Commands

```bash
cd android
./gradlew clean :app:testDebugUnitTest :app:lintDebug :app:assembleDebug \
  :app:assembleRelease :app:bundleRelease \
  -PpgrCompanionSigningPropertiesFile=/owner/controlled/path/signing.properties
```

Signing secrets stay outside Git. The build fails loudly rather than silently producing an unsigned
release when the property is absent.

## Signing key — read this before uploading

The build host holds **three** RSA-4096 keystores under `~/.config`, and only one of them belongs to
this package:

| Keystore | Certificate | Use |
|---|---|---|
| `pgr-companion/signing/` | `CN=Vexel Consultants, OU=Mobile, …, L=Islamabad` — SHA-256 `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` | **correct**; matches the 1.0.0 release |
| `vexel-health/` (also the `vexelRelease*` keys in `~/.gradle/gradle.properties`) | `CN=Vexel Health Passport, OU=Release, …, L=Karachi` — SHA-256 `e975397f…` | a different product |
| `fmu-pg-sims/signing/` | — | the abandoned `fmu.pg.sims` identity |

The `vexelRelease*` properties in the user-level `gradle.properties` are the most discoverable of
the three and are the wrong key; signing with them produces an APK Play will reject as an upload-key
mismatch. This was hit and caught during this pass. Always confirm with
`apksigner verify --print-certs` that the digest is `a858f42c…` before uploading.

## Results — 2026-09-06

| Check | Result |
|---|---|
| `:app:testDebugUnitTest` | **46 passed, 0 failed, 0 skipped** across 10 classes |
| `:app:lintDebug` | **0 errors.** Warnings are dependency-version nags, the pre-existing `mipmap-anydpi-v26` folder, and unused baseline resources |
| `:app:lintVitalRelease` | pass |
| `:app:assembleDebug` | pass |
| `:app:assembleRelease` (R8 + resource shrinking) | pass, 1.83 MB APK |
| `:app:bundleRelease` | pass, 3.68 MB AAB |
| `apksigner verify` | Verifies; v2 scheme; 1 signer; certificate SHA-256 `a858f42c…` (correct key) |
| `aapt2 dump badging` | `pk.vexel.pgrcompanion`, `versionCode=2`, `versionName=1.1.0`, `targetSdk=36` |

Declared permissions in the release APK: `POST_NOTIFICATIONS`, `RECEIVE_BOOT_COMPLETED`,
`INTERNET`, plus the AndroidX dynamic-receiver permission. No dangerous storage permission — the
Storage Access Framework is used for both workspaces' file picking.

Release-dex scan for embedded URLs and secrets found exactly one application URL, the production
HTTPS base, and no credential, key or `localhost`/`10.0.2.2` reference.

## Device verification — signed release APK, factory-reset AdForge_API_36

`AdForge_API_36` was wiped (`-wipe-data`) and rebooted before installation, so this is a genuine
first-install run. Everything below is the **minified, signed release build**, so R8 and the keep
rules for Retrofit, OkHttp, kotlinx.serialization and Tink were exercised for real. No other AVD was
started or touched.

| # | Scenario | Result |
|---|---|---|
| 1 | Fresh install on wiped API 36, launch with Wi-Fi and data off | Welcome screen; no login; no crash |
| 2 | Create personal profile offline | Works; reaches Home; five-tab bar; Continue stays disabled until a name is entered |
| 3 | Add a reminder | Android 13+ `POST_NOTIFICATIONS` prompt appears at that moment, not at launch |
| 4 | Choose a due date | Material date picker; copy states the 09:00 delivery and that nothing is sent anywhere |
| 5 | Save the reminder | `dumpsys alarm` shows `RTC_WAKEUP … origWhen=2026-09-12 09:00:00.000`, tag `*walarm*:pk.vexel.pgrcompanion.REMINDER` — exactly the chosen day |
| 6 | Deliver the reminder | Notification posted on channel `reminders`, title "Residency reminder", `AUTO_CANCEL`, correct body |
| 7 | Same broadcast sent from the shell uid (unprivileged) | Nothing delivered — the receiver is genuinely not exported |
| 8 | Force-stop and relaunch | Profile and reminder both restored; exactly one alarm pending, not a duplicate per launch |
| 9 | Institution tab, offline | Sign-in pane renders; Sign in disabled until both fields are filled; password masked |
| 10 | Sign in while offline | "Cannot reach the institution's server. Check your connection and try again." No crash |
| 11 | Sign in with network restored, live production backend | Connected; identity and role correct |
| 12 | Onboarding status card | Review Approved, Profile Complete, Declaration Accepted, Supervisor awaiting confirmation, and that supervisor item listed as the one outstanding requirement — all matching the live API payload |
| 13 | Institutional profile sections | Identity fields editable; Hospital / Department / Training program / Academic session / Specialty rendered read-only as "Recorded — Set by your institution", with **no raw row id shown** |
| 14 | Programme and training | "Active Surface Baseline Programme · y1 · 2026-09-03" from live data |
| 15 | Supervisor | Empty state reports the backend's own `supervisor_status` rather than implying nothing is known |
| 16 | Required documents | Both render as "Under review" (mapped from `PENDING_REVIEW`) with the stored filename and a "Replace" action |
| 17 | Replace an already-submitted document | Confirmation dialog first — no silent overwrite |
| 18 | Document picker | SAF picker opens with the allowed MIME types; cancelling returns cleanly with no upload |
| 19 | Force-stop and relaunch while connected | Session restored from encrypted storage — proves the Tink keep rules survive R8 |
| 20 | Institution sign out | Returns to disconnected; Home, profile, reminder and the pending alarm all intact |
| 21 | `logcat -b crash` across the whole run | **0 entries for this app** |
| 22 | Full 3,475-line log scanned for the submitted password, JWT-shaped strings and `Bearer` headers | **0 matches each** |

## Not verified

- **Live document upload was not executed against the production backend**, and neither was a live
  PATCH that changes a value. The only accounts that exist are seeded demo accounts on the real
  production database, and there is no staging resident; mutating one for no test value was not
  worth it. Instead the write endpoints were probed live with requests the backend rejects before
  it writes anything (see `PGR_SIMS_ANDROID_API_INTEGRATION.md`), which confirms the route,
  authentication, multipart part name, extension allowlist, ownership scoping and the `fields`
  envelope. The document list was re-read afterwards and was unchanged. What remains genuinely
  unproven is only the final success path — a `200` with a stored file. Run it once against a
  staging resident before rollout.
  - One side effect to be aware of: the bare-map PATCH probe writes an `ONBOARDING_DRAFT_SAVED`
    activity-log row with an empty field list. No institutional record changed.
- **The signing certificate was not compared against Play Console.** The correct
  `pk.vexel.pgrcompanion` key was used and its digest is recorded above; confirm it matches the
  registered upload key before uploading.
- Physical hardware, and Android versions other than API 36. Only the `AdForge_API_36` AVD was
  permitted in this environment.

## Policy position

The candidate is policy-safe. The Personal Workspace renders and is fully usable before any
institutional session exists — verified offline at item 1 and again after sign-out at item 20 — and
the one previously dead permission is now genuinely used by a feature the user opts into.

The blocking follow-up is unchanged: the Play Data Safety declaration no longer matches the app's
behaviour and must be updated before rollout. See `PGR_SIMS_ANDROID_API_INTEGRATION.md`.
