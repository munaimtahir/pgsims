# 76 — Deletion / Cleanup Report (Userbase Category)

## Removed Legacy Surfaces
- Removed duplicate legacy master-data API routes from rotations namespace:
  - deleted `/api/rotations/hospitals/*` routing
  - deleted `/api/rotations/hospital-departments/*` routing
- Removed now-unused legacy DRF viewsets from `sims.rotations.api_views`:
  - `HospitalViewSet`
  - `HospitalDepartmentViewSet`
- Removed now-unused legacy serializers from `sims.rotations.api_serializers`:
  - `HospitalSerializer`
  - `HospitalDepartmentSerializer`

## Why Safe
- Canonical replacements now exist and are active:
  - `/api/hospitals/*`
  - `/api/hospital-departments/*`
- Dependency audit confirmed no remaining backend references to removed legacy route paths after test updates.
- `_devtools` RBAC tests were updated to target canonical endpoints and pass.

## Dependency Audit Evidence
- Search for removed paths after cleanup:
  - pattern: `/api/rotations/hospitals/|/api/rotations/hospital-departments/`
  - scope: `backend/`
  - result: **no matches found**

## Verification
- `python manage.py check` ✅
- `python manage.py test --failfast` ✅
- `sims._devtools.tests.test_rbac_api` ✅ with canonical endpoint assertions.
