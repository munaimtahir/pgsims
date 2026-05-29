from django.urls import path
from django.http import HttpResponseRedirect
from . import views

app_name = "rotations"

def dummy_redirect(request, *args, **kwargs):
    return HttpResponseRedirect("/dashboard")

urlpatterns = [
    path(
        "api/departments/<int:hospital_id>/",
        views.department_by_hospital_api,
        name="departments_by_hospital",
    ),
    path("", dummy_redirect, name="list"),
    path("create/", dummy_redirect, name="create"),
    path("<int:pk>/", dummy_redirect, name="detail"),
    path("<int:pk>/edit/", dummy_redirect, name="edit"),
    path("<int:pk>/evaluate/", dummy_redirect, name="evaluate"),
    path("dashboard/", dummy_redirect, name="dashboard"),
    path("bulk-assignment/", dummy_redirect, name="bulk_assignment"),
    path("evaluation/<int:pk>/", dummy_redirect, name="evaluation_detail"),
    path("api/quick-stats/", dummy_redirect, name="quick_stats_api"),
]
