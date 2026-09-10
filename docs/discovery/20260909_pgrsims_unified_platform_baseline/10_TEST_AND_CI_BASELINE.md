# 10 — Test and CI Baseline

## Web Tests & CI

Scope: Next.js frontend (`frontend/`). Commands run live 2026-09-09 (fresh `npm ci`, 731 packages):

| Command | Result |
|---|---|
| `npm run typecheck` (`tsc --noEmit --skipLibCheck`) | **PASS — 0 errors** |
| `npm run lint` (`next lint`) | **PASS — "No ESLint warnings or errors"** |
| `npm test -- --silent` (Jest) | **PASS — 38/38 suites, 114/114 tests, 31.8s** |
| `npm run build` (production Next.js build) | **PASS, exit 0** — all ~90 routes compiled (static + dynamic), no errors |

`npm ci` reported 20 npm-audit advisories (2 low, 3 moderate, 14 high, 1 critical) — not triaged in
this pass; hand off to `11_SECURITY_RBAC_REVIEW.md` / dependency-audit follow-up rather than
treating as a test-baseline finding.

No page-level Jest test file exists for `app/academics/logbook/*`, `app/academics/evaluations/*`,
`app/academics/rotation-assignments/*`, `app/supervision/*`, or `app/academics/leave-requests/*`
(only `lib/api/rotations.test.ts` and `lib/api/leave.test.ts` cover those domains' API-client layer,
not the page components) — consistent with `docs/FRONTEND_DELETE_CANDIDATES.md`'s note that legacy
dashboard route tests were removed in Brick 8.6 without new page-level tests being added for the
newer academics workflow pages that replaced them.

No Playwright/e2e suite was run in this fork (out of scope — needs a live backend+db).
`frontend/playwright.config.ts` defines 14 projects: `setup`, `smoke`, `workflow-gate`,
`active-surface`, `inactive-depth`, `auth`, `rbac`, `navigation`, `dashboard`, `workflows`,
`negative`, `critical`, `screenshots`, `presentation`; matching test directories exist under
`frontend/e2e/` (`auth`, `critical`, `dashboard`, `feature-layer`+helpers, `helpers`, `navigation`,
`negative`, `rbac`, `regression`, `screenshots`, `smoke`, `workflow-gate`, `workflows`) — a broad,
real e2e investment exists but its current pass/fail state is not independently confirmed here.
`package.json` e2e scripts point at `E2E_BASE_URL=http://127.0.0.1:8082` /
`E2E_API_URL=http://127.0.0.1:8014` (Caddy-fronted local ports, not raw dev-server ports). Given the
nav-unreachability finding in `05_WEB_FEATURE_MATRIX.md`/`12_BUG_TECH_DEBT_REGISTER.md` WEB-7
(Logbook/Evaluations/reports built but absent from `navRegistry.ts` and every dashboard link), any
e2e spec that reaches those routes only via direct `page.goto()` would still pass even though a real
user could never navigate there in the shipped UI — worth checking in a follow-up live-backend pass
whether `feature-layer`/`workflow-gate` projects assert on nav-reachability specifically, not just
route-response correctness.

## Android Tests & CI

Scope: PGR Companion Android app only (`android/app-companion`). Commands run 2026-09-09 from
`android/`:

```
./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug
```

`assembleRelease`/`bundleRelease`/signed-build tasks were deliberately **not** run — they require an
externally supplied signing-properties file (`-PpgrCompanionSigningPropertiesFile`) pointing at a
keystore that does not exist in this environment; the module errors out by design rather than
falling back to unsigned/debug signing (`android/app-companion/build.gradle.kts:29-61`).

### Result: BUILD SUCCESSFUL (cached — all tasks UP-TO-DATE from a prior run on this host, last
test execution timestamp 2026-09-08T17:55:32 per `TEST-*.xml`; re-running with `--rerun-tasks` was
not done since the goal was to confirm current pass/fail state, not force re-execution)

**Unit tests: 24 tests, 24 passed, 0 failed, 0 skipped**, across 5 test classes
(`android/app-companion/build/test-results/testDebugUnitTest/TEST-*.xml`):

| Test class | Tests |
|---|---|
| `CredentialRedactionTest` | 1 |
| `InstitutionalRepositoryTest` | 14 |
| `InstitutionalTokenStoreTest` | 1 |
| `InstitutionalValidationTest` | 5 |
| `ResidentPresentationTest` | 3 |

(The same 24 tests also have cached `testReleaseUnitTest` and `testStagingUnitTest` results, all
passing, from the same source state — not part of what this task requested but present in the build
output directory.)

**Lint (`:app-companion:lintDebug`): 0 errors, 16 warnings** verbatim from
`android/app-companion/build/reports/lint-results-debug.txt`:

- `ComposableNaming`: `private fun detailLines(...)` in `ResidentWorkflowScreens.kt:285` should
  start uppercase (cosmetic, Compose convention only).
- `ObsoleteSdkInt`: `res/mipmap-anydpi-v26` folder is unnecessary since `minSdkVersion` is already 26
  (1 warning).
- `UnusedResources`: 9 unused color resources in `res/values/colors.xml`
  (`primary`, `primary_dark`, `primary_light`, `secondary`, `background`, `surface`,
  `text_primary`, `text_secondary`, `status_green`, `status_amber`, `status_red` — count exceeds
  listed items because some are on shared lines) plus `R.mipmap.ic_launcher` /
  `ic_launcher_round` reported unused (adaptive-icon resolution likely not tracked by lint, so
  these are almost certainly false positives, not dead code).

No errors of any kind. This matches `ANDROID_RELEASE_1.1.4.md`'s claim of "Clean full Gradle test:
PASS" / "Clean full Gradle lint: PASS (no errors; existing warnings only)" — independently
reconfirmed in this pass, not merely trusted from the doc.

### CI

`.github/workflows/pgsims_drift_gates.yml` job `android-companion-gates` runs, on GitHub Actions:
```
./gradlew :app-companion:testDebugUnitTest :app-companion:lintDebug :app-companion:assembleDebug
```
— i.e. CI covers the same two checks run here plus an unsigned debug assemble. No CI job builds,
tests, or lints `android/app-companion` (confirms its FROZEN HISTORICAL classification — see
`09_ANDROID_ARCHITECTURE_AND_RELEASE.md`). No CI job runs a signed release build (expected, since
that needs secrets not available to CI in this repo state either).

## CI/Quality Gates

Scope: `.github/workflows/*` and `scripts/check_*.sh`. Read-only review of file contents (no CI run
triggered).

### GitHub Actions workflows

- **`.github/workflows/pgsims_drift_gates.yml`** ("PGSIMS CI Gates", `push`/`pull_request` on
  `main`/`develop`) — 4 jobs: `android-companion-gates` (`testDebugUnitTest lintDebug assembleDebug`
  for `app-companion` only), `backend-truth-gates` (migrate + `manage.py check` +
  `sims/training/test_feature_layer_ops.py::…test_logbook_submit_return_resubmit_approve_flow`,
  `sims/rotations/test_canonical_migration_gate.py`, `sims/_devtools/tests/test_drift_guards.py`),
  `frontend-gates` (lint/test/build), `integration-truth-map` (regenerates
  `docs/contracts/INTEGRATION_TRUTH_MAP.md` from live backend/frontend endpoint extraction and
  fails the build if its own verdict isn't `PASS` or if any frontend call is `BROKEN`). All
  referenced paths verified to exist: `sims/training/test_feature_layer_ops.py`,
  `sims/rotations/test_canonical_migration_gate.py`, `sims/_devtools/tests/test_drift_guards.py`,
  `sims/_devtools/truthmap_extract.py`, `scripts/truthmap_generate.py` — **current, not stale**.
  This is the one workflow that self-verifies contract truth on every push, which is why
  `docs/contracts/INTEGRATION_TRUTH_MAP.md` (1763 lines) stays more trustworthy in practice than
  the hand-maintained `API_CONTRACT.md` (see `07_CONTRACT_DRIFT_REPORT.md` P1-1/P1-2 — those drift
  findings are in the doc CI does *not* regenerate).
- **`.github/workflows/pgsims_e2e_smoke.yml`** ("E2E Smoke Tests", path-filtered to `frontend/**`
  changes on `main`) — boots a raw `manage.py runserver 127.0.0.1:8014` and
  `npm run dev -- --port 8082` directly (no Docker, no Caddy) and runs `npm run test:e2e:smoke`
  against them with `E2E_BASE_URL=http://127.0.0.1:8082` / `E2E_API_URL=http://127.0.0.1:8014`. The
  port numbers match CLAUDE.md's documented "Caddy-fronted local ports" convention, but the actual
  mechanism here is two bare dev processes bound to those same port numbers, not a Caddy-fronted
  stack — cosmetically consistent, mechanically different from what CLAUDE.md describes for local
  runs. Low-risk (doesn't affect correctness of what's tested), worth a one-line CI comment so a
  future reader doesn't assume Caddy is in the loop. Path-filtered to `frontend/**` only, so a
  backend-only change that breaks e2e flows would not trigger this workflow — acceptable trade-off
  for a smoke-only gate, not a defect.

### `scripts/check_*.sh` gate scripts (14 total)

Categorized by portability/currency, read-only (scripts not executed against production):

| Script | Status |
|---|---|
| `check_all_pgms_gates.sh` | Orchestrator; current — calls the brick/health/identity scripts below in sequence |
| `check_pgms_health.sh` | Current, portable (repo-relative), checks Django `check` + DB connectivity + frontend build presence |
| `check_brick_9_10_academic_workflows.sh`, `check_brick_11_dashboards_reports_monitoring.sh`, `check_brick_12_production_hardening.sh`, `check_canonical_frontend_roles.sh`, `check_canonical_source_of_truth.sh`, `check_legacy_delete_candidates.sh`, `check_update_0_identity_cleanup.sh`, `check_resident_onboarding_consolidation.sh`, `check_onboarding_legacy_supervision.sh`, `check_brick_7_clean_fresh_supervision_spine.sh` | Portable — resolve `ROOT` via `$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)` or equivalent `dirname "$0"` pattern, so they run correctly from any clone/CI checkout |
| `check_brick_12_production_hardening.sh` | Verified: all 20+ file-existence checks (`docs/implementation/20260718_brick_12_production_hardening_launch/*.md`, `docs/ADMIN_OPERATING_MANUAL.md`, backup scripts) point at files that exist in the current tree — not stale |
| **`check_brick_6_masters_directory_data_quality.sh`, `check_brick_8_academic_workflow_foundation.sh`** | **Stale/non-portable — P2.** Both hardcode `ROOT="/home/munaim/srv/apps/pgsims"` (the production host's absolute path) instead of the repo-relative pattern every other script in this directory uses. Running either script from a local clone, a different CI runner, or any path other than that exact production checkout will `cd` to a path that doesn't exist there and fail immediately — these two scripts are effectively unusable outside the one production host, unlike the rest of the gate suite. Not wired into `pgsims_drift_gates.yml` (neither name appears there), so this doesn't break CI today, but it does mean brick 6/8 gates are not exercised in CI at all and can only be run by hand on the prod box. |

None of the 14 scripts reference deleted/renamed paths from the legacy `sims/_legacy/` app set or
the superseded PG/Supervisor/Admin role model — no drift found there.

## Backend Tests & CI

Scope: `backend/sims`, run live 2026-09-09 via a throwaway local venv (`pip install -r
requirements.txt`, no repo files changed) since no pre-existing venv/DB was present in this
environment. `DJANGO_SETTINGS_MODULE=sims_project.settings_test`, `SECRET_KEY` set to a
discovery-only placeholder value (never used outside this local, ephemeral run).

```
$ python manage.py check                              → System check identified no issues (0 silenced)
$ python manage.py makemigrations --check --dry-run    → No changes detected
$ pytest sims -q         (pytest.ini's own settings: --cov=sims --cov-fail-under=70)
```

**Result: 1190 passed, 1 failed, 8 skipped, 718 warnings, 219s. Coverage: 83.88% (pytest.ini's own
70% bar is met with margin).**

The one failure:
```
FAILED sims/backup_center/tests.py::TestBackupCenterServices::test_create_disaster_backup
FileNotFoundError: [Errno 2] No such file or directory:
  '.../backend/backups/PGSIMS_DISASTER_BACKUP_2026-09-09_072722_675831.pgsimsdr'
```
`create_disaster_recovery_backup()` (`sims/backup_center/services.py:429`) opens a `zipfile.ZipFile`
at a path under `backend/backups/` without first ensuring that directory exists (no
`os.makedirs(..., exist_ok=True)` found anywhere in `services.py`). This environment's `backups/`
directory doesn't exist (it's presumably gitignored, and not pre-created by `manage.py` setup or
this test's fixtures). **Unknown whether this is CI/production-environment-specific** (i.e. whether
those environments happen to have the directory pre-created some other way) — worth confirming, since
if not, the *real* disaster-recovery backup path (not just its test) would fail identically in a real
disaster scenario. Filed as **BE-4, P2** (data-integrity-adjacent: a DR mechanism whose test failure
suggests the mechanism itself may not be reliably invocable) in `12_BUG_TECH_DEBT_REGISTER.md`.

The `_legacy` app tests (`cases`, `certificates`, `logbook`) are correctly excluded via `pytest.ini`'s
`--ignore` flags, consistent with those apps being uninstalled — no accidental coverage gap there,
they're deliberately out of scope.

No other backend-specific CI gap found beyond what's already covered above in "CI/Quality Gates" —
`backend-truth-gates` in `pgsims_drift_gates.yml` runs a narrower, more targeted set (migrate +
check + 3 specific drift/truth-map test files) than the full `pytest sims` run performed here; CI
does not appear to run the full 1198-test suite on every push, only this drift-focused subset plus
whatever `frontend-gates`/`integration-truth-map` exercise indirectly. This is a reasonable CI-speed
trade-off, not a defect, but means a regression in, say, `sims/backup_center` or unrelated app logic
outside the drift-guard set would not be caught by `pgsims_drift_gates.yml` alone — worth knowing
when deciding whether "CI green" is sufficient signal before a merge, vs. running the full suite
locally first (as this pass did).
