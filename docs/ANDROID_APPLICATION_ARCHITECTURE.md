# Android application architecture

| Product | Module | Package | Purpose |
|---|---|---|---|
| PGR Companion | `:app-companion` | `pk.vexel.pgrcompanion` | Single login-gated institutional PGR SIMS Android application. |

`core:common` has only neutral visual primitives. PGR Companion owns its encrypted PGR SIMS JWT
storage and server-backed workflows. There is no second Android product or alternate module.

Build with `./gradlew :app-companion:bundleRelease`. The package ID is permanently
`pk.vexel.pgrcompanion`; debug, staging, and release are build variants of the same application.
