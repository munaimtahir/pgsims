# Verification

Passed: `./gradlew clean :app:bundleRelease :app:assembleRelease -PpgrCompanionSigningPropertiesFile=... --no-daemon`; `./gradlew :app:assembleDebug :app:testDebugUnitTest --no-daemon`; `./gradlew :app:lintDebug --no-daemon`; bundletool `validate`.

The signed release APK was verified with apksigner: package `pk.vexel.pgrcompanion`, version code `1`, version name `1.0.0`, target SDK `36`, v2 signature valid, RSA 4096-bit Vexel Consultants certificate. It declares only `POST_NOTIFICATIONS` plus the normal AndroidX dynamic receiver permission. Bundletool validation passed and a universal APK was derived.

ADB/device acceptance completed on wiped `AdForge_API_36` (`emulator-5554`, API 36): signed release APK installed, launched without login, profile created, app force-stopped/relaunched with profile retained, and Delete All App Data returned the app to the welcome screen. Three screenshots are in `store_listing_screenshots/pgr-companion-1.0.0/`: welcome, home, and document vault. The source creates a notification channel and persists reminder records; it does not yet schedule future alarm delivery.
