# Bulk Import Implementation Summary

## Overview

This document summarizes the implementation of the bulk CSV import functionality for supervisors and residents in the SIMS system.

## What Was Implemented

### 1. Enhanced Bulk Service (`sims/bulk/services.py`)

#### New Functions:
- **`_generate_secure_password(length=12)`**: Generates secure random passwords with uppercase, lowercase, digits, and special characters
- **`_generate_password_from_username(username, year=None)`**: Generates deterministic passwords (format: `{username}@{year}!` for residents, `{username}@123!` for supervisors)
- **`_parse_csv_rows(uploaded_file, required_columns=None)`**: Unified CSV/Excel parser that supports both formats with flexible column matching

#### New Methods:
- **`BulkService.import_supervisors()`**: Imports supervisor/faculty accounts from CSV/Excel
  - Creates accounts with role `supervisor`
  - Generates passwords automatically
  - Handles department linking (optional)
  - Validates specialty codes
  - Supports dry-run and partial import modes

- **`BulkService.import_residents()`**: Imports postgraduate resident accounts from CSV/Excel
  - Creates accounts with role `pg`
  - Links to supervisors (creates if missing)
  - Handles edge cases (residents without supervisors)
  - Validates year, specialty, and supervisor requirements
  - Tracks unlinked residents in response
  - Supports dry-run and partial import modes

#### Enhanced Functions:
- **`_get_or_create_supervisor()`**: Enhanced to accept specialty parameter and password generation option

### 2. New Serializers (`sims/bulk/serializers.py`)

- **`SupervisorImportSerializer`**: Serializer for supervisor import requests
  - Fields: `file`, `dry_run`, `allow_partial`, `generate_passwords`

- **`ResidentImportSerializer`**: Serializer for resident import requests
  - Fields: `file`, `dry_run`, `allow_partial`, `generate_passwords`

### 3. New API Views (`sims/bulk/views.py`)

- **`BulkSupervisorImportView`**: API endpoint for supervisor imports
  - `POST /api/bulk/import-supervisors/`
  - Requires authentication
  - Returns bulk operation results

- **`BulkResidentImportView`**: API endpoint for resident imports
  - `POST /api/bulk/import-residents/`
  - Requires authentication
  - Returns bulk operation results including unlinked residents

### 4. Updated URLs (`sims/bulk/urls.py`)

- Added route: `/api/bulk/import-supervisors/`
- Added route: `/api/bulk/import-residents/`

## Features

### Password Generation
1. **Deterministic Passwords** (default):
   - Supervisors: `{username}@123!`
   - Residents: `{username}@{year}!`

2. **Secure Random Passwords**:
   - 12-character passwords with mixed case, digits, and special characters
   - Used when `generate_passwords=false`

### CSV Support
- Supports both CSV and Excel (`.xlsx`, `.xls`) formats
- Flexible column matching (case-insensitive)
- Handles missing optional columns gracefully
- Validates required columns

### Error Handling
- Comprehensive error messages with row numbers
- Validation errors with specific field issues
- Handles missing supervisors, departments, and other edge cases
- Transaction rollback on failure (when `allow_partial=false`)

### Edge Cases Handled
1. **Missing Supervisors**: 
   - Attempts to create if name provided
   - Can continue with `allow_partial=true`
   - Tracks unlinked residents in response

2. **Missing Departments**: 
   - Continues without department if `allow_partial=true`
   - Warns in response

3. **Duplicate Usernames**: 
   - Auto-generates unique usernames with numeric suffix

4. **Existing Users**: 
   - Updates existing records instead of creating duplicates
   - Updates password if `generate_passwords=true`

5. **Invalid Specialty/Year**: 
   - Validates against allowed values
   - Provides helpful error messages

## CSV Format Specifications

### Supervisor Import

**Required Columns:**
- `Name` (or `First Name` + `Last Name`)
- `Specialty`

**Optional Columns:**
- `Email`
- `Department`
- `Phone` / `Phone Number`
- `Registration Number` / `Reg No`
- `Username`

### Resident Import

**Required Columns:**
- `Name` (or `First Name` + `Last Name`)
- `Year` (1, 2, 3, or 4)
- `Specialty`
- `Supervisor Name` or `Supervisor Username` (unless `allow_partial=true`)

**Optional Columns:**
- `Email`
- `Department`
- `Phone` / `Phone Number`
- `Registration Number` / `Reg No`
- `Username`
- `Date of Joining` / `Date Of Joining`

## API Endpoints

### Supervisor Import
```
POST /api/bulk/import-supervisors/
Content-Type: multipart/form-data

Parameters:
- file: CSV/Excel file (required)
- dry_run: boolean (default: true)
- allow_partial: boolean (default: false)
- generate_passwords: boolean (default: true)
```

### Resident Import
```
POST /api/bulk/import-residents/
Content-Type: multipart/form-data

Parameters:
- file: CSV/Excel file (required)
- dry_run: boolean (default: true)
- allow_partial: boolean (default: false)
- generate_passwords: boolean (default: true)
```

## Response Format

Both endpoints return:
```json
{
  "operation": "import",
  "status": "completed" | "failed",
  "success_count": 10,
  "failure_count": 2,
  "details": {
    "successes": [...],
    "failures": [...],
    "unlinked_residents": [...]  // Only for resident import
  },
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:05Z"
}
```

## Validation Rules

### Supervisor Validation
- Name required
- Specialty must be valid (from SPECIALTY_CHOICES)
- Email auto-generated if missing
- Username auto-generated if missing

### Resident Validation
- Name required
- Year must be 1, 2, 3, or 4
- Specialty must be valid
- Supervisor required (unless `allow_partial=true`)
- Email auto-generated if missing
- Username auto-generated if missing

## Workflow

### Recommended Import Flow

1. **Import Supervisors First**
   ```bash
   # Validate
   curl .../import-supervisors/ -F "dry_run=true" -F "file=@supervisors.csv"
   
   # Import
   curl .../import-supervisors/ -F "dry_run=false" -F "file=@supervisors.csv"
   ```

2. **Import Residents Second**
   ```bash
   # Validate
   curl .../import-residents/ -F "dry_run=true" -F "file=@residents.csv"
   
   # Import
   curl .../import-residents/ -F "dry_run=false" -F "file=@residents.csv"
   ```

3. **Handle Unlinked Residents**
   - Review `unlinked_residents` from response
   - Manually link via admin interface
   - Or create missing supervisors and re-import

## Testing Recommendations

1. **Test with dry_run first**: Always validate CSV before actual import
2. **Test edge cases**: 
   - Missing supervisors
   - Invalid specialty codes
   - Duplicate usernames
   - Missing required columns
3. **Test partial imports**: Use `allow_partial=true` to test error handling
4. **Verify passwords**: Check that passwords are generated correctly
5. **Check supervisor linking**: Verify residents are linked to correct supervisors

## Files Modified

1. `sims/bulk/services.py` - Added import methods and utilities
2. `sims/bulk/serializers.py` - Added import serializers
3. `sims/bulk/views.py` - Added import views
4. `sims/bulk/urls.py` - Added import routes

## Files Created

1. `docs/BULK_IMPORT_GUIDE.md` - User guide with examples
2. `docs/BULK_IMPORT_IMPLEMENTATION_SUMMARY.md` - This document

## Next Steps

1. Test the implementation with sample CSV files
2. Create sample CSV templates for users
3. Add frontend UI for bulk imports (if needed)
4. Add logging/audit trail enhancements
5. Consider adding email notifications for imported users

## Notes

- The implementation follows the existing code patterns in the codebase
- Password generation is secure but predictable for first-time login
- Supervisor auto-creation uses the specialty from the resident record
- Department linking is optional and requires departments to exist in the system
- The system tracks unlinked residents for manual follow-up
