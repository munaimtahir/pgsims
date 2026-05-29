# Final Pilot Readiness Report

## A. What Was Found

Demo data existed in:
- demo/e2e/test users and linked staff/resident profiles
- demo/e2e/test departments and hospitals
- seeded training programs, resident training records, assignments, postings, leave, research, thesis, workshops
- demo notifications
- demo-linked activity logs

Mechanisms that could recreate it:
- explicit seed/demo commands in repo:
  - `seed_demo_data`
  - `seed_e2e`
  - `import_demo_cases`
  - sandbox preload / notification scripts
- active backend startup previously ran `create_superadmin`

Preserved:
- migrations
- permissions
- canonical departments
- canonical hospital
- canonical hospital-department matrix
- admin recovery account
- compose / env structure

Removed:
- all clearly demo/e2e/test runtime data from the live database
- demo/test departments and hospitals
- demo notifications
- demo-linked runtime training records and relationships

## B. What Was Imported

Imported in this run:
- Supervisors imported: `0`
- Residents imported: `0`
- Relationships imported: `0`

Why:
- real pilot roster values are still absent; the new source package is header-only
- live backend image does not currently contain the new import command because no rebuild was done

Placeholders used:
- none in live data, because no live import occurred

Validation warnings:
- source files created but still empty of real pilot rows
- import command prepared in repo only
- email backend still console-only

## C. Deployment Status

Services updated:
- `backend`
- `worker`
- `beat`

App path verified:
- backend health endpoint: `http://127.0.0.1:8014/healthz/`
- frontend: `http://127.0.0.1:8082`

Health:
- backend healthy
- frontend healthy
- database healthy
- redis healthy
- admin login working

## D. Pilot Readiness Verdict

`FAIL — not ready`

## E. Exact Blockers

1. Real pilot roster values are still missing; the new files under `pilot_data/first_pilot_run/` are intentionally blank until the real roster is entered.
2. The currently running backend image does not contain the new reusable import command because a full image rebuild was intentionally avoided to prevent deploying unrelated dirty-worktree changes.
3. The live system currently contains zero residents, zero supervisors, and zero supervisor-resident links.

## F. Final Tables

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

Bottom line:
- The system is cleaned and stable.
- It is not yet a real pilot system because the real pilot dataset has not been entered into the new source package and therefore has not been imported.
