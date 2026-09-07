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
        applicationId = "pk.vexel.pgrportal.dev"
        minSdk = 26
        targetSdk = 36
        versionCode = 3
        versionName = "0.1.2-dev"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables { useSupportLibrary = true }
        buildConfigField("String", "INSTITUTIONAL_API_BASE_URL", "\"https://android.pgsims.alshifalab.pk/\"")
        buildConfigField("String", "INSTITUTION_DISPLAY_NAME", "\"Faisalabad Medical University\"")
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
            // Portal is a development track: use the standard debug key until an institutional
            // release owner supplies a dedicated key. This makes the test APK installable but is
            // deliberately not a production-signing arrangement.
            signingConfig = signingConfigs.getByName("debug")
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
