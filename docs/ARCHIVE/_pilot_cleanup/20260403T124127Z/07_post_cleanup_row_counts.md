# Post-Cleanup Row Counts

Source of final counts:
- Direct SQL counts against the cleaned live database after service recreate

Final major counts:

| Table | Final Count |
| --- | ---: |
| `users_user` | 1 |
| `users_staffprofile` | 0 |
| `users_residentprofile` | 0 |
| `users_supervisorresidentlink` | 0 |
| `users_departmentmembership` | 0 |
| `users_hospitalassignment` | 0 |
| `users_hodassignment` | 0 |
| `academics_department` | 5 |
| `rotations_hospital` | 1 |
| `rotations_hospitaldepartment` | 5 |
| `training_trainingprogram` | 0 |
| `training_residenttrainingrecord` | 0 |
| `training_rotationassignment` | 0 |
| `training_deputationposting` | 0 |
| `training_leaverequest` | 0 |
| `training_residentresearchproject` | 0 |
| `training_residentthesis` | 0 |
| `training_workshop` | 0 |
| `training_workshoprun` | 0 |
| `training_workshopblock` | 0 |
| `training_programmilestone` | 0 |
| `training_programmilestoneresearchrequirement` | 0 |
| `training_programmilestoneworkshoprequirement` | 0 |
| `training_programpolicy` | 0 |
| `training_residentmilestoneeligibility` | 0 |
| `notifications_notification` | 0 |
| `notifications_notificationpreference` | 1 |
| `audit_activitylog` | 43 |

History table spot-checks:

| Table | Final Count |
| --- | ---: |
| `users_historicaluser` | 7 |
| `training_historicaltrainingprogram` | 0 |
| `training_historicalresidenttrainingrecord` | 0 |
| `training_historicalrotationassignment` | 0 |
| `training_historicalresidentresearchproject` | 0 |
| `training_historicalresidentthesis` | 0 |
| `training_historicalworkshop` | 0 |
| `training_historicalworkshoprun` | 0 |
| `training_historicalworkshopblock` | 0 |
| `training_historicaldeputationposting` | 0 |
| `training_historicalleaverequest` | 0 |

Remaining intentional core data:
- User: `admin`
- Departments: `MED`, `SURG`, `PED`, `OBG`, `ORTH`
- Hospital: `UTRMC`

Post-cleanup data state:
- No residents remain
- No supervisors remain
- No pilot relationships remain
- No notifications remain
- No training programs remain
- No demo/test hospitals or departments remain

