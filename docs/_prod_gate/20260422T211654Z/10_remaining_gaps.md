# Remaining Gaps

## Release Blockers
- Backend line coverage is 54.38%, below the 95% threshold.
- Backend branch coverage is 28.69%, below the 90% threshold.
- Frontend line coverage is 8.71%, below the 90% threshold.
- Frontend branch coverage is 7.56%, below the 85% threshold.
- Strict OpenAPI schema generation fails with 49 warnings and 315 errors under `--fail-on-warn`.
- Active-surface E2E fails resident dashboard rendering.
- Active-surface E2E fails resident logbook draft creation confirmation.
- 100% active route/API/CTA/transition/unauthorized coverage was not achieved.
- Mounted UTRMC admin cluster is still not fully covered route/API/CTA-wise.

## Non-blocking Debt
- Backend health checks are slow but eventually healthy in Docker.
- Build emits outdated browser data notices.

## Deferred Items
Deferred or hidden modules remain outside the active-scope GO decision unless exposed by mounted runtime paths.
