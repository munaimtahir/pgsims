package pk.vexel.pgrcompanion

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

internal data class PasswordResetLink(val uid: String, val token: String) {
    companion object {
        fun fromSegments(segments: List<String>): PasswordResetLink? {
            val index = segments.indexOf("reset-password")
            if (index < 0 || segments.size <= index + 2) return null
            return PasswordResetLink(segments[index + 1], segments[index + 2])
        }
    }
}

internal enum class AuthoritativeRoute { CHANGE_PASSWORD, COMPLETE_PROFILE, WORKSPACE }

internal fun authoritativeRoute(me: JsonObject): AuthoritativeRoute = when {
    me.boolean("must_change_password") -> AuthoritativeRoute.CHANGE_PASSWORD
    me.string("allowed_next_route") == "/complete-profile" || me.strings("missing_required_fields").isNotEmpty() ->
        AuthoritativeRoute.COMPLETE_PROFILE
    else -> AuthoritativeRoute.WORKSPACE
}

@Composable
internal fun ChangePasswordScreen(
    repository: InstitutionalRepository,
    forced: Boolean,
    onComplete: () -> Unit,
    onCancel: (() -> Unit)?,
) {
    val scope = rememberCoroutineScope()
    var oldPassword by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var confirmation by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text(if (forced) "Change password to continue" else "Change password", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        if (forced) Text("PGR SIMS requires a new password before the rest of the app can be opened.")
        PasswordField("Current password", oldPassword, !busy) { oldPassword = it }
        PasswordField("New password", newPassword, !busy) { newPassword = it }
        PasswordField("Confirm new password", confirmation, !busy) { confirmation = it }
        if (newPassword.isNotBlank() && confirmation.isNotBlank() && newPassword != confirmation) {
            Text("The new passwords do not match.", color = MaterialTheme.colorScheme.error)
        }
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        if (busy) LinearProgressIndicator(Modifier.fillMaxWidth())
        Button(
            onClick = {
                busy = true; error = null
                scope.launch {
                    repository.changePassword(oldPassword, newPassword, confirmation).fold(
                        { onComplete() },
                        { error = it.message ?: "Could not change your password."; busy = false },
                    )
                }
            },
            enabled = !busy && oldPassword.isNotBlank() && newPassword.isNotBlank() && newPassword == confirmation,
            modifier = Modifier.fillMaxWidth(),
        ) { Text(if (busy) "Changing…" else "Change password") }
        onCancel?.let { OutlinedButton(onClick = it, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Cancel") } }
    }
}

@Composable
private fun PasswordField(label: String, value: String, enabled: Boolean, onChange: (String) -> Unit) {
    OutlinedTextField(
        value = value,
        onValueChange = onChange,
        label = { Text(label) },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
        singleLine = true,
        enabled = enabled,
        modifier = Modifier.fillMaxWidth(),
    )
}

@Composable
internal fun PasswordResetRequestScreen(repository: InstitutionalRepository, onBack: () -> Unit) {
    val scope = rememberCoroutineScope()
    var email by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf<String?>(null) }
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("Reset password", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text("Enter the email address on your PGR SIMS account. For privacy, the result is the same whether or not an account exists.")
        OutlinedTextField(email, { email = it }, Modifier.fillMaxWidth(), label = { Text("Email") }, singleLine = true,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email), enabled = !busy)
        message?.let { Text(it, color = MaterialTheme.colorScheme.primary) }
        Button(onClick = {
            busy = true; message = null
            scope.launch {
                repository.requestPasswordReset(email).fold(
                    { message = "If an account with that email exists, reset instructions have been sent." },
                    { message = it.message ?: "Could not request a password reset." },
                )
                busy = false
            }
        }, enabled = !busy && email.isNotBlank(), modifier = Modifier.fillMaxWidth()) { Text(if (busy) "Sending…" else "Send reset link") }
        OutlinedButton(onClick = onBack, enabled = !busy, modifier = Modifier.fillMaxWidth()) { Text("Back to sign in") }
    }
}

@Composable
internal fun PasswordResetConfirmScreen(repository: InstitutionalRepository, link: PasswordResetLink, onComplete: () -> Unit) {
    val scope = rememberCoroutineScope()
    var password by remember { mutableStateOf("") }
    var confirmation by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("Choose a new password", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        PasswordField("New password", password, !busy) { password = it }
        PasswordField("Confirm new password", confirmation, !busy) { confirmation = it }
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        Button(onClick = {
            busy = true; error = null
            scope.launch {
                repository.confirmPasswordReset(link.uid, link.token, password, confirmation).fold(
                    { onComplete() },
                    { error = it.message ?: "This reset link is invalid or has expired."; busy = false },
                )
            }
        }, enabled = !busy && password.isNotBlank() && password == confirmation, modifier = Modifier.fillMaxWidth()) {
            Text(if (busy) "Saving…" else "Set new password")
        }
    }
}

private fun JsonObject.formFields(): List<JsonObject> =
    runCatching { getValue("missing_fields").jsonArray.map { it.jsonObject } }.getOrDefault(emptyList())

private fun JsonObject.optionRows(key: String): List<JsonObject> =
    runCatching { getValue(key).jsonArray.map { it.jsonObject } }.getOrDefault(emptyList())

@Composable
internal fun DynamicProfileCompletionScreen(
    repository: InstitutionalRepository,
    role: String,
    onAuthoritativeRefresh: () -> Unit,
    onSignOut: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var form by remember { mutableStateOf<JsonObject?>(null) }
    var options by remember { mutableStateOf<JsonObject?>(null) }
    var loading by remember { mutableStateOf(true) }
    var saving by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    val values = remember { mutableStateMapOf<String, String>() }

    fun load() = scope.launch {
        loading = true; error = null
        repository.completeProfileForm().fold(
            { result ->
                form = result
                repository.identityOptions().fold({ options = it }, { error = it.message })
            },
            { error = it.message ?: "Could not load profile requirements." },
        )
        loading = false
    }
    LaunchedEffect(Unit) { load() }

    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("Complete your profile", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
        Text("PGR SIMS defines these required fields for ${InstitutionalLabels.humanize(role)} accounts. Newly required fields will appear here automatically.")
        if (loading) LinearProgressIndicator(Modifier.fillMaxWidth())
        val fields = form?.formFields().orEmpty()
        fields.forEach { field ->
            DynamicRequiredField(field, values[field.string("field").orEmpty()].orEmpty(), options, !saving) { key, value -> values[key] = value }
        }
        if (!loading && fields.isEmpty() && role == "RESIDENT") {
            Card(Modifier.fillMaxWidth()) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Resident declaration", fontWeight = FontWeight.SemiBold)
                    Text("I confirm that the information provided is correct and the documents are authentic. Deferred documents remain pending.")
                    Button(onClick = {
                        saving = true
                        scope.launch { repository.acceptDeclaration().fold({ onAuthoritativeRefresh() }, { error = it.message; saving = false }) }
                    }, enabled = !saving) { Text("Accept declaration") }
                }
            }
        }
        error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
        if (fields.isNotEmpty()) Button(onClick = {
            saving = true; error = null
            scope.launch {
                repository.completeProfile(fields.associate { it.string("field").orEmpty() to values[it.string("field").orEmpty()].orEmpty() }).fold(
                    { onAuthoritativeRefresh() },
                    { error = it.message ?: "Could not save your profile."; saving = false },
                )
            }
        }, enabled = !saving && fields.all { !it.boolean("required") || !values[it.string("field").orEmpty()].isNullOrBlank() }, modifier = Modifier.fillMaxWidth()) {
            Text(if (saving) "Saving…" else "Save and continue")
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedButton(onClick = { load() }, enabled = !loading && !saving) { Text("Reload") }
            OutlinedButton(onClick = onSignOut, enabled = !saving) { Text("Sign out") }
        }
    }
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
private fun DynamicRequiredField(
    field: JsonObject,
    value: String,
    options: JsonObject?,
    enabled: Boolean,
    onChange: (String, String) -> Unit,
) {
    val key = field.string("field").orEmpty()
    val label = field.string("label").orEmpty().ifBlank { InstitutionalLabels.humanize(key) }
    val inputType = field.string("input_type").orEmpty().ifBlank { "text" }
    val required = field.boolean("required")
    val optionsKey = field.string("options_key")
    val rows = optionsKey?.let { options?.optionRows(it) }.orEmpty()
    if (inputType == "select" || rows.isNotEmpty()) {
        var expanded by remember { mutableStateOf(false) }
        val selected = rows.firstOrNull { it.string("id") == value || it.string("code") == value }
        ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { if (enabled) expanded = !expanded }) {
            OutlinedTextField(
                value = selected?.string("name") ?: "",
                onValueChange = {},
                readOnly = true,
                enabled = enabled,
                label = { Text(if (required) "$label *" else label) },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded) },
                modifier = Modifier.menuAnchor().fillMaxWidth(),
            )
            ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                rows.forEach { option ->
                    val optionValue = option.string("id") ?: option.string("code").orEmpty()
                    androidx.compose.material3.DropdownMenuItem(
                        text = { Text(option.string("name").orEmpty()) },
                        onClick = { onChange(key, optionValue); expanded = false },
                    )
                }
            }
        }
    } else {
        val keyboard = when (inputType) {
            "email" -> KeyboardType.Email
            "phone" -> KeyboardType.Phone
            "number" -> KeyboardType.Number
            else -> KeyboardType.Text
        }
        OutlinedTextField(
            value = value,
            onValueChange = { onChange(key, it) },
            modifier = Modifier.fillMaxWidth(),
            label = { Text(if (required) "$label *" else label) },
            supportingText = field.string("help_text")?.takeIf { it.isNotBlank() }?.let { help -> ({ Text(help) }) },
            keyboardOptions = KeyboardOptions(keyboardType = keyboard),
            singleLine = inputType != "text",
            enabled = enabled,
        )
    }
}
