# Changes - Brick 11: Dashboards, Reports, and Exports

## Backend Changes
1. **academics/reporting.py**: Created to contain helper functions generating summary maps, monitoring metrics, filter queries, and data quality check sets.
2. **academics/views.py**: Registered APIViews for `AdminDashboardMonitoringView`, `SupervisorDashboardMonitoringView`, `MyProgressMonitoringView`, breakdowns, list/detail reports, and CSV exports.
3. **academics/workflow_urls.py**: Bound monitoring, reports, and CSV export URLs.
4. **academics/tests.py**: Added integration testing of dashboard views, filter options, scoping/permissions, and export pipelines.

## Frontend Changes
1. **lib/api/academics.ts**: Updated with `academicsApi` calls map for monitoring summaries, evaluation reports, logbooks, and details.
2. **app/academics/monitoring/page.tsx**: Interactive admin operational dashboard.
3. **app/academics/reports/resident-progress/page.tsx** & **[id]/page.tsx**: Listing and profile summary report views.
4. **app/academics/reports/supervisor-workload/page.tsx** & **[id]/page.tsx**: Supervisor detail workload reports.
5. **app/academics/reports/evaluations/page.tsx**: Filterable evaluation submissions audit table.
6. **app/academics/reports/logbook/page.tsx**: Case procedures and reflection logs details dashboard.
7. **app/academics/reports/data-quality/page.tsx**: Discrepancies report page.
