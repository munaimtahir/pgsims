# Android verification

Android scope remains the single `app-companion` module (`pk.vexel.pgrcompanion`). On the laptop,
`:app-companion:testDebugUnitTest`, `:app-companion:lintDebug`, and `:app-companion:assembleDebug`
passed in Gradle 8.7/AGP 8.5.2. Release signing is NOT VERIFIED because owner-controlled signing
properties were not supplied; no Play Console upload or signing-material operation was performed.
