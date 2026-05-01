# Regression Guards

To ensure this cross-origin/proxy issue doesn't regress, the following guards are established:

1. **Active-Surface Stability**: The `test:e2e:feature-layer:local` command is functionally restored to stability (7/7 tests passing) and effectively verifies the exact behavior and proxy routes of the frontend container.
2. **Regression Smoke Selector Fix**: In `frontend/e2e/feature-layer/regression-smoke.spec.ts`, the locator mismatch (`Research Project` vs `Research`) was updated to ensure that `inactive-depth` tests can reliably prove that core resident routes still load successfully under the proxy model.
3. **Environment Determinism**: `scripts/e2e_up.sh` provides a deterministic `.env` injection into the E2E framework, guaranteeing `NEXT_PUBLIC_API_URL=/api` behaves exactly as it will in the production Docker environment.
