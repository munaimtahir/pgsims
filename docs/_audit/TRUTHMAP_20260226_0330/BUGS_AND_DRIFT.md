# Bugs and Drift (Truth Map)

## Identified Drift Issues

### 1. Logbook Status & Feedback Drifts
- **Mismatch**: Backend model field vs View attribute.
- **Location**: `backend/sims/logbook/models.py` vs `backend/sims/logbook/api_views.py`.
- **Evidence**:
  - Model: `supervisor_feedback` (Line 534)
  - View: `entry.supervisor_comments = feedback` (Line 141)
- **Impact**: Server crash (AttributeError) when a supervisor tries to approve an entry with feedback.

### 2. Notification Model Schema Drift
- **Mismatch**: Notification creation logic is using old/wrong field names.
- **Location**: `backend/sims/logbook/models.py:726`.
- **Evidence**:
  ```python
  Notification.objects.create(
      user=self.supervisor, # Error: Should be 'recipient'
      title=...,
      message=...,          # Error: Should be 'body'
      type="logbook_submission", # Error: Should be 'verb'
      related_object_id=self.id, # Error: No such field (should be in metadata)
  )
  ```
- **Impact**: Notification delivery fails silently or crashes the `save()` method.

### 3. Duplicate Department Models
- **Drift**: Split definitions for the same organizational unit.
- **Location 1**: `sims.academics.models.Department` (Academic/Batch focus).
- **Location 2**: `sims.rotations.models.Department` (Clinical/Hospital focus).
- **Impact**: Impossible to maintain a single source of truth for "Department Head" or "Department Code".

### 4. Logbook Vocabulary Mismatch
- **Vocabulary**: `pending` vs `submitted`.
- **Evidence**: The backend uses `status="pending"` for entries that are "submitted to supervisor". The frontend `LogbookEntry` interface (TS) uses `submitted_at` but the backend model uses `submitted_to_supervisor_at`.

## Exact File Locations for Reference
- `backend/sims/logbook/models.py`: `LogbookEntry` definition.
- `backend/sims/logbook/api_views.py`: `VerifyLogbookEntryView` logic.
- `backend/sims/notifications/models.py`: `Notification` schema.

## Known Unknowns
- Are there other apps (e.g. `certificates`) also using the broken notification call?

## Immediate Next Actions
1. Run a global grep for `Notification.objects.create` and verify all calls match the schema in `sims.notifications`.
2. Determine which `Department` model should be the "Master" and refactor the other as a Proxy or Foreign Key.
