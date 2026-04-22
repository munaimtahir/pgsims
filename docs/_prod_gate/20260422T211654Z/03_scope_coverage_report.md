# Scope Coverage Report

## Status
FAIL for GO threshold.

| Coverage Area | Required for GO | Actual | Status |
|---|---:|---:|---|
| Active routes inventoried | 100% | 100% | PASS |
| Active routes tested | 100% | not fully closed | FAIL |
| Active APIs inventoried | 100% | 100% | PASS |
| Active APIs tested | 100% | not fully closed | FAIL |
| Active roles tested | 100% | 100% attempted | PARTIAL |
| Visible CTAs tested | 100% | not fully closed | FAIL |
| Critical workflows tested | 100% | active logbook failed live | FAIL |
| Invalid transitions tested | 100% critical scope | improved, not complete | FAIL |
| Unauthorized access tests | 100% active scope | improved, not complete | FAIL |
| Restart/reseed critical smoke | 100% | seed passes, smoke fails | FAIL |

## Closed in This Pass
- Added backend route/API tests for UTRMC roster and hospital-department matrix paths.
- Added backend read-only mutation denial tests for UTRMC user on HOD assignment, supervision link, hospital-department matrix, and user creation.
- Added backend invalid transition tests for logbook and leave workflows.
- Added frontend UTRMC HOD assignment CTA tests.
- Added frontend UTRMC hospital-department matrix CTA/read-only tests.

## Remaining Scope Gaps
- Full mounted UTRMC admin cluster is still not covered route/API/CTA-wise.
- Active-surface E2E fails resident dashboard and logbook runtime behavior.
- Prior untested active pages and CTAs are not all closed.
