from django.urls import path

from .views import GlobalSearchView, SearchHistoryView, SearchSuggestionsView

app_name = "search"

urlpatterns = [
    path("", GlobalSearchView.as_view(), name="global_search"),
    path("history/", SearchHistoryView.as_view(), name="history"),
    path("suggestions/", SearchSuggestionsView.as_view(), name="suggestions"),
]
