from django.urls import path

from . import views

app_name = "logbook"

urlpatterns = [
    # Main logbook views
    path("", views.LogbookEntryListView.as_view(), name="list"),
    path("dashboard/", views.LogbookDashboardView.as_view(), name="dashboard"),
    path("analytics/", views.LogbookAnalyticsView.as_view(), name="analytics"),
    # Entry management
    path(
        "entry/create/", views.LogbookEntryCreateRedirectView.as_view(), name="create"
    ),  # Redirect to PG entry create
    path(
        "entry/new/", views.PGLogbookEntryCreateView.as_view(), name="entry_new"
    ),  # Alternative URL for PG entry create
    # PG specific entry management
    path("pg/entries/", views.PGLogbookEntryListView.as_view(), name="pg_logbook_list"),
    path("pg/entry/new/", views.PGLogbookEntryCreateView.as_view(), name="pg_entry_create"),
    path(
        "pg/entry/<int:pk>/edit/",
        views.PGLogbookEntryUpdateView.as_view(),
        name="pg_logbook_entry_edit",
    ),
    # Generic entry views (might be used by admin/supervisor or for general detail)
    path("entry/quick/", views.QuickLogbookEntryView.as_view(), name="quick_create"),
    path(
        "entry/<int:pk>/", views.LogbookEntryDetailView.as_view(), name="detail"
    ),  # Detail view is generic
    path(
        "entry/<int:pk>/edit/", views.LogbookEntryUpdateView.as_view(), name="edit"
    ),  # Generic edit, might be admin/supervisor focused
    path("entry/<int:pk>/delete/", views.LogbookEntryDeleteView.as_view(), name="delete"),
    # Supervisor specific views
    path(
        "supervisor/dashboard/",
        views.SupervisorLogbookDashboardView.as_view(),
        name="supervisor_logbook_dashboard",
    ),
    path(
        "supervisor/all-entries/",
        views.SupervisorLogbookAllEntriesView.as_view(),
        name="supervisor_all_entries",
    ),
    path(
        "supervisor/bulk-review/",
        views.SupervisorBulkReviewView.as_view(),
        name="supervisor_bulk_review",
    ),
    path(
        "supervisor/entry/<int:entry_pk>/review/",
        views.SupervisorLogbookReviewActionView.as_view(),
        name="supervisor_logbook_review_action",
    ),
    # Review management
    path("entry/<int:entry_pk>/review/", views.LogbookReviewCreateView.as_view(), name="review"),
    path("review/<int:pk>/", views.LogbookReviewDetailView.as_view(), name="review_detail"),
    # Bulk operations
    path("bulk-actions/", views.BulkLogbookActionView.as_view(), name="bulk_actions"),
    # Export and reporting
    path("export/csv/", views.export_logbook_csv, name="export_csv"),
    # AJAX/API endpoints
    path("api/stats/", views.logbook_stats_api, name="stats_api"),
    path(
        "api/template/<int:template_id>/preview/",
        views.template_preview_api,
        name="template_preview_api",
    ),
    path(
        "api/entry/<int:entry_id>/complexity/",
        views.entry_complexity_api,
        name="entry_complexity_api",
    ),
    path("api/update-statistics/", views.update_logbook_statistics, name="update_stats_api"),
]

# Additional URL patterns for mobile app and external integrations
api_urlpatterns = [
    # REST API endpoints would go here
    # These would be included in the main API routing
]
