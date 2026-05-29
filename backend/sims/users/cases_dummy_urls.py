from django.urls import path
from django.http import HttpResponseRedirect

def dummy_redirect(request, *args, **kwargs):
    return HttpResponseRedirect("/dashboard")

app_name = "cases"

urlpatterns = [
    path("", dummy_redirect, name="case_list"),
    path("create/", dummy_redirect, name="case_create"),
    path("<int:pk>/", dummy_redirect, name="case_detail"),
    path("<int:pk>/edit/", dummy_redirect, name="case_update"),
    path("<int:pk>/delete/", dummy_redirect, name="case_delete"),
    path("<int:pk>/submit/", dummy_redirect, name="case_submit"),
    path("<int:case_pk>/review/", dummy_redirect, name="case_review"),
    path("statistics/", dummy_redirect, name="case_statistics"),
    path("export/", dummy_redirect, name="case_export"),
]
