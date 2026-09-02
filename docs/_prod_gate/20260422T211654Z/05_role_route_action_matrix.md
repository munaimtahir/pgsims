# Role Route Action Matrix

## Status
PARTIAL.

| Role | Covered Allow Paths | Covered Deny Paths | Remaining Gap |
|---|---|---|---|
| Resident | login attempted; dashboard attempted; logbook attempted | supervisor and UTRMC route denial passed in E2E | resident dashboard and logbook E2E fail |
| Supervisor | dashboard attempted; unrelated logbook review denied | unrelated resident logbook review denied | full CTA/route matrix still incomplete |
| HOD | dashboard expected through supervisor surface | not fully rerun | HOD-specific runtime route/action coverage incomplete |
| UTRMC admin | UTRMC HOD/matrix frontend tests; backend org graph mutation tests | not complete | mounted UTRMC cluster still not fully covered |
| UTRMC user | read-only backend denial tests; E2E mutation-control denial passed | HOD/matrix read-only frontend states covered | full read-only route/action matrix incomplete |

## Evidence
- Backend: `sims/users/test_userbase_api.py`
- Backend: `sims/training/test_feature_layer_ops.py`
- Frontend: `app/dashboard/utrmc/hod/page.test.tsx`
- Frontend: `app/dashboard/utrmc/matrix/page.test.tsx`
- E2E: `OUT/prod_gate_artifacts/20260422T211654Z/playwright/results`
