# Independent Android Foundation Release Verification

Verification date: 2026-09-03

## Verdict

**GO for local signed-release handoff.** Play Console configuration, privacy
forms, testers, store listing, and review access remain user-managed and were
not performed.

## Release evidence

- App name: FMU Postgraduate Residency Portal
- Application ID / namespace: `fmu.pg.sims`
- Version: `versionCode 1`, `versionName 0.1.0`
- SDKs: min 26, target 36, compile 36
- Toolchain: Gradle 8.7, AGP 8.5.2, Kotlin 2.0.0, JDK 21.0.12
- Release build: Android `test`, `lint`, `assembleRelease`, and `bundleRelease`
  succeeded after the final shell-label correction.
- Release is non-debuggable, uses HTTPS-only release network security, and
  has only INTERNET and ACCESS_NETWORK_STATE plus the generated AndroidX
  non-exported receiver permission.
- Root `logo.png` is packaged as `fmu_logo.png` and is used for the app and
  round launcher icons and the foundation shell.
- R8 is enabled; the genuine release mapping file is retained.
- No native `.so` libraries are present; native symbols and 16 KB native
  compatibility are not applicable.
- AAB signature verification succeeded with the dedicated external upload key.
- Bundletool 1.18.3 validation succeeded; a universal APK was generated from
  the final AAB, signed for local installation, and installed on the API 36
  emulator `emulator-5554`.
- The app launched as `fmu.pg.sims/.ui.MainActivity`; three final screenshots
  were captured on the emulator and saved at the repository root.

## Blocking verification gaps

- The release-preparation changes remain uncommitted by design; the external
  release manifest records the artifact checksums and verification state.
- The Android Gradle Plugin emits a compatibility warning because AGP 8.5.2
  predates compile SDK 36; the build and lint gates still pass.

## Signing

The private upload keystore is outside Git at
`/home/munaim/.config/fmu-pg-sims/signing/fmu-pg-sims-upload.jks`. Its alias is
`fmu-pg-sims-upload`; passwords are intentionally not documented. The public
certificate SHA-256 is
`35:16:7F:22:5F:FF:61:55:54:80:07:07:EA:F1:54:F1:E6:55:B4:8F:0A:FE:0E:0A:68:48:E4:CC:EB:DD:44:B9`.

The previous committed `android/app/release.keystore` was removed from the
repository and preserved outside Git under the signing directory's `legacy`
folder.
