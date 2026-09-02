from django.urls import path

from sims.cases import api_views

app_name = "cases_api"

urlpatterns = [
    path("categories/", api_views.CaseCategoryListView.as_view(), name="categories"),
    path("my/", api_views.PGCaseListCreateView.as_view(), name="my_cases"),
    path("my/<int:pk>/", api_views.PGCaseDetailView.as_view(), name="my_case_detail"),
    path("my/<int:pk>/submit/", api_views.PGCaseSubmitView.as_view(), name="my_case_submit"),
    path("pending/", api_views.PendingCaseListView.as_view(), name="pending_cases"),
    path("<int:pk>/review/", api_views.CaseReviewActionView.as_view(), name="review_case"),
    path("statistics/", api_views.CaseStatisticsView.as_view(), name="statistics"),
]
