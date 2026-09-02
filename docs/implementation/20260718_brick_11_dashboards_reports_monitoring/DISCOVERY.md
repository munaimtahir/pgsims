# Discovery - Brick 11 Dashboards, Reports, Exports, and Operational Monitoring

## Current State Analysis
Our application currently has:
1. **Universal Identity & Profiles**: Role-scoped profiles mapping to 4 primary roles: `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF`.
2. **Masters & Supervision Spine**: Canonical supervision mappings via `ResidentSupervisorAssignment`.
3. **Academic Training Records**: Spine tracking with `ResidentTrainingRecord`.
4. **Academic Workflows (Brick 9-10)**: Templates, categories, submissions, reviews, and data quality check helpers.

## Report Requirements
We need to implement dashboards, summaries, reports, and CSV exports for:
1. **Admin Monitoring Dashboard** (`GET /api/academics/monitoring/admin-dashboard/`): Global counts of records, supervisors, evaluations/logbooks, review states, and department breakdowns.
2. **Supervisor Workload Dashboard** (`GET /api/academics/monitoring/supervisor-dashboard/`): Filtered list of assigned resident records, pending reviews, and overdue counts.
3. **Resident Progress Dashboard** (`GET /api/academics/monitoring/my-progress/`): Self progress view, requirements, supervisors, evaluations, and logbooks.
4. **Department/Program/Session Monitoring**: Global aggregation counts for master data groups.
5. **Resident Progress Report** (`GET /api/academics/reports/resident-progress/` & `[id]/`): Detail summary of resident training.
6. **Supervisor Workload Report** (`GET /api/academics/reports/supervisor-workload/`): Workload tracking per supervisor.
7. **Evaluation & Logbook Reports**: Filterable record listing reports with CSV export capabilities.
8. **Data Quality Report**: Identifying validation warning list groups.

## Plan
1. Implement report services inside `backend/sims/academics/reporting.py`.
2. Implement serializer modifications and DRF views in `backend/sims/academics/views.py`.
3. Wire the endpoint routes in `backend/sims/academics/workflow_urls.py`.
4. Update the frontend API helpers in `frontend/lib/api/academics.ts`.
5. Integrate views on the frontend and ensure all validation gates pass.
