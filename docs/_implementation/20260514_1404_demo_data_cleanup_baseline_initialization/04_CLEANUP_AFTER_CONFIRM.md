# Cleanup After Confirm

## Command

```bash
docker exec pgsims_backend python manage.py reset_demo_data --confirm
```

## Result

Confirmed cleanup completed successfully.

## Deleted Rows

- `audit_activitylog: 397`
- `bulk_bulkoperation: 1`
- `training_logbookreview: 2`
- `training_logbookentry: 2`
- `training_logbookthresholdsnapshot: 6`
- `training_residentmilestoneeligibility: 9`
- `training_residentresearchproject: 4`
- `training_leave_request: 1`
- `training_programmilestoneresearchrequirement: 5`
- `training_programrotationrequirement: 1`
- `training_programmilestone: 5`
- `training_logbookthresholdconfig: 2`
- `training_programpolicy: 4`
- `training_submissionrequirementtemplate: 4`
- `training_residenttrainingrecord: 10`
- `training_trainingprogram: 9`
- `users_supervisorresidentlink: 7`
- `users_hodassignment: 4`
- `users_hospitalassignment: 3`
- `users_departmentmembership: 11`
- `users_staffprofile: 3`
- `users_residentprofile: 3`
- `users_user: 28`
- `rotations_hospitaldepartment: 3`
- `academics_department: 5`
- `rotations_hospital: 5`

## Historical Rows Removed

- `users_historicaluser: 232`
- `training_historicaltrainingprogram: 28`
- `training_historicalprogrampolicy: 11`
- `training_historicalprogrammilestone: 18`
- `training_historicalprogrammilestoneresearchrequirement: 21`
- `training_historicalprogramrotationrequirement: 6`
- `training_historicallogbookthresholdconfig: 12`
- `training_historicalresidenttrainingrecord: 40`
- `training_historicalleaverequest: 4`
- `training_historicalresidentresearchproject: 15`
- `training_historicallogbookentry: 9`
- `training_historicallogbookreview: 4`
- `training_historicalsubmissionrequirementtemplate: 24`

## Post-Cleanup State

- One admin/superuser remained available.
- Fake users, fake hospitals, fake departments, and the linked test operational rows were removed.
- Canonical master records were preserved and then re-initialized by the baseline command.

