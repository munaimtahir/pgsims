# Compatibility Review

This document records the compatibility state of the Brick 7 supervision spine.

## New Supervision Spine

The new supervision app uses:

- `backend/sims/supervision/models.py`
- `backend/sims/supervision/services.py`
- `backend/sims/supervision/views.py`
- `backend/sims/supervision/serializers.py`

It provides the canonical assignment model and endpoints under `/api/supervision/`.

## Legacy `SupervisorResidentLink`

The old `SupervisorResidentLink` model symbol still exists in the repository for historical model/migration/tests coverage, but it is no longer used by active supervision flows.

### Not used by active code

- `backend/sims/supervision/*`
- `backend/sims/training/views.py`
- `backend/sims/users/userbase_views.py`
- `backend/sims/users/userbase_serializers.py`
- `backend/sims/bulk/services.py`
- `backend/sims/bulk/userbase_engine.py`
- `frontend/lib/api/departments.ts`
- `frontend/lib/api/userbase.ts`
- resident dashboard supervision section
- supervisor dashboard supervision section

### Historical only

- `backend/sims/users/models.py`
- `backend/sims/users/admin.py`
- `backend/sims/users/migrations/*`
- test fixtures and archive snapshots that intentionally preserve historical references

## Conclusion

Active API, service, frontend, permission, and dashboard paths now resolve through `ResidentSupervisorAssignment` and `/api/supervision/*`. `SupervisorResidentLink` remains historical only.
