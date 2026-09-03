# Resident Onboarding MVP — Android Debug Build + Backend Completion

Date: 2026-09-03
Scope: full resident onboarding Android UI wired to the real canonical Django backend, plus the
backend gap-closure needed to support it. Produces a working **debug** APK — signing/Play upload
is explicitly deferred to a separate machine that holds the release keystore.

## 1. Starting state

- Android app (`android/`, package `fmu.pg.sims`, compileSdk/targetSdk 36, versionCode 1/0.1.0)
  was a foundation shell only: working Retrofit/OkHttp networking, encrypted token storage, and
  an `AuthRepository` with login/logout/refresh/health-check plumbing — but no login screen, no
  navigation graph, and no onboarding screens.
- Backend already had a mature, consolidated onboarding system (brick
  `20260821_resident_onboarding_consolidation`, 830 passing tests at the time): a dynamic
  backend-declared field registry, `/api/auth/me/` as the onboarding-state source of truth,
  `ResidentDocument`/`ResidentDocumentRequirement`, and `ResidentSupervisorAssignment` /
  `PendingSupervisorAssignment`. There was **no explicit admin approve / request-correction step**
  on the profile as a whole — only per-document review existed.

## 2. Backend changes

### 2.1 Profile-level review gate (new, additive)

`ResidentProfile` gained 5 fields (migration `users.0015_historicalresidentprofile_review_note_and_more`,
tracked by the existing `HistoricalRecords()`):

```
review_status   NOT_SUBMITTED | PENDING_REVIEW | APPROVED | CORRECTION_REQUIRED
review_note     reviewer's correction reason
submitted_at, reviewed_by, reviewed_at
```

- `POST /api/resident-onboarding/state/` (existing declaration-accept "submit" action) now
  requires `is_profile_complete` (400 otherwise), rejects resubmission once `APPROVED` (409), and
  sets `review_status = PENDING_REVIEW` on success.
- New admin-only actions on `ResidentProfileViewSet`: `POST /api/residents/<id>/approve-onboarding/`
  and `POST /api/residents/<id>/request-onboarding-correction/` (body `{"reason": "..."}`), both
  permission-checked via the existing `_is_manager` check, both logged via `ActivityLog`.
- `get_resident_onboarding_state()` and `/api/auth/me/` both surface the new fields
  (`review_status`/`onboarding_review_status` etc.). `onboarding_complete`/`allowed_next_route`
  (the *web* dashboard gate) were deliberately left unchanged — web behavior is unaffected; Android
  gates its own screens on `review_status`.

### 2.2 Real P0 found and fixed: unauthenticated media exposure

`backend/sims_project/wsgi.py`'s production branch wrapped the WSGI app with
`WhiteNoise(...).add_files(BASE_DIR / 'media', prefix='/media/')`, which would serve every file
under `MEDIA_ROOT` — resident documents, theses, workshop certificates, backup-restore uploads —
completely unauthenticated, bypassing Django's URL routing (and `ResidentDocumentViewSet`'s
permission checks) entirely. It hadn't fired in the current deployment only because the trigger
condition checked the wrong env var name (`DJANGO_DEBUG` instead of the real `DEBUG`) — a landmine,
not a false alarm. Fixed by removing the `add_files` call and correcting the env var check;
regression test at `sims_project/tests.py::WsgiMediaExposureTests`.

### 2.3 Pre-existing infra bug fixed: `pytest sims -v` was broken

`backend/sims/users/__init__.py` and `backend/sims/rotations/__init__.py` had been deleted in an
unrelated commit (`2047ebd`, 2026-08-14) prior to this work. Without them, pytest's default import
mode can't disambiguate the two same-named `tests.py` files across those app dirs, so the
documented `pytest sims -v` command failed at collection for anyone running it after that commit.
Restored both `__init__.py` files (matching the pattern already used by e.g. `sims/academics/`) —
`pytest sims -v` now works exactly as documented in `CLAUDE.md`/`AGENTS.md`.

### 2.4 Local dev-environment fix (not a code change)

`backend/media/` was owned by a stale `ubuntu:ubuntu` user in this checkout, so the (non-root)
`munaim` user couldn't create new subdirectories under it — Android's document upload failed with
`PermissionError` until `chown -R munaim:munaim backend/media/` was run. Environment-specific, not
committed (media/ is gitignored).

## 3. Android implementation

All new code under `android/app/src/main/java/fmu/pg/sims/`, following the existing manual-
singleton pattern (`ApiClient`, `AppContainer`) — no DI framework introduced.

- **Data layer**: `ApiService` completed with every onboarding/document/supervision/training
  endpoint; `OnboardingRepository`, `DocumentsRepository`, `SupervisionRepository`,
  `TrainingRepository` added alongside the existing `AuthRepository`. New models
  (`core/model/`) mirror the backend contract exactly, including a `PaginatedResponse<T>` wrapper
  discovered to be necessary: `resident-document-requirements`, `resident-training`, and
  `supervision/assignments` return DRF's default paginated envelope, while `resident-documents`
  and `supervision/options` are bare (a genuine backend inconsistency, not an Android assumption —
  confirmed against the real running server and captured in
  `SerializationContractTest`).
- **Navigation & auth**: `PgsimsNavHost` drives top-level routing entirely from
  `SessionViewModel`'s backend-derived destination (never a hardcoded Android state machine):
  Login → (must-change-password) → Onboarding (`NOT_SUBMITTED`) → Pending Review
  (`PENDING_REVIEW`) → Correction Required (`CORRECTION_REQUIRED`) → Home (`APPROVED`).
- **Onboarding flow**: Welcome → Personal Information → Training/Enrollment → Supervisor →
  Documents → Review & Submit, all Compose/Material 3, field set and requiredness driven by the
  backend's `sections`/`fields` payload (not hardcoded).
- **Supervisor**: search reuses `/api/supervision/options/` with client-side text filtering
  (no backend name-search param exists — added nothing new). **Contract nuance discovered during
  implementation**: `POST /api/supervision/assignments/` (creating a `ResidentSupervisorAssignment`
  directly) is restricted to ADMIN by `IsSupervisionAdminOrReadOnly` — a resident cannot self-link
  even to an existing, listed supervisor. Both "select existing supervisor" and "supervisor not
  listed" therefore converge on the same `PendingSupervisorAssignment` request-for-admin-resolution
  endpoint; picking an existing supervisor just pre-fills real name/department instead of free
  text. No fake `SupervisorProfile` is ever created client-side either way — verified live (see §4).
- **Documents**: system document picker (`ActivityResultContracts.OpenDocument`, `image/*` +
  `application/pdf`, no broad storage permission), upload/defer via the real endpoints, deferred
  documents stay outstanding (server-derived, never locally marked done).
- **Review/Submit/Correction**: submit calls the real backend transition; Correction Required shows
  `review_note` and routes back into onboarding for a fix-and-resubmit loop; Approved routes to a
  4-tab Home (Home/Training/Documents/Profile) whose outstanding-document banner is re-derived from
  the server on every load — never cached as dismissed.
- Fixed a small pre-existing contract bug while wiring login: `LoginResponse.role` doesn't exist
  at top level (the backend nests `role` under `user`), so `AuthRepository` was silently never
  persisting the user's role to `TokenStorage`. Fixed to read `user.role`.

## 4. Verification

### 4.1 Environment constraint

The Android emulator (`Sprint24_API_36`, x86_64) **cannot boot in this sandbox** — no `/dev/kvm`
and no CPU virtualization extensions exposed to the VM (confirmed: `ls /dev/kvm` → no such file;
`grep vmx /proc/cpuinfo` → empty). This is a genuine host-level limitation, not fixable from inside
the session. Substituted with the highest-value verification actually available:

### 4.2 Live API contract verification (real backend, real test accounts)

Using a fresh resident (`pgr002`, created via the canonical `create_user_with_profile`, never a
direct `User` row) and a fresh admin (`admin001`), the **complete lifecycle was driven end-to-end
via the real running Django dev server**:

```
PATCH  /api/auth/onboarding/ (bulk fields)        → profile_complete: True
POST   /api/resident-documents/1/upload/          → status PENDING_REVIEW (after fixing §2.4)
POST   /api/resident-onboarding/state/ (submit)   → review_status PENDING_REVIEW
POST   /api/residents/4/request-onboarding-correction/ (admin) → CORRECTION_REQUIRED
GET    /api/auth/me/ (resident)                   → sees review_note verbatim
PATCH  /api/auth/onboarding/ (fix field)
POST   /api/resident-onboarding/state/ (resubmit) → review_status PENDING_REVIEW
POST   /api/residents/4/approve-onboarding/ (admin) → review_status APPROVED
GET    /api/auth/me/ (resident)                   → review_status APPROVED
```

Negative/security paths also verified live:
- Resident self-approval → **403**
- Cross-resident approval (`pgr001` approving `pgr002`) → **403**
- Cross-resident document access (`pgr001` fetching `pgr002`'s document) → **404**
- Unauthenticated document access → **401**
- "Supervisor not listed" request → `PendingSupervisorAssignment` created with `status=PENDING`,
  `resolved_supervisor=None` — confirmed **zero** `SupervisorProfile` rows were created as a side
  effect (no fake supervisor).

This directly exercises every endpoint Android calls, using the exact payload shapes Android sends.

### 4.3 JVM-level serialization contract tests (substitute for on-device network testing)

`android/app/src/test/java/fmu/pg/sims/core/model/SerializationContractTest.kt` — 8 tests, each
deserializing **JSON captured verbatim from the real backend above** through the actual Kotlin
model classes (not synthetic fixtures). Catches exactly the class of bug that would otherwise only
surface at runtime on a device: confirmed the `PaginatedResponse` split, the `LoginResponse.role`
nesting bug, and that `isLenient = true` correctly coerces a raw JSON number (`hospitals[].id`)
into `OptionItem.id: String`. **8/8 passed.**

### 4.4 Automated suites

```
Backend:  manage.py check                        PASS (0 issues)
          manage.py makemigrations --check        PASS (no changes detected)
          pytest sims -v (plain, as documented)   1187 passed, 8 skipped, 0 failed (84.16% cov)
Web:      npm run typecheck                       PASS
          npm run lint                             PASS (no warnings/errors)
          npm test                                 PASS (38 suites, 114 tests)
          npm run build                            PASS
Android:  ./gradlew compileDebugKotlin             PASS
          ./gradlew testDebugUnitTest              PASS (8/8, SerializationContractTest)
          ./gradlew lintDebug                      PASS (0 errors, 66 pre-existing warnings)
          ./gradlew assembleDebug                  PASS
```

### 4.5 Not verified in this pass (explicit)

- On-device/emulator UI flow (login tap-through, screen rendering, Compose UI tests,
  instrumentation tests) — blocked by the KVM/emulator limitation above. The debug APK installs
  cleanly per `assembleDebug`'s packaging step but has not been launched on a real device or
  working emulator.
- Signed release AAB, bundletool validation, Play Console upload — explicitly out of scope for this
  pass; the machine with keystore access will do this after pulling this branch.

## 5. Release identity (debug)

```
Application:     FMU Postgraduate Residency Portal
Package:         fmu.pg.sims.debug (debug suffix; release remains fmu.pg.sims)
Version code:    2
Version name:    0.2.0
Target/Compile SDK: 36
APK:             android/app/build/outputs/apk/debug/app-debug.apk
SHA-256:         7a8a7d53070a90a5ebd5f1769477b00969cb02d8664191af5a2ad564959f4e87
Signing:         debug keystore only — no release signing in this pass
```

## 6. Known limitations / deferred scope

- On-device UI verification pending a working emulator or physical device (next machine).
- Minimal supervisor mobile view, push notifications: not attempted — resident onboarding was the
  gate per the approved plan, and these are explicitly deferred, not silently dropped.
- `/api/supervision/options/` returns both `residents` and `supervisors`; Android only consumes
  `supervisors`. Narrowing that endpoint's response for resident callers would be a minor backend
  cleanup, not a security issue (already `IsAuthenticated`-scoped) — flagged, not fixed, to keep
  this pass additive.
- Web `docs/contracts/API_CONTRACT.md` and `DATA_MODEL.md` were found to already be stale
  (pre-clean-room role model) independent of this work; not touched, to avoid conflating an
  unrelated docs debt with this change.

## 7. Verdict

Backend, web, and Android automated gates are green; the full resident-onboarding lifecycle
(submit → correction → resubmit → approve) and its authorization boundaries are verified live
against the real backend. The debug APK is built, checksummed, and ready to hand off to the
machine with keystore access for signed release build, on-device verification, and Play upload —
it is **not** itself Play-upload-ready (no signing, no on-device run performed here).
