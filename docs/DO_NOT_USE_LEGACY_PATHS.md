# Do Not Use Legacy Paths

Do not build new UI or tests against these route families:

- `/dashboard/pg*`
- `/dashboard/resident/(progress|schedule|research|thesis|workshops|postings)`
- `/dashboard/supervisor/(research-approvals|residents/[id]/progress)`
- `/dashboard/utrmc/(users|supervisors|hospitals|departments|matrix|programs|backup|eligibility-monitoring|postings|onboarding)`

Do not build new frontend code against these deleted helpers:

- `frontend/lib/api/departments.ts`
- `frontend/lib/api/hospitals.ts`
- `frontend/lib/api/training.ts`

Do not use `SupervisorResidentLink` for new backend work. Use `ResidentSupervisorAssignment`.
