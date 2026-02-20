"""
API URLs for JWT authentication endpoints.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views

app_name = "auth_api"

urlpatterns = [
    # JWT Token endpoints
    path("login/", api_views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", api_views.logout_view, name="logout"),
    # User registration
    path("register/", api_views.register_view, name="register"),
    # User profile
    path("profile/", api_views.user_profile_view, name="profile"),
    path("profile/update/", api_views.update_profile_view, name="profile_update"),
    # Password management
    path("password-reset/", api_views.password_reset_request_view, name="password_reset"),
    path(
        "password-reset/confirm/",
        api_views.password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    path("change-password/", api_views.change_password_view, name="change_password"),
]
