# Pre-Cleanup Row Counts

Source:
- `docs/_pilot_cleanup/20260403T124127Z/backups/precleanup-rowcounts.txt`

Important note:
- This snapshot came from the pre-cleanup database safety capture.
- It is suitable as a before-state audit reference.

Major pre-cleanup counts:

| Table | Count |
| --- | ---: |
| `users_user` | 24 |
| `users_staffprofile` | 5 |
| `users_residentprofile` | 9 |
| `users_supervisorresidentlink` | 9 |
| `users_departmentmembership` | 14 |
| `users_hospitalassignment` | 13 |
| `users_hodassignment` | 3 |
| `academics_department` | 12 |
| `rotations_hospital` | 8 |
| `rotations_hospitaldepartment` | 11 |
| `training_trainingprogram` | 5 |
| `training_residenttrainingrecord` | 10 |
| `training_rotationassignment` | 24 |
| `training_deputationposting` | 3 |
| `training_leaverequest` | 4 |
| `training_residentresearchproject` | 10 |
| `training_residentthesis` | 8 |
| `training_workshop` | 3 |
| `notifications_notification` | 15 |
| `notifications_notificationpreference` | 15 |
| `audit_activitylog` | 851 |

Notable pre-cleanup demo/test patterns found:
- usernames beginning with `demo_`
- usernames beginning with `e2e_`
- usernames including seeded `pg_`, `res_`, `sup_` pilot/e2e patterns
- departments including `DEMO-*`, `D########`, `TD*`, `SD*`
- hospitals including `DEMO-*`, `H########`, `TH*`, `SH*`
- programs including `DEMO-*`, `E2E-*`, `PROG-*`, `POLI-*`
- notifications with `metadata.seed_source = seed_demo_data`

Canonical data already present before cleanup:
- Departments: `MED`, `SURG`, `PED`, `OBG`, `ORTH`
- Hospital: `UTRMC`

