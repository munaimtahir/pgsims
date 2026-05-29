# PGSIMS Bulk Import Workflow

PGSIMS supports bulk setup and user onboarding via CSV imports. The import engine features a dry-run validation stage to ensure data consistency before commit.

## Supported Import Types
1. **Hospitals**: Upload of clinical training centers.
2. **Departments**: Upload of specialties.
3. **Hospital-Department Matrix**: Maps active department sites to hospitals.
4. **Supervisors**: Onboards supervisors, staff profiles, and memberships.
5. **Residents**: Onboards residents, profiles, home affiliations, and programs.
6. **Supervisor Assignments**: Bulk supervisor-resident links.
7. **Rotation Placements**: Bulk placement history.

## Dry-Run Validation Rules
Every bulk import undergoes a **Dry-Run** check which parses the file and reports:
- **Total Rows**: Total records detected in CSV.
- **Valid Rows**: Records passing formatting and schema validation.
- **Invalid Rows**: Records failing field formats (e.g., malformed email, missing required fields).
- **Duplicate Rows**: Records with duplicate unique keys (e.g., existing username, code, or email).
- **Ready for Import**: Rows cleared for database write.
- **Blocked Rows**: Rows that will be skipped.

### Trainee CSV Column Specification
- `username` (Required, string, unique)
- `email` (Required, email, unique)
- `first_name` (Required, string)
- `last_name` (Required, string)
- `pgr_id` (Required, string)
- `home_hospital_code` (Required, string, must exist in Hospital)
- `home_department_code` (Required, string, must exist in Department)
- `training_start` (Required, Date `YYYY-MM-DD`)
- `program_code` (Required, string, must exist in TrainingProgram)
- `level` (Required, choice `y1` to `y5`)
- `registration_number` (Optional, string)
- `phone_number` (Optional, string)

If validations fail, the system rolls back and outputs a detailed error report without writing to the database.
