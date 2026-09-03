# Verification

Passed: `./gradlew clean :app:bundleRelease :app:assembleRelease -PpgrCompanionSigningPropertiesFile=... --no-daemon`; `./gradlew :app:assembleDebug :app:testDebugUnitTest --no-daemon`; `./gradlew :app:lintDebug --no-daemon`; bundletool `validate`.

The signed release APK was verified with apksigner: package `pk.vexel.pgrcompanion`, version code `1`, version name `1.0.0`, target SDK `36`, v2 signature valid, RSA 4096-bit Vexel Consultants certificate. It declares only `POST_NOTIFICATIONS` plus the normal AndroidX dynamic receiver permission. Bundletool validation passed and a universal APK was derived.

Not completed: emulator journey and three emulator screenshots. The available API 36 AVDs exited before ADB registration; kernel evidence records a `libgfxstream_backend.so` RenderThread segmentation fault. APK installation therefore could not be attempted on a live device. The source creates a notification channel and persists reminder records; it does not yet schedule future alarm delivery.
