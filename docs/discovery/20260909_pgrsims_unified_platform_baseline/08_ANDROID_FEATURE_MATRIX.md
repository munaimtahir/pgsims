# 08 — Android Feature Matrix (PGR Companion, `android/app-companion`)

Scope: PGR Companion Android app only (`pk.vexel.pgrcompanion`, source module `android/app-companion`).
Evidence base: direct inspection of `android/app-companion/src/main/java/pk/vexel/pgrcompanion/*.kt`
(6 files, 1,482 lines) on 2026-09-09, cross-referenced against `SPRINT_STATE.md`'s claims and
`PGR_SIMS_ANDROID_API_INTEGRATION.md`'s endpoint table. There is no `feature/` or `core/` package
split inside `app-companion` — the module is a single flat package
(`pk.vexel.pgrcompanion`) with one Activity, one repository, and Composable screens; the task's assumed
`android/app-companion/feature/` and `android/app-companion/core/` directories do not exist as such (only
the separate Gradle module `core:common` exists, and it is a shared Compose theme only — see 09).

| Domain | UI | API Wired | Production Connected | E2E Verified | Status |
|---|---|---|---|---|---|
| Authentication | Sign-in form (`InstitutionalScreen.kt`), sign-out | `POST /api/auth/login/`, `/refresh/`, `/logout/`, `GET /api/auth/me/` (`InstitutionalRepository.kt:81-84`) | Yes | Yes — `ANDROID_RELEASE_VERIFICATION.md` items 9-11, 19-20 (sign-in, session restore across force-stop, sign-out) | COMPLETE |
| Home | `InstitutionalWorkspace` Home tab + `CurrentTrainingCard` (`ResidentWorkflowScreens.kt:51-`) showing current rotation from `residentSummary.rotation.current` | `GET /api/residents/me/summary/` (`InstitutionalRepository.kt:99`) | Yes | Yes — SPRINT_STATE.md "Verified all production reads for the synthetic resident" | COMPLETE |
| Profile | Onboarding/profile section render + editable-field form (`Onboarding.kt`, `InstitutionalScreen.kt`) | `GET/PATCH /api/auth/onboarding/` (`InstitutionalRepository.kt:85-86,267`) | Yes | Yes — verification items 12-13 (onboarding status card, editable vs read-only fields matching live payload) | COMPLETE |
| Documents | Document list + SAF file picker + upload/replace (`ResidentWorkflowScreens.kt`, `CompanionActivity.kt` `displayNameOf`) | `GET /api/resident-documents/`, `POST /{id}/upload/` (`InstitutionalRepository.kt:87-88,277-`) | Yes (reads); upload route probed non-mutating in prod, not executed live | Partial — verification items 16-18 (list/replace-dialog/picker) confirmed; live 200-with-stored-file explicitly **not** run (`ANDROID_RELEASE_VERIFICATION.md` "Not verified" section) | PARTIAL |
| Training | `TrainingScreen`/rotation history+detail cards (`ResidentWorkflowScreens.kt`) | `GET /api/resident-training/`, `GET /api/my/rotations/`, `GET /api/supervision/assignments/` (`InstitutionalRepository.kt:89-91`) | Yes | Yes — SPRINT_STATE.md: rotation presentation corrected against live response shape (`rotation.current`, `department_name`/`hospital_name`) | COMPLETE |
| Rotations | Rotation history/detail rendered inside Training tab (no separate top-level tab) | `GET /api/my/rotations/` | Yes | Yes (same evidence as Training) | COMPLETE |
| Supervision | Supervisor assignment display inside Training/Home (name, designation, department) | `GET /api/supervision/assignments/` | Yes | Yes — verification item 15 (empty state mirrors backend `supervisor_status`) | COMPLETE |
| Logbook | Draft/edit/submit UI (`ResidentWorkflowScreens.kt`), correction/resubmission flow | `GET/POST /api/academics/logbook-entries/`, `PATCH .../{id}/`, `POST .../{id}/submit/`, `GET .../logbook-categories/` (`InstitutionalRepository.kt:91-95,255-266`) | Yes | Yes — SPRINT_STATE.md: "Verified API logbook create, edit and submit and then created a separate synthetic draft through the API-36 Android UI"; correction/resubmission E2E verified per SPRINT_STATE closure notes | COMPLETE |
| Assessments | Read-only count in `RequirementsScreen` ("N assessments recorded"), no detail/submission UI | `GET /api/academics/evaluation-submissions/` (`InstitutionalRepository.kt:96`) | Yes (summary count only) | Not independently verified beyond the read | UI ONLY |
| Research | Read-only status line in `RequirementsScreen` (`data.research?.value("status")`) | `GET /api/my/research/` (`InstitutionalRepository.kt:97`) | Yes (summary only) | Not independently verified beyond the read | UI ONLY |
| Workshops | Read-only count in `RequirementsScreen` ("N completions recorded") | `GET /api/my/workshops/` (`InstitutionalRepository.kt:98`) | Yes (summary only) | Not independently verified beyond the read | UI ONLY |

## Reconciliation with SPRINT_STATE.md

SPRINT_STATE.md's claims ("Implemented Android Home training card, Training rotation history/
detail, Logbook draft/edit/submit, and Requirements summaries") are **accurate as stated** — note
the word "summaries," which matches the read-only, count/status-only implementation found for
Assessments/Research/Workshops. SPRINT_STATE.md does not claim full Assessments/Research/Workshops
CRUD, and none exists in source. No contradiction found.

## BUILD NOW vs WAIT FOR API/DOMAIN

- **Shippable now / already built**: Authentication, Home, Profile, Training, Rotations,
  Supervision, Logbook. Documents is functionally complete except the final live-upload success
  path, which only needs a staging resident run, not new code.
- **Wait for domain decision, not blocked by API**: Assessments, Research, Workshops already have
  working read-only summaries; building full submission/detail screens is additive UI work against
  endpoints that already exist server-side (`evaluation-submissions`, `my/research`, `my/workshops`)
  — no backend blocker identified, this is a scope/priority call, not an API gap.
