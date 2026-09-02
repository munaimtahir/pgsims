# Failures And Root Causes

## Release Blockers
1. Backend code coverage threshold failed.
   - Required: line >= 95%, branch >= 90%.
   - Actual: line 53.53%, branch 27.75%.
   - Root cause: broad active and adjacent backend modules have insufficient unit/integration coverage, especially permission helpers, UTRMC/admin views, bulk services, userbase views, and training views branches.

2. Frontend code coverage threshold failed.
   - Required: line >= 90%, branch >= 85%.
   - Actual: line 3.77%, branch 3.10%.
   - Root cause: only three Jest suites exist; most active pages, API client methods, nav/role logic, and UI states are untested at component/unit level.

3. 100% active mounted scope coverage was not achieved.
   - UTRMC visible admin cluster renders under runtime tests, but not every route, CTA, endpoint, and denial path has explicit evidence.
   - Supervisor resident progress route and some UTRMC detail/CTA paths remain insufficiently proven.

4. OpenAPI/schema generation is not wired.
   - `drf-spectacular` is installed, but no configured schema route or generation command was found.

## Fixed During This Gate
- Backend coverage harness setup via isolated venv.
- Stale Playwright selector on UTRMC overview.
- Stale navigation expectations for de-scoped resident/supervisor nav items.
- Stale workflow-gate assertions for de-scoped research/rotation/posting.
- Stale leave workflow selectors.

