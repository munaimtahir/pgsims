# Migration Risk Report

## Found Migrations Involving Key Models
Extracted from git history and migration files (`backend/sims/**/migrations/*`):
- `backend/sims/academics/migrations/0001_initial.py` (Creates `academics.Department`)
- `backend/sims/rotations/migrations/0001_initial.py` (Creates `Hospital`, `rotations.Department`, `Rotation`)
- `backend/sims/cases/migrations/0001_initial.py` (Links `logbook.LogbookEntry` to `Rotation`)
- `backend/sims/attendance/migrations/0001_initial.py` (Links Session to `Rotation`)

## Likely Data Migration Risks
If we unify the `Department` model into a canonical entity and add `HospitalDepartment` matrix structures, we encounter high-risk data transformation challenges:

1. **Orphaned Departments (`rotations.Department`)**
   - `rotations.Department` carries clinical data (`training_objectives`, `required_skills`, text-based `head_of_department`). `academics.Department` relies on FK linking for `head`.
   - **Risk Assessment**: Merging requires manual resolution of text string names to User FK profiles, risking data loss if unmatched.
2. **Loss of Location Specificity in Logbooks**
   - Current `Rotation` strictly owns the `rotations.Department` (which implies a hospital). If the schema shifts to `(Canonical Department) + (Hospital)`, old rotations must be successfully migrated to explicitly point to the `Hospital` ID rather than deriving it transitively via the old `rotations.Department`.
3. **Supervisor Mismatches**
   - If `trainee.home_hospital` rule locks are introduced, existing `Rotation` rows and `LogbookEntry` rows authored by PGs outside those rule parameters might violate database `CheckConstraint` structures during backwards migration running.

## Recommended Safety Strategy
1. Keep the old `rotations.Department` model transiently active. Do **not** drop it in Phase 1.
2. Build a new unified canonical `Department` model (perhaps expanding `academics.Department` into `core.Department`).
3. Create a Custom Python Migration (`RunPython`) to systematically parse every `rotations.Department`, find its `academics.Department` string match, update the matrix table (`HospitalDepartment`), and explicitly map the legacy records.
