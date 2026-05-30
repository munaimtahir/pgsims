"""Routing for bulk operations APIs."""

from django.urls import path

from sims.bulk.views import (
    BulkAssignmentView,
    BulkImportView,
    BulkDepartmentImportView,
    BulkResidentImportView,
    BulkReviewView,
    BulkExportView,
    BulkTemplateView,
    BulkSupervisorImportView,
    BulkTraineeImportView,
    BulkImportEntityView,
    FlexibleSchemasView,
    FlexibleDetectHeadersView,
    FlexibleValidateMappingView,
    FlexibleDryRunView,
    FlexibleImportApplyView,
    MappingPresetViewSet,
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
    path("templates/<str:resource>/", BulkTemplateView.as_view(), name="templates"),
    # New unified import endpoint
    path("import/<str:entity>/<str:action>/", BulkImportEntityView.as_view(), name="import_entity"),
    # Flexible mapping import endpoints
    path("flexible/schemas/", FlexibleSchemasView.as_view(), name="flexible_schemas"),
    path("flexible/detect-headers/", FlexibleDetectHeadersView.as_view(), name="flexible_detect_headers"),
    path("flexible/validate-mapping/", FlexibleValidateMappingView.as_view(), name="flexible_validate_mapping"),
    path("flexible/dry-run/", FlexibleDryRunView.as_view(), name="flexible_dry_run"),
    path("flexible/apply/", FlexibleImportApplyView.as_view(), name="flexible_apply"),
    path("flexible/presets/", MappingPresetViewSet.as_view({"get": "list", "post": "create"}), name="preset_list"),
    path("flexible/presets/<int:pk>/", MappingPresetViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="preset_detail"),
]
