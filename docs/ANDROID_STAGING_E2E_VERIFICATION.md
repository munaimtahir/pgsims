# Android staging and end-to-end verification — 2026-09-06

## Environment state

| Environment | URL | Result |
|---|---|---|
| Production | `https://android.pgsims.alshifalab.pk/` | Reachable; `/healthz/` returned 200. |
| Staging | `https://staging.pgsims.alshifalab.pk/` | Configured in Portal but DNS does not resolve; not deployed/reachable. |

The repository has compose/deployment configurations but no committed staging environment file,
staging DNS, isolated staging database, or safe staging credentials. This is classification **C —
configured but not deployed/reachable**. Production was not used for resident sign-in, profile
edits, uploads, or resubmissions.

## API inventory

| Capability | Method | Endpoint | Auth | Verified |
|---|---|---|---|---|
| Health | GET | `/healthz/` | No | Production live PASS |
| Login | POST | `/api/auth/login/` | No | Source + production route/method PASS |
| Refresh | POST | `/api/auth/refresh/` | Refresh token | Source verified |
| Logout | POST | `/api/auth/logout/` | Refresh token | Source verified |
| Identity/onboarding summary | GET | `/api/auth/me/` | Bearer | Source verified |
| Resident profile/onboarding | GET/PATCH | `/api/auth/onboarding/` | Bearer resident | Source verified |
| Programme/training | GET | `/api/resident-training/` | Bearer | Source verified |
| Supervisor | GET | `/api/supervision/assignments/` | Bearer | Source verified |
| Documents | GET | `/api/resident-documents/` | Bearer | Source verified |
| Upload/resubmission | POST multipart | `/api/resident-documents/{id}/upload/` | Bearer | Source verified |

`GET /api/auth/login/` returned production `405` and `Allow: POST`, a non-mutating route probe.
No source-only row is represented as a live staging result.

## Emulator checks

API 36 `emulator-5554` installed both `pk.vexel.pgrcompanion` and `pk.vexel.pgrportal.dev`
simultaneously. Companion’s actual AAB-derived APK created and persisted a local profile across
restart and worked with network disabled. Portal launched its distinct login UI. Full Portal auth,
session restoration/refresh/logout, onboarding edits, document upload/resubmission, and uninstall
isolation cannot run without staging and an isolated account.

## Required external closure

Deploy the configured staging hostname with its own database, secrets, TLS certificate, and no
production resident data. Run the existing `seed_android_e2e_demo` command only there, or create an
equivalent dedicated resident through canonical services. Then execute the live test matrix using
the documented endpoint contracts and record only test-account identifiers, never credentials.

## Build and security result

The full Android verification command completed successfully after the Portal wording correction:
both unit-test tasks, both debug lint tasks, and both release APK/AAB tasks passed. The rebuilt
Portal development artifacts are version `0.1.1-dev` / code `2`. Portal does not log credentials
or tokens, uses HTTPS-only traffic, and uses encrypted session storage. Companion’s frozen AAB was
not rebuilt or changed during this sprint.
