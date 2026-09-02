# Test And Verification Results

## Commands

- `npm run typecheck`
- `npm run lint`
- `npm run build`
- `E2E_BASE_URL=http://127.0.0.1:3005 E2E_API_URL=http://127.0.0.1:8014 npx playwright test frontend/e2e/smoke/ui_pilot_readiness.spec.ts --project=smoke`

## Notes

- `npm run lint`: PASS
- `npm run build`: PASS
- `npm run typecheck`: PASS
- Playwright pilot smoke spec: PASS
  - `frontend/e2e/smoke/ui_pilot_readiness.spec.ts`
  - Verified:
    - UTRMC dashboard operational summary and onboarding entry point
    - Supervisor dashboard empty-state behavior
    - Resident dashboard empty-state behavior
    - Resident schedule empty-state behavior
    - Data quality calm fallback on cleaned baseline
