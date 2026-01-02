from django.urls import path

from . import views

app_name = "cases"

urlpatterns = [
    # Case management URLs
    path("", views.CaseListView.as_view(), name="case_list"),
    path("create/", views.CaseCreateView.as_view(), name="case_create"),
    path("<int:pk>/", views.CaseDetailView.as_view(), name="case_detail"),
    path("<int:pk>/edit/", views.CaseUpdateView.as_view(), name="case_update"),
    path("<int:pk>/delete/", views.CaseDeleteView.as_view(), name="case_delete"),
    path("<int:pk>/submit/", views.submit_case, name="case_submit"),
    # Review URLs
    path("<int:case_pk>/review/", views.CaseReviewCreateView.as_view(), name="case_review"),
    # Statistics and analytics
    path("statistics/", views.case_statistics_view, name="case_statistics"),
    path("export/", views.case_export_data, name="case_export"),
    # AJAX endpoints
    path("api/diagnoses/", views.get_diagnoses_json, name="diagnoses_json"),
    path("api/procedures/", views.get_procedures_json, name="procedures_json"),
]
