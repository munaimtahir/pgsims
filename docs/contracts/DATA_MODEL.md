# Canonical Data Model (Locked, Simplified Names)

## Canonical entities

### Department (single canonical list)
- One university-wide list: Department A/B/C/D...
- Unique key: `code` (preferred) or normalized `name`.
- This is the ONLY Department model.
- Canonical table: `academics.Department`.

### Hospital (university sites)
- Multiple hospitals exist under the same university.
- Unique key: `code`.
- Canonical table stays as the existing `rotations.Hospital` model (class name: `Hospital`).

### HospitalDepartment (matrix)
- Represents which departments are hosted in which hospitals.
- (hospital, department) unique.

## Trainee home affiliation (stable until graduation)
For `User` with role=pg:
- `home_department` (FK Department)
- `home_hospital` (FK Hospital)

Home affiliation does not change during rotations.

## Rotation (posting)
A rotation is a time-bounded placement in a (Hospital, Department) pair.

Fields (simple names):
- `pg`
- `department` (FK Department)          # destination department
- `hospital` (FK Hospital)              # destination hospital
- Optional snapshots (audit isolation):
  - `source_department` (FK Department)
  - `source_hospital` (FK Hospital)
- `start_date`, `end_date`
- `status` (planned/ongoing/completed/cancelled/pending_approval)
- `approved_by`, `approved_at`

### Inter-hospital policy rule
If `hospital != home_hospital`:
- Allowed if the destination department is NOT available in the home hospital (missing HospitalDepartment row), OR
- Requires:
  - `override_reason`
  - approval by `utrmc_admin`

If `department == home_department` AND `hospital != home_hospital`:
- Always requires override_reason + `utrmc_admin` approval (rare exception).
