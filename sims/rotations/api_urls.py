"""API URL routing for rotation endpoints."""

from django.urls import path

from sims.rotations.api_views import PGMyRotationDetailView, PGMyRotationsListView

app_name = "rotations_api"

urlpatterns = [
    path("my/", PGMyRotationsListView.as_view(), name="my_rotations"),
    path("my/<int:pk>/", PGMyRotationDetailView.as_view(), name="my_rotation_detail"),
]
