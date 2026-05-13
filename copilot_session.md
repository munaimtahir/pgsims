# PGSIMS Pilot Deployment Readiness Plan

## Purpose
Coordinate the sprint that moves PGSIMS from conditional go to controlled pilot readiness without adding product features or changing pilot scope.

## Scope
In scope:
- Baseline capture and git/Docker status
- Docker root-cause analysis and helper scripts
- Docker restart stability proof
- Backend, frontend, E2E, RBAC, schema, and coverage checks
- Backup/rollback readiness
- Pilot user/data readiness
- Monitoring/healthcheck readiness
- Pilot checklist, risks, and final verdict

Out of scope:
- New features
- Research workflow implementation
- `/dashboard/admin`
- Destructive database operations
- Secret exposure
- Unapproved scope expansion

## Execution order
1. Confirm baseline and working tree state.
2. Diagnose why Docker restarts depend on env handling or stale runtime state.
3. Add official helper scripts so future runs always use `--env-file .env`.
4. Prove Docker restart stability with the helper scripts.
5. Run backend gate and classify any remaining legacy failures precisely.
6. Run frontend gate and classify any known test-only typecheck noise precisely.
7. Run E2E gates after reseeding local test data.
8. Verify RBAC boundaries and active workflows on the live pilot surfaces.
9. Run schema and coverage checks if available.
10. Create backup and document restore/rollback paths.
11. Document pilot user/data readiness for a coordinator.
12. Document monitoring and healthcheck readiness.
13. Produce the pilot checklist.
14. Capture remaining risks and the final controlled pilot verdict.
15. Record final git status and commit only if explicitly instructed.

## Working notes
- Every command must be logged in `COMMAND_LOG.md` during execution.
- Every changed file must be logged in `FILES_CHANGED.md`.
- Evidence should live under `docs/_implementation/<timestamp>_pilot_deployment_readiness/`.
- Keep changes small, reversible, and fully documented.
- Use exact pass/fail counts when reporting test and gate results.

## Todo tracker
- [x] Confirm baseline and git status
- [x] Diagnose Docker env root cause
- [x] Add Docker helper scripts
- [x] Prove Docker restart stability
- [x] Run backend final gate
- [x] Run frontend final gate
- [x] Run E2E final gate
- [x] Verify RBAC and active workflows
- [x] Check schema and coverage gates
- [x] Prepare backup and rollback readiness
- [x] Document pilot user and data readiness
- [x] Document monitoring and health checks
- [x] Create pilot deployment checklist
- [x] Capture remaining risks and final verdict
- [x] Record final git status

## Gate notes
- Backend: conditional pass (335 passed, 19 failed; failures are legacy user-view/bulk coverage paths)
- Frontend: conditional pass (lint/build/Jest pass; typecheck has 7 test-file-only errors)
- E2E: pass (smoke 17/17, active-surface 7/7, critical 5/5 with 1 expected skip)
- RBAC/workflows: pass (auth 10/10, rbac 20/20, dashboard 18/18; workflows 22/23 with excluded research-path failure)
- Schema: pass; coverage ran at 63.22% and remains a known limitation for pilot

## Handoff rule
Update this file as each phase completes so the next agent can resume without redoing completed work.
