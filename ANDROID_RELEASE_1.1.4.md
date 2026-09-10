# PGR Companion 1.1.4 — Release Record

## Release identity

- Application: `pk.vexel.pgrcompanion`
- Version: `1.1.4`
- Version code: `4`
- Production API: `https://android.pgsims.alshifalab.pk/`
- Branch: `main`
- Source freeze commit: `4f8e27624c0c01c6dadd82322220ad06b99cdc51`
- Final release-readiness commit: recorded in Git history with tag `v1.1.4`

## Build and signing

- Compile/target SDK: 36
- Minimum SDK: 26
- APK: `android/app-companion/build/outputs/apk/release/app-companion-release.apk`
- AAB: `android/app-companion/build/outputs/bundle/release/app-companion-release.aab`
- APK SHA-256: `1015563f97839846fb4c428958bdf9d3495c3c24b6aeb449b68e1ab01b80ee0d`
- AAB SHA-256: `4f9fcd0b38005e8aecda4c0508d26f6f8abd6b3c1fba2e374cf0dfa95d44d708`
- Certificate SHA-256: `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`

## Verification

- Clean full Gradle `test`: PASS
- Clean full Gradle `lint`: PASS (no errors; existing warnings only)
- Debug APK: PASS
- Signed release APK/AAB: PASS
- Release gate script: PASS with `rg` and fallback without `rg`
- Deliberate forbidden-pattern probe: correctly rejected with exit 1
- API-36 emulator smoke test: PASS
- Production API and correction/resubmission E2E: previously verified PASS
- Crash buffer: no fatal application exception

## Play readiness

Version code 4 is confirmed available by the owner. The AAB is ready for Google Play upload. Play
Console upload and Data Safety/App Access configuration remain external console actions and were not
performed by this release freeze.

## Release notes

What's new in version 1.1.4

- Added a resident home dashboard with current training information.
- Added current rotation, rotation history, and posting details.
- Added supervisor assignment information.
- Added resident logbook drafts, submission, correction feedback, and resubmission.
- Added requirements tracking for assessments, research/synopsis, workshops, and documents.
- Improved institutional residency integration, session handling, stability, and reliability.
