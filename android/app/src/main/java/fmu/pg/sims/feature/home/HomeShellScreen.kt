package fmu.pg.sims.feature.home

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.School
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import fmu.pg.sims.core.ViewModelFactory
import fmu.pg.sims.feature.documents.DocumentsScreen
import fmu.pg.sims.feature.profile.ProfileScreen
import fmu.pg.sims.feature.training.TrainingScreen
import fmu.pg.sims.ui.TestTags

private enum class HomeTab(val label: String) { HOME("Home"), TRAINING("Training"), DOCUMENTS("Documents"), PROFILE("Profile") }

@Composable
fun HomeShellScreen(
    viewModelFactory: ViewModelFactory,
    onLogout: () -> Unit,
) {
    var selectedTab by remember { mutableStateOf(HomeTab.HOME) }

    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = selectedTab == HomeTab.HOME,
                    onClick = { selectedTab = HomeTab.HOME },
                    icon = { Icon(Icons.Default.Home, contentDescription = null) },
                    label = { Text(HomeTab.HOME.label) },
                    modifier = Modifier.testTag(TestTags.HOME_TAB_HOME),
                )
                NavigationBarItem(
                    selected = selectedTab == HomeTab.TRAINING,
                    onClick = { selectedTab = HomeTab.TRAINING },
                    icon = { Icon(Icons.Default.School, contentDescription = null) },
                    label = { Text(HomeTab.TRAINING.label) },
                    modifier = Modifier.testTag(TestTags.HOME_TAB_TRAINING),
                )
                NavigationBarItem(
                    selected = selectedTab == HomeTab.DOCUMENTS,
                    onClick = { selectedTab = HomeTab.DOCUMENTS },
                    icon = { Icon(Icons.Default.Description, contentDescription = null) },
                    label = { Text(HomeTab.DOCUMENTS.label) },
                    modifier = Modifier.testTag(TestTags.HOME_TAB_DOCUMENTS),
                )
                NavigationBarItem(
                    selected = selectedTab == HomeTab.PROFILE,
                    onClick = { selectedTab = HomeTab.PROFILE },
                    icon = { Icon(Icons.Default.Person, contentDescription = null) },
                    label = { Text(HomeTab.PROFILE.label) },
                    modifier = Modifier.testTag(TestTags.HOME_TAB_PROFILE),
                )
            }
        },
    ) { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when (selectedTab) {
                HomeTab.HOME -> HomeScreen(viewModelFactory = viewModelFactory, onGoToDocuments = { selectedTab = HomeTab.DOCUMENTS })
                HomeTab.TRAINING -> TrainingScreen(viewModelFactory = viewModelFactory)
                HomeTab.DOCUMENTS -> DocumentsScreen(viewModelFactory = viewModelFactory)
                HomeTab.PROFILE -> ProfileScreen(viewModelFactory = viewModelFactory, onLogout = onLogout)
            }
        }
    }
}
