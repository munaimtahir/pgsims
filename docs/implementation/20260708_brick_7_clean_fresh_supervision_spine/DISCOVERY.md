# DISCOVERY — PGMS Brick 7 Clean Fresh Pilot Supervision Spine

This document records the system discovery and compatibility review for **Brick 7**.

---

## 1. Current State Verification

- **Update 0 Verification**:
  - The four-role system (`ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`) is active and enforced.
  - HOD is removed as a role/profile/endpoint/dashboard. Only designation text metadata is permitted.
  - `/users/new` is the universal user creation center.
- **Brick 6 Verification**:
  - Master models and ViewSets for `Institution`, `Hospital`, `Department`, `TrainingProgram`, `Specialty`, `Designation`, and `AcademicSession` are active.
  - Identity options list dynamically from master tables.
  - Data-quality dashboard exists.
  - Seed commands and tests pass cleanly.

---

## 2. Compatibility Shims Classification

The following compatibility shims introduced in Brick 6 have been identified and classified:

1. **`SafeForeignKeyDescriptor`** (in `backend/sims/users/models.py`):
   - **Classification**: *Temporary compatibility debt / required by bulk engine*.
   - **Details**: Intercepts string assignments to ForeignKey fields in profiles. It is still required by the active `import_entity` bulk engine which parses strings from CSV rows, and by old test fixtures.
   - **Action**: Keep for now to avoid breaking existing userbase import/tests, but do NOT use in the new `supervision` app.

2. **`__eq__` and `__hash__` Overrides** (in `backend/sims/academics/models.py`):
   - **Classification**: *Temporary compatibility debt*.
   - **Details**: Allows comparing master model instances to strings in unit test assertions (e.g., `designation_ref == "Junior"`).
   - **Action**: Keep for now to prevent breaking unrelated legacy tests, but all new supervision tests must use clean object-level comparisons.

3. **`to_field="code"` ForeignKeys** (in `backend/sims/users/models.py`):
   - **Classification**: *Required by current active code*.
   - **Details**: Used on `academic_session_ref`, `specialty_ref`, and `designation_ref` to align with the string-based columns in the legacy schema.
   - **Action**: Keep for the existing profile fields. The new `ResidentSupervisorAssignment` model will use standard ID-based ForeignKeys.

---

## 3. Legacy Supervision Analysis

- **Existing Model**: `SupervisorResidentLink` exists in `backend/sims/users/models.py`.
- **Classification**: *Compatibility debt*.
- **Details**: The model is still used by legacy userbase/bulk/training code paths and by frontend API helpers that still target `/api/supervision-links/`.
- **Action**: Keep it isolated from the new supervision spine and do not expand its surface further.
