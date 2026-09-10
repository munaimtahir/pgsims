# Platform API Contract Matrix

Scope: resident-facing + core RBAC-relevant API surface actually wired into `sims_project/urls.py`
(installed apps only: `users, academics, rotations, audit, bulk, notifications, training,
supervision, backup_center`). Verified against `backend/sims/*/urls.py`, `views.py`,
`frontend/lib/api/*.ts`, and `android/app-companion` source on 2026-09-09 at HEAD `5686112`.

Legend for **Maturity**: UNUSED / LEGACY / DRAFT / IMPLEMENTED / TESTED / PRODUCTION VERIFIED /
STABLE FOR WEB / STABLE FOR MOBILE / DEPRECATED. Multiple labels may apply (e.g. a route can be
TESTED + STABLE FOR WEB but not yet consumed by Android).

## Auth / Identity

| Endpoint | Method | Backend | Web consumer | Android consumer | Maturity |
|---|---|---|---|---|---|
| `/api/auth/profile/` | GET/PATCH | `sims/users/api_urls.py` → canonical current-user | `frontend/lib/api/auth.ts` | not used (Android uses `/api/auth/me/`) | STABLE FOR WEB, PRODUCTION VERIFIED |
| `/api/auth/me/` | GET | `sims/users/userbase_urls.py` | admin tooling | `android/app-companion` session bootstrap | STABLE FOR MOBILE, PRODUCTION VERIFIED (per SPRINT_STATE synthetic-resident E2E) |
| `/api/auth/change-password/` | POST | `sims/users/api_urls.py` | `frontend/lib/api/auth.ts` | not confirmed in Android source scan | TESTED, STABLE FOR WEB |
| `/api/auth/password-reset/`, `.../confirm/` | POST | `sims/users/api_urls.py` | `frontend/lib/api/auth.ts` | not used | TESTED |

Note: **two parallel current-user endpoints exist** (`/api/auth/profile/` for web, `/api/auth/me/`
for Android + admin tooling) with different payload shapes by design (per
`docs/contracts/API_CONTRACT.md` Phase 7 note). This is documented intentionally, not drift, but
is a real dual-contract surface a future client author must know about — flagged for
`13_FEATURE_DEPENDENCY_GRAPH.md`.

## Rotation Assignments (`sims.training`, mounted at `/api/...`)

| Endpoint | Method | Backend | Web consumer | Android consumer | Maturity |
|---|---|---|---|---|---|
| `/api/rotations/` | GET/POST | `training/views.py::RotationAssignmentViewSet` | `frontend/lib/api/rotations.ts` | not directly listed; Android reads via summary | TESTED, STABLE FOR WEB |
| `/api/rotations/{id}/submit,hod-approve,utrmc-approve,activate,complete,returned,reject/` | POST | same | `rotations.ts` | not used | TESTED, STABLE FOR WEB |
| `/api/my/rotations/` | GET | `training/views.py::MyRotationsView` | `rotations.ts` | not confirmed as a direct call — Android instead reads rotation data embedded in `/api/residents/me/summary/` (`rotation.current`) | IMPLEMENTED, STABLE FOR WEB; Android path is the summary endpoint, not this one |
| `/api/residents/me/summary/` | GET | `training/views.py::ResidentSummaryView` | not the web's primary source (web uses discrete rotations/leaves calls) | **primary Android data source** — `ResidentWorkflowScreens.kt` reads `residentSummary.rotation.current.{department_name,hospital_name,status,...}` | PRODUCTION VERIFIED for Android (SPRINT_STATE: verified against real production response shape) |

Field-shape note (verified, not drift): `RotationAssignment` in `frontend/lib/api/rotations.ts:34-52`
declares `hospital_name`/`department_name` as flat strings on the list/detail serializer, while
`ResidentSummaryView`'s embedded `rotation.current` object (consumed by Android) exposes the same
concept sometimes as `department`/`hospital` and sometimes as `department_name`/`hospital_name`
depending on serializer path — Android code defensively falls back between both
(`ResidentWorkflowScreens.kt:65,124,126,144`, `.ifBlank { ... }` chains). This is the exact
mismatch SPRINT_STATE.md says was "corrected" — it was corrected on the **Android consumption
side** (defensive fallback), not by unifying the two serializer paths. See `07_CONTRACT_DRIFT_REPORT.md` P2-1.

## Leave Requests (`sims.training`)

| Endpoint | Method | Web consumer | Android consumer | Maturity |
|---|---|---|---|---|
| `/api/leaves/`, `/api/leaves/{id}/`, `/submit,approve,reject/` | GET/POST | `frontend/lib/api/leave.ts` | embedded read-only via summary; no direct leave-creation flow found in Android source | TESTED, STABLE FOR WEB; Android read-only |
| `/api/my/leaves/` | GET | `leave.ts` | not confirmed direct | IMPLEMENTED |

## Logbook (`sims.academics`, mounted at `/api/academics/` via `workflow_urls.py` — verify prefix)

| Endpoint | Method | Web consumer | Android consumer | Maturity |
|---|---|---|---|---|
| `LogbookEntry` CRUD/submit/review | GET/POST/PATCH | `frontend/lib/api/academics.ts` | `android/app-companion` Logbook draft/edit/submit screens (per SPRINT_STATE: "Implemented ... Logbook draft/edit/submit") | PRODUCTION VERIFIED both clients per SPRINT_STATE ("Verified API logbook create, edit and submit and then created a separate synthetic draft through the API-36 Android UI") |

Status/field aliasing (`feedback`↔`supervisor_feedback`, `submitted_to_supervisor_at`↔`submitted_at`)
is documented in `docs/contracts/API_CONTRACT.md` L14-22 and `docs/TERMINOLOGY.md` — see drift
report for whether both clients apply it consistently.

## Notifications (`sims.notifications`)

| Endpoint | Web consumer | Android consumer | Maturity |
|---|---|---|---|
| `/api/notifications/...` | `frontend/lib/api/notifications.ts` | not confirmed in Android source | STABLE FOR WEB, UNUSED for mobile |

## Users / Org graph (`sims.users`)

| Endpoint | Web consumer | Android consumer | Maturity |
|---|---|---|---|
| `/api/users/`, `/api/residents/{id}/`, `/api/staff/{id}/` | `frontend/lib/api/userbase.ts`, `users.ts` | not used (Android is resident-scoped self-service only) | STABLE FOR WEB, UNUSED for mobile (by design — Android is single-role resident client) |
| `/api/hospitals/`, `/api/departments/`, `/api/hospital-departments/` | `frontend/lib/api/masters.ts` | not used | STABLE FOR WEB |

## Deferred/legacy surface (present in `docs/contracts/API_CONTRACT.md`, confirmed still routed but not on the active gated UI)

Research (`/api/my/research/...`), Thesis (`/api/my/thesis/...`), Workshops (`/api/my/workshops/...`),
Submissions/Synopsis/Certificates (`/api/submissions/...`), Deputation Postings (`/api/postings/...`),
Rotation Phase-1 completion verification (`/api/rotations/completions/...`) — all still registered
in `sims/training/urls.py` (verified live in source, not removed) but the contract doc itself
labels them "Status as of 2026-04-21: route/API retained, not part of active release-gated UI."
Neither web nor Android has active navigation entries wired to these (confirmed: no route matches
in `frontend/app/` for `/research`, `/thesis`, `/workshops`, `/postings` as top-level pages beyond
what's under `/academics`). **Maturity: IMPLEMENTED, DEPRECATED-FROM-UI** — endpoints exist and
presumably still pass their own tests, but are intentionally dark. Do not build new Android or web
work against these without an explicit decision to re-activate that surface.

## RBAC role model — CRITICAL documentation drift

`docs/contracts/API_CONTRACT.md` L7-12 declares "Roles (locked)" as `pg`, `supervisor`, `admin`,
`utrmc_user`, `utrmc_admin` — this is **stale**. Verified in `backend/sims/users/models.py:11-13`
the actual `User.role` choices are exactly `RESIDENT`, `SUPERVISOR`, `ADMIN`, `SUPPORT_STAFF` (the
4-role clean-room model CLAUDE.md declares authoritative). Code comments/tests in
`sims/training/views.py` and `sims/training/tests.py` use `utrmc_admin`/`utrmc_user` only as
*semantic labels* for `ADMIN`/`SUPPORT_STAFF` respectively (e.g.
`test_feature_layer_ops.py:59-60`: `make_user("fl_utrmc_admin", "ADMIN")`,
`make_user("fl_utrmc_user", "SUPPORT_STAFF")`) — never as literal enum values. See
`07_CONTRACT_DRIFT_REPORT.md` P1-1.

## Full detail

`docs/contracts/API_CONTRACT.md` (494 lines) remains the most complete single endpoint list and is
largely accurate on URL/payload shape for the phases it documents (Phase 6/7/8, backup center,
bulk import/export) — this matrix does not attempt to re-enumerate every route it already covers
accurately (e.g. backup_center Google Drive connector, bulk import/export, analytics) since no
drift was found there in spot checks. This matrix's value-add is the **web vs Android consumption
mapping**, which no existing doc provides.
