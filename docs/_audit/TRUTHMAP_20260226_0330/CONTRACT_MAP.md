# Contract Map (Truth Map)

## UI ↔ API Feature Mapping

| UI Feature | Frontend SDK Method | Backend Endpoint | Status |
|------------|---------------------|------------------|--------|
| Logbook Submission | `logbookApi.submitMyEntry` | `POST /api/logbook/my/<id>/submit/` | ✅ Exists |
| Supervisor Verification | `logbookApi.verify` | `PATCH /api/logbook/<id>/verify/` | ❌ Broken (Logic Error) |
| UTRMC Dashboard | `analyticsApi.getDashboardOverview` | `GET /api/analytics/dashboard/overview/` | ✅ Exists |
| Resident Logbook View | `logbookApi.getMyEntries` | `GET /api/logbook/my/` | ✅ Exists |

## Major Contract Issues

### 1. Verification Field Mismatch
- **Frontend Sends**: `{ "feedback": "..." }`
- **Backend Receives**: `feedback`
- **Backend Model Has**: `supervisor_feedback`
- **Backend View Sets**: `entry.supervisor_comments`
- **Result**: `AttributeError` on backend during verification.

### 2. Notification Field Mismatch
The backend attempts to trigger notifications via cross-app calls that use an outdated/incorrect field names.
- **Evidence**: `backend/sims/logbook/models.py:726` uses `user=...` instead of `recipient=...`.

### 3. Missing Fields in Serializers
`PGLogbookEntrySerializer` does not include `supervisor_feedback`, meaning residents cannot see why an entry was rejected or returned.
- **Evidence**: `backend/sims/logbook/api_serializers.py:11` missing `supervisor_feedback`.

## Client SDK Status
- **Location**: `frontend/lib/api/`
- **Type**: Manual Axios wrappers.
- **Consistency**: High consistency in naming, but disconnected from recent model refactors (`feedback` vs `comments`).

## Known Unknowns
- Are there any "dead" UI pages using mock data? (Search results page should be checked).

## Immediate Next Actions
1. Audit all `Model.objects.create(...)` calls in signals and views to ensure field compatibility.
2. Regenerate or manually sync `PGLogbookEntrySerializer` with the full `LogbookEntry` model.
