# Android dual-track architecture

| Product | Module | Package | Purpose |
|---|---|---|---|
| PGR Companion: Residency | `:app-companion` | `pk.vexel.pgrcompanion` | Offline generic residency portfolio and Play baseline. |
| PGR Portal Dev | `:app-portal` | `pk.vexel.pgrportal.dev` | FMU-first institutional PGR SIMS client. |

`core:common` has only neutral visual primitives. Companion owns `LocalStore`; Portal owns its
encrypted PGR SIMS JWT storage. Neither product reads or writes the other's state, so both can
coexist and removing Portal cannot alter Companion records.

Build independently with `./gradlew :app-companion:bundleRelease` and
`./gradlew :app-portal:bundleRelease`. Companion has no PGR SIMS endpoint, login, network
permission, or dormant institutional switch. Portal has `debug`, `staging`, and `release` builds.
