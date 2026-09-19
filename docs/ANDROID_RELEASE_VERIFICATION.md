# Android release verification

The current canonical candidate is `pk.vexel.pgrcompanion` version `1.1.9` / code `9`. Older
1.1.7 and earlier entries in this file are historical evidence. Current gap-closure status and
the complete pending Android backlog are tracked in `SPRINT_STATE.md` and
`docs/implementation/20260920_android_gap_closure/PENDING_WORK_REGISTER.md`.

Run from `android/` for a later release gate:

```bash
./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleRelease :app-companion:bundleRelease
```

Or run `scripts/build_android_tracks.sh` from the repository root to generate untracked artifacts
under `builds/companion/`. Release signing remains owner-controlled:
pass `-PpgrCompanionSigningPropertiesFile=…` if signing is required. PGR Companion uses development
signing until its institutional release owner supplies a production key; never create a replacement
production key.

Manual device checks: install the PGR Companion APK, sign in and out, verify session restoration,
and confirm the application remains functional.

## 2026-09-06 evidence

Companion AAB validation and connected-device installation passed via bundletool 1.18.1 on the
available API 36 emulator (`emulator-5554`). The derived APK launched, persisted a local profile
across force-stop/restart, and rendered correctly with Wi-Fi and cellular data disabled. The Portal
APK installed and launched to its PGR Companion login screen. PGR Companion live
login and uninstall-isolation remain blocked by the absent staging environment; no production
resident credentials were used.

## 2026-09-07 PGR Companion staging closure

Public isolated staging is now available at `https://staging.pgsims.alshifalab.pk/` and passed its
health check. PGR Companion staging `1.1.7` / code `7` passed debug unit tests, debug lint, release APK/AAB,
and staging APK assembly. Targeted backend authentication/onboarding/security tests passed 38
tests. The frozen Companion AAB was not replaced.
