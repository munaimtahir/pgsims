# Release Gate Recheck

Date (UTC): 2026-04-21

## Decision
**GO**

## Why
- The active surface is now narrowed to truthful, reproducible workflows.
- Resident baseline and leave create no longer depend on untracked manual runtime state.
- Supervisor RBAC contract matches runtime self-scoped read behavior.
- Inactive rotations/synopsis/thesis surfaces are hidden from active navigation and excluded from the active release gate.
- Backend, frontend, and focused active-surface Playwright gates passed.

## Final Truth Classification
| Surface | Classification |
|---|---|
| Auth/login/profile | WORKING PERFECTLY |
| Resident dashboard | WORKING PERFECTLY |
| Leave create flow | WORKING PERFECTLY |
| Supervisor dashboard | WORKING PERFECTLY |
| UTRMC dashboard | WORKING PERFECTLY |
| UTRMC read-only permission boundary | WORKING PERFECTLY |
| Supervisor `/api/users/` self-scoped read | WORKING PERFECTLY |
| Logbook active path | WORKING PERFECTLY |
| Rotations phase-1 | NOT DONE / MISLEADING / HIDDEN |
| Synopsis workflow | NOT DONE / MISLEADING / HIDDEN |
| Thesis workflow | NOT DONE / MISLEADING / HIDDEN |

## Remaining Release Notes
- Do not advertise rotations phase-1, synopsis, or thesis as active until their inactive-depth tests are fixed and promoted.
- Direct URLs for deferred routes may still build, but they are outside the active release contract.
