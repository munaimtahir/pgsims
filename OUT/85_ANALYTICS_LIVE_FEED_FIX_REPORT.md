# 85 — Analytics Live Feed Fix Report

## Scope
- Target: `frontend/e2e/critical/admin_analytics_live_feed.spec.ts`
- Branch: `main` (no quarantine, no branch split)

## Root Cause
1. **Submit confirmation dialog not handled** in this spec, so the PG submit action could be canceled and the success assertion failed.
2. **Non-deterministic wait** (`waitForTimeout(8000)`) for live feed refresh caused race/timing instability.
3. **Setup auth flow intermittency** (`auth.setup.ts` UI login path) introduced unrelated flakiness during repeated runs.

## Fix Path Chosen
- **PATH C — Race/selector instability**
  - Added deterministic dialog handling (`confirm` accept) in target spec.
  - Replaced arbitrary sleep with deterministic response-based waits (`page.waitForResponse` with filtered query checks).
  - Kept meaningful assertions:
    - submit API returns 200 and yields entry id
    - filtered live feed response includes matching submitted event/entity id
    - key columns (`occurred at`, `event type`, `actor role`) are visible
    - submitted entry link id is visible in live table
  - Stabilized setup dependency by using API-based `loginAs` in `auth.setup.ts` (instead of brittle UI login flow).

## Backend Contract/Data Confirmation
- Frontend live feed API path: `/api/analytics/events/live`
- Backend endpoint confirmed:
  - `backend/sims/analytics/urls.py` → `path("events/live", AnalyticsLiveView...)`
  - `backend/sims/analytics/views.py` → `AnalyticsLiveView`
  - `backend/sims/analytics/dashboard_v1.py` → `build_live_payload`
- Logbook submit emits analytics event:
  - `backend/sims/logbook/api_views.py` emits `logbook.case.submitted`
- Access probe:
  - admin: `200`
  - pg: `403`

## Files Changed
- `frontend/e2e/critical/admin_analytics_live_feed.spec.ts`
- `frontend/e2e/auth.setup.ts`
- `frontend/playwright.config.ts`
- Evidence files:
  - `OUT/86_ANALYTICS_LIVE_FEED_REPRO_LOGS.md`
  - `OUT/87_ANALYTICS_SEED_EVIDENCE.md`
  - `OUT/88_PLAYWRIGHT_RERUN_STABILITY.md`
  - `OUT/analytics_ui_refs.txt`
  - `OUT/analytics_backend_refs.txt`

## Validation & Stability Evidence
1. Repro failure captured with trace/screenshots:
   - `OUT/86_ANALYTICS_LIVE_FEED_REPRO_LOGS.md`
2. Required single run with trace retain-on-failure:
   - PASS (local docker-backed backend + local frontend dev base URL)
3. 5x rerun loop:
   - PASS 5/5 (`OUT/88_PLAYWRIGHT_RERUN_STABILITY.md`)
4. Critical suite regression run:
   - Target analytics spec passed
   - One unrelated failure remained in `e2e/critical/userbase_foundation.spec.ts` (not touched by this fix)

## Final Verdict
- **TARGET FIX PASS**: `admin_analytics_live_feed.spec.ts` is now deterministic under validated local/docker-backed conditions without quarantining.
