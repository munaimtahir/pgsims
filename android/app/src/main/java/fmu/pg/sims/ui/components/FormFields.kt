package fmu.pg.sims.ui.components

import android.app.DatePickerDialog
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.CalendarToday
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import fmu.pg.sims.core.model.OptionItem
import java.util.Calendar

@Composable
fun LabeledTextField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    required: Boolean = false,
    enabled: Boolean = true,
    modifier: Modifier = Modifier,
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(if (required) "$label *" else label) },
        enabled = enabled,
        singleLine = true,
        modifier = modifier.fillMaxWidth(),
    )
}

@Composable
fun DropdownField(
    label: String,
    options: List<OptionItem>,
    selectedId: String,
    onSelect: (OptionItem) -> Unit,
    required: Boolean = false,
    modifier: Modifier = Modifier,
) {
    var expanded by remember { mutableStateOf(false) }
    val selectedLabel = options.firstOrNull { it.id == selectedId }?.name ?: ""

    Box(modifier = modifier.fillMaxWidth()) {
        OutlinedTextField(
            value = selectedLabel,
            onValueChange = {},
            readOnly = true,
            label = { Text(if (required) "$label *" else label) },
            trailingIcon = {
                IconButton(onClick = { expanded = true }) {
                    Icon(Icons.Default.ArrowDropDown, contentDescription = "Select $label")
                }
            },
            modifier = Modifier.fillMaxWidth(),
        )
        Box(
            modifier = Modifier
                .matchParentSize()
                .clickable { expanded = true }
        )
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            if (options.isEmpty()) {
                DropdownMenuItem(text = { Text("No options available") }, onClick = {}, enabled = false)
            }
            options.forEach { option ->
                DropdownMenuItem(
                    text = { Text(option.name) },
                    onClick = {
                        onSelect(option)
                        expanded = false
                    },
                )
            }
        }
    }
}

@Composable
fun DateField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    required: Boolean = false,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val calendar = remember { Calendar.getInstance() }
    val openPicker = {
        if (value.length == 10) {
            runCatching {
                val (y, m, d) = value.split("-").map { it.toInt() }
                calendar.set(y, m - 1, d)
            }
        }
        DatePickerDialog(
            context,
            { _, year, month, dayOfMonth ->
                onValueChange("%04d-%02d-%02d".format(year, month + 1, dayOfMonth))
            },
            calendar.get(Calendar.YEAR),
            calendar.get(Calendar.MONTH),
            calendar.get(Calendar.DAY_OF_MONTH),
        ).show()
    }

    Box(modifier = modifier.fillMaxWidth()) {
        OutlinedTextField(
            value = value,
            onValueChange = {},
            readOnly = true,
            label = { Text(if (required) "$label *" else label) },
            placeholder = { Text("YYYY-MM-DD") },
            trailingIcon = {
                IconButton(onClick = openPicker) {
                    Icon(Icons.Default.CalendarToday, contentDescription = "Pick date")
                }
            },
            modifier = Modifier.fillMaxWidth(),
        )
        Box(
            modifier = Modifier
                .matchParentSize()
                .clickable(onClick = openPicker)
        )
    }
}

