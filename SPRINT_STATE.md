# Android mega sprint — complete mobile workflow and release closure

## Scope

Close every Android item in `pendingwork.md` and `android.md`, including the
canonical backend work it requires, VPS deployment verification, physical-device
acceptance, and the requested Play release `1.1.9` / code `9`.

Excluded by owner decision: FCM activation, Google Drive, Android backup/restore,
academic seed/demo actions, and web-only audit work. The Update 0 identity gate is
already `GO` (`docs/implementation/20260626_update_0_universal_identity_dynamic_onboarding/FINAL_VERDICT.md`).

The separate three-account demonstration dataset is complete; see
`DEMO_WALKTHROUGH.md` for live IDs and pending examples. Preserve those records.

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
- Added the backend-backed flexible-import workflow: schema-driven source-column mapping,
  header detection, mapping validation, named mapping presets, and a dry-run-before-apply
  safeguard. The fixed-contract and flexible flows both remain restricted to canonical datasets.
- Added MockWebServer coverage for flexible header detection, mapping validation, and mapped
  import uploads; the Android unit suite passes after the new contract coverage.
- Added allow-listed master-data template and current-data CSV export actions in the same
  import workspace, routed through the Android share sheet without persisting institutional data.
- Pushed `d2f2646` and fast-forwarded the VPS checkout at
  `/home/munaim/srv/apps/pgsims` to that commit. Production HTTPS health returned
  `{"status":"ok","database":"ok"}`; no backend migration or service restart was required
  because this slice changes Android source only.
- Factory-reset only the dedicated `pgsims` AVD, which restarted as `emulator-5556` on Android 16.
  The fresh-device connected suite reports `OK (29 tests)`; the seven authenticated recovery tests
  remain intentionally credential-gated and skipped.
- Added canonical admin edit controls plus guarded lifecycle actions to end supervision assignments,
  close training records, and atomically change a resident's primary supervisor. The Android client
  exposes no arbitrary mutation path and has MockWebServer coverage for the new contract.
- Added a distinct debuggable `staging` Android build type (`.staging` application-id suffix) with
  an owner-overridable isolated staging base URL; it falls back to the documented HTTPS staging host.
  The staging-only Android fixture command now also provisions the final `SUPPORT_STAFF` role.
- Android gate after the changes: `:app-companion:testDebugUnitTest`, `lintDebug`, and
  `assembleDebug` pass.
- `pgsims` emulator connected suite passes 51 tests with the existing 22 credential-gated
  authenticated/lifecycle tests intentionally skipped.
- Fixed resident web onboarding: declaration acceptance is saved independently before final
  submission, and the final documents step now exposes upload/replace controls backed by the
  resident document upload API.

## Pending Work

1. Complete resident progress/report detail and cross-screen list/filter/error behavior.
2. Complete supervisor generic review queue/workload/status parity and workflow refresh behavior.
3. Add guarded staging-only synthetic fixture cleanup tooling and certify all four fixture roles.
4. Certify resident leave/evaluation edit-resubmit, notifications, onboarding/session, and
   offline lifecycle paths with authenticated four-role fixtures on `pgsims`.
5. Add Android unit/instrumentation coverage for the remaining new contract and failure paths.
6. Run physical-device accessibility/lifecycle/performance acceptance, rebuild/sign/version-verify
   `1.1.9` / code `9`, then upload and verify Play Console publication if code `9` is unused.

## Next Command

Add report detail/filter/error parity without enabling seed/demo actions; staging build and all four
fixture identities are available for the later authenticated gate.
