# Instructions to Get Lists of Trainees and Supervisors

## Summary

I've reviewed the IMPORT_TRAINEES_GUIDE.md and created a preview command to help you extract and review all trainees and supervisors from the Excel file before importing them.

## What Has Been Created

1. **Preview Command**: `preview_trainees` management command
   - Location: `sims/users/management/commands/preview_trainees.py`
   - Purpose: Analyzes Excel file and displays all trainees and supervisors without importing

2. **Updated Guide**: Enhanced IMPORT_TRAINEES_GUIDE.md with preview instructions

3. **Usage Documentation**: PREVIEW_TRAINEES_USAGE.md with detailed instructions

## How to Get the Lists

Since the Excel file is not currently available in the expected location (`/home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx`), follow these steps:

### Step 1: Locate the Excel File

Find your Excel file with the trainee data. It should be named something like:
- `Trainee_Data_Department_of_Urology.xlsx`
- Or any Excel file containing the urology trainee data

### Step 2: Run the Preview Command

```bash
cd /home/munaim/srv/apps/pgsims
python manage.py preview_trainees /path/to/your/excel/file.xlsx
```

**Example:**
```bash
python manage.py preview_trainees /home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx
```

### Step 3: Review the Output

The command will display:

#### Supervisors List
- Full Name
- Generated Username
- Generated Email (format: username.supervisor@pmc.edu.pk)

#### Trainees List
- Full Name
- Generated Username
- Generated Email (format: username.pgr@pmc.edu.pk)
- Training Year (auto-calculated)
- Supervisor Name

#### Summary Statistics
- Total rows parsed
- Number of valid trainees
- Number of unique supervisors
- Any warnings or errors

## Alternative: Using Dry-Run Import

You can also use the existing import command with `--dry-run` flag:

```bash
python manage.py import_trainees /path/to/file.xlsx --dry-run --allow-partial
```

This will validate the data and show what would be imported, but the preview command provides a cleaner, more readable output focused on listing users and supervisors.

## What the Preview Command Shows

The preview command generates:

1. **All Unique Supervisors** that will be created/used:
   - Shows supervisor name
   - Generated username (firstname.lastname format)
   - Generated email address

2. **All Trainees** that will be imported:
   - Shows full name
   - Generated username
   - Generated email
   - Training year (calculated from join date)
   - Assigned supervisor

3. **Data Validation**:
   - Identifies missing required fields
   - Date parsing errors
   - Name parsing issues
   - Other validation problems

## Next Steps After Preview

1. Review the lists to ensure data is correct
2. Check for any warnings or errors
3. Verify usernames and emails are appropriate
4. If everything looks good, proceed with the actual import using:
   ```bash
   python manage.py import_trainees /path/to/file.xlsx --allow-partial
   ```

## Notes

- The preview command does **NOT** create any database records
- It's safe to run multiple times
- Usernames shown are the base format (duplicates will be handled with numbers during actual import)
- All trainees will be assigned specialty "urology"
- All auto-created supervisors will have specialty "urology"
