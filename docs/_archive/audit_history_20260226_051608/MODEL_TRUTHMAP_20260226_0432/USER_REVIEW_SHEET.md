# User Review Sheet: Model Truth-Map Decisions

Please review the following structural decisions deduced from the audit. For each decision, we present options, the technical impact, and our recommendation. 

**Instruction**: Reply to this sheet approving your choices (e.g., "I approve 1.A, 2.A, 3.B, etc.").

---

### 1. Canonical Department Entity
Currently, there are two models representing a "Department" (`academics.Department` and `rotations.Department`).
- **[ Option A ] (RECOMMENDED)**: Consolidate to a single canonical `academics.Department` (or move to a generic app like `core.Department`). Add all clinical fields to it. Drop `rotations.Department`.
- **[ Option B ]**: Keep them separate. Treat `academics.Department` as a "Program" container and `rotations.Department` simply as a physical clinical ward.
*Impact*: Option A makes the codebase DRY and domain-correct but requires a complex data migration mapping.

### 2. Hospital matrix referencing (HospitalDepartment)
If we use a single canonical Department (e.g., "General Surgery"), we must represent that it operates in multiple hospitals.
- **[ Option A ] (RECOMMENDED)**: Create a `HospitalDepartment` matrix table mapping `Hospital` <-> `Department`. Rotations will select this matrix row or select a Hospital + Canonical Department.
- **[ Option B ]**: Keep current logic: duplicate entire Department rows per hospital.
*Impact*: Option A scales infinitely if Vexel/SIMS expands to a massive multi-hospital network.

### 3. Trainee Home Designation
Currently, there are no fields indicating a PG's primary affiliation base, relying solely on batch or supervisor.
- **[ Option A ] (RECOMMENDED)**: Add `home_hospital` and `home_department` to `users.User` under the postgraduate block.
- **[ Option B ]**: Create a distinct `TraineeProfile` model extending the `User` with these clinical routing fields.
- **[ Option C ]**: Leave as is (rely on `Batch.department` and Supervisor hospital).
*Impact*: Option A is fastest and keeps Auth queries simple, but adds blank fields for Admin/Supervisor roles.

### 4. Rotation Movement Mapping
Real-world systems distinguish between a PG's "Home" status and their "Visitiation" target on rotations.
- **[ Option A ] (RECOMMENDED)**: Update `Rotation` to capture explicit `destination_hospital` and `destination_department`, checking it against the PG's `home_hospital` to deduce if it constitutes an "external rotation".
- **[ Option B ]**: Explicitly add `from_hospital` and `to_hospital` snapshot fields to the `Rotation` model at time of creation to isolate historical changes.

### 5. Inter-Hospital Rotation Policy Enforcement
When a rotation places a PG in a Hospital outside their designated "home" affiliation, how should the system enforce it?
- **[ Option A ] (RECOMMENDED)**: Soft-Block with Override. The system requires an `override_reason` field and elevates the rotation `status` to a special `pending_director_approval` state.
- **[ Option B ]**: Hard-block. Only administrators can schedule cross-hospital rotations.
