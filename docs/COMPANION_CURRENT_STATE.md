# Companion current state

`PGR Companion: Residency` (`pk.vexel.pgrcompanion`, 1.0.2/code 2) is a standalone offline
product: local profile, milestones, rotations, activities, document vault, and reminders. It
requires no account, network connection, FMU affiliation, or Portal installation. The 1.0.0
closed-testing provenance remains tagged `play-closed-testing-baseline-1.0.0`.

## Frozen 1.0.2 candidate audit — 2026-09-06

- Artifact: `builds/companion/PGR-Companion-1.0.2.aab` (2,954,384 bytes)
- SHA-256: `0f2062528459d3f79c9c71ccbb58f30e2b7412d1d3fc13dff2ff8b9d7fb616c0`
- Source commit recorded in the artifact report: `afca40153a1b4a0e0266ab2ee249b2e273e82c98`
- Package/version validated from generated APK: `pk.vexel.pgrcompanion`, code `2`, name `1.0.2`;
  minSdk `26`, target/compile SDK `36`.
- Manifest permissions: `POST_NOTIFICATIONS` and `RECEIVE_BOOT_COMPLETED` only, plus Android's
  generated non-exported dynamic-receiver permission. No `INTERNET`, storage, contacts, location,
  microphone, camera, phone, SMS, or accessibility permission is present.
- The AAB is JAR signed (`SHA384withRSA`) by `CN=Vexel Consultants, OU=Mobile, O=Vexel Consultants,
  L=Islamabad, ST=Islamabad, C=PK`; certificate SHA-1 is
  `45:8F:8D:D8:50:2D:B6:11:2D:BF:E5:F6:53:5B:77:93:DB:3D:6A:D5`, SHA-256 is
  `A8:58:F4:2C:44:60:FE:AB:68:8E:3E:9F:CE:28:B3:E9:E0:D5:AF:03:A5:55:13:3E:5E:13:4F:89:0B:61:F0:10`,
  valid 2026-09-04 through 2054-01-20.

Bundletool 1.18.1 validated the AAB, generated connected-device APK splits, and installed them on
an API 36 emulator. Fresh launch, local profile creation, restart persistence, and offline restart
passed without a Companion crash.

**Signing-key continuity: PASS.** The tagged `play-closed-testing-baseline-1.0.0` source
(`f37469a`, `versionCode=1`, `versionName=1.0.0` — the last artifact accepted by Google Play; no
binary of that upload exists on this machine or in git history, so it was rebuilt from that exact
tag) was signed with the same documented keystore
(`~/.config/pgr-companion/signing/signing.properties`) and its embedded certificate was extracted
independently with both `apksigner verify --print-certs` and `keytool -printcert -jarfile`, on both
APK and AAB. Both tools agree the certificate SHA-256
(`A8:58:F4:2C:44:60:FE:AB:68:8E:3E:9F:CE:28:B3:E9:E0:D5:AF:03:A5:55:13:3E:5E:13:4F:89:0B:61:F0:10`)
is identical to this 1.0.2 candidate's. This is not merely "same keystore file/alias" — the actual
embedded certificate bytes match. What remains **PLAY CONSOLE CONFIRMATION REQUIRED** is only
Google's own record of the registered upload key (no Play Console API access from this
environment); the local signing-key-continuity blocker is closed.
