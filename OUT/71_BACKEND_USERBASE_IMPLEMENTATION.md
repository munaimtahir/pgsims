# 71 — Backend Userbase Implementation

## Final Model Set
- Canonical existing:
  - `rotations.Hospital`
  - `academics.Department`
  - `rotations.HospitalDepartment`
- Added in `sims.users.models`:
  - `StaffProfile`
  - `ResidentProfile`
  - `DepartmentMembership`
  - `HospitalAssignment`
  - `SupervisorResidentLink`
  - `HODAssignment`

## Key Constraints/Validation
- `HospitalDepartment`: unique `(hospital, department)` (existing canonical matrix)
- `DepartmentMembership`:
  - one active primary membership per user (`uniq_active_primary_dept_member_user`)
  - date validity check (`end_date >= start_date`)
  - `member_type` must match user role
- `HospitalAssignment`: date validity check
- `SupervisorResidentLink`:
  - active unique `(supervisor_user, resident_user, department)` link
  - role constraint: supervisor/faculty -> resident/pg
- `HODAssignment`:
  - one active HOD per department (`uniq_active_hod_assignment_per_department`)
  - role constraint: `hod_user` in `faculty|supervisor`
- Role expansion:
  - `User.role` now supports `resident` and `faculty` (legacy `pg` still supported).

## Migration IDs
- `sims/users/migrations/0002_alter_historicaluser_role_and_more.py`
  - role/supervisor field alterations
  - all six userbase models
  - indexes + constraints listed above.

## Admin Registrations
- Existing operational registrations retained:
  - `Hospital`, `HospitalDepartment` (`sims.rotations.admin`)
  - `Department` (`sims.academics.admin`)
- New registrations added (`sims.users.admin`):
  - `StaffProfileAdmin`
  - `ResidentProfileAdmin`
  - `DepartmentMembershipAdmin`
  - `HospitalAssignmentAdmin`
  - `SupervisorResidentLinkAdmin`
  - `HODAssignmentAdmin`

## Backend Gate Evidence
- `python manage.py check` ✅
- `python manage.py migrate --noinput` ✅
- Targeted regression tests:
  - `sims.users.test_userbase_api` ✅
  - `sims._devtools.tests.test_rbac_api` ✅
  - Truth test `sims.logbook.test_api...submit_return...` ✅
- Full backend suite:
  - `python manage.py test --failfast` ✅ (292 tests local venv)
