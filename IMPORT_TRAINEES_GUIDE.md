# Trainee Data Import Guide

## Overview
This guide explains how to import trainee data from the Excel file `Trainee_Data_Department_of_Urology.xlsx` into the SIMS application.

## Prerequisites

1. **Run the migration** to add urology specialty:
   ```bash
   python manage.py migrate users
   ```

2. **Ensure you have an admin user** in the system (the import will use an admin account)

## Import Methods

### Method 1: Using Django Management Command (Recommended)

```bash
# Step 1: Validate the data (dry run)
python manage.py import_trainees /home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx --dry-run --allow-partial

# Step 2: If validation passes, run the actual import
python manage.py import_trainees /home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx --allow-partial
```

**Command Options:**
- `--dry-run`: Validate data without creating records
- `--allow-partial`: Continue importing even if some rows fail
- `--admin-username USERNAME`: Specify admin username (default: import_admin)

### Method 2: Using API Endpoint

If you have API access configured:

**Endpoint:** `POST /api/bulk/import-trainees/`

**Request (multipart/form-data):**
- `file`: Excel file
- `dry_run`: true/false (default: true)
- `allow_partial`: true/false (default: false)

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/bulk/import-trainees/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx" \
  -F "dry_run=false" \
  -F "allow_partial=true"
```

## Expected Excel Format

The Excel file should have the following columns (first 5 columns are used):
1. **Sr. No.** - Serial number (ignored)
2. **Name of Trainee** - Full name (required)
3. **Date of Joining** - Join date (required)
4. **MS/FCPS** - Qualification type (optional)
5. **Supervisor Name** - Supervisor's name (optional, will be created if not found)

## What Happens During Import

1. **Name Parsing**: Full names are split into first_name and last_name
2. **Username Generation**: Creates usernames in `firstname.lastname` format
3. **Email Generation**: Creates emails as `username.pgr@pmc.edu.pk`
4. **Training Year**: Automatically calculated based on months since joining date
5. **Supervisor Creation**: If supervisor doesn't exist, creates one with specialty "urology"
6. **User Creation**: Creates User records with role="pg" and specialty="urology"

## Verification

After import, verify the data:

```bash
# Check imported trainees
python manage.py shell
>>> from sims.users.models import User
>>> trainees = User.objects.filter(role='pg', specialty='urology')
>>> print(f"Total trainees: {trainees.count()}")
>>> for t in trainees[:10]:
...     print(f"{t.username} - {t.get_full_name()} - Year {t.year}")
```

## Troubleshooting

### Common Issues

1. **"Missing required columns" error**
   - Ensure Excel file has "Name of Trainee" and "Date of Joining" columns
   - Column names are case-insensitive and can have variations

2. **"Supervisor is required" error**
   - Ensure Supervisor Name column is present
   - Or use `--allow-partial` flag to continue with missing supervisors

3. **Date parsing errors**
   - Supported formats: DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY, etc.
   - Check date format in Excel file

4. **Duplicate username errors**
   - System automatically appends numbers (e.g., john.doe2)
   - This is handled automatically

## Default Passwords

- **New trainees**: `changeme123` (should be changed on first login)
- **Auto-created supervisors**: `changeme123` (should be changed)

## Notes

- The import creates a default password `changeme123` for all new users
- Users should change their password on first login
- Supervisors are automatically created if they don't exist
- Training year is automatically calculated from joining date
- All trainees are assigned specialty "urology"
