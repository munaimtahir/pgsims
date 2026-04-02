# Next Milestone Baseline

## What can now be treated as stable
- Resident, supervisor, and UTRMC dashboard route boundary
- Userbase/org graph administration surface
- Research workflow baseline
- Resident leave workflow baseline
- Eligibility contract shape using canonical `reasons`
- Password-reset request path behavior
- Backend canonical Department/Hospital model rule and drift guards

## What must still not be assumed complete
- Logbook
- Cases
- Legacy analytics modules
- Full rotation lifecycle
- Full postings lifecycle
- Broad end-to-end coverage outside the promoted workflow gate

## Recommended next milestone
- Rotation and postings closure on the verified active surface

## Recommended do-not-touch areas
- Canonical Department/Hospital data model boundaries
- Frozen route structure and terminology
- Stable RBAC foundations and migration history
- Legacy module activation unless there is an explicit milestone to reopen those boundaries

## Recommended verification gates before new feature work
1. Re-run `docs/contracts/TRUTH_TESTS.md` gates on the current checked-out code.
2. Rebuild Docker runtime before using it as evidence.
3. Confirm new work stays inside the active surface map before implementation starts.
4. Update `docs/contracts/` and the current recovery/status pack in the same run if any active-surface truth changes.
