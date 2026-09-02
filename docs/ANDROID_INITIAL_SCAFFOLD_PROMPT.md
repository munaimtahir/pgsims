# PGR SIMS ANDROID — INITIAL REPOSITORY SCAFFOLD SPRINT

You are working from the root of the existing PGR SIMS repository.

Your task in this sprint is ONLY to establish the initial Android project directory architecture and repository scaffolding required for the future PGR SIMS Android application.

DO NOT start implementing Android features.
DO NOT change existing backend business logic.
DO NOT change existing web frontend behavior.
DO NOT create speculative APIs.
DO NOT migrate or duplicate existing data models.
DO NOT refactor unrelated code.

The existing web application and backend are production-sensitive and must remain functional.

## PRODUCT CONTEXT

PGR SIMS currently has an existing web frontend and canonical backend.

The Android application will become a second first-class frontend/client of the SAME PGR SIMS platform.

The Android MVP will initially focus primarily on resident onboarding, but the architecture must support gradual expansion until Android and web provide the same postgraduate management functionality where appropriate.

The Android application must NOT become a separate system.

## STEP 1 — INSPECT FIRST

Before making changes:

1. Inspect the repository root.
2. Identify backend, frontend, docs, CI, root `.gitignore`, naming conventions, and any existing mobile/android directories.
3. Check git status.
4. Preserve all unrelated existing files and uncommitted work.
5. If an Android/mobile directory already exists, inspect it before creating anything and adapt safely rather than duplicating it.

Do not delete anything.

## STEP 2 — CREATE TOP-LEVEL ANDROID AREA

Preferred root structure:

```text
android/
├── app/
├── core/
│   ├── common/
│   ├── model/
│   ├── network/
│   ├── auth/
│   ├── data/
│   ├── database/
│   ├── designsystem/
│   ├── navigation/
│   └── testing/
├── feature/
│   ├── authentication/
│   ├── onboarding/
│   ├── home/
│   ├── profile/
│   ├── training/
│   ├── documents/
│   ├── supervision/
│   ├── notifications/
│   └── supervisor/
└── README.md
```

Reserve/document future feature families without unnecessary empty modules:

- logbook
- workshops
- research
- assessments
- rotations
- attendance
- leave
- admin/staff operational functionality

## STEP 3 — STRUCTURAL PRINCIPLES

`app/`: composition, app entry, root wiring, top-level navigation, lifecycle, role-aware routing.

`core/common/`: cross-cutting utilities only.

`core/model/`: Android-side representations of canonical backend API contracts.

`core/network/`: API client, serialization, auth interceptors, error parsing.

`core/auth/`: session/authentication infrastructure.

`core/data/`: shared repositories/data orchestration.

`core/database/`: local cache only, never competing source of truth.

`core/designsystem/`: reusable Compose components/theme.

`core/navigation/`: shared navigation contracts.

`core/testing/`: test helpers, fixtures, fakes.

`feature/*`: functional UI/state/use cases consuming canonical backend capabilities.

Feature modules must not duplicate backend business rules.

## STEP 4 — README

Create `android/README.md` documenting:

1. Android is a client of the canonical PGR SIMS backend.
2. Web and Android share one source of truth.
3. MVP focus is resident onboarding.
4. Long-term goal is progressive parity with web.
5. Backend owns business rules, permissions and validation.
6. Android consumes APIs/services rather than recreating logic.
7. Scaffold is intentionally implementation-light.
8. Phase M0 discovery precedes substantial implementation.

## STEP 5 — PLACEHOLDERS

Use repository conventions such as `.gitkeep` sparingly if needed.

Do not create meaningless boilerplate.

## STEP 6 — ROOT INTEGRATION

Review `.gitignore`.

Add only genuinely required Android ignores, e.g. `.gradle/`, build outputs, `local.properties`, private signing files, IDE caches.

Never add secrets.

## STEP 7 — NO PREMATURE GRADLE ARCHITECTURE

Do not create a complex multi-module Gradle build unless necessary based on the existing repository.

Do not prematurely lock:
- Kotlin versions
- AGP
- Compose BOM
- SDK levels
- application ID
- DI
- Retrofit
- Room
- WorkManager

## STEP 8 — VALIDATE

1. Display the new Android tree.
2. Confirm backend/web files were not unintentionally modified.
3. Run git diff/status.
4. Run only lightweight relevant validation.

## REQUIRED FINAL REPORT

### SCAFFOLD VERDICT
PASS / BLOCKED

### Repository discovered
- backend path
- frontend path
- docs path
- CI path
- existing mobile artifacts

### Created
Exact directories/files.

### Modified
Exact existing files and why.

### Android architecture
Show resulting tree.

### Protected
Confirm:
- backend business logic untouched
- web frontend behavior untouched
- no API invented
- no existing model duplicated
- unrelated working tree changes preserved

### Next recommended action
State readiness for:

**Phase M0 — Android Mobile Architecture & API Readiness Discovery**

Do not start M0 automatically.
