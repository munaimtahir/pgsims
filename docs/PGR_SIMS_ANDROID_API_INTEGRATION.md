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
confirming the deployed route/method boundary. The configured staging hostname
`staging.pgsims.alshifalab.pk` did not resolve in DNS, so no credentials or production data were
used to test write endpoints. Staging endpoint contracts are source-verified, not live-verified.
