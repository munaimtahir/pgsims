# Workflow Transition Coverage

| Workflow | Valid transitions tested | Invalid transitions tested | Status |
|---|---|---|---|
| Auth | valid login, invalid login, empty fields | unauthenticated dashboard redirect | PASS |
| Leave | draft -> submitted -> approved | missing/unauthenticated coverage partial | PARTIAL |
| Logbook | draft -> submitted -> returned -> resubmitted -> approved | unrelated supervisor blocked | PASS |
| UTRMC read-only | page render/read-only controls | mutation controls hidden | PASS |
| UTRMC admin CRUD/import cluster | bulk hospital dry-run; page render | validation tests for forms | PARTIAL |

Critical active workflows passed. Required invalid-transition coverage for every critical path is still incomplete.

