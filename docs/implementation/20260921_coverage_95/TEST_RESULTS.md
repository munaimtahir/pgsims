# Coverage Sprint Test Results

## Measurement status — 2026-09-24

All results are local to `/home/munaim/srv/apps/pgsims` at the then-current
source state. They are not production verification.

| Platform | Command | Result | Coverage |
| --- | --- | --- | --- |
| Frontend | `python3 scripts/coverage_gate.py frontend` | PASS — 421 tests, 48 suites, no skips | lines 48.23%; branches 36.80%; statements 46.45%; functions 43.83% |
| Backend onboarding boundaries | `DATABASE_URL=sqlite:////tmp/pgsims-onboarding-coverage.sqlite3 SECRET_KEY=coverage-local-test .venv/bin/python backend/manage.py test sims.users.test_onboarding_boundaries --keepdb --verbosity=1` | PASS — 10 tests | malformed payloads, authorization, transactional document and onboarding branches |
| Backend focused onboarding regression | `DATABASE_URL=sqlite:////tmp/pgsims-onboarding-focused.sqlite3 SECRET_KEY=coverage-local-test DJANGO_SETTINGS_MODULE=sims_project.settings_test .venv/bin/python backend/manage.py test sims.users.test_onboarding_boundaries sims.users.test_resident_onboarding --verbosity=1` | PASS — 28 tests in 4.061s | resident draft/state/declaration/document validation, authorization, review, and correction transitions |
| Android unit baseline | `python3 scripts/coverage_gate.py android --unit-only` | PASS | lines 16.06%; branches 6.02%; methods 13.24% |
| Android connected coverage | `python3 scripts/coverage_gate.py android` | Not run on VPS | Requires the dedicated `pgsims` emulator and isolated loopback backend on the Laptop |
| Backend merged SQLite/PostgreSQL coverage | `.venv/bin/python scripts/coverage_gate.py backend` | Completed — 1,245 passed; 0 failed; 0 skipped; 245 warnings; SQLite 762.56s + PostgreSQL 45.20s | 84.02% lines; 68.63% branches. Fresh evidence at commit `822fab8`, source hash `8872bc98…`; below the new target, so the gate correctly reports BLOCKED. |

The current sprint is enforced with
`--target-profile sprint_risk_reduction`; its exact targets are in
`COVERAGE_TARGETS.md`. It intentionally measures backend and frontend only.
The 95% release floor remains `phase_3_release_floor`; no platform or area is
averaged, and any failed or skipped test blocks a report.

## Initial improvements

- Web baseline before this work: 29.16% lines / 25.50% branches.
- Current web suite: 421 passing tests and 48.23% lines / 36.80% branches.
- Android had no report before this work; the unit baseline now has a reproducible
  JaCoCo XML report. Android is deferred to its dedicated Laptop connected-test
  sprint and is not counted toward this sprint's result.

## Next measured gaps

The largest untested web surfaces are backup administration, workflow creation/
review pages, report detail pages, and the remaining shared API error branches.
The Android report shows Compose screens, recovery storage/worker paths, and
role workflows require both pure-function extraction tests and connected tests.

## Backend fresh baseline — 2026-09-24

| Area | Lines | Branches |
| --- | ---: | ---: |
| academics | 93.44% | 78.31% |
| backup_integrations | 90.77% | 78.30% |
| directories | 78.21% | 56.93% |
| identity | 76.13% | 60.27% |
| imports_reporting | 79.84% | 68.60% |
| infrastructure | 93.81% | 90.62% |
| notifications | 80.28% | 50.00% |
| onboarding | 76.80% | 70.29% |
| training | 89.52% | 69.54% |

All formerly skipped coverage tests now run: backup/Google Drive paths are fully
mocked, and the PostgreSQL-only idempotency path runs in a disposable container.
The next limiting work is the measured branch deficit, especially identity,
directories, notifications, onboarding, and training.
