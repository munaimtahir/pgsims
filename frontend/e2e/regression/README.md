# Regression Tests — Pending Feature Completion

This folder contains regression specs for features that are **partially or not yet implemented** in the current codebase. These tests are intentionally excluded from the default `playwright.config.ts` test runs (`testMatch` only picks up `smoke/` and `critical/`).

## Files

| Spec | Depends on | Status |
|------|-----------|--------|
| `login.spec.ts` | Login page (implemented) | ✅ Promoted to `smoke/auth_flow.spec.ts` — kept here as original |
| `utrmc_readonly_dashboard.spec.ts` | `data-testid` attributes on UTRMC dashboard | ⏳ Needs `data-testid` hooks added to components |
| `logbook_submit_return_resubmit_approve.spec.ts` | Logbook submission form UI | ⏳ Needs logbook form `data-testid` hooks |
| `admin_analytics.spec.ts` | Analytics dashboard page | ⏳ Feature not yet implemented |
| `import_reports_dashboard.spec.ts` | Bulk import UI | ⏳ Feature not yet implemented |
| `cases_create_submit_review.spec.ts` | Cases submission UI | ⏳ Needs verification |

## Running Regression Tests

These tests are NOT included in the default test run. To run them explicitly:

```bash
# Run all regression tests
cd frontend
npx playwright test e2e/regression/

# Run a specific regression spec
npx playwright test e2e/regression/login.spec.ts
```

## How to Graduate a Test from Regression → Critical

1. Verify the underlying feature is fully implemented.
2. Add any required `data-testid` attributes to the components.
3. Run the spec standalone: `npx playwright test e2e/regression/<name>.spec.ts`
4. Once passing, move it to `e2e/critical/` and update `playwright.config.ts` if needed.
5. Remove from this folder.
