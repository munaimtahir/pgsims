import java.util.Properties
import java.io.File

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "pk.vexel.pgrportal"
    compileSdk = 36
    defaultConfig {
        // As of 2026-09-07 this module produces the published pk.vexel.pgrcompanion listing,
        // superseding the former android/app-companion offline-only build under the same
        // identity. This was an explicit repository-level decision, not a package-rename mistake.
        applicationId = "pk.vexel.pgrcompanion"
        minSdk = 26
        targetSdk = 36
        versionCode = 3
        versionName = "1.1.3"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables { useSupportLibrary = true }
        buildConfigField("String", "INSTITUTIONAL_API_BASE_URL", "\"https://android.pgsims.alshifalab.pk/\"")
        buildConfigField("String", "INSTITUTION_DISPLAY_NAME", "\"Faisalabad Medical University\"")
    }
    signingConfigs {
        create("release") {
            val releaseSigningRequested = gradle.startParameter.taskNames.any { taskName ->
                val requestedTask = taskName.substringAfterLast(':').lowercase()
                val targetsPortal = taskName.contains("app-portal") || !taskName.contains(":app-")
                targetsPortal && requestedTask in setOf("assemblerelease", "bundlerelease", "signingreport")
            }
            val propertiesPath = providers.gradleProperty("pgrCompanionSigningPropertiesFile").orNull
            val signingProperties = propertiesPath?.let { path ->
                file(path).takeIf(File::isFile)?.let { propertiesFile ->
                    Properties().also { properties ->
                        propertiesFile.inputStream().use(properties::load)
                    }
                }
            }
            val requiredKeys = listOf("storeFile", "storePassword", "keyAlias", "keyPassword")
            val missingKeys = requiredKeys.filter { signingProperties?.getProperty(it).isNullOrBlank() }
            if (releaseSigningRequested && missingKeys.isNotEmpty()) {
                error(
                    "Release signing requires -PpgrCompanionSigningPropertiesFile=<owner-readable properties file> " +
                        "with keys: ${requiredKeys.joinToString()}. Missing: ${missingKeys.joinToString()}"
                )
            }
            val keystorePath = signingProperties?.getProperty("storeFile")
            if (keystorePath != null) {
                val keystore = file(keystorePath)
                if (releaseSigningRequested && !keystore.isFile) {
                    error("Release signing keystore does not exist: $keystorePath")
                }
                storeFile = keystore
            }
            signingProperties?.getProperty("storePassword")?.let { storePassword = it }
            signingProperties?.getProperty("keyAlias")?.let { keyAlias = it }
            signingProperties?.getProperty("keyPassword")?.let { keyPassword = it }
        }
    }
    buildTypes {
        debug { applicationIdSuffix = ".debug"; isDebuggable = true }
        create("staging") {
            initWith(getByName("debug"))
            applicationIdSuffix = ".staging"
            // Shared core publishes debug/release variants, not a separate staging variant.
            // Staging is debug-derived, so resolve its shared dependencies from debug.
            matchingFallbacks += listOf("debug")
            // CI and normal staging builds retain the canonical HTTPS URL. A local, isolated
            // emulator stack may override this with -PpgrPortalStagingBaseUrl=http://10.0.2.2:18014/
            // without changing the release build or committing an environment-specific URL.
            val stagingBaseUrl = providers.gradleProperty("pgrPortalStagingBaseUrl")
                .getOrElse("https://staging.pgsims.alshifalab.pk/")
            buildConfigField("String", "INSTITUTIONAL_API_BASE_URL", "\"$stagingBaseUrl\"")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            // Must be signed with the same upload key already registered on Play for
            // pk.vexel.pgrcompanion, or Play will reject this as an upload-key mismatch.
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true; buildConfig = true }
    packaging { resources { excludes += "/META-INF/{AL2.0,LGPL2.1}" } }
}

dependencies {
    implementation(project(":core:common"))
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.compose.bom))
    implementation(libs.compose.ui)
    implementation(libs.compose.ui.graphics)
    implementation(libs.compose.material3)
    implementation(libs.compose.material.icons)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.kotlinx.coroutines.core)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.androidx.security.crypto)
    implementation(libs.retrofit.core)
    implementation(libs.retrofit.kotlinx.serialization)
    implementation(libs.okhttp.core)
    // Tink (via AndroidX encrypted storage) references these at R8 time.
    implementation(libs.errorprone.annotations)
    testImplementation(libs.junit)
    testImplementation(libs.okhttp.mockwebserver)
    testImplementation(libs.kotlinx.coroutines.test)
}
