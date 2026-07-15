from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sims.users import userbase_views

router = DefaultRouter()
router.register(r"hospitals", userbase_views.HospitalViewSet, basename="userbase-hospitals")
router.register(r"departments", userbase_views.DepartmentViewSet, basename="userbase-departments")
router.register(
    r"hospital-departments",
    userbase_views.HospitalDepartmentViewSet,
    basename="userbase-hospital-departments",
)
router.register(r"admins", userbase_views.AdminProfileViewSet, basename="userbase-admins")
router.register(r"residents", userbase_views.ResidentProfileViewSet, basename="userbase-residents")
router.register(r"supervisors", userbase_views.SupervisorProfileViewSet, basename="userbase-supervisors")
router.register(r"support-staff", userbase_views.SupportStaffProfileViewSet, basename="userbase-support-staff")
router.register(r"staff", userbase_views.StaffProfileViewSet, basename="userbase-staff")
router.register(
    r"department-memberships",
    userbase_views.DepartmentMembershipViewSet,
    basename="userbase-department-memberships",
)
router.register(
    r"hospital-assignments",
    userbase_views.HospitalAssignmentViewSet,
    basename="userbase-hospital-assignments",
)

urlpatterns = [path("", include(router.urls))]

urlpatterns += [
    path("identity/options/", userbase_views.IdentityOptionsView.as_view(), name="identity_options"),
    path("data-quality/", userbase_views.DataQualityView.as_view(), name="data-quality"),
    path("admin/data-quality/summary", userbase_views.DataQualitySummaryView.as_view(), name="data-quality-summary"),
    path("admin/data-quality/users", userbase_views.DataQualityUsersView.as_view(), name="data-quality-users"),
    path("admin/data-quality/recompute", userbase_views.DataQualityRecomputeView.as_view(), name="data-quality-recompute"),
    path("admin/data-quality/audit", userbase_views.DataCorrectionAuditView.as_view(), name="data-quality-audit"),
]
