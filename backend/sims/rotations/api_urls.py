"""API URL routing for rotation endpoints."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sims.rotations.api_views import (
    HospitalDepartmentViewSet,
    HospitalViewSet,
    PGMyRotationDetailView,
    PGMyRotationsListView,
    UTRMCRotationOverrideApproveView,
)

app_name = "rotations_api"

router = DefaultRouter()
router.register(r"hospitals", HospitalViewSet, basename="hospital")
router.register(r"hospital-departments", HospitalDepartmentViewSet, basename="hospital-department")

urlpatterns = [
    path("", include(router.urls)),
    path("my/", PGMyRotationsListView.as_view(), name="my_rotations"),
    path("my/<int:pk>/", PGMyRotationDetailView.as_view(), name="my_rotation_detail"),
    path("<int:pk>/utrmc-approve/", UTRMCRotationOverrideApproveView.as_view(), name="utrmc_approve"),
]
