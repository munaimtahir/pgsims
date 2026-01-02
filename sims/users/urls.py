from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html", success_url="/users/password-change/done/"
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
    # Password Reset URLs (moved from accounts/)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html", success_url="/users/password-reset/done/"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/password-reset-complete/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Dashboard URLs (role-based)
    path("dashboard/", views.DashboardRedirectView.as_view(), name="dashboard"),
    path("admin-dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path(
        "supervisor-dashboard/",
        views.SupervisorDashboardView.as_view(),
        name="supervisor_dashboard",
    ),
    path("pg-dashboard/", views.PGDashboardView.as_view(), name="pg_dashboard"),
    # Profile Management
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    # User Management (Admin only)
    path("list/", views.UserListView.as_view(), name="user_list"),
    path("create/", views.UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/edit/", views.UserEditView.as_view(), name="user_edit"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    path("<int:pk>/activate/", views.UserActivateView.as_view(), name="user_activate"),
    path("<int:pk>/deactivate/", views.UserDeactivateView.as_view(), name="user_deactivate"),
    path("<int:pk>/archive/", views.UserArchiveView.as_view(), name="user_archive"),
    # Supervisor Management
    path("supervisors/", views.SupervisorListView.as_view(), name="supervisor_list"),
    path("supervisor/<int:pk>/pgs/", views.SupervisorPGsView.as_view(), name="supervisor_pgs"),
    path("assign-supervisor/", views.AssignSupervisorView.as_view(), name="assign_supervisor"),
    # PG Management
    path("pgs/", views.PGListView.as_view(), name="pg_list"),
    path("pgs/bulk-upload/", views.PGBulkUploadView.as_view(), name="pg_bulk_upload"),
    path("pg/<int:pk>/progress/", views.PGProgressView.as_view(), name="pg_progress"),
    # Reports and Analytics
    path("reports/", views.UserReportsView.as_view(), name="user_reports"),
    path("reports/export/", views.UserExportView.as_view(), name="user_export"),
    path("activity-log/", views.ActivityLogView.as_view(), name="activity_log"),
    # Role-based Analytics
    path("analytics/admin/", views.admin_analytics_view, name="admin_analytics"),
    path("analytics/supervisor/", views.supervisor_analytics_view, name="supervisor_analytics"),
    path("analytics/pg/", views.pg_analytics_view, name="pg_analytics"),
    # AJAX/API endpoints
    path("api/users/search/", views.UserSearchAPIView.as_view(), name="user_search_api"),
    path(
        "api/supervisors/specialty/<str:specialty>/",
        views.SupervisorsBySpecialtyAPIView.as_view(),
        name="supervisors_by_specialty",
    ),
    path("api/user/<int:pk>/stats/", views.UserStatsAPIView.as_view(), name="user_stats_api"),
    path("api/stats/", views.UserListStatsAPIView.as_view(), name="user_list_stats_api"),
    path("api/admin/stats/", views.admin_stats_api, name="admin_stats_api"),
]
