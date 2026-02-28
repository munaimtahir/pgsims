# OUT/105 — Import/Export Templates

## Template Files

Located at `/frontend/public/templates/`:

| File | Entity | Stable Key | Required Columns |
|------|--------|-----------|-----------------|
| hospitals.csv | Hospitals | hospital_code | hospital_code, hospital_name |
| departments.csv | Departments | department_code | department_code, department_name |
| hospital_departments.csv | Matrix | hospital_code + department_code | both required |
| supervisors.csv | Supervisors | email | email, full_name, department_code |
| residents.csv | Residents | email | email, full_name, department_code |
| supervisor_resident_links.csv | Links | supervisor_email + resident_email | both emails required |

## Download URLs (served as static assets)
- `https://pgsims.alshifalab.pk/templates/hospitals.csv`
- `https://pgsims.alshifalab.pk/templates/departments.csv`
- `https://pgsims.alshifalab.pk/templates/hospital_departments.csv`
- `https://pgsims.alshifalab.pk/templates/supervisors.csv`
- `https://pgsims.alshifalab.pk/templates/residents.csv`
- `https://pgsims.alshifalab.pk/templates/supervisor_resident_links.csv`

## UI Download Location
- Templates page: `/dashboard/utrmc/data-admin/templates`
