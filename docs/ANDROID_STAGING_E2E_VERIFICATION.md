# Android staging and end-to-end verification — 2026-09-06

## Environment state

| Environment | URL | Result |
|---|---|---|
| Production | `https://android.pgsims.alshifalab.pk/` | Reachable; `/healthz/` returned 200. |
| VM-isolated staging | `http://127.0.0.1:18014/` | Live and healthy; isolated Compose project, database, Redis, media volumes, and staging-only accounts. |
| Public staging | `https://staging.pgsims.alshifalab.pk/` | Live HTTPS Caddy route to isolated staging; `/healthz/` returned 200. |

The VM deployment is an isolated staging runtime, provisioned from
`docker/docker-compose.staging.yml` under project name `pgsims-staging`. Its local environment
file is mode 600 and ignored by Git. Production was not used for resident sign-in, profile edits,
uploads, or resubmissions. The public hostname now resolves and is served by a validated/reloaded
Caddy route to port `18014`; production `android.pgsims.alshifalab.pk` was not changed.

## API inventory

| Capability | Method | Endpoint | Auth | Verified |
|---|---|---|---|---|
| Health | GET | `/healthz/` | No | Production live PASS |
| Login | POST | `/api/auth/login/` | No | Public staging PASS; invalid login returned 401 |
| Refresh | POST | `/api/auth/refresh/` | Refresh token | Public staging PASS |
| Logout | POST | `/api/auth/logout/` | Bearer + refresh token | Public staging PASS; subsequent refresh returned 401 |
| Identity/onboarding summary | GET | `/api/auth/me/` | Bearer | Public staging PASS |
| Resident profile/onboarding | GET/PATCH | `/api/auth/onboarding/` | Bearer resident | Public staging PASS |
| Programme/training | GET | `/api/resident-training/` | Bearer | Public staging PASS with active record |
| Supervisor | GET | `/api/supervision/assignments/` | Bearer | Public staging PASS with active assignment |
| Documents | GET | `/api/resident-documents/` | Bearer | Public staging PASS: missing/verified/correction states |
| Upload/resubmission | POST multipart | `/api/resident-documents/{id}/upload/` | Bearer | Public staging PASS; invalid extension rejected 400 |

`GET /api/auth/login/` returned production `405` and `Allow: POST`, a non-mutating route probe.
No source-only row is represented as a live staging result.

## Emulator checks

API 36 `emulator-5554` installed Companion and the distinct `pk.vexel.pgrportal.dev.staging`
local-staging variant simultaneously. Portal completed a live resident login through the tunnel and
rendered server-provided incomplete-profile/onboarding requirements. The authenticated logout defect
found during this probe was fixed and covered by a unit test; server-side logout/revocation was
also live-verified directly. Public staging API now verifies profile PATCH, programme/supervisor
fixtures, upload, review feedback and resubmission. The emulator became unavailable before the
final rebuilt APK session-restore/logout/uninstall pass.

## Required external closure

When API 36 is available, install final Portal `0.1.2-dev`, verify session restoration,
document-picker upload, logout, and uninstall isolation. Record only account identifiers, never
credentials.

## Build and security result

The final Android verification command completed successfully: both unit-test tasks, both debug
lint tasks, both release APK/AAB tasks, and Portal staging APK assembly passed. The rebuilt Portal
development artifacts are version `0.1.2-dev` / code `3`. Portal does not log credentials
or tokens, uses HTTPS-only traffic, and uses encrypted session storage. Companion’s frozen AAB was
not rebuilt or changed during this sprint.
