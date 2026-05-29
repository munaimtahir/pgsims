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
