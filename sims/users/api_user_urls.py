"""
API URLs for user-related endpoints.
"""

from django.urls import path

from . import api_views

app_name = "users_api"

urlpatterns = [
    path("assigned-pgs/", api_views.SupervisorAssignedPGsView.as_view(), name="assigned_pgs"),
]
