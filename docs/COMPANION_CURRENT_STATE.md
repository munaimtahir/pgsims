# Companion current state

`PGR Companion: Residency` (`pk.vexel.pgrcompanion`, 1.1.0/code 2) is a standalone offline
product: local profile, milestones, rotations, activities, document vault, and reminders. It
requires no account, network connection, FMU affiliation, or Portal installation. The 1.0.0
closed-testing provenance remains tagged `play-closed-testing-baseline-1.0.0`.

## Frozen 1.1.0 candidate audit — 2026-09-06

- Artifact: `builds/companion/PGR-Companion-1.1.0.aab` (2,954,048 bytes)
- SHA-256: `f48ae84b95f0553f6ed983fab0f5036044a07ac99e2b5f64230e2e0421e23e9e`
- Source commit recorded in the artifact report: `87a0bd4e50f9364a02273e82df6d7199f5b43da4`
- Package/version validated from generated APK: `pk.vexel.pgrcompanion`, code `2`, name `1.1.0`;
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
passed without a Companion crash. The upload-key comparison remains **LOCAL VERIFIED — PLAY CONSOLE
CONFIRMATION REQUIRED**, because this workspace has no Play Console access.
