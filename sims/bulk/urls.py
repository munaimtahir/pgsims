"""Routing for bulk operations APIs."""

from django.urls import path

from sims.bulk.views import BulkAssignmentView, BulkImportView, BulkReviewView

app_name = "bulk_api"

urlpatterns = [
    path("review/", BulkReviewView.as_view(), name="review"),
    path("assignment/", BulkAssignmentView.as_view(), name="assignment"),
    path("import/", BulkImportView.as_view(), name="import"),
]
