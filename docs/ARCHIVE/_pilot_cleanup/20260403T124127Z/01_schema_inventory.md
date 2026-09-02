# Schema Inventory

Deployment target:
- Compose project: `docker`
- Compose file: `docker/docker-compose.yml`
- Active backend container: `pgsims_backend`
- Active database container: `pgsims_db`

Database connection discovered from active env / compose:
- Engine: PostgreSQL
- Database: `sims_db`
- User: `sims_user`
- Host in compose network: `db`
- Effective backend URL pattern: `postgresql://sims_user:${DB_PASSWORD}@db:5432/sims_db`

Canonical structural entities confirmed:
- `academics_department`
- `rotations_hospital`
- `rotations_hospitaldepartment`
- `auth_permission`
- `django_migrations`
- `django_content_type`
- Celery beat schedule tables

User / auth tables:
- `users_user`
- `users_staffprofile`
- `users_residentprofile`
- `users_departmentmembership`
- `users_hospitalassignment`
- `users_hodassignment`
- `users_supervisorresidentlink`
- `users_historicaluser`

Training / runtime tables:
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
- `training_programmilestone`
- `training_programmilestoneresearchrequirement`
- `training_programmilestoneworkshoprequirement`
- `training_programpolicy`
- matching `training_historical*` tables

Notification / audit tables:
- `notifications_notification`
- `notifications_notificationpreference`
- `audit_activitylog`

Runtime vs structural split used for cleanup:
- Preserved as structural / master: canonical departments, canonical hospital, hospital-department matrix, permissions, migrations, content types, celery schedules, admin account, config.
- Treated as runtime and eligible for purge when clearly demo/e2e/test: residents, supervisors, links, training programs, training records, assignments, postings, leave, theses, research, workshops, notifications, demo activity logs, demo departments, demo hospitals.

Canonical university model preserved:
- One canonical hospital remains: `UTRMC`
- One canonical department set remains:
  - `MED`
  - `SURG`
  - `PED`
  - `OBG`
  - `ORTH`

