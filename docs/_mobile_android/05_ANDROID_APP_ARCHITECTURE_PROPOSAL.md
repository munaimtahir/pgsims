# Android App Architecture Proposal

To ensure scalability, testability, and a modern user experience, the following architecture is proposed for the PGSIMS Android companion app.

## 1. Tech Stack
- **Language**: Kotlin (100%).
- **UI Framework**: Jetpack Compose (Declarative UI).
- **Navigation**: Jetpack Compose Navigation.
- **Asynchronous Work**: Kotlin Coroutines + Flow.
- **Dependency Injection**: Hilt (Standard for modern Android).

## 2. Architectural Pattern: MVVM (Model-View-ViewModel)
- **View**: Composable functions that observe state from the ViewModel.
- **ViewModel**: Manages UI state, handles user actions, and communicates with the Repository.
- **Repository**: Single source of truth for data. Orchestrates between Network (Retrofit) and Local Database (Room).
- **Model**: Data classes representing the API entities (LogbookEntry, User, etc.).

## 3. Networking & Data
- **Retrofit 2**: For consuming the Django REST API.
- **OkHttp 4**: With an `AuthInterceptor` to automatically attach JWT Bearer tokens and handle 401 token refreshing.
- **Room Persistence**: To cache logbook drafts and dashboard data for offline access.
- **Moshi**: For JSON serialization/deserialization.

## 4. Key Modules
- **`:core:data`**: Repositories, API interfaces, DTOs, and Database.
- **`:core:ui`**: Shared theme (FMU branding), components, and styling.
- **`:feature:auth`**: Login, Profile, and Password Reset screens.
- **`:feature:resident`**: Logbook creation, history, and dashboard.
- **`:feature:supervisor`**: Review queue and approval workflows.
- **`:feature:notifications`**: List and badge management.

## 5. Offline-First Strategy
- Residents often work in areas with poor connectivity.
- **Drafts**: All logbook entries should be saved locally first.
- **Sync**: A `WorkManager` job can attempt to sync "Pending Upload" entries when a stable connection is detected.

## 6. Testing Strategy
- **Unit Tests**: For ViewModels, Repositories, and UseCases (using MockK).
- **Integration Tests**: Using Hilt and MockWebServer to test the API layer.
- **UI Tests**: Using Compose Test Library to verify critical paths (Login, Submit Logbook).
