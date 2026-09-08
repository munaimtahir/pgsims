# PGR Companion API contract verification

Verified on 2026-09-08 against the PGR SIMS backend routes and the isolated staging service.
No production data or reviewer credentials were used for write operations.

| Capability | PGR SIMS route | Android implementation | Verification |
| --- | --- | --- | --- |
| Login | `POST /api/auth/login/` | `InstitutionalApi.login` | Staging resident sign-in passed. |
| Token refresh | `POST /api/auth/refresh/` | `InstitutionalApi.refresh`; one retry on 401 | Unit-tested; session restore passed. |
| Logout | `POST /api/auth/logout/` | `InstitutionalApi.logout` plus mandatory local clear | Staging logout/re-login passed. |
| Identity | `GET /api/auth/me/` | snapshot identity request | Passed during each authenticated staging load. |
| Onboarding read | `GET /api/auth/onboarding/` | Profile and Home data | Passed; backend sections and missing fields rendered. |
| Onboarding edit | `PATCH /api/auth/onboarding/` | field patch only | Staging email edit persisted and was confirmed from staging. |
| Training | `GET /api/resident-training/` | Training and Home summary | Staging programme/department/status rendered. |
| Supervisor | `GET /api/supervision/assignments/` | Training and Home summary | Staging assignment rendered. |
| Documents | `GET /api/resident-documents/` | Documents list/status | Required, approved, correction, and upload states rendered. |
| Upload/resubmit | `POST /api/resident-documents/{id}/upload/` | SAF picker, local type/size validation, multipart upload | Staging Training Letter uploaded and changed to Under review. |

The Android client uses bearer access tokens, encrypted SharedPreferences backed by the Android
Keystore, and no HTTP logging interceptor. It does not store passwords. Contract errors are mapped
to resident-safe messages rather than exposing JSON bodies or tokens.
