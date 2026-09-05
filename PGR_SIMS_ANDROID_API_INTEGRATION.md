# PGR SIMS Android API integration

Release API base URL: `https://android.pgsims.alshifalab.pk/` (HTTPS only; cleartext is disabled
outright in release, and permitted for emulator loopback in a debug-only manifest overlay).

## Verified contracts

Every row below was confirmed twice on 2026-09-06: by reading the backend source on the canonical
host (`backend/sims/users/api_urls.py`, `userbase_urls.py`, `onboarding_api.py`,
`sims/training/urls.py`, `sims/supervision/`), and by issuing the actual request against the live
server with a seeded demo resident account. Nothing here is inferred.

| Method | Endpoint | Request | Response shape |
|---|---|---|---|
| POST | `/api/auth/login/` | `{username, password}` | `{access, refresh, user{id,username,email,role,first_name,last_name,full_name}}` |
| POST | `/api/auth/refresh/` | `{refresh}` | `{access, refresh}` — **rotates the refresh token** |
| POST | `/api/auth/logout/` | `{refresh}` | `{message}`; blacklists the token |
| GET | `/api/auth/me/` | — | identity + onboarding summary (see below) |
| GET | `/api/auth/onboarding/` | — | full onboarding state; **RESIDENT only, 403 otherwise** |
| PATCH | `/api/auth/onboarding/` | `{"fields": {name: value}}` | the full onboarding state, re-read |
| GET | `/api/resident-documents/` | — | **bare JSON array**, not paginated |
| POST | `/api/resident-documents/{id}/upload/` | multipart, part name `file` | the updated document |
| GET | `/api/resident-training/` | — | DRF page `{count, next, previous, results}` |
| GET | `/api/supervision/assignments/` | — | DRF page `{count, next, previous, results}` |

Two shape details are easy to get wrong and are both covered by tests: `/api/resident-documents/`
overrides `list()` and returns a bare array while the other two collections are paginated at
`PAGE_SIZE=25`, and the onboarding PATCH takes a `{"fields": ...}` envelope, not a bare map.

### Fields the client actually reads

- `me`: `username`, `role`, `must_change_password`, `onboarding_review_status`,
  `pending_upload_count`. **`/api/auth/me/` does not return `full_name`** — only the login response
  does — so the header uses `username`.
- `onboarding`: `sections[{key, title, fields[{field, label, value, required}]}]`, `review_status`.
- `documents`: `id`, `title`, `status`, `verification_remarks`.
- `resident-training` results: `program_name`, `program_code`, `current_level`, `start_date`,
  `expected_end_date`.
- `supervision/assignments` results: `supervisor{name, designation, department}`,
  `assignment_type`.

### Server-side rules the client mirrors

Upload: 10 MB maximum, extensions `.pdf .jpg .jpeg .png .doc .docx`. The client validates both
before sending so the user gets a sentence instead of a 400. The backend remains authoritative for
field permissions, review states and validation.

## Auth behaviour

Bearer authentication is added by an interceptor on the authorized client only. Refresh and logout
go through a separate client with no interceptor. A `401` refreshes once and replays; a failed
refresh clears the session. HTTP status is mapped to a plain sentence — 401 expired session, 403
not permitted, 429 too many attempts, 5xx server unavailable, `IOException` unreachable — and no
user-facing string contains a token, a bearer header or the submitted password.

## Play Data Safety consequence

Version 1.0.0 collected and transmitted nothing. Version 1.1.0 does, **but only for users who
choose to sign in on the Institution tab**. The declaration must be updated before rollout:

- **Personal info (name, email, phone, user ID)** — transmitted to the institution, and displayed
  from it. Optional; user-initiated; not shared with third parties.
- **Files and docs** — uploaded to the institution only when the user picks a file for a document
  the institution has requested. Optional; user-initiated.
- **App activity / credentials** — username and password are transmitted to the institution to
  authenticate. **Not stored on the device**; only the resulting session tokens are, encrypted.
- Data is encrypted in transit (HTTPS enforced; cleartext disabled in release).
- No advertising, no analytics, no third-party sharing, in either workspace.

The offline Personal Workspace still collects and transmits nothing, which is why the in-app copy
now distinguishes the two rather than claiming the app has no connection at all.
