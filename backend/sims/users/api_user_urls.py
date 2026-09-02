"""API URLs for user-related endpoints."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sims.users import api_views, userbase_views

app_name = "users_api"

router = DefaultRouter()
router.register(r"", userbase_views.UserViewSet, basename="users")

urlpatterns = [
    path("assigned-pgs/", api_views.SupervisorAssignedPGsView.as_view(), name="assigned_pgs"),
    path("", include(router.urls)),
]
