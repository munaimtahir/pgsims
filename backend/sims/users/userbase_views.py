"""DRF views for userbase/org graph feature pack."""

from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.academics.models import Department
from sims.common_permissions import IsTechAdmin
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    DepartmentMembership,
    HODAssignment,
    HospitalAssignment,
    ResidentProfile,
    StaffProfile,
    SupervisorResidentLink,
)
from sims.users.userbase_serializers import (
    DepartmentMembershipSerializer,
    DepartmentSerializer,
    HODAssignmentSerializer,
    HospitalAssignmentSerializer,
    HospitalDepartmentSerializer,
    HospitalSerializer,
    ResidentProfileSerializer,
    StaffProfileSerializer,
    SupervisorResidentLinkSerializer,
    UserManagementSerializer,
)

User = get_user_model()


def _is_manager(user) -> bool:
    return bool(
        user
        and user.is_authenticated
        and (user.is_superuser or user.role in {"admin", "utrmc_admin"})
    )


def _is_roster_reader(user) -> bool:
    return bool(
        user
        and user.is_authenticated
        and (user.is_superuser or user.role in {"admin", "utrmc_admin", "utrmc_user"})
    )


def _active_q(prefix: str = "") -> Q:
    today = date.today()
    return (
        Q(**{f"{prefix}active": True})
        & (Q(**{f"{prefix}end_date__isnull": True}) | Q(**{f"{prefix}end_date__gte": today}))
        & Q(**{f"{prefix}start_date__lte": today})
    )


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all().order_by("name")
    serializer_class = HospitalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["is_active"]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsTechAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        if _is_manager(self.request.user):
            return qs
        return qs.filter(is_active=True)

    @action(detail=True, methods=["get"], url_path="departments")
    def departments(self, request, pk=None):
        hospital = self.get_object()
        queryset = (
            HospitalDepartment.objects.filter(hospital=hospital, is_active=True)
            .select_related("department")
            .order_by("department__name")
        )
        return Response(
            [
                {
                    "id": item.id,
                    "department": {
                        "id": item.department_id,
                        "name": item.department.name,
                        "code": item.department.code,
                        "active": item.department.active,
                    },
                    "active": item.is_active,
                }
                for item in queryset
            ]
        )


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "created_at"]

    def get_permissions(self):
        if self.action == "roster":
            return [permissions.IsAuthenticated()]
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsTechAdmin()]

    @action(detail=True, methods=["get"], url_path="roster")
    def roster(self, request, pk=None):
        department = self.get_object()
        user = request.user
        if not _is_roster_reader(user):
            allowed = (
                DepartmentMembership.objects.filter(
                    user=user,
                    department=department,
                )
                .filter(_active_q())
                .filter(member_type__in=["faculty", "supervisor", "resident"])
            )
            if not allowed.exists():
                raise PermissionDenied("You are not allowed to view this department roster.")

        active_hod = (
            HODAssignment.objects.select_related("hod_user")
            .filter(department=department)
            .filter(_active_q())
            .order_by("-start_date")
            .first()
        )
        memberships = (
            DepartmentMembership.objects.filter(department=department)
            .select_related("user")
            .filter(_active_q())
            .order_by("-is_primary", "user__last_name", "user__first_name")
        )

        def _rows(member_type: str):
            return [
                {
                    "id": row.user_id,
                    "username": row.user.username,
                    "full_name": row.user.get_full_name(),
                    "role": row.user.role,
                    "is_primary": row.is_primary,
                    "start_date": row.start_date,
                    "end_date": row.end_date,
                }
                for row in memberships
                if row.member_type == member_type
            ]

        return Response(
            {
                "department": {
                    "id": department.id,
                    "name": department.name,
                    "code": department.code,
                    "active": department.active,
                },
                "hod": (
                    {
                        "id": active_hod.hod_user_id,
                        "username": active_hod.hod_user.username,
                        "full_name": active_hod.hod_user.get_full_name(),
                        "start_date": active_hod.start_date,
                        "end_date": active_hod.end_date,
                    }
                    if active_hod
                    else None
                ),
                "faculty": _rows("faculty"),
                "supervisors": _rows("supervisor"),
                "residents": _rows("resident"),
            }
        )


class HospitalDepartmentViewSet(viewsets.ModelViewSet):
    queryset = HospitalDepartment.objects.select_related("hospital", "department").order_by(
        "hospital__name", "department__name"
    )
    serializer_class = HospitalDepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["hospital", "department", "is_active"]
    search_fields = ["hospital__name", "department__name", "department__code"]
    ordering_fields = ["hospital__name", "department__name", "created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        if _is_manager(self.request.user):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        qs = super().get_queryset()
        if _is_manager(self.request.user):
            return qs
        return qs.filter(is_active=True, hospital__is_active=True, department__active=True)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("home_department", "home_hospital", "supervisor")
    serializer_class = UserManagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["role", "is_active"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering_fields = ["username", "first_name", "last_name", "date_joined"]

    def _ensure_manage_permission(self):
        if not _is_manager(self.request.user):
            raise PermissionDenied("Only admin/utrmc_admin can manage users.")

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not _is_manager(user):
            return queryset.filter(id=user.id)

        role = self.request.query_params.get("role")
        department = self.request.query_params.get("department")
        active = self.request.query_params.get("active")
        search = self.request.query_params.get("search")

        if role:
            queryset = queryset.filter(role=role)
        if department:
            queryset = queryset.filter(
                department_memberships__department_id=department,
                department_memberships__active=True,
            )
        if active in {"true", "false"}:
            queryset = queryset.filter(is_active=(active == "true"))
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
            )
        return queryset.distinct()

    def create(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not _is_manager(request.user) and obj.id != request.user.id:
            raise PermissionDenied("You may only view your own profile.")
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


class BaseManagedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _assert_view_scope(self):
        if _is_manager(self.request.user):
            return
        raise PermissionDenied("Only admin/utrmc_admin can manage this resource.")

    def list(self, request, *args, **kwargs):
        self._assert_view_scope()
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self._assert_view_scope()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._assert_view_scope()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._assert_view_scope()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._assert_view_scope()
        return super().destroy(request, *args, **kwargs)


class ResidentProfileViewSet(BaseManagedModelViewSet):
    queryset = ResidentProfile.objects.select_related("user").order_by("user__last_name")
    serializer_class = ResidentProfileSerializer
    lookup_field = "user_id"
    filterset_fields = ["active", "training_level"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "pgr_id"]

    def retrieve(self, request, *args, **kwargs):
        if _is_manager(request.user):
            return super().retrieve(request, *args, **kwargs)
        if str(request.user.id) != str(kwargs.get("user_id")):
            raise PermissionDenied("You may only view your own profile.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


class StaffProfileViewSet(BaseManagedModelViewSet):
    queryset = StaffProfile.objects.select_related("user").order_by("user__last_name")
    serializer_class = StaffProfileSerializer
    lookup_field = "user_id"
    filterset_fields = ["active"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "designation"]

    def retrieve(self, request, *args, **kwargs):
        if _is_manager(request.user):
            return super().retrieve(request, *args, **kwargs)
        if str(request.user.id) != str(kwargs.get("user_id")):
            raise PermissionDenied("You may only view your own profile.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


class DepartmentMembershipViewSet(BaseManagedModelViewSet):
    queryset = DepartmentMembership.objects.select_related("user", "department").order_by(
        "department__name", "user__last_name"
    )
    serializer_class = DepartmentMembershipSerializer
    filterset_fields = ["department", "user", "member_type", "active", "is_primary"]
    search_fields = ["department__name", "user__username", "user__first_name", "user__last_name"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.active = False
        instance.end_date = instance.end_date or date.today()
        instance.updated_by = self.request.user
        instance.save(update_fields=["active", "end_date", "updated_by", "updated_at"])


class HospitalAssignmentViewSet(BaseManagedModelViewSet):
    queryset = HospitalAssignment.objects.select_related(
        "user",
        "hospital_department",
        "hospital_department__hospital",
        "hospital_department__department",
    ).order_by("hospital_department__hospital__name")
    serializer_class = HospitalAssignmentSerializer
    filterset_fields = ["user", "hospital_department", "assignment_type", "active"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "hospital_department__hospital__name",
        "hospital_department__department__name",
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.active = False
        instance.end_date = instance.end_date or date.today()
        instance.updated_by = self.request.user
        instance.save(update_fields=["active", "end_date", "updated_by", "updated_at"])


class SupervisionLinkViewSet(BaseManagedModelViewSet):
    queryset = SupervisorResidentLink.objects.select_related(
        "supervisor_user", "resident_user", "department"
    ).order_by("-active", "resident_user__last_name")
    serializer_class = SupervisorResidentLinkSerializer
    filterset_fields = ["supervisor_user", "resident_user", "department", "active"]
    search_fields = [
        "supervisor_user__username",
        "supervisor_user__first_name",
        "supervisor_user__last_name",
        "resident_user__username",
        "resident_user__first_name",
        "resident_user__last_name",
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class HODAssignmentViewSet(BaseManagedModelViewSet):
    queryset = HODAssignment.objects.select_related("department", "hod_user").order_by(
        "department__name", "-start_date"
    )
    serializer_class = HODAssignmentSerializer
    filterset_fields = ["department", "active"]
    search_fields = [
        "department__name",
        "department__code",
        "hod_user__username",
        "hod_user__first_name",
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AuthMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserManagementSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
