# Cleanup Actions

Actions executed:

1. Created safety artifacts under `docs/_pilot_cleanup/20260403T124127Z/backups/`.
2. Added reusable cleanup management command:
   - `backend/sims/users/management/commands/cleanup_pilot_runtime.py`
3. Dry-ran the cleanup plan to classify affected objects before deletion.
4. Applied the cleanup against the live database.
5. Fixed a deletion bug in the cleanup command caused by `delete()` after `distinct()`, then re-ran successfully.
6. Ran cleanup again to remove residual demo-tagged activity logs created during the first purge pass.
7. Removed `python manage.py create_superadmin` from backend startup in `docker/docker-compose.yml`.
8. Recreated `backend`, `worker`, and `beat` services without rebuilding images so the startup command change took effect without deploying unrelated dirty-worktree code.

Live cleanup intent:
- Remove demo/e2e/test runtime entities in dependency-safe order.
- Preserve canonical structure and the admin recovery account.

Reusable cleanup command:

```bash
python manage.py cleanup_pilot_runtime
python manage.py cleanup_pilot_runtime --apply
python manage.py cleanup_pilot_runtime --apply --keep-username admin
```

Scope of objects removed by the cleanup command:
- demo/e2e/test `users_user`
- `users_staffprofile`
- `users_residentprofile`
- `users_departmentmembership`
- `users_hospitalassignment`
- `users_hodassignment`
- `users_supervisorresidentlink`
- demo/test `academics_department`
- demo/test `rotations_hospital`
- linked `rotations_hospitaldepartment`
- `training_trainingprogram`
- `training_residenttrainingrecord`
- `training_rotationassignment`
- `training_deputationposting`
- `training_leaverequest`
- `training_residentresearchproject`
- `training_residentthesis`
- `training_workshop`
- `training_workshoprun`
- `training_workshopblock`
- milestone / policy / template records linked to demo programs
- `notifications_notification`
- demo-linked `audit_activitylog`
- matching simple-history rows for purged runtime entities

What was deliberately not removed:
- migrations
- permissions
- content types
- canonical departments
- canonical hospital
- canonical hospital-department matrix
- remaining admin account

