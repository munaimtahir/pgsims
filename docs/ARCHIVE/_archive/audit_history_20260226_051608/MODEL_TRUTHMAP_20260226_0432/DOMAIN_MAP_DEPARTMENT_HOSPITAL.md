# Domain Map: Department & Hospital

## Current Concepts
### Department
There are currently two detached representations of "Department" in the database schema:
1. `backend/sims/academics/models.py:16` - **academics.Department**
   - Concept: Strictly academic tracking. Groups program `Batch` entities together.
   - Fields: `name`, `code`, `description`, `active`, and FK `head` (User).
2. `backend/sims/rotations/models.py:83` - **rotations.Department**
   - Concept: Clinical deployment unit stationed under a hospital.
   - Fields: `name`, FK `hospital` (rotations.Hospital), `head_of_department` (Char, not FK!), `is_active`.
   - Structural constraint: `unique_together = ["hospital", "name"]`. A single real-world Department operating in 5 hospitals requires 5 separate `rotations.Department` entries.

### Hospital
`backend/sims/rotations/models.py:18` - **rotations.Hospital**
- Concept: Location for clinical rotation deployments.
- Fields: `name`, `code`, `address`, `phone`, etc.
- No direct tie to academic structure, ONLY tied to `rotations.Department`.

## Current Rotations Linking
When a trainee creates a `Rotation` (`rotations.models.Rotation` line 157):
- They link it to an explicitly local `rotations.Department` (e.g. "Surgery at Hospital X") and a `rotations.Hospital` ("Hospital X"). The `save()` method sets `self.hospital = self.department.hospital`.

## Conflicts with Real-World Domain Reality
- **Canonical Department Missing**: In practice, a "Department of General Surgery" is a single academic entity that deploys trainees across multiple teaching hospitals. The database schema fractures this by demanding an N:N structure represented redundantly.
- **Char vs FK mapping**: `academics.Department.head` is a User FK, while `rotations.Department.head_of_department` is a plain `CharField`.
- **Scaling friction**: Adding a new hospital requires duplicating all departments into `rotations.Department` for that hospital. A resolving matrix (e.g., `HospitalDepartment` M2M mapping table) is required to bridge one canonical `Department` and multiple `Hospitals`.
