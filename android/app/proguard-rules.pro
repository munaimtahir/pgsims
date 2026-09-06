# Kotlinx Serialization
-keepattributes *Annotation*,InnerClasses
-dontnote kotlinx.serialization.SerializationKt
-keepclassmembers class * {
    *** Companion;
}
-keepclasseswithmembers class * {
    kotlinx.serialization.KSerializer serializer(...);
}
-keepclassmembers class * {
    kotlinx.serialization.KSerializer serializer(...);
}
-keep,allowobfuscation,allowshrinking class * {
    <fields>;
}

# Retrofit & OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
-dontwarn retrofit2.**
-keepattributes Signature
-keepattributes Exceptions
-keepclassmembers,allowobfuscation interface * {
    @retrofit2.http.* <methods>;
}

# AndroidX Security / Tink / ErrorProne
-dontwarn com.google.errorprone.annotations.**
-dontwarn com.google.crypto.tink.**
-dontwarn javax.annotation.**
-dontwarn org.checkerframework.**

# Retrofit 2.11 keeps generic signatures of suspend service methods via these:
-keep,allowobfuscation,allowshrinking interface retrofit2.Call
-keep,allowobfuscation,allowshrinking class retrofit2.Response
-keep,allowobfuscation,allowshrinking class kotlin.coroutines.Continuation

# Application models. Both workspaces' @Serializable payloads must survive R8.
-keep class pk.vexel.pgrcompanion.**$$serializer { *; }
-keepclassmembers class pk.vexel.pgrcompanion.** {
    *** Companion;
    kotlinx.serialization.KSerializer serializer(...);
}
