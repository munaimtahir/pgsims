# SPRINT_STATE.md — Supervisor Android: action-capable build

## Scope

Extend the "PGR Companion" Android app's Supervisor role from read-only (view residents +
per-workflow pending counts) to action-capable: approve / reject / return-for-revision on pending
Logbook, Leave, Rotation, and Research items, directly from Android. No new backend endpoints
required — every action endpoint already existed and was already scoped to the caller's own
supervised residents. Full detail: `android/docs/SUPERVISOR_API_CAPABILITY_MATRIX.md`.

## Completed work

- `InstitutionalRepository.kt`: added 4 on-demand queue GETs (`supervisorLogbookQueue`,
  `supervisorLeaveQueue`, `supervisorRotationQueue`, `supervisorResearchQueue`, kept out of
  `InstitutionalSnapshot`/`snapshot()` deliberately) and 8 action POSTs (logbook verify/return/reject,
  leave approve/reject, rotation hod-approve/reject/returned, research supervisor-approve/return),
  following the existing `submitLogbook`/`supervisorResidentProgress` templates.
- New file `SupervisorWorkflowScreens.kt`: `SupervisorWorkflowQueueScreen` (queue list + item
  `AlertDialog` + `ReasonConfirmDialog` for reject/return), `SupervisorWorkflow` enum
  (LOGBOOK/LEAVE/ROTATION/RESEARCH) driving per-workflow endpoint/field dispatch.
- `SupervisorScreens.kt`: added `selectedWorkflow` drill-down state (same pattern as the existing
  `selectedResidentId` resident drill-down), made Home's workflow rows tappable, removed the old
  "actions not available on Android" disclaimer.
- Corrected a stale claim in `SUPERVISOR_API_CAPABILITY_MATRIX.md`: rotation reject/return DO exist
  (`/api/rotations/{id}/reject/`, `.../returned/`) — it was not approve-only as previously documented.
- Updated `docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md`: Supervisor scope section and
  M7 milestone marked superseded/fulfilled.
- Consolidated Android naming to one PGR Companion application: `android/app-companion`,
  namespace `pk.vexel.pgrcompanion`, with the former duplicate offline module and Portal naming removed.
- `./gradlew :app-companion:compileDebugKotlin` passes clean.
- Per explicit user instruction, `versionCode`/`versionName` in `app-companion/build.gradle.kts` were
  **left unchanged** (still 7 / "1.1.7") — do not bump without asking first.

## Release verification — 2026-09-10

- `./gradlew clean :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:bundleRelease
  -PpgrCompanionSigningPropertiesFile=~/.config/pgr-companion/signing/signing.properties`: **27/27
  unit tests pass, 0 lint errors, signed AAB built** (`app-companion/build/outputs/bundle/release/app-companion-release.aab`,
  ~3.3 MB). Signing cert SHA-256 `A8:58:F4:2C…0B:61:F0:10` confirmed via `keytool -printcert -jarfile`
  — matches the correct registered Play upload key per `ANDROID_RELEASE_VERIFICATION.md` (not the
  wrong `vexel-health` key).
- Verified live against production (`https://android.pgsims.alshifalab.pk/`) as `supervisor` /
  `supervisor123` (M. Tahir Bashir Malik, id 63 → real identity id 3, 7 residents): login succeeds,
  all 4 new queue endpoints return 200 and are correctly scoped (3 empty, 1 populated).
- **Found and fixed a real bug during this verification**: the logbook queue was reading
  `/api/academics/review-queue/`, whose item `id` (44) is a queue-row id, not the actual
  `logbook-entries` id (28) that `verify`/`reject`/`return_revision` require — calling those
  actions would have 404'd or acted on the wrong resource. Fixed to reuse the existing `logbook()`
  endpoint (already supervisor-scoped server-side), filtered client-side to `status == "SUBMITTED"`;
  confirmed post-fix that it now resolves to the correct `id=28`. Rebuilt and re-verified tests/lint/
  bundle after the fix.
- Not executed: a live approve/reject/return call. Per the precedent in
  `ANDROID_RELEASE_VERIFICATION.md` ("mutating one for no test value was not worth it"), the seeded
  demo data was not mutated for no test benefit — endpoint/ID correctness was confirmed via read-only
  cross-checks instead (logbook entry 28's id matches the id referenced in the old queue row's notes).
  Run one real approve/reject/return per workflow against a disposable/reseedable account before
  relying on this build for a real approval.
- No physical/emulator device verification was performed (still blocked on device access, see below).
- Dedicated `pgsims` Pixel 8 / API 36 AVD created on the laptop; the existing
  `app-companion-debug.apk` was installed and launched successfully on `emulator-5554`. The emulator
  is now available for manual UI verification.

## Pending work

1. Run one real approve/reject/return-for-revision call per workflow (Logbook, Leave, Rotation,
   Research) against reseedable demo data, then re-seed, to prove the write path end-to-end — not
   done this pass (see "Release verification" above).
2. Manually verify the new workflow screens in the running `pgsims` emulator (the app is installed
   and launched on `emulator-5554`); record the results in the Android verification docs.
3. Upload `app-companion/build/outputs/bundle/release/app-companion-release.aab` to Play Console (internal
   testing track recommended before production) — not done by this session; that's a Play Console
   action for the user.
4. Carried over from the prior sprint (Supervisor/resident demo identity linkage, now otherwise
   closed): Android emulator verification of the `resident`/`supervisor` demo-login chain is still
   ready to execute on the running `pgsims` emulator — see
   `docs/implementation/20260910_urology_institutional_demo/SUPERVISOR_RESIDENT_IDENTITY_LINKAGE.md`.

## Closure state

Android client changes for action-capable Supervisor are implemented, unit-tested, lint-clean, and
a correctly-signed release AAB has been built and endpoint-verified live against production (read
paths only). Not yet uploaded to Play Console and no real write action has been exercised end-to-end.
