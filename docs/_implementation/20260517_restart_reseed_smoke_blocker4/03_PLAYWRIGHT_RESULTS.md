# Playwright Results

## Regression Smoke

Initial run:

```bash
cd frontend && npx playwright test e2e/feature-layer/regression-smoke.spec.ts
```

Initial result:

```text
2 failed, 1 passed
```

Cause:

- Stale assertions after UI pilot-readiness repair.
- `/dashboard/resident/research` now intentionally renders the deferred workflow page with heading `Research`, not `Research Project`.
- HOD reaches the repaired `Supervisor Dashboard`; old `Operational Snapshot (HOD Scope)` copy no longer exists.

Fix:

- Updated `frontend/e2e/feature-layer/regression-smoke.spec.ts` to assert current page-load behavior and meaningful visible headings.

Final regression smoke result:

```text
3 passed (15.0s)
```

## Active-Surface Suite

Command:

```bash
cd frontend && npm run test:e2e:feature-layer:local
```

Result:

```text
7 passed (34.3s)
```

Covered:

- Role login and dashboard surfaces.
- Key feature-layer route rendering.
- Logbook workflow.
- Permission boundaries.
- UTRMC read-only mutation controls.

