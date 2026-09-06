# Android staging and end-to-end verification — 2026-09-06

## Environment state

| Environment | URL | Result |
|---|---|---|
| Production | `https://android.pgsims.alshifalab.pk/` | Reachable; `/healthz/` returned 200. |
| VM-isolated staging | `http://127.0.0.1:18014/` (SSH tunnel / emulator `10.0.2.2`) | Live and healthy; isolated Compose project, database, Redis, media volumes, and staging-only accounts. |
| Public staging | `https://staging.pgsims.alshifalab.pk/` | DNS does not resolve; public HTTPS edge remains unavailable. |

The VM deployment is an isolated staging runtime, provisioned from
`docker/docker-compose.staging.yml` under project name `pgsims-staging`. Its local environment
file is mode 600 and ignored by Git. Production was not used for resident sign-in, profile edits,
uploads, or resubmissions. Public hostname status remains classification **C — configured but not
deployed/reachable** because DNS/TLS cannot complete without a DNS record.

## API inventory

| Capability | Method | Endpoint | Auth | Verified |
|---|---|---|---|---|
| Health | GET | `/healthz/` | No | Production live PASS |
| Login | POST | `/api/auth/login/` | No | VM staging live PASS; invalid login returned 401 |
| Refresh | POST | `/api/auth/refresh/` | Refresh token | VM staging live PASS |
| Logout | POST | `/api/auth/logout/` | Bearer + refresh token | VM staging live PASS; subsequent refresh returned 401 |
| Identity/onboarding summary | GET | `/api/auth/me/` | Bearer | VM staging live PASS |
| Resident profile/onboarding | GET/PATCH | `/api/auth/onboarding/` | Bearer resident | VM staging GET live PASS; PATCH not executed |
| Programme/training | GET | `/api/resident-training/` | Bearer | VM staging live PASS (empty fixture) |
| Supervisor | GET | `/api/supervision/assignments/` | Bearer | VM staging live PASS (empty fixture) |
| Documents | GET | `/api/resident-documents/` | Bearer | VM staging live PASS |
| Upload/resubmission | POST multipart | `/api/resident-documents/{id}/upload/` | Bearer | Source verified |

`GET /api/auth/login/` returned production `405` and `Allow: POST`, a non-mutating route probe.
No source-only row is represented as a live staging result.

## Emulator checks

API 36 `emulator-5554` installed Companion and the distinct `pk.vexel.pgrportal.dev.staging`
local-staging variant simultaneously. Portal completed a live resident login through the tunnel and
rendered server-provided incomplete-profile/onboarding requirements. The authenticated logout defect
found during this probe was fixed and covered by a unit test; server-side logout/revocation was
also live-verified directly. Full profile PATCH, programme/supervisor fixtures, upload/resubmission,
and uninstall isolation remain pending.

## Required external closure

Create DNS for the configured staging hostname and install the Caddy site fragment, enabling HTTPS
before treating staging as externally reachable. Extend the staging-only fixture through canonical
services with training, assignment, document review states, then execute profile PATCH,
upload/resubmission, session restore, and uninstall isolation. Record only account identifiers,
never credentials.

## Build and security result

The full Android verification command completed successfully after the Portal wording correction:
both unit-test tasks, both debug lint tasks, and both release APK/AAB tasks passed. The rebuilt
Portal development artifacts are version `0.1.1-dev` / code `2`. Portal does not log credentials
or tokens, uses HTTPS-only traffic, and uses encrypted session storage. Companion’s frozen AAB was
not rebuilt or changed during this sprint.
