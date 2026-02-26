# Fix Report - Phase-1 Logbook Verify Flow (FIXPACK_20260226_0351)

## Summary
This fix pack unblocks the Phase-1 pilot flow for logbook verification by fixing the supervisor verify API crash, aligning notification writes with the canonical `Notification` schema, exposing supervisor feedback to PG-facing API responses, and adding an end-to-end smoke test.

## What Was Broken
1. Supervisor verify crash:
   - `VerifyLogbookEntryView` wrote to `entry.supervisor_comments`.
   - `LogbookEntry` model field is `supervisor_feedback`.
   - Result: runtime error during supervisor verify/return action.

2. API/Frontend contract drift for feedback:
   - Frontend verify client sends `{ feedback }`.
   - PG serializer did not expose `supervisor_feedback`, so PG users could not see supervisor feedback after review.

3. Notification schema drift:
   - Multiple direct `Notification.objects.create(...)` calls used legacy fields (`user`, `message`, `type`, `related_object_id`).
   - Canonical model expects `recipient`, `body`, `verb`, `metadata`.
   - Result: notification creation could crash during logbook/rotation/certificate workflows.

4. API immutability gap for returned entries:
   - API detail update allowed only `draft` edits despite model exposing `can_be_edited()` for `draft` and `returned`.
   - PG resubmission workflow after supervisor return was blocked/inconsistent.

## Exact Changes Made
### 1) Verify endpoint crash + contract fixes
- `backend/sims/logbook/api_views.py`
  - Replaced invalid write target with `entry.supervisor_feedback`.
  - Verify endpoint now accepts both `feedback` and `supervisor_feedback` keys.
  - Added optional `action` support with backward-compatible default (`approved`).
  - Supported actions: `approved`, `returned`, `rejected` (plus `approve/return/reject` aliases).
  - Added status guard: only `pending` entries can be verified.
  - Verify response now returns:
    - `supervisor_feedback`
    - `feedback` (alias)
    - `verified_at` (nullable for returned/rejected)

### 2) PG serializer feedback visibility + timestamp aliasing
- `backend/sims/logbook/api_serializers.py`
  - Added `supervisor_feedback` to `PGLogbookEntrySerializer`.
  - Added `feedback` alias (`source="supervisor_feedback"`, read-only).
  - Added `submitted_at` alias (`source="submitted_to_supervisor_at"`, read-only) to match frontend contract shape.

### 3) Notification model drift fixes (schema-correct creates)
- `backend/sims/logbook/models.py`
  - Fixed logbook submission notification create call to use:
    - `recipient`, `verb`, `body`, `metadata`
- `backend/sims/logbook/admin.py`
- `backend/sims/rotations/admin.py`
- `backend/sims/certificates/admin.py`
  - Updated legacy direct notification creates to canonical schema.
  - Moved related object references into `metadata` JSON (`object_type`, `object_id`, `action`).

### 4) API-layer immutability / editability guard
- `backend/sims/logbook/api_views.py`
  - PG update endpoint now uses `entry.can_be_edited()` to permit edits for `draft` and `returned`, and block otherwise.
  - PG submit endpoint now accepts `draft` and `returned` for resubmission.
- `backend/sims/logbook/api_serializers.py`
  - Added serializer-level validation guard to reject updates when instance is not editable.

### 5) Minimal frontend compatibility (no route/UI redesign)
- `frontend/lib/api/logbook.ts`
  - Extended `LogbookEntry` type with `feedback` and `supervisor_feedback`.
- `frontend/app/dashboard/pg/logbook/page.tsx`
  - Added a lightweight "Supervisor Feedback" table column (reads `feedback` / `supervisor_feedback` / fallback legacy key).
  - Enabled existing Edit/Submit actions for `returned` entries (same page/flow, no redesign).

### 6) Smoke test evidence
- `backend/sims/logbook/test_api.py`
  - Added end-to-end API smoke test covering:
    - PG create -> submit
    - Supervisor return with feedback
    - PG list sees status + feedback alias + canonical field
    - PG edits returned entry and resubmits
    - Supervisor approves with feedback alias key (`supervisor_feedback`)
    - PG cannot edit after approval
    - Notification row created with canonical schema/metadata

## Files Changed
- `backend/sims/logbook/api_views.py`
- `backend/sims/logbook/api_serializers.py`
- `backend/sims/logbook/models.py`
- `backend/sims/logbook/admin.py`
- `backend/sims/rotations/admin.py`
- `backend/sims/certificates/admin.py`
- `backend/sims/logbook/test_api.py`
- `frontend/lib/api/logbook.ts`
- `frontend/app/dashboard/pg/logbook/page.tsx`

## Validation / Evidence
### Backend checks
- `python manage.py check` -> PASS
- Result: `System check identified no issues (0 silenced).`

### Backend smoke test (targeted)
- `python manage.py test sims.logbook.test_api.PGLogbookEntryAPITests.test_submit_return_feedback_visible_and_resubmit_approve_flow -v 2` -> PASS
- Result: `Ran 1 test ... OK`

### Backend logbook API test module
- `python manage.py test sims.logbook.test_api -v 1` -> PASS
- Result: `Ran 18 tests ... OK`

### Frontend build sanity
- `npm run build` (in `frontend/`) -> PASS
- Next.js build completed successfully.

## Remaining Risks / Follow-ups (not part of this surgical fix pack)
- Duplicate/overlapping Department model/domain concerns still need a separate cleanup pass.
- Explicit `utrmc` role support remains a follow-up (not introduced here).
- Reminder scheduling/notification timing via Celery Beat should be validated separately in deployed env.
- Some legacy admin flows still use old status vocabulary (`submitted`, `needs_revision`) in admin-specific logic and may need a future normalization pass (not changed beyond notification schema patching).
