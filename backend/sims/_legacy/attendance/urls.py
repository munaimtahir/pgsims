"""API URL routing for attendance endpoints."""

from django.urls import path

from .api_views import AttendanceSummaryView, BulkAttendanceUploadView

app_name = "attendance_api"

urlpatterns = [
    path("upload/", BulkAttendanceUploadView.as_view(), name="upload"),
    path("summary/", AttendanceSummaryView.as_view(), name="summary"),
]
