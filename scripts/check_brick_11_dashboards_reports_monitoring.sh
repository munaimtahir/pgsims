#!/bin/bash
set -e

# Brick 11 Dashboards, Reports, and Monitoring gate check script

echo "Verifying Brick 11 codebase boundaries..."

# 1. Check reporting service layer exists
if [ ! -f "backend/sims/academics/reporting.py" ]; then
    echo "reporting.py missing!"
    exit 1
fi

# 2. Check view class registrations
grep -q "AdminDashboardMonitoringView" backend/sims/academics/views.py || (echo "AdminDashboardMonitoringView missing!" && exit 1)
grep -q "SupervisorDashboardMonitoringView" backend/sims/academics/views.py || (echo "SupervisorDashboardMonitoringView missing!" && exit 1)
grep -q "MyProgressMonitoringView" backend/sims/academics/views.py || (echo "MyProgressMonitoringView missing!" && exit 1)
grep -q "ResidentProgressReportView" backend/sims/academics/views.py || (echo "ResidentProgressReportView missing!" && exit 1)
grep -q "SupervisorWorkloadReportView" backend/sims/academics/views.py || (echo "SupervisorWorkloadReportView missing!" && exit 1)
grep -q "EvaluationReportView" backend/sims/academics/views.py || (echo "EvaluationReportView missing!" && exit 1)
grep -q "LogbookReportView" backend/sims/academics/views.py || (echo "LogbookReportView missing!" && exit 1)

# 3. Check CSV Export views exist
grep -q "ResidentProgressExportCSVView" backend/sims/academics/views.py || (echo "ResidentProgressExportCSVView missing!" && exit 1)
grep -q "SupervisorWorkloadExportCSVView" backend/sims/academics/views.py || (echo "SupervisorWorkloadExportCSVView missing!" && exit 1)
grep -q "EvaluationReportExportCSVView" backend/sims/academics/views.py || (echo "EvaluationReportExportCSVView missing!" && exit 1)
grep -q "LogbookReportExportCSVView" backend/sims/academics/views.py || (echo "LogbookReportExportCSVView missing!" && exit 1)
grep -q "DataQualityReportExportCSVView" backend/sims/academics/views.py || (echo "DataQualityReportExportCSVView missing!" && exit 1)

# 4. Check URL routes exist
grep -q "monitoring/admin-dashboard" backend/sims/academics/workflow_urls.py || (echo "admin-dashboard route missing!" && exit 1)
grep -q "monitoring/supervisor-dashboard" backend/sims/academics/workflow_urls.py || (echo "supervisor-dashboard route missing!" && exit 1)
grep -q "monitoring/my-progress" backend/sims/academics/workflow_urls.py || (echo "my-progress route missing!" && exit 1)
grep -q "reports/resident-progress" backend/sims/academics/workflow_urls.py || (echo "resident-progress report route missing!" && exit 1)
grep -q "reports/supervisor-workload" backend/sims/academics/workflow_urls.py || (echo "supervisor-workload report route missing!" && exit 1)
grep -q "reports/evaluations" backend/sims/academics/workflow_urls.py || (echo "evaluations report route missing!" && exit 1)
grep -q "reports/logbook" backend/sims/academics/workflow_urls.py || (echo "logbook report route missing!" && exit 1)

# 5. Check frontend monitoring pages exist
if [ ! -f "frontend/app/academics/monitoring/page.tsx" ]; then
    echo "monitoring/page.tsx frontend route missing!"
    exit 1
fi
if [ ! -f "frontend/app/academics/reports/resident-progress/page.tsx" ]; then
    echo "reports/resident-progress/page.tsx frontend route missing!"
    exit 1
fi
if [ ! -f "frontend/app/academics/reports/supervisor-workload/page.tsx" ]; then
    echo "reports/supervisor-workload/page.tsx frontend route missing!"
    exit 1
fi
if [ ! -f "frontend/app/academics/reports/evaluations/page.tsx" ]; then
    echo "reports/evaluations/page.tsx frontend route missing!"
    exit 1
fi
if [ ! -f "frontend/app/academics/reports/logbook/page.tsx" ]; then
    echo "reports/logbook/page.tsx frontend route missing!"
    exit 1
fi
if [ ! -f "frontend/app/academics/reports/data-quality/page.tsx" ]; then
    echo "reports/data-quality/page.tsx frontend route missing!"
    exit 1
fi

# 6. Check that HOD and SupervisorResidentLink are not reintroduced or actively used
if grep -rn "SupervisorResidentLink" backend/sims/academics/ | grep -v "_legacy" || false; then
    echo "Warning: found active reference to SupervisorResidentLink!"
    exit 1
fi

echo "Brick 11 academic monitoring and reports gate: PASS"
