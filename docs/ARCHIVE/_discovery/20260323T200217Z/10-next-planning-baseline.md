# Next Planning Baseline

## First fixes before new features

1. Reconcile logbook/cases contract claims with active frontend/backend routing.
2. Restore frontend lint pass.
3. Standardize documentation authority and remove stale references from top-level docs.
4. Confirm frontend build exits cleanly in reproducible CI/local command path.

## Stable foundations

- Backend workflow and RBAC core has strong passing evidence.
- Canonical data model governance is enforced by drift gates.
- Core deployment topology is in place (db/redis/backend/frontend/worker/beat).

## Freeze guidance

- Keep route/terminology contracts frozen unless explicitly approved.
- Keep canonical Department/Hospital model design untouched.

## Redesign guidance

- Clarify active-vs-legacy module boundaries in docs and ownership.
- Align role-home routing behavior consistently across middleware and client redirect helpers.

## Recommended milestone order

1. Truth-alignment milestone (contracts/routes/docs).
2. Frontend quality baseline milestone (lint/build stability).
3. Workflow closure milestone (implement or retire missing core UI workflows).
4. New feature milestones after above are green.

## Do not assume complete

- Logbook and cases end-to-end paths.
- Analytics UI presence in App Router.
- Regression-marked features in e2e docs.

## Safe foundations already available

- Auth and RBAC backend core.
- Userbase/org APIs.
- Training domain models and major endpoints.
- Drift/migration gate coverage.
