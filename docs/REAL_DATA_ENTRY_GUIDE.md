# PGSIMS Real Data Entry Guide

This document is the onboarding manual for administrative staff entering real trainee and supervisor records for the initial pilot launch.

## Prerequisites
Before any user data is imported:
1. Verify that `Hospital` list has correct codes (e.g. UTRMC).
2. Verify that `Department` list contains canonical specialties (e.g., Surgery `SURG`, Pathology `PATH`).
3. Ensure the matrix list (`HospitalDepartment`) represents actual active clinics.

## Steps for Data Entry

### Phase A: Preparing Roster CSV Files
Align source rosters to the templates under `pilot_data/first_pilot_run/`. Use placeholder emails in format `pgr###@placeholder.example.com` only if trainee email is unavailable.

### Phase B: Upload and Import Workspace
1. Log in as an **Admin** or **UTRMC Admin**.
2. Navigate to `/dashboard/utrmc` and select the **Bulk Setup** workspace.
3. Upload the prepared rosters sequentially:
   - `Hospitals CSV`
   - `Departments CSV`
   - `Matrix CSV`
   - `Supervisors CSV`
   - `Residents CSV`
   - `Supervisor Assignments CSV`
4. Click **Dry Run** for each file. Confirm there are **0 Invalid Rows** and **0 Duplicate Rows**.
5. Once dry-runs report success, click **Import** to save to the database.

## Post-Entry Verification
Navigate to `/dashboard/utrmc/users` and `/dashboard/utrmc/matrix` to verify that active residents and supervisors are listed in their respective departments and hospitals.

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

