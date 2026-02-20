"""API URL routing for logbook endpoints."""

from django.urls import path

from sims.logbook.api_views import (
    PendingLogbookEntriesView,
    PGLogbookEntryDetailView,
    PGLogbookEntryListCreateView,
    PGLogbookEntrySubmitView,
    VerifyLogbookEntryView,
)

app_name = "logbook_api"

urlpatterns = [
    path("pending/", PendingLogbookEntriesView.as_view(), name="pending"),
    path("<int:pk>/verify/", VerifyLogbookEntryView.as_view(), name="verify"),
    path("my/", PGLogbookEntryListCreateView.as_view(), name="my_entries"),
    path("my/<int:pk>/", PGLogbookEntryDetailView.as_view(), name="my_entry_detail"),
    path("my/<int:pk>/submit/", PGLogbookEntrySubmitView.as_view(), name="my_entry_submit"),
]
