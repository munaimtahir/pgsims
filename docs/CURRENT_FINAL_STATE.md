# PGSIMS Current Final State

## Application Metadata
- **App Name**: PGSIMS
- **Version**: Pilot Baseline v1.0
- **Status**: Real-Data Ready Candidate / GO
- **Branch**: `main`
- **Latest Commit Hash**: `2b28525a1ab47ade4b5c5c9bcb4cffd5e3e5e498`
- **Date/Time**: 2026-05-29T11:00:00Z

## Current Model Decision
The PGSIMS data model is strictly locked:
- **Hospital**: Canonical Hospital entity.
- **Department**: Single canonical department/specialty list (`academics.Department`). No separate academic vs rotation department models exist.
- **HospitalDepartment**: The only hospital-department matrix.
- **Resident Placements / Rotations**: Points directly to `HospitalDepartment`.
- **Supervisor Assignments**: Mapped within canonical department context.

## Cleanup Summary
- **Database Schema**: Deleted legacy undergraduate models `Batch` and `StudentProfile`.
- **Codebase Cleanups**: Removed unused directories, deprecated variables, and temporary files.
- **Documentation**: Archiving all presentation, staging, and discovery documents under `docs/ARCHIVE/`.

## Test Result Summary
- **Backend Unit Tests**: 358 passed / 358 total (100% success rate).
- **Django system check**: Passed (0 errors).
- **Migration dry-run**: No changes detected.

## Known Issues
- Playwright E2E tests have dashboard timing issues locally. Handled using explicit wait shims.

## Next Approved Step
- Deploy to the staging server and initiate the real data onboarding import workflow using the provided Urology pilot roster.

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

