from django.urls import path

from sims.users import resident_onboarding_views as views

app_name = "resident_selfservice_api"

urlpatterns = [
    path("me/profile-completion-status/", views.ResidentProfileCompletionStatusView.as_view(), name="resident_profile_completion_status"),
    path("complete-profile/", views.ResidentCompleteProfileView.as_view(), name="resident_complete_profile"),
]
