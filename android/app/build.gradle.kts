import java.util.Properties
import java.io.File

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "pk.vexel.pgrcompanion"
    compileSdk = 36

    defaultConfig {
        applicationId = "pk.vexel.pgrcompanion"
        minSdk = 26
        targetSdk = 36
        versionCode = 2
        versionName = "1.1.0"

        // Institutional Workspace endpoint. HTTPS only — see the cleartext ban below.
        buildConfigField(
            "String",
            "INSTITUTIONAL_API_BASE_URL",
            "\"https://android.pgsims.alshifalab.pk/\"",
        )

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }

    }

    signingConfigs {
        create("release") {
            val releaseSigningRequested = gradle.startParameter.taskNames.any { taskName ->
                taskName.substringAfterLast(':').lowercase() in setOf(
                    "assemblerelease", "bundlerelease", "signingreport"
                )
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
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("release")
        }
        debug {
            applicationIdSuffix = ".debug"
            isDebuggable = true
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.navigation.compose)

    implementation(platform(libs.compose.bom))
    implementation(libs.compose.ui)
    implementation(libs.compose.ui.graphics)
    implementation(libs.compose.ui.tooling.preview)
    implementation(libs.compose.material3)
    implementation(libs.compose.material.icons)

    implementation(libs.kotlinx.serialization.json)
    implementation(libs.kotlinx.coroutines.core)
    implementation(libs.kotlinx.coroutines.android)

    // Institutional Workspace only. The Personal Workspace uses none of these.
    implementation(libs.androidx.security.crypto)
    implementation(libs.retrofit.core)
    implementation(libs.retrofit.kotlinx.serialization)
    implementation(libs.okhttp.core)

    testImplementation(libs.junit)
    testImplementation(libs.okhttp.mockwebserver)
    testImplementation(libs.kotlinx.coroutines.test)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.compose.bom))
    androidTestImplementation(libs.compose.ui.test.junit4)

    debugImplementation(libs.compose.ui.tooling)
    debugImplementation(libs.compose.ui.test.manifest)
}
