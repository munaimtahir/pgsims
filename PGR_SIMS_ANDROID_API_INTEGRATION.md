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

### Live probes run on 2026-09-06 (non-mutating by construction)

Each of these was issued against production with a seeded demo resident and is designed to be
rejected *before* the backend changes anything, so the route, auth, parser and error contract are
proven without touching a record. The document list was re-read afterwards and was byte-identical.

| Probe | Result |
|---|---|
| `POST .../1/upload/` multipart with no `file` part | `400 {"detail":"file is required"}` — part name confirmed |
| `POST .../1/upload/` multipart with `notes.txt` | `400` listing `.doc .docx .jpeg .jpg .pdf .png` — matches the client allowlist exactly |
| `POST .../999999/upload/` (someone else's document) | `404`, not `403` — the queryset is scoped, so nothing leaks |
| `PATCH /api/auth/onboarding/` `{"fields":{"not_a_real_field":…}}` | `400 {"not_a_real_field":"Unsupported onboarding field."}`, rolled back inside `transaction.atomic()` |
| `PATCH /api/auth/onboarding/` with a **bare map** | `200` — and nothing is written |
| `GET /api/auth/me/` with no token | `401` |

The bare-map result is the important one. `patch()` falls back to
`{request.data.get("field"): request.data.get("value")}`, which filters to `{}`, so a client that
sent a bare map would get a cheerful `200` while saving nothing. The client sends the
`{"fields": …}` envelope and a unit test asserts the wire shape, precisely because the failure mode
is silent.

### Fields the client actually reads

- `me`: `username`, `role`, `must_change_password`, `onboarding_review_status`,
  `pending_upload_count`. **`/api/auth/me/` does not return `full_name`** — only the login response
  does — so the header uses `username`.
- `onboarding`: `sections[{key, title, fields[{field, label, value, required}]}]`, `review_status`,
  `review_note`, `supervisor_status`, `profile_complete`, `declaration_accepted`,
  `onboarding_complete`, `required_onboarding_fields`, `documents`.
- `documents`: `id`, `title`, `status`, `original_filename`, `verification_remarks`.
- `resident-training` results: `program_name`, `program_code`, `current_level`, `start_date`,
  `expected_end_date`.
- `supervision/assignments` results: `supervisor{name, designation, department}`,
  `assignment_type`.

### Server-side rules the client mirrors

Upload: 10 MB maximum, extensions `.pdf .jpg .jpeg .png .doc .docx`. The client validates both
before sending so the user gets a sentence instead of a 400. The backend remains authoritative for
field permissions, review states and validation.

Editable fields: `_set_resident_onboarding_field` accepts free text for `full_name`, `phone`,
`email`, `registration_no`, `cnic` and `notes` only. `hospital`, `department_ref` and `program_ref`
resolve by **primary key**; `academic_session_ref` and `specialty_ref` resolve by **code**;
`training_start_date` and `expected_end_date` want ISO-8601 and 400 otherwise. Live values observed
for the demo resident were `hospital=9`, `department_ref=31`, `program_ref=15`,
`academic_session_ref="JAN-2026"`, `specialty_ref="anesthesia"`. The client renders all of those
read-only rather than as text boxes holding a row id — see
`INSTITUTIONAL_WORKSPACE_ARCHITECTURE.md`.

## Auth behaviour

Bearer authentication is added by an interceptor on the authorized client only. Refresh and logout
go through a separate client with no interceptor. A `401` refreshes once and replays; a failed
refresh clears the session. HTTP status is mapped to a plain sentence — 401 expired session, 403
not permitted, 429 too many attempts, 5xx server unavailable, `IOException` unreachable — and no
user-facing string contains a token, a bearer header or the submitted password.

## Play Data Safety consequence

**As of `versionCode 3` / `1.1.3`, the `pk.vexel.pgrcompanion` listing is built from
`android/app-portal` — a login-gated PGR SIMS client, not the offline-only `1.0.2` build.** This
was an explicit repository-level decision (see `builds/companion/build-info.json` and
`SPRINT_STATE.md`): there is no offline Personal Workspace in this listing any more, and login is
required to use the app at all. The declaration reflects that:

- **Personal info (name, email, phone, user ID)** — transmitted on login and displayed back from
  the server. **Required** — the app cannot be used without signing in. Not shared with third
  parties.
- **Files and docs** — uploaded only when the user picks a file for a document the SIMS deployment
  has requested. Optional; user-initiated.
- **App activity / credentials** — username and password are transmitted to authenticate.
  **Not stored on the device**; only the resulting session tokens are, encrypted.
- Data is encrypted in transit (HTTPS enforced; cleartext disabled in release).
- No advertising, no analytics, no third-party sharing.

The prior `1.0.2` offline-only build (`android/app-companion`) collected and transmitted nothing;
it is now superseded and frozen. See `data_safety_export.csv` for the full machine-readable
declaration matching this build.
