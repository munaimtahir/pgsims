package fmu.pg.sims.core

import android.content.Context
import android.net.Uri
import android.webkit.MimeTypeMap
import java.io.File
import java.util.UUID

/** Copies a picked content:// Uri into the app cache so it can be uploaded as a plain File. */
fun copyUriToCacheFile(context: Context, uri: Uri): File? {
    val resolver = context.contentResolver
    val mimeType = resolver.getType(uri) ?: "application/octet-stream"
    val extension = MimeTypeMap.getSingleton().getExtensionFromMimeType(mimeType) ?: "bin"
    val target = File(context.cacheDir, "upload_${UUID.randomUUID()}.$extension")
    return try {
        resolver.openInputStream(uri)?.use { input ->
            target.outputStream().use { output -> input.copyTo(output) }
        }
        target
    } catch (e: Exception) {
        null
    }
}

fun mimeTypeFor(context: Context, uri: Uri): String =
    context.contentResolver.getType(uri) ?: "application/octet-stream"
