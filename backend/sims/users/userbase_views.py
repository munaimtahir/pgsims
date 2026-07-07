from datetime import date
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from sims.academics.models import Department
from sims.common_permissions import IsTechAdmin
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    DataCorrectionAudit,
    DepartmentMembership,
    HospitalAssignment,
    AdminProfile,
    ResidentProfile,
    SupervisorProfile,
    SupportStaffProfile,
    SupervisorResidentLink,
)
from sims.users.data_quality import log_data_correction, recompute_all, recompute_flags_for_user
from sims.academics.serializers import DepartmentSerializer as CanonicalDepartmentSerializer
from sims.users.userbase_serializers import (
    DepartmentMembershipSerializer,
    HospitalAssignmentSerializer,
    HospitalDepartmentSerializer,
    HospitalSerializer,
    AdminProfileSerializer,
    ResidentProfileSerializer,
    SupervisorProfileSerializer,
    SupportStaffProfileSerializer,
    SupervisorResidentLinkSerializer,
    UserManagementSerializer,
)
from sims.users.services import (
    create_user_with_profile,
    get_missing_profile_fields,
    recalculate_profile_completion,
    PROFILE_COMPLETION_REQUIREMENTS,
)

User = get_user_model()


class UserbaseEmptySchemaSerializer(serializers.Serializer):
    pass


def _is_manager(user) -> bool:
    return bool(
        user
        and user.is_authenticated
        and (user.is_superuser or user.role == "ADMIN")
    )


def _is_roster_reader(user) -> bool:
    return bool(
        user
        and user.is_authenticated
        and (user.is_superuser or user.role == "ADMIN")
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
    serializer_class = CanonicalDepartmentSerializer
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

        active_hod_profile = (
            SupervisorProfile.objects.select_related("user")
            .filter(department_ref=department, designation_ref="HOD")
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
                        "id": active_hod_profile.user_id,
                        "username": active_hod_profile.user.username,
                        "full_name": active_hod_profile.user.get_full_name(),
                        "start_date": active_hod_profile.created_at.date() if active_hod_profile.created_at else date.today(),
                        "end_date": None,
                    }
                    if active_hod_profile
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
    search_fields = ["hospital__name", "department__name"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        return [IsTechAdmin()]

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
        if not _is_roster_reader(user):
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
        role = request.data.get("role")
        full_name = request.data.get("full_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        username = request.data.get("username")
        password = request.data.get("password")

        if role not in ["ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF"]:
            return Response({"detail": "Invalid role value"}, status=status.HTTP_400_BAD_REQUEST)

        if not full_name:
            return Response({"detail": "full_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        profile_payload = request.data.get("profile", {})
        svc_profile = {}

        for field in [
            "registration_no", "cnic", "phone", "email", "pmdc_no", "official_email",
            "designation", "designation_ref", "academic_session_ref", "specialty_ref", "scope_notes"
        ]:
            if field in profile_payload:
                svc_profile[field] = profile_payload[field]

        # Resolve ForeignKey relations
        hospital_id = profile_payload.get("hospital") or profile_payload.get("training_site_ref") or profile_payload.get("hospital_id")
        if hospital_id:
            try:
                svc_profile["hospital"] = Hospital.objects.get(id=hospital_id)
            except (Hospital.DoesNotExist, ValueError):
                return Response({"detail": f"Hospital ID {hospital_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        dept_id = profile_payload.get("department_ref") or profile_payload.get("department") or profile_payload.get("department_id")
        if dept_id:
            try:
                svc_profile["department_ref"] = Department.objects.get(id=dept_id)
            except (Department.DoesNotExist, ValueError):
                return Response({"detail": f"Department ID {dept_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        prog_id = profile_payload.get("program_ref") or profile_payload.get("program") or profile_payload.get("program_id")
        if prog_id:
            try:
                svc_profile["program_ref"] = TrainingProgram.objects.get(id=prog_id)
            except Exception:
                # If training app is not initialized or invalid ID
                pass

        try:
            user = create_user_with_profile(
                role=role,
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                profile_payload=svc_profile,
                actor=request.user,
                source="manual"
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        missing = get_missing_profile_fields(user)
        missing_fields = [m["field"] for m in missing]

        req_config = PROFILE_COMPLETION_REQUIREMENTS[role]
        profile_relation = req_config["profile_relation"]
        profile = getattr(user, profile_relation)

        allowed_next_route = "/change-password" if user.must_change_password else ("/complete-profile" if missing else user.get_dashboard_url())

        resp_data = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "profile_type": profile.__class__.__name__,
            "profile_id": profile.id,
            "profile_status": profile.profile_status,
            "profile_schema_version": profile.profile_schema_version,
            "completed_schema_version": profile.completed_schema_version,
            "must_change_password": user.must_change_password,
            "is_profile_complete": user.is_profile_complete,
            "temporary_password_set": not bool(password),
            "missing_required_fields": missing_fields,
            "allowed_next_route": allowed_next_route
        }
        return Response(resp_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        instance = self.get_object()
        before = {"email": instance.email, "year": instance.year}
        response = super().partial_update(request, *args, **kwargs)
        instance.refresh_from_db()
        after = {"email": instance.email, "year": instance.year}
        for field in ("email", "year"):
            if str(before[field]) != str(after[field]):
                log_data_correction(
                    actor=request.user,
                    entity_type="user",
                    entity_id=instance.id,
                    field_name=field,
                    old_value=before[field],
                    new_value=after[field],
                    metadata={"source": "user_patch"},
                )
        return response

    def destroy(self, request, *args, **kwargs):
        self._ensure_manage_permission()
        return super().destroy(request, *args, **kwargs)


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.select_related("user").order_by("user__last_name")
    serializer_class = AdminProfileSerializer
    lookup_field = "user_id"
    filterset_fields = ["profile_status"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "designation"]

    def retrieve(self, request, *args, **kwargs):
        if _is_manager(request.user):
            return super().retrieve(request, *args, **kwargs)
        if str(request.user.id) != str(kwargs.get("user_id")):
            raise PermissionDenied("You may only view your own profile.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


class ResidentProfileViewSet(viewsets.ModelViewSet):
    queryset = ResidentProfile.objects.select_related("user").order_by("user__last_name")
    serializer_class = ResidentProfileSerializer
    lookup_field = "user_id"
    filterset_fields = ["is_archived", "profile_status"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "registration_no", "cnic"]

    def retrieve(self, request, *args, **kwargs):
        if _is_manager(request.user):
            return super().retrieve(request, *args, **kwargs)
        if str(request.user.id) != str(kwargs.get("user_id")):
            raise PermissionDenied("You may only view your own profile.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


class SupervisorProfileViewSet(viewsets.ModelViewSet):
    queryset = SupervisorProfile.objects.select_related("user").order_by("user__last_name")
    serializer_class = SupervisorProfileSerializer
    lookup_field = "user_id"
    filterset_fields = ["is_archived", "profile_status"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "pmdc_no"]

    def retrieve(self, request, *args, **kwargs):
        if _is_manager(request.user):
            return super().retrieve(request, *args, **kwargs)
        if str(request.user.id) != str(kwargs.get("user_id")):
            raise PermissionDenied("You may only view your own profile.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


class SupportStaffProfileViewSet(viewsets.ModelViewSet):
    queryset = SupportStaffProfile.objects.select_related("user").order_by("user__last_name")
    serializer_class = SupportStaffProfileSerializer
    lookup_field = "user_id"
    filterset_fields = ["is_archived", "profile_status"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "designation"]

    def retrieve(self, request, *args, **kwargs):
        if _is_manager(request.user):
            return super().retrieve(request, *args, **kwargs)
        if str(request.user.id) != str(kwargs.get("user_id")):
            raise PermissionDenied("You may only view your own profile.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


class StaffProfileViewSet(SupervisorProfileViewSet):
    pass


class DepartmentMembershipViewSet(viewsets.ModelViewSet):
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


class HospitalAssignmentViewSet(viewsets.ModelViewSet):
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


class SupervisionLinkViewSet(viewsets.ModelViewSet):
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

    def _ensure_manage_permission(self):
        if not _is_manager(self.request.user):
            raise PermissionDenied("Only admins may manage supervision links.")

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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def list(self, request, *args, **kwargs):
        if not _is_roster_reader(request.user):
            raise PermissionDenied("Only UTRMC/admin oversight roles may view supervision links.")
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not _is_roster_reader(request.user):
            raise PermissionDenied("Only UTRMC/admin oversight roles may view supervision links.")
        return viewsets.ModelViewSet.retrieve(self, request, *args, **kwargs)


@extend_schema(responses={200: None})
class AuthMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        recalculate_profile_completion(user)
        user.refresh_from_db()
        missing = get_missing_profile_fields(user)
        missing_fields = [m["field"] for m in missing]

        role = user.role
        profile_type = ""
        profile_id = None
        profile_status = "INCOMPLETE"
        profile_schema_version = 1
        completed_schema_version = 0

        if role in PROFILE_COMPLETION_REQUIREMENTS:
            req_config = PROFILE_COMPLETION_REQUIREMENTS[role]
            profile_relation = req_config["profile_relation"]
            profile = getattr(user, profile_relation, None)
            if profile:
                profile_type = profile.__class__.__name__
                profile_id = profile.id
                profile_status = profile.profile_status
                profile_schema_version = profile.profile_schema_version
                completed_schema_version = profile.completed_schema_version

        if user.must_change_password:
            allowed_next_route = "/change-password"
        elif missing:
            allowed_next_route = "/complete-profile"
        else:
            allowed_next_route = user.get_dashboard_url()

        data = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "must_change_password": user.must_change_password,
            "is_profile_complete": user.is_profile_complete,
            "profile_type": profile_type,
            "profile_id": profile_id,
            "profile_status": profile_status,
            "profile_schema_version": profile_schema_version,
            "completed_schema_version": completed_schema_version,
            "missing_required_fields": missing_fields,
            "allowed_next_route": allowed_next_route,
        }
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(responses={200: None})
class CompleteProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        recalculate_profile_completion(user)
        user.refresh_from_db()
        missing = get_missing_profile_fields(user)

        role = user.role
        profile_type = ""
        profile_status = "INCOMPLETE"
        profile_schema_version = 1
        completed_schema_version = 0

        if role in PROFILE_COMPLETION_REQUIREMENTS:
            req_config = PROFILE_COMPLETION_REQUIREMENTS[role]
            profile_relation = req_config["profile_relation"]
            profile = getattr(user, profile_relation, None)
            if profile:
                profile_type = profile.__class__.__name__
                profile_status = profile.profile_status
                profile_schema_version = profile.profile_schema_version
                completed_schema_version = profile.completed_schema_version

        return Response({
            "profile_type": profile_type,
            "profile_status": profile_status,
            "schema_version": profile_schema_version,
            "completed_schema_version": completed_schema_version,
            "missing_fields": missing,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        role = user.role
        if role not in PROFILE_COMPLETION_REQUIREMENTS:
            return Response({"detail": "User role does not require profile completion"}, status=status.HTTP_400_BAD_REQUEST)

        req_config = PROFILE_COMPLETION_REQUIREMENTS[role]
        profile_relation = req_config["profile_relation"]
        profile = getattr(user, profile_relation, None)
        if not profile:
            return Response({"detail": "Profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if profile.profile_status != "COMPLETE":
            ActivityLog.log(
                actor=user,
                action="update",
                verb="PROFILE_COMPLETION_STARTED",
                target=profile,
                metadata={"role": role, "schema_version": profile.profile_schema_version}
            )

        data = request.data
        for req in req_config["required_fields"]:
            field_name = req["field"]
            source = req["source"]

            if field_name in data:
                val = data[field_name]
                if source == "user":
                    if field_name == "full_name":
                        names = val.strip().split(" ", 1)
                        user.first_name = names[0]
                        user.last_name = names[1] if len(names) > 1 else ""
                    elif field_name == "phone":
                        user.phone_number = val
                    else:
                        setattr(user, field_name, val)
                elif source == "profile":
                    if field_name in ["hospital", "training_site_ref"]:
                        try:
                            profile.hospital = Hospital.objects.get(id=val)
                        except (Hospital.DoesNotExist, ValueError):
                            return Response({"detail": f"Hospital ID {val} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                    elif field_name in ["department_ref", "department"]:
                        try:
                            profile.department_ref = Department.objects.get(id=val)
                        except (Department.DoesNotExist, ValueError):
                            return Response({"detail": f"Department ID {val} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                    elif field_name in ["program_ref", "program"]:
                        try:
                            from sims.training.models import TrainingProgram
                            profile.program_ref = TrainingProgram.objects.get(id=val)
                        except Exception:
                            return Response({"detail": f"Program ID {val} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        setattr(profile, field_name, val)

        user.save()
        profile.save()

        recalculate_profile_completion(user)
        user.refresh_from_db()
        profile.refresh_from_db()

        if profile.profile_status == "COMPLETE":
            ActivityLog.log(
                actor=user,
                action="update",
                verb="PROFILE_COMPLETED",
                target=profile,
                metadata={"role": role, "schema_version": profile.profile_schema_version}
            )

        missing = get_missing_profile_fields(user)
        missing_fields = [m["field"] for m in missing]
        allowed_next_route = "/change-password" if user.must_change_password else ("/complete-profile" if missing else user.get_dashboard_url())

        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "must_change_password": user.must_change_password,
            "is_profile_complete": user.is_profile_complete,
            "profile_type": profile.__class__.__name__,
            "profile_id": profile.id,
            "profile_status": profile.profile_status,
            "profile_schema_version": profile.profile_schema_version,
            "completed_schema_version": profile.completed_schema_version,
            "missing_required_fields": missing_fields,
            "allowed_next_route": allowed_next_route,
        }, status=status.HTTP_200_OK)


@extend_schema(responses={200: None})
class IdentityOptionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        hospitals = Hospital.objects.filter(is_active=True).order_by("name")
        departments = Department.objects.filter(active=True).order_by("name")
        
        # Safe lookup for TrainingProgram if initialized
        programs_qs = []
        try:
            from sims.training.models import TrainingProgram
            programs_qs = TrainingProgram.objects.filter(active=True).order_by("name")
        except Exception:
            pass

        academic_sessions = [
            {"id": "2025-2026", "name": "2025-2026 Session"},
            {"id": "2026-2027", "name": "2026-2027 Session"},
            {"id": "2027-2028", "name": "2027-2028 Session"},
        ]

        designations = [
            {"id": "HOD", "name": "Head of Department (HOD)"},
            {"id": "Professor", "name": "Professor"},
            {"id": "Associate Professor", "name": "Associate Professor"},
            {"id": "Assistant Professor", "name": "Assistant Professor"},
            {"id": "Senior Registrar", "name": "Senior Registrar"},
            {"id": "Consultant", "name": "Consultant"},
        ]

        return Response({
            "hospitals": [{"id": h.id, "name": h.name, "code": h.code} for h in hospitals],
            "departments": [{"id": d.id, "name": d.name, "code": d.code} for d in departments],
            "programs": [{"id": p.id, "name": p.name, "code": p.code} for p in programs_qs],
            "academic_sessions": academic_sessions,
            "designations": designations,
        }, status=status.HTTP_200_OK)


def _dq_enabled() -> bool:
    return bool(getattr(settings, "ENABLE_DATA_CORRECTION_LAYER", True))


@extend_schema(responses={200: None})
class DataQualitySummaryView(APIView):
    serializer_class = UserbaseEmptySchemaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not _is_manager(request.user):
            raise PermissionDenied("Only admin/utrmc_admin can view data quality summary.")
        if not _dq_enabled():
            return Response({"detail": "Data correction layer is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        residents = User.objects.filter(role="RESIDENT")
        total = residents.count()
        placeholders = residents.filter(has_placeholder_email=True).count()
        incomplete = residents.filter(is_profile_complete=False).count()
        complete = residents.filter(is_profile_complete=True).count()
        
        # Safe count for missing dates
        missing_dates = 0
        try:
            missing_dates = residents.filter(
                Q(training_records__isnull=True)
                | Q(training_records__has_default_dates=True)
                | Q(resident_links__isnull=True)
                | Q(resident_links__has_default_dates=True)
            ).distinct().count()
        except Exception:
            pass

        return Response(
            {
                "total_users": total,
                "users_with_placeholder_email": placeholders,
                "users_with_missing_dates": missing_dates,
                "complete_profiles": complete,
                "incomplete_profiles": incomplete,
            }
        )


@extend_schema(responses={200: None})
class DataQualityUsersView(APIView):
    serializer_class = UserbaseEmptySchemaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not _is_manager(request.user):
            raise PermissionDenied("Only admin/utrmc_admin can view data quality users.")
        if not _dq_enabled():
            return Response({"detail": "Data correction layer is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        filter_value = (request.query_params.get("filter") or "").strip().lower()
        queryset = User.objects.filter(role="RESIDENT").select_related("supervisor").order_by(
            "last_name", "first_name"
        )
        if filter_value == "placeholder_email":
            queryset = queryset.filter(has_placeholder_email=True)
        elif filter_value == "incomplete_profile":
            queryset = queryset.filter(is_profile_complete=False)
        elif filter_value == "missing_dates":
            try:
                queryset = queryset.filter(
                    Q(training_records__isnull=True)
                    | Q(training_records__has_default_dates=True)
                    | Q(resident_links__isnull=True)
                    | Q(resident_links__has_default_dates=True)
                ).distinct()
            except Exception:
                pass
        elif filter_value == "missing_email":
            queryset = queryset.filter(Q(email__isnull=True) | Q(email=""))

        payload = []
        for user in queryset:
            has_missing_dates = False
            try:
                has_missing_dates = (
                    not user.training_records.exists()
                    or user.training_records.filter(has_default_dates=True).exists()
                    or not user.resident_links.exists()
                    or user.resident_links.filter(has_default_dates=True).exists()
                )
            except Exception:
                pass

            payload.append(
                {
                    "id": user.id,
                    "name": user.get_full_name() or user.username,
                    "email": user.email,
                    "year": user.year,
                    "supervisor": user.supervisor.get_full_name() if user.supervisor else "",
                    "issues": user.data_issues or [],
                    "is_complete_profile": user.is_profile_complete,
                    "has_placeholder_email": user.has_placeholder_email,
                    "has_missing_dates": has_missing_dates,
                }
            )
        return Response(payload)


@extend_schema(responses={200: None})
class DataQualityRecomputeView(APIView):
    serializer_class = UserbaseEmptySchemaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not _is_manager(request.user):
            raise PermissionDenied("Only admin/utrmc_admin can recompute data quality.")
        if not _dq_enabled():
            return Response({"detail": "Data correction layer is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        summary = recompute_all()
        return Response(summary, status=status.HTTP_200_OK)


@extend_schema(responses={200: None})
class DataCorrectionAuditView(APIView):
    serializer_class = UserbaseEmptySchemaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not _is_manager(request.user):
            raise PermissionDenied("Only admin/utrmc_admin can view correction audits.")
        if not _dq_enabled():
            return Response({"detail": "Data correction layer is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        rows = DataCorrectionAudit.objects.select_related("actor").order_by("-created_at")[:200]
        return Response(
            [
                {
                    "id": row.id,
                    "actor": row.actor.get_full_name() if row.actor else "",
                    "entity_type": row.entity_type,
                    "entity_id": row.entity_id,
                    "field_name": row.field_name,
                    "old_value": row.old_value,
                    "new_value": row.new_value,
                    "metadata": row.metadata,
                    "fingerprint": settings.ADMIN_RESET_FINGERPRINT,
                    "timestamp": row.created_at,
                }
                for row in rows
            ]
        )
