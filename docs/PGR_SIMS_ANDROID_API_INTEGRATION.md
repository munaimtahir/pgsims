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
