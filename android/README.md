# PGR SIMS — Android

PGR SIMS Android is a client of the canonical PGR SIMS backend (Django REST API under
`backend/`). It is a second first-class frontend of the same platform — it does not become a
separate system.

## Relationship to the rest of the repository

- The Django backend (`backend/`) is the single source of truth for data, business rules,
  permissions, and validation.
- The existing Next.js web frontend (`frontend/`) and this Android app are both clients of that
  same backend. They read and write the same data through the same API surface.
- Android must consume the backend's APIs/services rather than recreate business logic locally.
  Local storage (`core/database/`) is a cache/client facility, not a competing source of truth.

## Current foundation release

The current deliverable is a minimal branded, launchable foundation shell. It uses the canonical
backend contract for health/auth primitives and deliberately does not include resident onboarding
or other substantive feature UI. The production application identity is `fmu.pg.sims` and the
store-facing name is **FMU Postgraduate Residency Portal**.

## Status of this scaffold

The project contains the Android `app` module with Compose/Material 3, Retrofit/OkHttp,
serialization, encrypted token storage, navigation/auth foundations, and the minimal shell. Feature
directories listed below remain planned architecture rather than implemented feature modules.

Before substantial Android feature implementation begins, a **Phase M0 — Android Mobile
Architecture & API Readiness Discovery** pass must occur to confirm current backend API surface,
auth flow, and contract alignment against `docs/contracts/` (see the repository root `CLAUDE.md`
and `AGENTS.md` for the canonical backend/contract model). Note: prior mobile discovery notes exist
under `docs/ARCHIVE/_mobile_android/` but predate the current 4-role clean-room identity model
(`ADMIN` / `RESIDENT` / `SUPERVISOR` / `SUPPORT_STAFF`) — treat them as historical background only,
not as a current spec.

## Directory layout

```
android/
├── app/                    Application composition: entry point, root DI wiring,
│                           top-level navigation host, global session/app lifecycle,
│                           role-aware entry routing. No feature business logic here.
├── core/
│   ├── common/             Cross-cutting utilities.
│   ├── model/              Shared Android-side representations of backend API contracts.
│   ├── network/            HTTP/API infrastructure (client, serialization, auth
│   │                       interceptors, error parsing).
│   ├── auth/               Session/authentication infrastructure.
│   ├── data/                Repository/data orchestration shared across features.
│   ├── database/           Local caching/persistence infrastructure (cache, not source
│   │                       of truth).
│   ├── designsystem/       Reusable UI primitives, typography, dimensions, theme.
│   ├── navigation/         Shared navigation contracts and destinations.
│   └── testing/            Shared test helpers, fixtures, fakes.
└── feature/
    ├── authentication/
    ├── onboarding/         MVP focus.
    ├── home/
    ├── profile/
    ├── training/
    ├── documents/
    ├── supervision/
    ├── notifications/
    └── supervisor/
```

Each `feature/*` module owns its own UI/state/use cases and consumes canonical services through
the shared `core/data` and `core/network` abstractions — it must not duplicate backend business
rules.

Future feature families that are reserved but not yet scaffolded as modules: logbook, workshops,
research, assessments, rotations, attendance, leave, and admin/staff operational functionality.
These will be added as modules only when their implementation phase begins.

## Build tooling

No Gradle build files are included in this scaffold. Gradle module wiring, Kotlin/AGP/Compose BOM
versions, SDK levels, application ID, and the dependency injection / networking / persistence
library choices are deliberately deferred to the next implementation phase (Phase M0 and beyond).
