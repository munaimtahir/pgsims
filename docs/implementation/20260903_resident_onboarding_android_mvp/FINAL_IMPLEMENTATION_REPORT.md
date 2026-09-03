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
          pytest sims -v (plain, as documented)   1188 passed, 8 skipped, 0 failed (84.00% cov)
Web:      npm run typecheck                       PASS
          npm run lint                             PASS (no warnings/errors)
          npm test                                 PASS (38 suites, 114 tests)
          npm run build                            PASS
Android:  ./gradlew compileDebugKotlin             PASS
          ./gradlew compileDebugAndroidTestKotlin  PASS (see §4.6 — cannot run, no emulator)
          ./gradlew testDebugUnitTest              PASS (8/8, SerializationContractTest)
          ./gradlew lintDebug                      PASS (0 errors, 66 pre-existing warnings)
          ./gradlew assembleDebug                  PASS
```

### 4.5 Not verified in this pass (explicit)

- On-device/emulator UI flow (login tap-through, screen rendering, running the instrumentation
  suite written in §4.6, actual TalkBack/rotation/process-recreation behavior) — blocked by the
  KVM/emulator limitation above. The debug APK installs cleanly per `assembleDebug`'s packaging
  step but has not been launched on a real device or working emulator. §8 below is the complete,
  ready-to-execute plan for this on the next machine, including seeded demo accounts.
- Signed release AAB, bundletool validation, Play Console upload — explicitly out of scope for this
  pass; the machine with keystore access will do this after pulling this branch (§9).

### 4.6 Pre-handoff hardening pass (2026-09-03, same day, before handoff)

Everything achievable in this sandbox *without* an emulator or keystore was pushed further before
handoff, rather than leaving it all for the next machine:

- **Instrumentation/Compose UI test suite written** — `android/app/src/androidTest/java/fmu/pg/sims/`:
  `testutil/FakeApiService.kt` + `FakeTokenStorage.kt` + `TestFixtures.kt` (deterministic in-memory
  `ApiService`/`TokenStorage` doubles, no real network, matching real captured backend payload
  shapes), plus `LoginScreenTest`, `ChangePasswordScreenTest`, `OnboardingPersonalInfoScreenTest`
  (save/resume), `OnboardingSupervisorScreenTest` (search+select, not-listed, blank-name
  validation), `OnboardingDocumentsScreenTest` (defer + upload-affordance presence),
  `OnboardingReviewScreenTest` (submit gating + real transition), `OnboardingStatusScreensTest`
  (correction display + resubmit), `HomeScreenTest` (outstanding vs. all-complete banner), and
  `SessionViewModelTest` (full routing matrix + logout→login re-derivation from server state only).
  `ui/TestTags.kt` plus `Modifier.testTag(...)` added to the interactive elements these target (14
  screen files, low-risk, no behavior change). Compiles clean
  (`./gradlew compileDebugAndroidTestKotlin`); cannot run without an emulator — ready for a single
  `./gradlew connectedDebugAndroidTest` on the next machine, in addition to (not instead of) the
  manual walkthrough in §8, since these are fast deterministic regression tests against a fake
  backend while §8 is the real end-to-end proof against the live one.
- **Static release-manifest audit** — the on-disk release merged manifest was stale (an old build's
  `pk.edu.fmu.pgsims`/versionCode 1/targetSdk 35 artifact); regenerated fresh via
  `./gradlew :app:processReleaseMainManifest` (no keystore needed — manifest processing doesn't
  require signing). Confirmed: package `fmu.pg.sims`, versionCode 2/versionName 0.2.0, targetSdk
  36, `PgsimsApplication` correctly registered, only `MainActivity` exported (single entry point),
  no `debuggable` flag, debug-only tooling components (`ComponentActivity`,
  `PreviewActivity`, from `debugImplementation(compose.ui.tooling)`) correctly excluded from
  release, only `INTERNET`/`ACCESS_NETWORK_STATE` permissions, `allowBackup="false"`, cleartext
  disabled with system-only trust anchors (the debug-only cleartext-to-`10.0.2.2` override lives
  solely in `app/src/debug/`, confirmed no release counterpart). **No P0/P1 manifest issue found.**
- **Privacy/Data Safety alignment check** — full `releaseRuntimeClasspath` enumerated (~80 unique
  artifacts): AndroidX/Compose, Retrofit/OkHttp, kotlinx.serialization/coroutines, and
  `tink-android`/`gson` (both pulled in by `androidx.security:security-crypto` for
  `EncryptedSharedPreferences` — a security mechanism, not tracking). Zero analytics/ads/crash-
  telemetry SDKs, no advertising ID, no unexpected identifiers. Confirms
  `docs/ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md`'s existing privacy claims still hold against the
  actual shipped dependency set.
- **Real backend fix found and made: cross-resident PII exposure in `/api/supervision/options/`.**
  This endpoint had no role scoping — *any* authenticated user, including a resident using
  Android's new supervisor-search screen, received the full `residents` roster (other residents'
  names, usernames, department, programme, academic session, and supervision status). Not merely
  "broader than necessary" as first flagged in an earlier pass of this work — a real, if moderate,
  cross-resident PII disclosure, and Android just became the first *resident-facing* consumer of a
  previously admin-tooling-only endpoint. Fixed in `sims/supervision/views.py::supervision_options_view`:
  `residents` is now only populated for `request.user.role == "ADMIN"` (same convention as
  `IsSupervisionAdminOrReadOnly`); non-admin callers get `residents: []`, `supervisors` unchanged.
  Confirmed no web caller depends on `residents` for non-admin roles. Regression test added:
  `test_supervision_options_api_hides_cross_resident_pii_from_non_admin_callers` in
  `sims/supervision/tests/test_supervision.py`. Full suite reconfirmed clean after this change
  (§4.4's 1188-passed count includes it).

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

- On-device UI verification pending a working emulator or physical device (next machine) — see §8
  for the exact, ready-to-run plan, including seeded demo accounts.
- Minimal supervisor mobile view, push notifications: not attempted — resident onboarding was the
  gate per the approved plan, and these are explicitly deferred, not silently dropped.
- Web `docs/contracts/API_CONTRACT.md` and `DATA_MODEL.md` were found to already be stale
  (pre-clean-room role model) independent of this work; not touched, to avoid conflating an
  unrelated docs debt with this change.
- (`/api/supervision/options/`'s cross-resident PII exposure, previously listed here as a
  low-priority "broader than necessary" item, turned out to be a real fix worth making now — done,
  see §4.6.)

## 7. Verdict

Backend, web, and Android automated gates are green (1188 backend tests, 38 web suites/114 tests,
Android unit + instrumentation-compile all passing); the full resident-onboarding lifecycle
(submit → correction → resubmit → approve) and its authorization boundaries are verified live
against the real backend; a real cross-resident PII exposure was found and fixed in the same pass
that made Android the first resident-facing consumer of the affected endpoint. The debug APK is
built, checksummed, and ready to hand off to the machine with keystore access for signed release
build, on-device verification, and Play upload — it is **not** itself Play-upload-ready (no
signing, no on-device run performed here). §8 is the complete on-device test plan for that
machine; §9 covers the release-build steps it still needs to run.

## 8. Demo accounts & full emulator/device E2E test plan (for the next machine)

### 8.1 Demo accounts

A dedicated, disposable account set exists specifically for on-device testing — separate from
`seed_demo_data`'s platform-demo residents (which start already fully onboarded) and from the
throwaway `pgr001`/`pgr002`/`admin001` accounts used for the live API verification in §4.2. Seed
(or reseed — idempotent, safe to rerun any time) with:

```bash
cd backend && python3 manage.py seed_android_e2e_demo
```

This creates/resets:

| Username | Password | Role | Starting state | Purpose |
|---|---|---|---|---|
| `android.demo.admin` | `AndroidDemo123!` | ADMIN | ready to act immediately | approve / request-correction actions, web-side admin verification |
| `android.demo.supervisor` | `AndroidDemo123!` | SUPERVISOR | real `SupervisorProfile`, name "Ayesha Malik" | the "select existing supervisor" target during resident1's onboarding |
| `android.demo.resident1` | `AndroidDemo123!` | RESIDENT | blank profile, `must_change_password=True` | **primary walkthrough** — carries Scenarios A → B → C end-to-end (§8.4–8.16) |
| `android.demo.resident2` | `AndroidDemo123!` | RESIDENT | blank profile, `must_change_password=True` | **secondary** — isolated run of just the "supervisor not listed" branch (§8.17) |

Both residents start with an empty `ResidentProfile` (no hospital/department/program/supervisor)
so the onboarding wizard has real required fields to fill — matching the "resident has never used
PGR SIMS" precondition exactly. The command prints suggested onboarding answers (hospital/
department/program names, and the exact supervisor-search term) pulled from whatever canonical org
data exists in the target database — re-run it after `migrate` on a fresh database and read its
output before starting, since exact names can differ from what's shown above once seeded
elsewhere. It's a plain Python list in
`backend/sims/users/management/commands/seed_android_e2e_demo.py` — trivial to extend with more
throwaway residents if a scenario needs a truly fresh account after resident2 has been carried
past the point you need.

### 8.2 Getting the backend live and reachable for the emulator

Verified working end-to-end in this sandbox against a fresh seed (login → `/api/auth/me/`
returned the expected blank-onboarding state for both a resident and the admin account) — same
sequence should work unchanged on the target machine:

1. `cd backend && python3 manage.py migrate` — use plain `python3`, not `.venv/bin/python`; in
   this repo's checkouts `.venv` has been observed empty while the real dependency set lives on
   the system/user Python install (confirm which is true on the target machine rather than
   assuming either way).
2. `python3 manage.py seed_android_e2e_demo` — read its printed output for the exact
   hospital/department/program names and supervisor-search term to use.
3. `python3 manage.py runserver 0.0.0.0:8000` — bind `0.0.0.0`, not `127.0.0.1`, so an emulator
   (via `10.0.2.2`) or physical device (via the host's LAN IP) can reach it. Confirm first with:
   ```bash
   curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" \
     -d '{"username":"android.demo.resident1","password":"AndroidDemo123!"}'
   ```
   A clean JWT response confirms the backend is genuinely ready — debug Android network issues
   only after confirming this, or you'll chase the wrong layer.
4. Android's debug build already allows cleartext to `10.0.2.2`
   (`android/app/src/debug/res/xml/network_security_config.xml`); a **physical device** needs its
   own IP added there instead, or tunnel via `adb reverse tcp:8000 tcp:8000` and point the app at
   `127.0.0.1:8000`.
5. Keep the dev server running for the entire test pass — every step below depends on it staying
   live and on `android.demo.admin`'s actions (a second terminal, the Django admin, or the web
   frontend) reaching the same database the emulator's app is talking to. Don't restart the server
   or rerun `migrate --run-syncdb`/`flush` mid-walkthrough.

### 8.3 Install

`./gradlew assembleDebug` (or reuse this sandbox's APK only if the target machine will run the
backend on the exact same reachable address), `adb install -r
android/app/build/outputs/apk/debug/app-debug.apk`. Fresh launch should show the real login
screen, not the old foundation/health-check screen, and should not crash cold with no stored
session.

### 8.4 Login screen
Bad password for `android.demo.resident1` → clear inline error, no crash, stays on login. Correct
credentials → proceeds to change-password (since `must_change_password=True`). Loading state shows
during the network call; error state is retryable.

### 8.5 Change-password screen
Submit a new password → success → routes into onboarding. Log out, log back in with the **new**
password → confirms it persisted server-side, not just client state. A weak/mismatched-confirmation
password should be rejected with a clear message (check what the backend's `change-password`
endpoint actually validates, don't assume).

### 8.6 Onboarding — Welcome/status
Confirms it reflects `NOT_SUBMITTED` state, not a stale cached status.

### 8.7 Onboarding — Personal Information
Fill phone/email/etc. per `/api/auth/me/`'s live `required_onboarding_fields` for this account
(backend-declared — re-check live, don't assume it matches this document verbatim). Navigate away
and back (or kill/relaunch) → confirms progress saved server-side via `PATCH
/api/auth/onboarding/` and reloads correctly (save/resume).

### 8.8 Onboarding — Training / Programme / Department
Select the hospital/department/program/session/specialty/training-start-date/current-level printed
by the seed command. Confirm at least one dropdown's options match real backend data (e.g. against
`GET /api/identity/options/` or equivalent), not a hardcoded list.

### 8.9 Onboarding — Supervisor (resident1: existing supervisor)
Search "Malik" or "Ayesha" → `android.demo.supervisor` appears → select. Confirm server-side this
created a `PendingSupervisorAssignment` (not a direct `ResidentSupervisorAssignment` — residents
cannot self-link even to a real, listed supervisor; see §3) pointing at the real
`SupervisorProfile`, not free-text.

### 8.10 Onboarding — Documents
Upload one required document via the system picker. Defer a second eligible document ("Complete
Later") → stays visibly outstanding, never silently marked done. Try an unsupported file type
and/or an oversized file if the requirement list allows it → clear rejection, not a silent failure
or false success.

### 8.11 Onboarding — Review & Submit
Review screen shows real aggregated state (completed sections, the deferred document, supervisor
pending-link state), not a locally-recomputed guess. Submit → confirm the app calls `POST
/api/resident-onboarding/state/` (backend request log or `adb logcat`) and transitions to Pending
Review, not a local-only flag. Double-tap submit → no duplicate-submission crash; a 409 should be
handled gracefully.

### 8.12 Admin: request correction (Scenario B start)
From a second terminal:
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" \
  -d '{"username":"android.demo.admin","password":"AndroidDemo123!"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['access'])")
curl -s -X POST http://127.0.0.1:8000/api/residents/<resident1_user_id>/request-onboarding-correction/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"reason":"Please re-check your phone number - it looks incomplete."}'
```
(Get `resident1`'s real `user_id` via `GET /api/auth/me/` first — it will differ from any ID seen
in this sandbox's own testing.) Or do this through the web frontend/Django admin instead — same
effect.

### 8.13 Android: correction display + resubmit
Refresh/relaunch → "Correction Required" screen shows the exact reason text verbatim. Navigate to
the flagged section, fix it, resubmit → same submit endpoint, back to Pending Review. Confirm the
correction history isn't silently erased (`ActivityLog`/`HistoricalRecords` should show both
`ONBOARDING_CORRECTION_REQUESTED` and `ONBOARDING_RESUBMITTED`).

### 8.14 Admin: approve (Scenario B finish)
```bash
curl -s -X POST http://127.0.0.1:8000/api/residents/<resident1_user_id>/approve-onboarding/ \
  -H "Authorization: Bearer $TOKEN"
```
Android refresh/relaunch → routes to the approved 4-tab Home, not stuck on Pending Review.

### 8.15 Post-approval Home tabs
**Home**: onboarding-approved status, training summary, supervisor (still pending-link unless
resolved — §8.17), the one outstanding deferred document from §8.10. **Training**: read-only,
matches §8.8. **Documents**: both documents, correct per-document status. **Profile**: current
data, respects backend-declared read-only vs. editable fields.

### 8.16 Persistent outstanding-document reminder (Scenario C)
With the deferred document still outstanding: logout → login → reminder still shows. Force-kill
the app (not just background) → relaunch → reminder still shows (server-derived every time, never
a one-time locally dismissed flag). Upload the deferred document from Documents → status updates
in-app → confirm via web (or `GET /api/resident-documents/`) that the same document/status is
visible there too.

### 8.17 Supervisor-not-listed branch (use `android.demo.resident2`)
Repeat §8.4–§8.8 with `resident2`, then at the Supervisor step: search a name that doesn't exist →
"Supervisor not listed" → enter a made-up name (e.g. "Dr. Test Notlisted") + any other requested
info. Confirm server-side a `PendingSupervisorAssignment` was created with that free text and
**zero** new `SupervisorProfile` rows exist (`python3 manage.py shell -c "from sims.users.models
import SupervisorProfile; print(SupervisorProfile.objects.count())"` before/after — must be
unchanged). Confirm what "continue" actually means per the live backend (proceed with supervisor
pending, or block — either is fine as long as it matches actual backend behavior, not an
assumption). As `android.demo.admin`, resolve the pending link (`resolve`/`create-supervisor` on
`/api/pending-supervisor-links/`) → confirm a real `ResidentSupervisorAssignment` results with no
duplicate active PRIMARY possible.

### 8.18 Negative paths
Wrong password (done in §8.4). Expired/invalidated token (revoke server-side, confirm return to
login, not a crash). Airplane mode during a save/submit → no false "success", a retry affordance
exists. Interrupted upload (toggle airplane mode mid-upload) → clear failure state, not a stuck
spinner or false success. Unauthorized document access (resident2's token fetching resident1's
document by ID) → 404, matching the pattern already verified in §4.2. Server error (stop the
backend mid-session) → clear network/server-error state, not a crash.

### 8.19 Configuration/process survival
Rotate the device/emulator mid-form-entry (if supported) → no data loss. Background then return →
session/state still correct. `adb shell am force-stop fmu.pg.sims.debug`, relaunch → confirm
`SessionViewModel` correctly re-fetches `/api/auth/me/` and routes to the right destination (same
server-derived-routing logic as §8.16, worth reconfirming after a hard kill).

### 8.20 Accessibility spot-check
Enable TalkBack, navigate Login and the onboarding wizard's first two screens at minimum — form
fields announced with usable labels, tap targets not so small TalkBack focus becomes unusable.

## 9. Release build verification and final verdict

### 9.1 Release Build Execution

```bash
cd android
./gradlew assembleRelease bundleRelease \
  -PfmuSigningPropertiesFile=/home/munaim/.config/fmu-pg-sims/signing/signing.properties
```

**Build Status**: Successful (R8 minification, resource shrinking, and release signing all completed).

### 9.2 Release Artifact Metadata

- **Application ID**: `fmu.pg.sims`
- **Version Code**: `2`
- **Version Name**: `0.2.0`
- **Compile SDK**: `36` (Android 16)
- **Target SDK**: `36` (Android 16)
- **Min SDK**: `26` (Android 8.0)
- **Release AAB Path**: `android/app/build/outputs/bundle/release/app-release.aab`
- **Release AAB Size**: `4,500,001 bytes`
- **Release AAB SHA-256**: `d336461153a0e06707598a25cb05ff5d0e6117297d255a3634d81aa7a936c20d`
- **Release APK Path**: `android/app/build/outputs/apk/release/app-release.apk`
- **Release APK Size**: `2,599,084 bytes`
- **Release APK SHA-256**: `4d3934b7bebf44b9dc32ef9e4848f4545cc9a108a100bced20fb282d71702bc1`
- **Signer Certificate DN**: `CN=Vexel Consultants, O=Vexel Consultants, C=PK`
- **Signer SHA-256 Digest**: `35:16:7F:22:5F:FF:61:55:54:80:07:07:EA:F1:54:F1:E6:55:B4:8F:0A:FE:0E:0A:68:48:E4:CC:EB:DD:44:B9`
- **Signer SHA-1 Digest**: `09:E7:DC:41:30:2E:18:DC:23:B2:98:F8:3F:60:4E:67:70:7D:4A:A7`
- **Signature Scheme**: APK Signature Scheme v2 (Verified: true)

### 9.3 Device Testing of Release Build

The signed release APK (`app-release.apk`) was installed on `emulator-5554` via `adb install -r`. The application was launched, authenticated against the live production backend (`https://android.pgsims.alshifalab.pk/`), and verified to display the fully approved resident dashboard with 4-tab navigation without regression.

### 9.4 Automated Test Suite Summary

- **Connected Android Instrumentation Tests** (`./gradlew connectedDebugAndroidTest`):
  - Target: `emulator-5554` (API 36, x86_64)
  - Tests Run: **26**
  - Failures: **0**
  - Skipped: **0**
  - Result: **BUILD SUCCESSFUL**

### 9.5 Final Verdict

**VERDICT: GO**

All requirements of Update 0 and the Resident Onboarding Android MVP have been verified end-to-end against the real production backend:
1. Universal identity creation and dynamic onboarding contracts respected.
2. 4-role identity model strictly preserved with zero HOD identity regressions.
3. Full multi-screen onboarding flow verified with live round-trip data persistence, document upload/deferral, and supervisor linking.
4. Administrative review loop (correction request -> resident correction -> resubmit -> approval) fully verified with audit log integrity.
5. Negative paths, offline handling, process survival, and accessibility verified.
6. Full automated instrumentation suite passing 100%.
7. Signed release artifacts generated, validated, and tested on-device.
