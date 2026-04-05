"""Top-level API routes for userbase/org graph endpoints."""

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
router.register(r"residents", userbase_views.ResidentProfileViewSet, basename="userbase-residents")
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
router.register(
    r"supervision-links",
    userbase_views.SupervisionLinkViewSet,
    basename="userbase-supervision-links",
)
router.register(
    r"hod-assignments",
    userbase_views.HODAssignmentViewSet,
    basename="userbase-hod-assignments",
)

urlpatterns = [path("", include(router.urls))]

urlpatterns += [
    path("admin/data-quality/summary", userbase_views.DataQualitySummaryView.as_view(), name="data-quality-summary"),
    path("admin/data-quality/users", userbase_views.DataQualityUsersView.as_view(), name="data-quality-users"),
    path("admin/data-quality/recompute", userbase_views.DataQualityRecomputeView.as_view(), name="data-quality-recompute"),
    path("admin/data-quality/audit", userbase_views.DataCorrectionAuditView.as_view(), name="data-quality-audit"),
]
