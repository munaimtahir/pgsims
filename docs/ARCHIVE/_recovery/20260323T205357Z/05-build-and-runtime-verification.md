# Build and Runtime Verification

## Commands run
- Frontend:
  - `cd frontend && npm run -s lint`
  - `cd frontend && npm test -- --runInBand --watch=false`
  - `cd frontend && npm run -s build`
- Backend:
  - `cd backend && SECRET_KEY=test-secret-key-for-ci pytest sims -q`
  - `cd backend && SECRET_KEY=test-secret-key-for-ci python3 manage.py check`
  - Truth-test subset:
    - `pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -q`
    - `pytest sims/training/test_phase6.py::EligibilityAPITests::test_my_eligibility_items_use_reasons_field -q`
    - `pytest sims/training/test_phase6.py::EligibilityAPITests::test_utrmc_eligibility_items_use_reasons_field -q`
    - `pytest sims/rotations/test_canonical_migration_gate.py -q`
    - `pytest sims/_devtools/tests/test_drift_guards.py -q`

## Outcomes
- Frontend lint: pass (0 errors/warnings).
- Frontend tests: pass (`2/2` suites, `4/4` tests).
- Frontend build: pass (route generation complete).
- Backend full gate: pass (`188 passed`).
- Backend `manage.py check`: pass (file-log permission warning noted, non-blocking).
- Truth subset gates: all pass.

## Runtime notes
- Build log shows repeated Node warning: `--localstorage-file` without valid path; did not block build.
- Legacy logbook/cases routes remain intentionally inactive.

## Reproducibility confidence
- High for active surfaces covered by current tests/lint/build.
- Medium for deferred legacy workflows pending dedicated reactivation milestone.
