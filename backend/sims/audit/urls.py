from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActivityLogViewSet, AuditReportViewSet

router = DefaultRouter()
router.register(r"activity", ActivityLogViewSet, basename="activity-log")
router.register(r"reports", AuditReportViewSet, basename="audit-report")

urlpatterns = [
    path("", include(router.urls)),
]
