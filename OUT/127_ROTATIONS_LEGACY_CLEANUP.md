# OUT/127 — Rotations Legacy Cleanup Report

Generated: 2026-03-01

## Summary
Phase 6 removed the legacy rotation API surface that conflicted with the new `sims/training/` module.
The legacy `Rotation` model was **retained** (see rationale below).

---

## What Was Removed

### 1. Legacy API URL Mount
**File**: `backend/sims_project/urls.py`

**Removed**:
```python
path("api/rotations/", include("sims.rotations.api_urls")),
```

**Reason**: This URL prefix intercepted `/api/rotations/<id>/utrmc-approve/` before the new training
ViewSet could handle it. The legacy handler only allowed PATCH; the new system uses POST. This caused
a 405 error on the critical UTRMC approval action.

**Effect**: The following legacy endpoints are now unreachable:
- `GET /api/rotations/my/` (superseded by `GET /api/my/rotations/`)
- `GET /api/rotations/my/{id}/` (superseded by `GET /api/rotations/{id}/` scoped to resident)
- `PATCH /api/rotations/{id}/utrmc-approve/` (superseded by `POST /api/rotations/{id}/utrmc-approve/`)

---

## What Was Kept (With Rationale)

### Legacy `Rotation` Model (`sims/rotations/models.py`)

**Decision: RETAINED**

**Reason**: `sims/logbook/models.py` has:
```python
rotation = models.ForeignKey("rotations.Rotation", ...)
```
Deleting the Rotation table would require:
1. A data migration to remove/null FK on all LogbookEntry records
2. Changes to logbook admin, API, serializers
3. Seed data refactoring (seed_demo_data.py creates Rotation + LogbookEntry pairs)

This is out of scope for Phase 6 and carries significant risk. The Rotation model is effectively
**superseded by RotationAssignment for new workflows** but retained for LogbookEntry FK integrity.

**Files using legacy Rotation (kept as-is):**
- `sims/rotations/api_urls.py` — no longer mounted; kept for reference
- `sims/rotations/api_views.py` — no longer reachable; kept for reference
- `sims/rotations/api_serializers.py` — no longer used via API; kept for reference
- `sims/rotations/services.py` — `evaluate_rotation_override_policy()` still used by domain
- `sims/rotations/forms.py` — Django admin forms; still valid
- `sims/users/management/commands/seed_demo_data.py` — creates demo Rotation rows (OK, table exists)
- `sims/users/management/commands/seed_e2e.py` — creates E2E Rotation rows (OK, table exists)

---

## Updated References

### `sims/users/models.py`
Updated 3 stat counter methods to query `RotationAssignment` instead of legacy `Rotation`:
```python
# Before
from sims.rotations.models import Rotation
count += Rotation.objects.filter(pg=user, status="pending").count()

# After
from sims.training.models import RotationAssignment
count += RotationAssignment.objects.filter(
    resident_training__resident_user=user, status="SUBMITTED"
).count()
```
These are dashboard stat counters — they now reflect the new training system's data.

### `sims/users/views.py`
Updated 4 view functions with same pattern as above. Dashboard "rotations_count" and "pg_progress_stats"
now use RotationAssignment queryset.

### `sims/rotations/test_canonical_migration_gate.py`
Removed 2 API tests that called the removed endpoints:
- `test_migration_gate_inter_hospital_same_department_requires_override_and_utrmc_approval` (used PATCH endpoint)
- `test_rotation_summary_api_returns_contract_shape` (used `/api/rotations/my/{id}/`)

Kept:
- `test_migration_gate_inter_hospital_same_department_requires_utrmc_approval` (domain logic only)
- `test_migration_gate_deficiency_rule_no_utrmc_approval_required` (domain logic only)

### `sims/_devtools/tests/test_rbac_api.py`
Replaced 2 failing tests with updated versions:
- `test_rotations_pg_only_sees_own_detail` → `test_rotations_pg_my_schedule_via_new_training_api`
  (tests `GET /api/my/rotations/`)
- `test_rotation_override_approval_requires_utrmc_admin` → `test_rotation_utrmc_approve_endpoint_requires_post_and_admin_role`
  (creates RotationAssignment, tests POST `/api/rotations/{id}/utrmc-approve/`)

---

## Test Results After Cleanup

```
Ran 302 tests in 21.682s
OK
```

All 302 backend tests pass. No regressions.

---

## Frontend Legacy Pages

The old `/dashboard/pg/rotations/page.tsx` uses `rotationsApi.getMyRotations()` which calls
`/api/rotations/my/` — now removed. This page still exists in the codebase but returns empty data
since the endpoint no longer exists. The replacement is `/dashboard/my-training/page.tsx` added
in Phase 3 which uses `/api/my/rotations/`.

**Recommended follow-up** (out of scope for this phase):
- Remove `/dashboard/pg/rotations/page.tsx`
- Remove `frontend/lib/api/rotations.ts` (legacy rotations API client)
- Update any navigation pointing to the old page

---

## Forbidden Pattern Scan

✅ No duplicate Department models introduced
✅ No legacy Notification keys introduced
✅ No direct DB state mutations bypassing audit trail
✅ Hospital/HospitalDepartment canonical entities unchanged
