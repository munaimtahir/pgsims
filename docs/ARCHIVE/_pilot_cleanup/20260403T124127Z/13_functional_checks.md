# Functional Checks

Checks executed against the cleaned live system:

| Check | Result | Evidence |
| --- | --- | --- |
| Admin can log in | PASS | Django auth check returned `admin_login True` |
| Supervisors exist and list correctly | FAIL | `/api/users/?role=supervisor` returned count `0` |
| Residents exist and list correctly | FAIL | `/api/users/?role=resident` returned count `0` |
| Resident-supervisor linkage is correct | FAIL | `/api/supervision-links/` returned count `0` |
| Imported pilot records view/edit | FAIL | No pilot records exist because import did not run |
| Search/filter on imported residents | FAIL | No residents exist to search |
| No demo data appears in lists | PASS | `/api/users/?search=demo` returned empty; UI user page had `hasDemo: false` |
| Canonical departments remain visible | PASS | `/api/departments/` returned 5 canonical departments |
| Canonical hospital remains visible | PASS | `/api/hospitals/` returned only `UTRMC` |
| Notifications are clean | PASS | `/api/notifications/` returned count `0` |
| Dashboard loads after cleanup | PASS | UI reached `/dashboard/utrmc` and `/dashboard/utrmc/users` |
| Program/training areas survive empty state | PARTIAL | endpoints load with count `0`, but real pilot workflow not validated |

Functional interpretation:
- The cleaned system is stable and no longer visibly demo-driven.
- It is not operationally ready for pilot use because the real pilot records were not imported.

