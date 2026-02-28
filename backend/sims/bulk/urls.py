"""Routing for bulk operations APIs."""

from django.urls import path

from sims.bulk.views import (
    BulkAssignmentView,
    BulkImportView,
    BulkDepartmentImportView,
    BulkResidentImportView,
    BulkReviewView,
    BulkExportView,
    BulkSupervisorImportView,
    BulkTraineeImportView,
    BulkImportEntityView,
)

app_name = "bulk_api"

urlpatterns = [
    path("review/", BulkReviewView.as_view(), name="review"),
    path("assignment/", BulkAssignmentView.as_view(), name="assignment"),
    path("import/", BulkImportView.as_view(), name="import"),
    path("import-trainees/", BulkTraineeImportView.as_view(), name="import_trainees"),
    path("import-supervisors/", BulkSupervisorImportView.as_view(), name="import_supervisors"),
    path("import-residents/", BulkResidentImportView.as_view(), name="import_residents"),
    path("import-departments/", BulkDepartmentImportView.as_view(), name="import_departments"),
    path("exports/<str:resource>/", BulkExportView.as_view(), name="exports"),
    # New unified import endpoint
    path("import/<str:entity>/<str:action>/", BulkImportEntityView.as_view(), name="import_entity"),
]
