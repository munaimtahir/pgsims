# API Contract and Runtime Alignment

## Summary

Current active-surface runtime alignment is good. The login, dashboard, workflow, RBAC, and negative-access flows all succeeded once the local seed data was corrected.

## Alignment matrix

| UI Feature | Frontend API Call | Backend Endpoint | OpenAPI Present | Runtime Result | Status |
|---|---|---|---|---|---|
| Login | auth helper | `/api/auth/login/` | yes | PASS | aligned |
| Session check | auth helper | `/api/auth/me/` | yes | PASS | aligned |
| Resident dashboard | dashboard pages | resident summary/dashboard APIs | yes | PASS | aligned |
| Supervisor dashboard | dashboard pages | supervisor APIs | yes | PASS | aligned |
| UTRMC dashboard | dashboard pages | userbase/training APIs | yes | PASS | aligned |
| Logbook workflow | active-surface workflow | logbook APIs | yes | PASS | aligned |
| Leave workflow | workflow-gate | leave APIs | yes | PASS | aligned |
| UTRMC management | workflow-gate/dashboard | bulk/userbase/training APIs | yes | PASS | aligned |
| Resident research page | resident research page | research API exists | yes | PARTIAL | UI is intentionally deferred |
| Admin dashboard/reports | legacy tests | no current app route | n/a | FAIL | stale/legacy surface |

## Notes

- `/dashboard/admin` is present in legacy tests, but the current app route tree does not implement it.
- The contract/runtime surface that is actually used by the active release route set is consistent.
