# Dry Run Results Matrix

| Category | Status | Command | What happened | Infra/App | Fixed? | Evidence |
|---|---|---|---|---|---|---|
| Backend dependency sanity | PASS | `python3 -m pip check` | no broken requirements | infra | n/a | terminal |
| Backend migration drift | PASS | `manage.py makemigrations --check --dry-run` | no changes detected | app | n/a | terminal |
| Django system check | PASS | `manage.py check` | no issues; local log permission warning | infra debt | no | terminal |
| Backend tests | PASS | `python3 -m pytest sims -q` | `217 passed` | app | n/a | terminal |
| Backend coverage harness | PARTIAL | venv + pytest-cov | harness repaired; coverage measured | infra | yes | `coverage/backend_coverage.json` |
| Backend coverage threshold | FAIL | pytest-cov branch run | line 53.53%, branch 27.75% | app/test debt | no | `coverage/backend_coverage.json` |
| Frontend dependency sanity | PASS | `npm ci --dry-run` | up to date | infra | n/a | terminal |
| Frontend lint | PASS | `npm run lint` | no warnings/errors | app | n/a | terminal |
| Frontend typecheck | PASS | `npm run typecheck` | passed | app | n/a | terminal |
| Frontend unit tests | PASS | `npm test -- --watch=false` | 3 suites, 5 tests passed | app | n/a | terminal |
| Frontend coverage threshold | FAIL | Jest coverage | line 3.77%, branch 3.10% | app/test debt | no | `coverage/frontend/coverage-summary.json` |
| Frontend build | PASS | `npm run build` | Next production build passed | app | n/a | terminal |
| OpenAPI generation | BLOCKED | repo scan | dependency exists, no wired schema endpoint/command found | infra | no | `01_testing_truth_audit.md` |
| Diff whitespace | PASS | `git diff --check` | clean | repo | n/a | terminal |

