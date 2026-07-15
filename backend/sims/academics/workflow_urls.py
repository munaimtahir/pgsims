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

urlpatterns = [
    path("overview/", views.AcademicOverviewView.as_view(), name="academic-overview"),
    path("data-quality/", views.AcademicDataQualityView.as_view(), name="academic-data-quality"),
    path("options/", views.AcademicOptionsView.as_view(), name="academic-options"),
    path("residents/<int:resident_id>/summary/", views.ResidentAcademicSummaryView.as_view(), name="academic-resident-summary"),
    path("residents/me/summary/", views.MyResidentAcademicSummaryView.as_view(), name="academic-my-resident-summary"),
    path("supervisors/<int:supervisor_id>/summary/", views.SupervisorAcademicSummaryView.as_view(), name="academic-supervisor-summary"),
    path("supervisors/me/summary/", views.MySupervisorAcademicSummaryView.as_view(), name="academic-my-supervisor-summary"),
    path("seed/", views.AcademicSeedView.as_view(), name="academic-seed"),
    path("", include(router.urls)),
]
