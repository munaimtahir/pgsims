# Android release verification

Run from `android/`:

```bash
./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleRelease :app-companion:bundleRelease
./gradlew :app-portal:testDebugUnitTest :app-portal:lintDebug :app-portal:assembleRelease :app-portal:bundleRelease
```

Or run `scripts/build_android_tracks.sh` from the repository root to generate untracked artifacts
under `builds/companion/` and `builds/portal/`. Companion release signing remains owner-controlled:
pass `-PpgrCompanionSigningPropertiesFile=…` if signing is required. Portal uses development
signing until its institutional release owner supplies a production key; never create a replacement
production key.

Manual device checks: install both APKs at once, create and restart a Companion profile, sign in
and out of Portal, then remove Portal and relaunch Companion. Confirm Companion records remain.

## 2026-09-06 evidence

Companion AAB validation and connected-device installation passed via bundletool 1.18.1 on the
available API 36 emulator (`emulator-5554`). The derived APK launched, persisted a local profile
across force-stop/restart, and rendered correctly with Wi-Fi and cellular data disabled. The Portal
APK installed alongside it under its distinct package and launched to its login screen. Portal live
login and uninstall-isolation remain blocked by the absent staging environment; no production
resident credentials were used.

## 2026-09-07 Portal staging closure

Public isolated staging is now available at `https://staging.pgsims.alshifalab.pk/` and passed its
health check. Portal `0.1.2-dev` / code `3` passed debug unit tests, debug lint, release APK/AAB,
and staging APK assembly. Targeted backend authentication/onboarding/security tests passed 38
tests. The frozen Companion AAB was not replaced.
