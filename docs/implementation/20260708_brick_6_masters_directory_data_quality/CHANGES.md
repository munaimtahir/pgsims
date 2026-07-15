# CHANGES — PGMS Brick 6 Masters and Data Quality

The following changes were implemented to satisfy all Workstreams of Brick 6:

---

## 1. Backend Code Changes
- **Models (`sims/academics/models.py`)**:
  - Created `Institution`, `Specialty`, `Designation`, and `AcademicSession` models.
  - Added `__eq__` and `__hash__` methods to compare master models to strings transparently.
- **Models (`sims/rotations/models.py`)**:
  - Added `institution` ForeignKey relationship to the `Hospital` model.
- **Models (`sims/users/models.py`)**:
  - Updated `ResidentProfile` (`academic_session_ref`, `specialty_ref`) and `SupervisorProfile` (`designation_ref`, `specialty_ref`) to use ForeignKeys with `to_field="code"`.
  - Added `SafeForeignKeyDescriptor` wrapper to safely intercept and resolve string values assigned to ForeignKeys, preserving test assertions and legacy datasets.
- **Serializers (`sims/academics/serializers.py` & `sims/users/userbase_serializers.py`)**:
  - Created Django Rest Framework (DRF) serializers for all new master models.
  - Explicitly configured `SlugRelatedField` on profiles to map foreign keys as strings (codes) to/from client payloads.
- **Views & Routes (`sims/academics/views.py` & `sims/academics/urls.py` & `sims_project/urls.py`)**:
  - Implemented DRF ViewSets for all 7 master models.
  - Configured `/api/masters/` URL prefix routing to direct requests to the master viewsets.
  - Updated `IdentityOptionsView` to load values dynamically from the database.
  - Implemented detailed `/api/data-quality/` endpoint to compute 16 data quality metrics and drill-down lists.
- **Onboarding (`sims/users/services.py` & `sims/users/userbase_views.py`)**:
  - Added lookups in `create_user_with_profile` and `CompleteProfileView` to resolve string code values to ForeignKey master objects.
  - Updated `PROFILE_COMPLETION_REQUIREMENTS` registry to include `hospital`, `department_ref`, `program_ref`, `academic_session_ref`, and `designation_ref` as completion required fields.
- **Management Command (`sims/users/management/commands/seed_pilot_masters.py`)**:
  - Created `seed_pilot_masters` command to seed FMU, Allied Hospital, DHQ, Medicine, Surgery, FCPS, MS, and designations idempotently.

---

## 2. Frontend Code Changes
- **API Client (`frontend/lib/api/auth.ts` & `frontend/lib/api/userbase.ts`)**:
  - Registered `getIdentityOptions` and `getDataQuality` API requests.
  - Extended `UserbaseUserUpsert` to accurately type profile and user optional properties.
- **Onboarding View (`frontend/app/complete-profile/page.tsx`)**:
  - Added options prefetching and dynamic rendering of `<select>` dropdowns for select-type fields.
- **New User Form (`frontend/app/users/new/page.tsx`)**:
  - Wired live master options and dynamically displayed optional profile selection fields (hospitals, departments, programs, sessions, designations) based on the selected user role.
- **Data Quality Dashboard (`frontend/app/dashboard/utrmc/data-quality/page.tsx`)**:
  - Re-implemented the data quality dashboard to use the new `/api/data-quality/` summary and display drill-down sections for all 16 categories.
