# Code Coverage Report

## Backend
- Command: `SECRET_KEY=test-secret ../OUT/prod_gate_artifacts/20260421T233708Z/backend-venv/bin/coverage run --branch -m pytest sims -q && ../OUT/prod_gate_artifacts/20260421T233708Z/backend-venv/bin/coverage json -o ../OUT/prod_gate_artifacts/20260422T211654Z/coverage/backend/coverage.json && ../OUT/prod_gate_artifacts/20260421T233708Z/backend-venv/bin/coverage report`
- Result: `222 passed`.
- Line coverage: 54.38%.
- Branch coverage: 28.69%.
- Required for GO: 95% line, 90% branch.
- Status: FAIL.

## Frontend
- Command: `npm test -- --watch=false --coverage --coverageReporters=json-summary --coverageReporters=text --coverageDirectory=../OUT/prod_gate_artifacts/20260422T211654Z/coverage/frontend`
- Result: 5 suites passed, 9 tests passed.
- Line coverage: 8.71%.
- Branch coverage: 7.56%.
- Required for GO: 90% line, 85% branch.
- Status: FAIL.

## Notes
The new tests improved active UTRMC page coverage locally, but repo-wide active coverage remains far below the mandatory thresholds.
