# Remaining Gaps And Risks

## True Release Blockers
- Required code coverage thresholds were not achieved.
- Required 100% active mounted scope coverage was not achieved.
- OpenAPI/SDK generation/freshness gate is not available.

## Non-Blocking Debt
- Local `backend/logs` permission warning disables file logging in local dry-run checks; container runtime still produced logs, but local observability setup should be cleaned up.
- Jest haste-map warning from `.next/standalone/package.json` indicates build output can interfere with test discovery if not ignored more explicitly.

## Deferred Items Correctly Out Of Scope
- Rotations phase-1 workflow.
- Synopsis workflow.
- Thesis workflow.
- Resident postings/workshops/research direct routes.
- Supervisor research approvals direct route.

## Future Hardening Needed
- Add component/unit tests for active resident, supervisor, and UTRMC pages.
- Add backend tests for every active UTRMC org-graph/detail endpoint response shape and role matrix.
- Add direct API negative tests for malformed inputs and invalid state transitions across active logbook/leave flows.
- Wire schema generation and contract drift checks.

