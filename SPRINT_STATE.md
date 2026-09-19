# Android gap closure — current source, no release rebuild

## Scope

Close current Android parity gaps and document the complete remaining Android backlog. Keep the
existing PGR Companion release identity at `1.1.9` / versionCode `9`. Do not rebuild the release
APK/AAB or upload to Play during this sprint.

## Completed Work

- Audited `android.md`, `pendingwork.md`, `docs/implementation/20260915_android_parity_acceptance/`,
  and reconciliation evidence; older 1.1.3/1.1.7/1.1.8/1.1.10 notes are historical.
- Added repository-wide DRF pagination traversal for resident snapshot lists, admin setup lists,
  supervisor queues, notifications, templates, and academic lists.
- Added a MockWebServer regression test proving notification page 2 is fetched and merged.
- Android gate after pagination change: 39 unit tests pass, lint has 0 errors, debug assembly passes.
- Dedicated `pgsims` API 36 emulator started from the documented AVD; connected suite passes 51
  tests with 22 intentional credential-gated skips and 0 failures.
- Isolated `InboxUiTest` passes all 3 tests after fixtures were made query-aware for `page=1`.
- Synthetic process-death harness passes post-ack death, pre-ack cleanup, in-flight upload recovery,
  source failure, staging/reconciliation race, and metadata failure.
- Full categorized backlog recorded in `docs/implementation/20260920_android_gap_closure/PENDING_WORK_REGISTER.md`.

## Pending Work

1. Run authenticated emulator acceptance for resident, supervisor, notification, onboarding,
   returned-workflow, pagination, session, and recovery paths; the available suite is currently
   credential-gated and intentionally skips these tests.
2. Close any defects found in authenticated returned evaluation/leave editing, review transitions,
   notification isolation, expiry/refresh, and schema/onboarding.
3. Record physical-device testing and final release rebuild/Play upload as later release gates only.
4. Start the next sprint from the `NEXT SPRINT` section of the pending-work register; do not pull
   bulk import, backup/restore, Google Drive, FCM activation, or other deferred integrations into
   this sprint.

## Current Evidence

- Android source: `android/app-companion/src/main/java/pk/vexel/pgrcompanion/InstitutionalRepository.kt`
- Android tests: `android/app-companion/src/test/java/pk/vexel/pgrcompanion/InstitutionalRepositoryTest.kt`
- Gate: `./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleDebug`
- Emulator gate: `./gradlew :app-companion:connectedDebugAndroidTest`
- Recovery gate: `python3 scripts/verify_android_process_death.py --serial emulator-5554`

## Verdict

Implementation progress: PASS for pagination and synthetic recovery. Overall Android gap-closure
sprint: IN PROGRESS pending credentialed acceptance. Release artifact and Play upload: intentionally
not performed.

---

## Web implementation sprint — verification, navigation, approval contract — 2026-09-19

Completed: repaired the admin dashboard test contract; added admin/supervisor academic monitoring,
workload, and progress navigation; renamed the HOD-labelled rotation approval route/client contract
to `supervisor-approve`; updated affected tests/contracts/truth maps and regenerated the endpoint
inventory.

Pending: complete the remaining Update 0 identity/onboarding and HOD designation cleanup; obtain
valid isolated browser credentials for role-based E2E workflows; resolve the root-owned frontend
`.next/trace-build` build artifact blocker; run full browser verification after those blockers are
cleared.

Evidence: backend pytest 1,211 passed/9 skipped/82.13% coverage; affected frontend suites 142/142
passed; full frontend Jest 252/252 passed; typecheck and lint passed; Django check/migration check
passed; prior Playwright smoke 19/25 passed with six baseline-admin 401 blockers; direct frontend
build remains blocked by root-owned `.next/trace-build`.
