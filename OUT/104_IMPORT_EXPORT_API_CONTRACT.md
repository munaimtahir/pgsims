# OUT/104 — Import/Export API Contract

## Endpoints

### Unified Import Endpoint
```
POST /api/bulk/import/<entity>/<action>/
```
- `entity`: hospitals | matrix | supervision-links | departments | supervisors | residents | trainees
- `action`: dry-run | apply
- Body: `multipart/form-data` with `file` field (CSV or XLSX)
- Auth: `utrmc_admin` or `admin` role required

**Response** (200 OK or 400 Bad Request):
```json
{
  "operation": "import",
  "status": "completed",
  "success_count": 3,
  "failure_count": 1,
  "details": {
    "successes": [{"row": 2, "code": "AH", "name": "Allied Hospital"}],
    "failures": [{"row": 4, "error": "Missing hospital_code", "data": {}}]
  },
  "dry_run": true
}
```

### Export Endpoint
```
GET /api/bulk/exports/<resource>/
```
- `resource`: hospitals | matrix | departments | supervisors | residents | supervision_links
- Query param: `file_format=csv` or `file_format=xlsx` (default: xlsx)
- Response: binary file attachment

### Legacy Import Endpoints (still available)
```
POST /api/bulk/import/              — generic logbook import
POST /api/bulk/import-trainees/     — trainee CSV import
POST /api/bulk/import-supervisors/  — supervisor CSV import
POST /api/bulk/import-residents/    — resident CSV import
POST /api/bulk/import-departments/  — department CSV import
```

## Template Files (static)
```
GET /templates/hospitals.csv
GET /templates/departments.csv
GET /templates/hospital_departments.csv
GET /templates/supervisors.csv
GET /templates/residents.csv
GET /templates/supervisor_resident_links.csv
```
