# Android mega sprint — complete mobile workflow and release closure

## Scope

Close every Android item in `pendingwork.md` and `android.md`, including the
canonical backend work it requires, VPS deployment verification, physical-device
acceptance, and the requested Play release `1.1.9` / code `9`.

Excluded by owner decision: FCM activation, Google Drive, Android backup/restore,
academic seed/demo actions, and web-only audit work. The Update 0 identity gate is
already `GO` (`docs/implementation/20260626_update_0_universal_identity_dynamic_onboarding/FINAL_VERDICT.md`).

## Completed Work

- Reconciled the mega-sprint scope with the canonical Android backlog and confirmed
  the Update 0 gate passes on `main` (`9ea8420`).
- Prior Android pagination, non-credentialed emulator, inbox UI, and synthetic
  recovery verification remain valid baseline evidence.
- Added the Android admin authoring workspace for canonical document requirements,
  supervision assignments, training records, periods, rotation/evaluation templates,
  logbook categories, and review-queue records. Repository mutations are restricted
  to a fixed canonical API allow-list and have MockWebServer coverage.
- Added pending-supervisor list/resolution, authoritative user-detail loading, and the
  missing resident-progress report/CSV contract; corrected the existing CSV label
  mismatch affecting logbook, evaluation, and workload exports.
- Added standard CSV/Excel import selection with an explicit dry-run-before-apply gate
  for canonical master, identity, supervision, and academic datasets.
- Android gate after the changes: `:app-companion:testDebugUnitTest`, `lintDebug`, and
  `assembleDebug` pass.
- `pgsims` emulator connected suite passes 51 tests with the existing 22 credential-gated
  authenticated/lifecycle tests intentionally skipped.

## Pending Work

1. Add admin edit/end/close lifecycle controls, flexible import header/mapping/presets,
   and master-data/template export surfaces.
2. Complete resident progress/report detail and cross-screen list/filter/error behavior.
3. Complete supervisor generic review queue/workload/status parity and workflow refresh behavior.
4. Certify resident leave/evaluation edit-resubmit, notifications, onboarding/session, and
   offline lifecycle paths with authenticated four-role fixtures on `pgsims`.
5. Add Android unit/instrumentation coverage for every new contract and failure path.
6. Push the verified commit, synchronize `/home/munaim/srv/apps/pgsims` through `ssh test`,
   migrate and deploy only the scoped PGSIMS services, then verify HTTPS/API routing.
7. Run physical-device accessibility/lifecycle/performance acceptance, rebuild/sign/version-verify
   `1.1.9` / code `9`, then upload and verify Play Console publication if code `9` is unused.

## Next Command

Add flexible import header detection, mapping validation, persisted presets, dry-run/apply,
and master-data/template export without enabling seed/demo actions.
