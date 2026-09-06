# Android release verification

Baseline: `play-closed-testing-baseline-1.0.0` (`pk.vexel.pgrcompanion`, `1.0.0`, `versionCode 1`).
Candidate: `1.1.0`, `versionCode 2`.

## Commands

```bash
cd android
./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
./gradlew :app:assembleRelease :app:bundleRelease \
  -PpgrCompanionSigningPropertiesFile=/owner/controlled/path/signing.properties
```

Signing secrets stay outside Git. The build fails loudly rather than silently producing an unsigned
release when the property is absent.

## Results — 2026-09-06

| Check | Result |
|---|---|
| `:app:testDebugUnitTest` | **22 passed, 0 failed** (2 pre-existing + 20 new) |
| `:app:lintDebug` | pass, no errors |
| `:app:lintVitalRelease` | pass |
| `:app:assembleRelease` (R8 + resource shrinking) | pass, 1.60 MB APK |
| `:app:bundleRelease` | pass, 3.38 MB AAB |
| `apksigner verify` | Verifies; v2 scheme; 1 signer |

Signer DN `CN=Vexel Consultants, OU=Mobile, O=Vexel Consultants, L=Islamabad, ST=Islamabad, C=PK`,
RSA 4096, certificate SHA-256
`a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`.

APK manifest: `versionCode=2`, `versionName=1.1.0`, `targetSdk=36`, permissions
`POST_NOTIFICATIONS` and `INTERNET` only.

## Device verification — signed release APK, AdForge_API_36 emulator

Run against the **minified, signed release build**, not a debug build, so R8 and the ProGuard keep
rules for Retrofit, OkHttp, kotlinx.serialization and Tink were exercised for real.

| # | Scenario | Result |
|---|---|---|
| 1 | Cold launch with Wi-Fi and data **off** | Personal Workspace renders; no crash; no network required |
| 2 | Create personal profile offline | Works; reaches Home; five-tab bar with a distinct Institution icon |
| 3 | Institution tab, offline | Sign-in pane renders; Sign in disabled until both fields are filled |
| 4 | Password entry | Masked |
| 5 | Sign in while offline | "Cannot reach the institution's server. Check your connection and try again." No crash |
| 6 | Sign in with network restored, live production backend | Connected; identity, role and review status correct |
| 7 | Backend-declared onboarding sections | Rendered dynamically with correct labels, values and required markers |
| 8 | Training / supervisor / documents | All render from live data, including the empty supervisor state |
| 9 | Force-stop and relaunch | Session restored from encrypted storage — proves the Tink keep rules survive R8 |
| 10 | Sign out | Returns to disconnected; Home still shows the personal profile intact |
| 11 | `logcat -b crash` across the whole run | **0 entries** |
| 12 | `logcat` grep for JWTs, bearer headers, submitted password | **0 matches** |

## Not verified

- **Live document upload was not executed against the production backend.** The demo resident's
  profile is in an `APPROVED` review state on the real production database, and pushing a file
  would mutate live institutional records for no test value. The path is covered by unit tests
  (multipart part name, endpoint, client-side validation) and the contract was read from
  `onboarding_api.py`. Run it once against a staging resident before rollout.
- **Live PATCH of onboarding fields** was likewise not executed against production, for the same
  reason. The envelope shape is asserted by test and confirmed by source.
- **The signing certificate was not compared against Play Console.** The key at the owner-controlled
  path for this package was used and its fingerprint is recorded above; confirm it matches the
  registered upload key before uploading. Note a second, unrelated keystore exists on the build host
  for the abandoned `fmu.pg.sims` identity — it is not the one used here.
- Physical hardware, and Android versions other than API 36.

## Policy position

The candidate is policy-safe: the Personal Workspace renders, and is fully usable, before any
institutional session exists — verified offline at item 1 and again after sign-out at item 10.
The one blocking follow-up is the Data Safety declaration, which no longer matches the app's
behaviour; see `PGR_SIMS_ANDROID_API_INTEGRATION.md`.
