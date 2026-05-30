# PGSIMS Testing and QA Guide

Quality Assurance in PGSIMS is driven by backend unit tests, frontend component tests, and Playwright E2E integration tests.

## Running Tests

### 1. Backend Pytest
Run unit tests with:
```bash
cd backend
SECRET_KEY=test-secret pytest sims -v
```
To run backend test coverage:
```bash
cd backend
pytest sims --cov=sims --cov-report=html
```

### 2. Frontend Checks
Run tests, linter, typecheck, and build:
```bash
cd frontend
npm test -- --watch=false
npm run lint
npx tsc --noEmit
npm run build
```

### 3. E2E Playwright Tests
To execute E2E tests:
1. Seed E2E database:
   ```bash
   cd backend && python3 manage.py seed_e2e
   ```
2. Run Playwright:
   ```bash
   cd frontend
   npm run test:e2e:smoke:local
   ```

## Gates and Thresholds
Before declaring a release ready, the codebase must pass all validation gates:
- **Strict OpenAPI Schema**: 0 errors.
- **E2E Integration Suite**: 100% tests passing.
- **Backend Line Coverage**: >=95%.
- **Frontend Line Coverage**: >=90%.
- **Unauthorized Paths**: All secured routes redirect or deny access appropriately.

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

