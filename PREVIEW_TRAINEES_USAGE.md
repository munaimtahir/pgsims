# How to Preview Trainee Import Data

## Overview
The `preview_trainees` command allows you to view all trainees and supervisors that will be created from the Excel file **without actually importing them** into the database.

## Usage

```bash
python manage.py preview_trainees <path_to_excel_file>
```

## Example

```bash
python manage.py preview_trainees /home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx
```

## Output

The command will display:

1. **Summary Information**
   - Total rows parsed from the Excel file
   - Number of valid trainees
   - Number of unique supervisors
   - Any warnings or errors

2. **Supervisors List**
   - Full name
   - Generated username
   - Generated email address

3. **Trainees List**
   - Full name
   - Generated username
   - Generated email address
   - Training year (calculated from join date)
   - Supervisor name

4. **Warnings/Errors** (if any)
   - Row numbers with issues
   - Description of the problem

## Benefits

- **No database changes**: Preview command does not create any records
- **Verify data before import**: Check usernames, emails, and other generated fields
- **Identify issues early**: See errors before running the actual import
- **Plan deployment**: Review the complete list of users and supervisors to be created

## Next Steps

After reviewing the preview:

1. Verify the data looks correct
2. Note any warnings or errors
3. Run the import with `--dry-run` flag for validation
4. Run the actual import once validated
