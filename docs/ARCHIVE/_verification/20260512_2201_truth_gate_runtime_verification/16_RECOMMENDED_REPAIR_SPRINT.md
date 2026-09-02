# Recommended Repair Sprint

| Priority | Task | Evidence | Expected Outcome | Risk |
|---|---|---|---|---|
| 1 | Retire or rebaseline `/dashboard/admin` critical tests | app has no `frontend/app/dashboard/admin/` route | remove stale failures from the critical gate | low |
| 2 | Decide the resident research baseline | `frontend/app/dashboard/resident/research/page.tsx` is a deferred notice | either implement the wizard or update the test baseline | medium |
| 3 | Restore backend regression dependency coverage | backend pytest collection stops on missing `pandas` | backend regression gate can execute fully | low |
| 4 | Fix frontend test typing/harness issues | `typecheck` reports missing Jest globals | clean frontend type gate | low |
| 5 | Finish/retire legacy analytics live-feed spec | legacy file is outside current active-surface baseline | no confusion in the critical suite | low |

## Scope guard

This sprint should stay limited to the smallest set of changes needed to make the active gate clean and remove stale admin expectations.
