# Migration Plan (Department/Hospital/Rotation Unification)

## Locked decisions
- Canonical Department table: keep `academics.Department`
- Remove legacy `rotations.Department` after cutover
- Canonical Hospital table: keep existing `rotations.Hospital`
- Department properties are department-specific (NOT hospital-specific)

## Principle
Additive → Backfill → Cutover → Cleanup (no breaking changes until cutover is complete).

## Phase 1 (Additive)
- Introduce `HospitalDepartment` matrix
- Add `home_department`, `home_hospital` to PG users
- Add Rotation fields:
  - `department` (FK academics.Department)
  - `hospital` (FK rotations.Hospital)
  - optional `source_*`
- Keep legacy `rotations.Department` temporarily (renamed to avoid confusion)

## Phase 2 (Backfill)
- Create mapping: rotations.Department(name, hospital) → academics.Department(name/code) + rotations.Hospital
- Backfill:
  - Rotation.department / Rotation.hospital
  - HospitalDepartment rows from existing legacy rotations.Department rows
  - User.home_department from StudentProfile.batch.department where available
  - User.home_hospital via deterministic rule (documented in audit report)
- Produce mapping report under docs/_audit/ (matches + unresolved)

## Phase 3 (Cutover)
- Update code to use canonical Department everywhere
- Update serializers + frontend SDK to use `rotation.department` and `rotation.hospital`
- Keep API backwards compatible until frontend updated

## Phase 4 (Cleanup)
- Remove legacy `rotations.Department`
- Add constraints:
  - (hospital, department) unique in HospitalDepartment
  - home fields required for role=pg (after backfill)
- Enforce override policy for inter-hospital rotations
