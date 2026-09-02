from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"training-records", views.ResidentTrainingRecordViewSet, basename="academic-training-record")
router.register(r"periods", views.AcademicPeriodViewSet, basename="academic-period")
router.register(r"rotation-templates", views.RotationTemplateViewSet, basename="academic-rotation-template")
router.register(r"evaluation-templates", views.EvaluationFormTemplateViewSet, basename="academic-evaluation-template")
router.register(r"logbook-categories", views.LogbookCategoryViewSet, basename="academic-logbook-category")
router.register(r"review-queue", views.SupervisorReviewQueueItemViewSet, basename="academic-review-queue")
router.register(r"evaluation-submissions", views.EvaluationSubmissionViewSet, basename="academic-evaluation-submission")
router.register(r"logbook-entries", views.LogbookEntryViewSet, basename="academic-logbook-entry")

urlpatterns = [
    path("overview/", views.AcademicOverviewView.as_view(), name="academic-overview"),
    path("data-quality/", views.AcademicDataQualityView.as_view(), name="academic-data-quality"),
    path("options/", views.AcademicOptionsView.as_view(), name="academic-options"),
    path("residents/<int:resident_id>/summary/", views.ResidentAcademicSummaryView.as_view(), name="academic-resident-summary"),
    path("residents/me/summary/", views.MyResidentAcademicSummaryView.as_view(), name="academic-my-resident-summary"),
    path("supervisors/<int:supervisor_id>/summary/", views.SupervisorAcademicSummaryView.as_view(), name="academic-supervisor-summary"),
    path("supervisors/me/summary/", views.MySupervisorAcademicSummaryView.as_view(), name="academic-my-supervisor-summary"),
    path("seed/", views.AcademicSeedView.as_view(), name="academic-seed"),
    
    path("my-progress/", views.MyAcademicProgressView.as_view(), name="academic-my-progress"),
    path("residents/<int:resident_id>/progress/", views.ResidentAcademicProgressView.as_view(), name="academic-resident-progress"),
    path("supervisor-workload/", views.SupervisorAcademicWorkloadView.as_view(), name="academic-supervisor-workload"),
    path("admin-workflow-overview/", views.AdminAcademicWorkflowOverviewView.as_view(), name="academic-admin-workflow-overview"),
    path("workflow-data-quality/", views.AcademicWorkflowDataQualityView.as_view(), name="academic-workflow-data-quality"),
    path("seed-workflows/", views.AcademicWorkflowSeedView.as_view(), name="academic-seed-workflows"),
    
    # Brick 11: Monitoring views
    path("monitoring/admin-dashboard/", views.AdminDashboardMonitoringView.as_view(), name="monitoring-admin-dashboard"),
    path("monitoring/supervisor-dashboard/", views.SupervisorDashboardMonitoringView.as_view(), name="monitoring-supervisor-dashboard"),
    path("monitoring/my-progress/", views.MyProgressMonitoringView.as_view(), name="monitoring-my-progress"),
    path("monitoring/departments/", views.DepartmentMonitoringSummaryView.as_view(), name="monitoring-departments"),
    path("monitoring/programs/", views.ProgramMonitoringSummaryView.as_view(), name="monitoring-programs"),
    path("monitoring/sessions/", views.SessionMonitoringSummaryView.as_view(), name="monitoring-sessions"),
    
    # Brick 11: Reports
    path("reports/resident-progress/export.csv", views.ResidentProgressExportCSVView.as_view(), name="reports-resident-progress-export"),
    path("reports/resident-progress/", views.ResidentProgressReportView.as_view(), name="reports-resident-progress-list"),
    path("reports/resident-progress/<int:resident_id>/", views.ResidentProgressReportDetailView.as_view(), name="reports-resident-progress-detail"),
    
    path("reports/supervisor-workload/export.csv", views.SupervisorWorkloadExportCSVView.as_view(), name="reports-supervisor-workload-export"),
    path("reports/supervisor-workload/", views.SupervisorWorkloadReportView.as_view(), name="reports-supervisor-workload-list"),
    path("reports/supervisor-workload/<int:supervisor_id>/", views.SupervisorWorkloadReportDetailView.as_view(), name="reports-supervisor-workload-detail"),
    
    path("reports/evaluations/export.csv", views.EvaluationReportExportCSVView.as_view(), name="reports-evaluations-export"),
    path("reports/evaluations/", views.EvaluationReportView.as_view(), name="reports-evaluations"),
    
    path("reports/logbook/export.csv", views.LogbookReportExportCSVView.as_view(), name="reports-logbook-export"),
    path("reports/logbook/", views.LogbookReportView.as_view(), name="reports-logbook"),
    
    path("reports/data-quality/export.csv", views.DataQualityReportExportCSVView.as_view(), name="reports-data-quality-export"),
    path("reports/data-quality/", views.DataQualityReportView.as_view(), name="reports-data-quality"),

    path("", include(router.urls)),
]

