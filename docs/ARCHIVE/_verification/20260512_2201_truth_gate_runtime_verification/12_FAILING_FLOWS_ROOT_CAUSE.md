# Failing Flows Root Cause

| Failure | Category | Root Cause | Fix Type | Priority |
|---|---|---|---|---|
| `sims/tests/test_bulk_userbase_engine.py` collection | Environment/config issue | `pandas` missing from backend image | dependency/image update | P1 |
| `app/dashboard/utrmc/hod/page.test.tsx` timeout | Test harness issue | CTA test exceeds default timeout / leaks async work | test stabilization | P2 |
| `components/auth/ProtectedRoute.test.tsx` / `lib/api/*.test.ts` typecheck errors | Test harness issue | Jest globals not visible to `tsc` in tests | test typing config | P2 |
| `frontend/app/dashboard/resident/research/page.tsx` vs wizard spec | Stale test / documentation drift | App intentionally shows deferred research notice, test expects old wizard | rebaseline test or implement workflow | P2 |
| `frontend/e2e/critical/admin_critical.spec.ts` | Stale test / missing feature | `/dashboard/admin` is not implemented in the app route tree | remove/rebaseline test or add route | P2 |
| `frontend/e2e/critical/admin_analytics_live_feed.spec.ts` | Legacy test | explicitly outside current active-surface baseline | keep skipped or move to legacy suite | P3 |

## Notes

- The remaining runtime gaps are narrow and well-scoped.
- None of the observed failures require broad refactors.
