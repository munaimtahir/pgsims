# Bulk Import Guide for Supervisors and Residents

This guide explains how to use the new bulk CSV import functionality for supervisors and residents in the SIMS system.

## Overview

The system now provides two separate bulk import endpoints:
1. **Supervisor Import** - For importing faculty/supervisor accounts
2. **Resident Import** - For importing postgraduate resident accounts (linked to supervisors)

Both imports support CSV and Excel file formats and include automatic password generation.

## API Endpoints

### 1. Supervisor Import
**Endpoint:** `POST /api/bulk/import-supervisors/`

**Purpose:** Bulk import supervisor/faculty accounts

**Request Parameters:**
- `file` (required): CSV or Excel file with supervisor data
- `dry_run` (optional, default: `true`): If `true`, validates without creating records
- `allow_partial` (optional, default: `false`): If `true`, continues on errors
- `generate_passwords` (optional, default: `true`): If `true`, generates deterministic passwords

**CSV Format - Required Columns:**
- `Name` (or `First Name` + `Last Name`)
- `Specialty` (required)

**CSV Format - Optional Columns:**
- `Email` - If not provided, will be generated as `{username}.supervisor@pmc.edu.pk`
- `Department` - Department name (must exist in system)
- `Phone` or `Phone Number`
- `Registration Number` or `Reg No`
- `Username` - If not provided, will be generated from name

**Example CSV:**
```csv
Name,Specialty,Email,Department,Phone,Registration Number
Dr. John Smith,Urology,john.smith@example.com,Department of Urology,+1234567890,REG123456
Dr. Jane Doe,Surgery,jane.doe@example.com,Department of Surgery,+1234567891,REG123457
Dr. Ahmed Khan,Medicine,,Department of Medicine,+1234567892,
```

**Specialty Values:**
Valid specialties include:
- `medicine`, `surgery`, `pediatrics`, `gynecology`, `orthopedics`
- `cardiology`, `neurology`, `urology`, `psychiatry`, `dermatology`
- `radiology`, `anesthesia`, `pathology`, `microbiology`, `pharmacology`
- `community_medicine`, `forensic_medicine`, `other`

### 2. Resident Import
**Endpoint:** `POST /api/bulk/import-residents/`

**Purpose:** Bulk import postgraduate resident accounts (linked to supervisors)

**Request Parameters:**
- `file` (required): CSV or Excel file with resident data
- `dry_run` (optional, default: `true`): If `true`, validates without creating records
- `allow_partial` (optional, default: `false`): If `true`, continues on errors (may create residents without supervisors)
- `generate_passwords` (optional, default: `true`): If `true`, generates deterministic passwords

**CSV Format - Required Columns:**
- `Name` (or `First Name` + `Last Name`)
- `Year` - Training year (1, 2, 3, or 4)
- `Specialty` (required)
- `Supervisor Name` or `Supervisor Username` (required, unless `allow_partial=true`)

**CSV Format - Optional Columns:**
- `Email` - If not provided, will be generated as `{username}.pgr@pmc.edu.pk`
- `Department` - Department name (must exist in system)
- `Phone` or `Phone Number`
- `Registration Number` or `Reg No`
- `Username` - If not provided, will be generated from name
- `Date of Joining` or `Date Of Joining` - Format: YYYY-MM-DD, DD/MM/YYYY, etc.

**Example CSV:**
```csv
Name,Year,Specialty,Supervisor Name,Email,Department,Phone,Registration Number,Date of Joining
Ahmed Ali,1,Urology,Dr. John Smith,ahmed.ali@example.com,Department of Urology,+1234567890,PG123456,2024-01-15
Fatima Khan,2,Surgery,Dr. Jane Doe,fatima.khan@example.com,Department of Surgery,+1234567891,PG123457,2024-02-01
Omar Hassan,1,Medicine,Dr. Ahmed Khan,omar.hassan@example.com,Department of Medicine,+1234567892,PG123458,2024-03-10
```

**Notes:**
- If a supervisor is specified by name but doesn't exist, the system will attempt to create it
- If `allow_partial=true` and supervisor cannot be found/created, resident will be created without supervisor (will need manual linking)
- Year must be one of: 1, 2, 3, or 4

## Password Generation

### Deterministic Passwords (Default)
When `generate_passwords=true`:
- **Supervisors:** Format: `{username}@123!`
- **Residents:** Format: `{username}@{year}!`

Example:
- Username: `john.smith`, Year: `2` → Password: `john.smith@2!`
- Username: `ahmed.ali`, Year: `1` → Password: `ahmed.ali@1!`

### Secure Random Passwords
When `generate_passwords=false`:
- Generates a secure 12-character password with uppercase, lowercase, digits, and special characters
- Passwords are included in the response for first-time distribution

## Response Format

Both endpoints return the same response format:

```json
{
  "operation": "import",
  "status": "completed",
  "success_count": 10,
  "failure_count": 2,
  "details": {
    "successes": [
      {
        "row": 2,
        "username": "john.smith",
        "name": "Dr. John Smith",
        "email": "john.smith.supervisor@pmc.edu.pk",
        "specialty": "urology",
        "password": "john.smith@123!",
        "department": "Department of Urology"
      }
    ],
    "failures": [
      {
        "row": 5,
        "error": "Missing 'Specialty'",
        "data": {...}
      }
    ],
    "unlinked_residents": [
      {
        "row": 8,
        "username": "test.user",
        "warning": "Created without supervisor - will need manual linking"
      }
    ]
  },
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:30:05Z"
}
```

## Error Handling

### Common Errors

1. **Missing Required Columns**
   - Error: `"Missing required columns: specialty, year"`
   - Solution: Ensure all required columns are present in the CSV

2. **Invalid Specialty**
   - Error: `"Invalid specialty 'XYZ'"`
   - Solution: Use valid specialty codes or names from the SPECIALTY_CHOICES list

3. **Invalid Year**
   - Error: `"Invalid year '5'. Must be one of: 1, 2, 3, 4"`
   - Solution: Use valid year values (1-4)

4. **Supervisor Not Found**
   - Error: `"Supervisor with username 'xyz' not found"`
   - Solution: Ensure supervisor exists or provide `Supervisor Name` to auto-create

5. **Department Not Found**
   - Warning: `"Department 'XYZ' not found. Continuing without department."`
   - Solution: Create department in system or leave blank

### Edge Cases Handled

1. **Residents Without Supervisors**
   - If `allow_partial=true`, residents can be created without supervisors
   - These are tracked in `unlinked_residents` in the response
   - Manual linking required after import

2. **Duplicate Usernames**
   - System automatically appends numbers to duplicate usernames
   - Example: `john.smith`, `john.smith1`, `john.smith2`

3. **Existing Users**
   - If a user with the same username exists, the record is updated instead of creating a new one
   - Password is updated if `generate_passwords=true`

## Usage Examples

### cURL Example - Supervisor Import

```bash
curl -X POST http://localhost:8000/api/bulk/import-supervisors/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@supervisors.csv" \
  -F "dry_run=false" \
  -F "allow_partial=false" \
  -F "generate_passwords=true"
```

### Python Example - Resident Import

```python
import requests

url = "http://localhost:8000/api/bulk/import-residents/"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
files = {"file": open("residents.csv", "rb")}
data = {
    "dry_run": False,
    "allow_partial": True,  # Allow residents without supervisors
    "generate_passwords": True
}

response = requests.post(url, headers=headers, files=files, data=data)
result = response.json()

print(f"Success: {result['success_count']}")
print(f"Failures: {result['failure_count']}")
print(f"Unlinked Residents: {len(result['details'].get('unlinked_residents', []))}")
```

### JavaScript Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('dry_run', 'false');
formData.append('allow_partial', 'true');
formData.append('generate_passwords', 'true');

fetch('/api/bulk/import-residents/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Success:', data.success_count);
  console.log('Failures:', data.failure_count);
});
```

## Best Practices

1. **Always use dry_run first**: Start with `dry_run=true` to validate your CSV before actual import
2. **Check for duplicates**: Ensure usernames don't conflict with existing users
3. **Verify supervisors exist**: For resident imports, ensure supervisors are imported first (or use `allow_partial=true`)
4. **Validate specialty codes**: Use the exact specialty codes or full names from the system
5. **Keep passwords secure**: Don't log or expose passwords in production environments
6. **Review unlinked_residents**: After import, check and manually link any residents without supervisors

## Workflow Recommendations

1. **Import Supervisors First**
   ```bash
   # Step 1: Validate supervisor CSV
   curl .../import-supervisors/ -F "dry_run=true" -F "file=@supervisors.csv"
   
   # Step 2: Import supervisors
   curl .../import-supervisors/ -F "dry_run=false" -F "file=@supervisors.csv"
   ```

2. **Import Residents Second**
   ```bash
   # Step 1: Validate resident CSV
   curl .../import-residents/ -F "dry_run=true" -F "file=@residents.csv"
   
   # Step 2: Import residents (with supervisors)
   curl .../import-residents/ -F "dry_run=false" -F "allow_partial=false" -F "file=@residents.csv"
   ```

3. **Handle Unlinked Residents**
   - Review `unlinked_residents` from the response
   - Manually link them to supervisors via the admin interface
   - Or create missing supervisors and re-import

## Troubleshooting

### Issue: All imports failing
- Check file format (must be CSV or Excel)
- Verify column names match exactly (case-insensitive)
- Check authentication token

### Issue: Passwords not working
- Verify password format matches the generation logic
- Check if password was changed by user
- Use password reset functionality

### Issue: Residents not linked to supervisors
- Check supervisor names match exactly
- Verify supervisors were imported first
- Check `unlinked_residents` in response
- Use `allow_partial=true` to create residents first, then link manually

### Issue: Validation errors
- Run with `dry_run=true` first to see all validation errors
- Fix all errors before running actual import
- Check specialty and year values are valid

## Schema Reference

### Department Model
- Required: `name`, `hospital` (Hospital must exist)
- Optional: `head_of_department`, `contact_email`, `contact_phone`, etc.

### User Model (Supervisor)
- Required: `username`, `role='supervisor'`, `specialty`
- Optional: `email`, `first_name`, `last_name`, `phone_number`, `registration_number`

### User Model (Resident/PG)
- Required: `username`, `role='pg'`, `specialty`, `year`, `supervisor`
- Optional: `email`, `first_name`, `last_name`, `phone_number`, `registration_number`

## Support

For issues or questions:
1. Check the error messages in the response
2. Review the edge cases section above
3. Use `dry_run=true` to validate before importing
4. Check logs for detailed error information
