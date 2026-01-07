"""Routing for bulk operations APIs."""

from django.urls import path

from sims.bulk.views import (
    BulkAssignmentView,
    BulkImportView,
    BulkReviewView,
    BulkTraineeImportView,
)

app_name = "bulk_api"

urlpatterns = [
    path("review/", BulkReviewView.as_view(), name="review"),
    path("assignment/", BulkAssignmentView.as_view(), name="assignment"),
    path("import/", BulkImportView.as_view(), name="import"),
    path("import-trainees/", BulkTraineeImportView.as_view(), name="import_trainees"),
]
