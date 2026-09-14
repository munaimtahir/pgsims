package pk.vexel.pgrcompanion

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonObject

@Composable
internal fun OwnProfileEditor(repository: InstitutionalRepository, onSaved: () -> Unit = {}) {
    val scope = rememberCoroutineScope()
    var profile by remember { mutableStateOf<JsonObject?>(null) }
    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(true) }
    var message by remember { mutableStateOf<String?>(null) }
    LaunchedEffect(Unit) {
        repository.ownProfile().fold(
            { value -> profile = value; firstName = value.string("first_name").orEmpty(); lastName = value.string("last_name").orEmpty(); email = value.string("email").orEmpty(); phone = value.string("phone_number").orEmpty() },
            { message = it.message },
        )
        busy = false
    }
    Text("My profile", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
    profile?.let { Text("${it.string("username").orEmpty()} · ${InstitutionalLabels.humanize(it.string("role").orEmpty())}") }
    if (busy) LinearProgressIndicator(Modifier.fillMaxWidth())
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        OutlinedTextField(firstName, { firstName = it }, Modifier.fillMaxWidth(), label = { Text("First name") }, enabled = !busy)
        OutlinedTextField(lastName, { lastName = it }, Modifier.fillMaxWidth(), label = { Text("Last name") }, enabled = !busy)
        OutlinedTextField(email, { email = it }, Modifier.fillMaxWidth(), label = { Text("Email") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email), enabled = !busy)
        OutlinedTextField(phone, { phone = it }, Modifier.fillMaxWidth(), label = { Text("Phone") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone), enabled = !busy)
        message?.let { Text(it, color = if (it == "Profile saved.") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error) }
        Button(onClick = {
            busy = true; message = null
            scope.launch {
                repository.updateOwnProfile(mapOf("first_name" to firstName, "last_name" to lastName, "email" to email, "phone_number" to phone)).fold(
                    { profile = it; message = "Profile saved."; onSaved() },
                    { message = it.message ?: "Could not save your profile." },
                )
                busy = false
            }
        }, enabled = !busy && firstName.isNotBlank(), modifier = Modifier.fillMaxWidth()) { Text(if (busy) "Saving…" else "Save profile") }
    }
}
