# Gap Analysis

## Major Gaps Found

| Gap | Evidence | Effect | Resolution |
|---|---|---|---|
| Supervisor rotation visibility only matched department/HOD scope | `backend/sims/training/views.py` before `_get_rotation_scope()` reuse | Supervisor dashboard count and actionable queue could disagree for directly supervised residents | Unified direct-supervision and department scope across rotation list/inbox endpoints |
| Returned rotations could not actually be resubmitted | `RotationAssignmentViewSet.submit()` only accepted `DRAFT` | Resident schedule offered a resubmit path that backend rejected | `submit()` now accepts `RETURNED` and clears `return_reason` |
| Resident schedule used summary snapshot instead of real rotation records | `frontend/app/dashboard/resident/schedule/page.tsx` | Missing notes, return reason, reject reason, and submit actions | Switched to `GET /api/my/rotations/` and rendered real rotation records |
| No active UTRMC rotation operations surface | old `frontend/app/dashboard/utrmc/page.tsx` only showed counts | Backend lifecycle existed but could not be driven from the active frontend | Added draft creation and lifecycle queues/actions on the existing overview route |
| Resident postings create path missed required contract field | resident page sent only form fields, not `resident_training` | UI showed a create path that returned `400` at runtime | Resident postings now loads summary and sends `resident_training` |
| Postings UI assumed lowercase statuses | `frontend/app/dashboard/resident/postings/page.tsx` and `frontend/app/dashboard/utrmc/postings/page.tsx` | Status labels and UTRMC action buttons were wrong/missing against real API responses | Normalized UI checks to real uppercase backend status values |
| UTRMC postings route could imply write capability for `utrmc_user` | route accessible via direct URL | Read-only users could be misled about action capability | Added explicit read-only banner and action hiding |

## Drift Items Downgraded or Removed

- Resident postings draft/delete fiction was not reintroduced.
- No dedicated new rotation route was added.
- No deferred legacy surface was reactivated.

## Unresolved but Contained

- Posting and rotation coverage outside the promoted happy paths remains broader than this milestone verified.
- `README.md` and contract docs were updated, but older historical discovery/recovery packs remain historical records rather than rewritten current docs.
