# Open Blockers and Deferred Items

## Deferred workflows/modules

### Logbook workflow
- Status: Deferred
- Why deferred:
  - Not in active frontend nav/routes.
  - Not in active backend URL includes.
  - Legacy module import paths reference non-importable package names in active runtime.
- Required in separate milestone:
  - Controlled namespace reconciliation and safe reactivation plan with contract updates and E2E truth tests.

### Cases workflow
- Status: Deferred
- Why deferred:
  - Same activation boundary issues as logbook.
- Required in separate milestone:
  - Decide active-scope ownership (legacy migration vs archive), then wire FE/BE/contracts together.

## Remaining blockers (top set)
1. Legacy module activation mismatch (`sims.logbook`/`sims.analytics` imports vs `_legacy` package reality).
2. Documentation over-claims in some top-level materials.
3. Build config currently allows skipped lint/type checks.
4. No fresh browser E2E proof for all resident/UTRMC happy paths in this pass.
5. Log permission warning in backend environment (`logs/sims_error.log`) indicates environment hygiene issue.
