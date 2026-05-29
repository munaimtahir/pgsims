# Next Milestone Baseline

## Stable enough to build on now
- Active training surface (research/thesis/workshops/eligibility/summaries/postings).
- UTRMC userbase admin surface.
- Backend core active apps and truth tests.
- Frontend lint/test/build baseline restored.

## Must NOT be assumed complete
- Logbook and cases are not active workflows.
- Legacy analytics/logbook/cases docs are not runtime truth by default.
- Build pass alone is not sufficient quality signal unless lint/type/test gates are also enforced.

## Recommended next milestone
- **Legacy Workflow Boundary Decision + Controlled Reactivation/Archival**
  - Either:
    - Reactivate logbook/cases properly (contracts + FE pages + BE includes + tests), or
    - Archive and remove active claims comprehensively.

## Recommended do-not-touch areas (without explicit plan)
- Canonical Department/Hospital model and related migration gate semantics.
- Audit/history and notification schema contracts.
- Core training eligibility contract (`reasons` payload shape).

## Verification gates before any new feature expansion
- `cd frontend && npm run -s lint`
- `cd frontend && npm test -- --watch=false`
- `cd frontend && npm run -s build`
- `cd backend && SECRET_KEY=... pytest sims -q`
- `cd backend && SECRET_KEY=... pytest sims/_devtools/tests/test_drift_guards.py -q`
- `cd backend && SECRET_KEY=... pytest sims/training/test_phase6.py::ResearchProjectAPITests::test_supervisor_return_transitions_project_to_draft -q`
