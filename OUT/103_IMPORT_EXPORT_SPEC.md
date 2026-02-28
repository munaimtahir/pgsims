# OUT/103 — Import/Export Spec Lock

## Supported Entities
| Entity | Stable Key | API Entity Slug |
|--------|-----------|----------------|
| Hospitals | hospital_code | hospitals |
| Departments | department_code | departments |
| H-D Matrix | hospital_code + department_code | matrix |
| Supervisors | email | supervisors |
| Residents | email | residents |
| Supervision Links | supervisor_email + resident_email | supervision-links |

## Template Columns

### hospitals.csv
| Column | Required | Notes |
|--------|----------|-------|
| hospital_code | ✓ | Unique stable key, uppercase |
| hospital_name | ✓ | Human-readable name |
| active | - | true/false/yes/no/0/1 (default: true) |

### departments.csv
| Column | Required | Notes |
|--------|----------|-------|
| department_code | ✓ | Unique stable key |
| department_name | ✓ | Human-readable name |
| active | - | default: true |

### hospital_departments.csv (matrix)
| Column | Required | Notes |
|--------|----------|-------|
| hospital_code | ✓ | Must reference existing hospital |
| department_code | ✓ | Must reference existing department |
| active | - | default: true |

### supervisors.csv
| Column | Required | Notes |
|--------|----------|-------|
| email | ✓ | Unique identifier, used for upsert |
| full_name | ✓ | Full name (space-delimited) |
| phone | - | Phone number |
| role | - | supervisor \| faculty (default: supervisor) |
| department_code | ✓ | Primary department |
| hospital_code | - | Primary hospital |
| active | - | default: true |

### residents.csv
| Column | Required | Notes |
|--------|----------|-------|
| email | ✓ | Unique identifier |
| full_name | ✓ | Full name |
| phone | - | Phone number |
| role | - | resident (default) |
| pgr_id | - | PGR registration ID |
| training_start | - | YYYY-MM-DD |
| department_code | ✓ | Primary department |
| hospital_code | - | Primary hospital |
| active | - | default: true |

### supervisor_resident_links.csv
| Column | Required | Notes |
|--------|----------|-------|
| supervisor_email | ✓ | Must reference existing supervisor |
| resident_email | ✓ | Must reference existing resident |
| department_code | - | Optional department filter |
| start_date | - | YYYY-MM-DD |
| end_date | - | YYYY-MM-DD |
| active | - | default: true |

## Behavior on Conflicts
- **Upsert by stable key**: existing records are updated, not duplicated
- **dry-run**: validates rows, returns errors, no DB writes
- **apply**: writes to DB (with allow_partial=true so partial success is possible)
- **Row-level errors**: returned in `details.failures` array with row number and message
- **Referential integrity**: matrix/links rows fail if referenced codes don't exist
