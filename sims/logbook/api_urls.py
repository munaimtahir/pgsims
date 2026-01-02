"""API URL routing for logbook endpoints."""

from django.urls import path

from sims.logbook.api_views import PendingLogbookEntriesView, VerifyLogbookEntryView

app_name = "logbook_api"

urlpatterns = [
    path("pending/", PendingLogbookEntriesView.as_view(), name="pending"),
    path("<int:pk>/verify/", VerifyLogbookEntryView.as_view(), name="verify"),
]
