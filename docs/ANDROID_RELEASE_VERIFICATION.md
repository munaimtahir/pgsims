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
