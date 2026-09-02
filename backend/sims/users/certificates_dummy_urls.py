from django.urls import path
from django.http import HttpResponseRedirect

def dummy_redirect(request, *args, **kwargs):
    return HttpResponseRedirect("/dashboard")

app_name = "certificates"

urlpatterns = [
    path("", dummy_redirect, name="list"),
    path("dashboard/", dummy_redirect, name="dashboard"),
    path("create/", dummy_redirect, name="create"),
    path("<int:pk>/", dummy_redirect, name="detail"),
    path("<int:pk>/edit/", dummy_redirect, name="edit"),
    path("<int:certificate_pk>/review/", dummy_redirect, name="review"),
    path("export/csv/", dummy_redirect, name="export_csv"),
]
