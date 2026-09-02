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

## Flexible Column Mapping Import
The Flexible Column Mapping Import feature allows administrators to upload CSV or Excel files from arbitrary sources (like Google Forms or third-party systems) that do not match the fixed PGSIMS template.

### When to Use
- **Standard Template (Recommended)**: Use for bulk imports when you can easily conform your data to the standard PGSIMS layout templates. This is the default and safest route.
- **Custom File & Map Columns**: Use when you have a roster or sheet with non-standard column headers and want to map them on the fly.

### Target Import Types & Required Fields
- **Residents**: Requires mapping `email`, `full_name`, `specialty`, `year`, `training_start`.
- **Supervisors**: Requires mapping `email`, `full_name`, `role` (must be `faculty` or `supervisor`).
- **Resident Placement (Rotation Placements)**: Requires mapping `resident_email`, `hospital_code`, `department_code`, `start_date`, `end_date`.
- **Supervisor Assignment (Supervision Links)**: Requires mapping `supervisor_email`, `resident_email`, `start_date`.

### How to Use the Custom Flow
1. **Upload & Parse**: Choose the target import type, upload your CSV or Excel file, and select the sheet if Excel has multiple sheets.
2. **Column Mapping & Auto-Suggestions**:
   - The interface auto-suggests matches based on normalized headers (e.g. `CustomEmail` -> `email`).
   - Manually map any required fields that weren't auto-matched.
   - Leave optional fields unmapped if not present in your file.
   - (Optional) Save your mappings as a **Mapping Preset** for future uploads of the same format. You can also load existing presets.
3. **Dry-Run & Preview**:
   - Execute the Dry-Run. This transforms your custom rows in-memory and runs the standard validation engine.
   - **No database records are created at this step.**
   - Review the validation summary (total, valid, and error rows) and inspect the transformed preview grid.
   - If there are errors, download the **Error Report CSV** to see detailed row-by-row error descriptions.
4. **Final Import**:
   - **Strict Mode (Default & Recommended)**: Rollback the entire transaction if any single row contains an error. This prevents importing partial/broken data.
   - **Partial Mode**: Import only valid rows and skip/log the failed ones.

