from django.urls import path
from django.http import HttpResponseRedirect

def dummy_redirect(request, *args, **kwargs):
    return HttpResponseRedirect("/dashboard")

app_name = "logbook"

urlpatterns = [
    path("", dummy_redirect, name="list"),
    path("dashboard/", dummy_redirect, name="dashboard"),
    path("analytics/", dummy_redirect, name="analytics"),
    path("entry/create/", dummy_redirect, name="create"),
    path("entry/new/", dummy_redirect, name="entry_new"),
    path("pg/entries/", dummy_redirect, name="pg_logbook_list"),
    path("pg/entry/new/", dummy_redirect, name="pg_entry_create"),
    path("pg/entry/<int:pk>/edit/", dummy_redirect, name="pg_logbook_entry_edit"),
    path("entry/quick/", dummy_redirect, name="quick_create"),
    path("entry/<int:pk>/", dummy_redirect, name="detail"),
    path("entry/<int:pk>/edit/", dummy_redirect, name="edit"),
    path("entry/<int:pk>/delete/", dummy_redirect, name="delete"),
    path("supervisor/dashboard/", dummy_redirect, name="supervisor_logbook_dashboard"),
    path("supervisor/all-entries/", dummy_redirect, name="supervisor_all_entries"),
    path("supervisor/bulk-review/", dummy_redirect, name="supervisor_bulk_review"),
    path("supervisor/entry/<int:entry_pk>/review/", dummy_redirect, name="supervisor_logbook_review_action"),
    path("entry/<int:entry_pk>/review/", dummy_redirect, name="review"),
    path("review/<int:pk>/", dummy_redirect, name="review_detail"),
    path("bulk-actions/", dummy_redirect, name="bulk_actions"),
    path("export/csv/", dummy_redirect, name="export_csv"),
    path("api/stats/", dummy_redirect, name="stats_api"),
    path("api/template/<int:template_id>/preview/", dummy_redirect, name="template_preview_api"),
    path("api/entry/<int:entry_id>/complexity/", dummy_redirect, name="entry_complexity_api"),
    path("api/update-statistics/", dummy_redirect, name="update_stats_api"),
]
