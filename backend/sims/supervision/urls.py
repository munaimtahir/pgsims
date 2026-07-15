from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ResidentSupervisorAssignmentViewSet,
    change_primary_view,
    supervision_options_view,
    supervision_data_quality_view,
    supervision_import_view,
)

app_name = "supervision"

router = DefaultRouter()
router.register(r"assignments", ResidentSupervisorAssignmentViewSet, basename="assignment")

urlpatterns = [
    path("change-primary/", change_primary_view, name="change_primary"),
    path("options/", supervision_options_view, name="options"),
    path("data-quality/", supervision_data_quality_view, name="data_quality"),
    path("import/", supervision_import_view, name="import"),
    path("", include(router.urls)),
]
