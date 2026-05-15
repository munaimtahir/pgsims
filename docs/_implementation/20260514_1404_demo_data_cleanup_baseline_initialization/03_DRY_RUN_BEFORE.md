# Dry Run Before Cleanup

## Command

```bash
docker exec pgsims_backend python manage.py reset_demo_data --dry-run
```

## Result

Dry-run completed successfully and reported the rows that would be deleted.

## Summary

- Total planned deletions: `881`

## Key Planned Deletions

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

## Evidence

The command printed counts before deletion and did not modify the database.

