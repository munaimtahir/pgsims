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

# Local application models' @Serializable payloads must survive R8.
-keep class pk.vexel.pgrcompanion.**$$serializer { *; }
-keepclassmembers class pk.vexel.pgrcompanion.** {
    *** Companion;
    kotlinx.serialization.KSerializer serializer(...);
}
