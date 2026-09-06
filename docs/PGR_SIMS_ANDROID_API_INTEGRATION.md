# PGR SIMS Android API integration

Portal uses HTTPS PGR SIMS endpoints verified in backend source and prior production probes:
`POST /api/auth/login/`, `refresh/`, `logout/`; `GET /api/auth/me/`, `onboarding/`,
`resident-documents/`, `resident-training/`, `supervision/assignments/`; `PATCH
/api/auth/onboarding/`; and multipart `POST /api/resident-documents/{id}/upload/` with part name
`file`. Login returns access and refresh tokens; refresh rotates the refresh token. The client
uses a bearer interceptor only for authorized calls and puts tokens in encrypted preferences.

The onboarding patch is `{"fields": {…}}`; document lists are bare arrays and training/assignment
lists are paginated. Upload accepts PDF, JPEG, PNG, DOC, DOCX up to 10 MB. The backend is
authoritative for permissions, review state, allowed fields, validation and resubmission flow.
No credentials, tokens, or production secrets are committed or logged.

## Environment verification — 2026-09-06

Production `https://android.pgsims.alshifalab.pk/healthz/` returned `200` with healthy database,
cache, and Celery checks. Its login route returned `405 Allow: POST` to a safe unauthenticated GET,
confirming the deployed route/method boundary.

An isolated VM staging service now verifies live `POST` login (including invalid credentials),
refresh, authenticated logout/revocation, and authenticated `GET` calls to `me`, onboarding,
documents, training, and supervisor assignments. The probe found that backend logout correctly
requires a bearer token in addition to the refresh payload; Portal now sends it and its logout
test asserts the header. The configured public staging hostname still does not resolve, so this
local isolated endpoint is reached only through an SSH tunnel/emulator loopback override. Profile
PATCH and document upload/resubmission are not yet live-verified.
