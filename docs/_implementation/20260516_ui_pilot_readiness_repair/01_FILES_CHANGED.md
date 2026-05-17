# Files Changed

## Frontend Pages

- `frontend/app/dashboard/resident/page.tsx`
- `frontend/app/dashboard/resident/schedule/page.tsx`
- `frontend/app/dashboard/supervisor/page.tsx`
- `frontend/app/dashboard/utrmc/page.tsx`
- `frontend/app/dashboard/utrmc/onboarding/page.tsx`
- `frontend/app/dashboard/utrmc/matrix/page.tsx`
- `frontend/app/dashboard/utrmc/hospitals/page.tsx`
- `frontend/app/dashboard/utrmc/departments/page.tsx`
- `frontend/app/dashboard/utrmc/users/page.tsx`
- `frontend/app/dashboard/utrmc/data-quality/page.tsx`

## Tests

- `frontend/app/dashboard/resident/page.test.tsx`
- `frontend/app/dashboard/resident/schedule/page.test.tsx`
- `frontend/app/dashboard/supervisor/page.test.tsx`
- `frontend/app/dashboard/utrmc/page.test.tsx`
- `frontend/e2e/smoke/auth_flow.spec.ts`
- `frontend/e2e/smoke/dashboards.spec.ts`
- `frontend/e2e/smoke/ui_pilot_readiness.spec.ts`
- `frontend/e2e/feature-layer/regression-smoke.spec.ts`
- `frontend/e2e/feature-layer/rotations-phase1.spec.ts`
- `frontend/e2e/feature-layer/dashboards.spec.ts`
- `frontend/e2e/feature-layer/permissions.spec.ts`
- `frontend/e2e/feature-layer/auth-and-smoke.spec.ts`
- `frontend/e2e/workflow-gate/bulk-setup.spec.ts`

## Notes

- The new onboarding route keeps import tools accessible without dominating the main UTRMC overview.
- The resident and schedule routes now degrade to calm empty states instead of throwing on missing resident data.

