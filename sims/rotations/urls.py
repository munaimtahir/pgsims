from django.urls import path

from . import views

app_name = "rotations"

urlpatterns = [
    # Main rotation views
    path("", views.RotationListView.as_view(), name="list"),
    path("dashboard/", views.RotationDashboardView.as_view(), name="dashboard"),
    path("create/", views.RotationCreateView.as_view(), name="create"),
    path("<int:pk>/", views.RotationDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.RotationUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.RotationDeleteView.as_view(), name="delete"),
    # Rotation evaluation views
    path(
        "<int:rotation_pk>/evaluate/", views.RotationEvaluationCreateView.as_view(), name="evaluate"
    ),
    path(
        "evaluation/<int:pk>/",
        views.RotationEvaluationDetailView.as_view(),
        name="evaluation_detail",
    ),
    # Bulk operations
    path("bulk-assignment/", views.BulkRotationAssignmentView.as_view(), name="bulk_assignment"),
    # Export and reporting
    path("export/csv/", views.export_rotations_csv, name="export_csv"),
    # AJAX/API endpoints
    path("api/calendar/", views.rotation_calendar_api, name="calendar_api"),
    path("api/stats/", views.rotation_stats_api, name="stats_api"),
    path("api/quick-stats/", views.rotation_quick_stats, name="quick_stats_api"),
    path(
        "api/departments/<int:hospital_id>/",
        views.department_by_hospital_api,
        name="departments_by_hospital",
    ),
]

# API URLs for mobile app and external integrations
api_urlpatterns = [
    # REST API endpoints would go here
    # These would be included in the main API routing
]
