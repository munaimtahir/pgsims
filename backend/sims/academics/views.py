from datetime import date

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sims.common_permissions import ReadAnyWriteAdminOnly

from .models import (
    AcademicPeriod,
    AcademicSession,
    Department,
    Designation,
    EvaluationFormTemplate,
    Institution,
    LogbookCategory,
    ResidentTrainingRecord,
    RotationTemplate,
    Specialty,
    SupervisorReviewQueueItem,
)
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile

from .serializers import (
    AcademicPeriodSerializer,
    DepartmentSerializer,
    InstitutionSerializer,
    HospitalSerializer,
    TrainingProgramSerializer,
    SpecialtySerializer,
    DesignationSerializer,
    AcademicSessionSerializer,
    EvaluationFormTemplateSerializer,
    LogbookCategorySerializer,
    ResidentTrainingRecordSerializer,
    RotationTemplateSerializer,
    SupervisorReviewQueueItemSerializer,
)
from .permissions import (
    IsAcademicAdminOrReadOnly,
    can_view_resident_profile,
    can_view_supervisor_profile,
)
from .services import (
    close_training_record,
    create_review_queue_item,
    create_training_record,
    dismiss_review_queue_item,
    get_academic_data_quality,
    get_admin_academic_overview,
    get_resident_academic_summary,
    get_supervisor_academic_summary,
    seed_pilot_academics,
    update_training_record,
)


class InstitutionViewSet(viewsets.ModelViewSet):
    """ViewSet for Institution CRUD operations."""

    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(active=True)


class HospitalViewSet(viewsets.ModelViewSet):
    """ViewSet for Hospital CRUD operations."""

    queryset = Hospital.objects.all().order_by("name")
    serializer_class = HospitalSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["is_active", "code"]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(is_active=True)


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(active=True)


class TrainingProgramViewSet(viewsets.ModelViewSet):
    """ViewSet for TrainingProgram CRUD operations."""

    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code", "degree_type"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(active=True)


class SpecialtyViewSet(viewsets.ModelViewSet):
    """ViewSet for Specialty CRUD operations."""

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(active=True)


class DesignationViewSet(viewsets.ModelViewSet):
    """ViewSet for Designation CRUD operations."""

    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(active=True)


class AcademicSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for AcademicSession CRUD operations."""

    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        return queryset.filter(active=True)


class ResidentTrainingRecordViewSet(viewsets.ModelViewSet):
    queryset = ResidentTrainingRecord.objects.select_related(
        "resident__user",
        "program",
        "academic_session",
        "training_site",
        "department",
    ).order_by("-is_active", "-created_at")
    serializer_class = ResidentTrainingRecordSerializer
    permission_classes = [IsAcademicAdminOrReadOnly]
    filterset_fields = ["resident", "program", "academic_session", "department", "status", "is_active"]
    search_fields = ["resident__user__username", "resident__user__first_name", "resident__user__last_name"]
    ordering_fields = ["created_at", "start_date", "training_year"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        if getattr(user, "role", None) == "RESIDENT" and hasattr(user, "resident_profile"):
            return queryset.filter(resident=user.resident_profile)
        if getattr(user, "role", None) == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            return queryset.filter(
                resident__supervisor_assignments__supervisor=user.supervisor_profile,
                resident__supervisor_assignments__is_active=True,
            ).distinct()
        if getattr(user, "role", None) == "SUPPORT_STAFF":
            return queryset
        return queryset.none()

    def perform_create(self, serializer):
        resident = serializer.validated_data["resident"]
        record = create_training_record(actor=self.request.user, resident=resident, **{
            key: serializer.validated_data.get(key)
            for key in ["program", "academic_session", "training_site", "department", "start_date", "expected_end_date", "training_year", "notes"]
        })
        serializer.instance = record

    def perform_update(self, serializer):
        update_training_record(record=serializer.instance, actor=self.request.user, **serializer.validated_data)

    @action(detail=True, methods=["post"], url_path="close")
    def close(self, request, pk=None):
        record = self.get_object()
        actual_end_date = request.data.get("actual_end_date")
        if actual_end_date:
            actual_end_date = date.fromisoformat(actual_end_date)
        close_training_record(
            record=record,
            actual_end_date=actual_end_date,
            status_value=request.data.get("status", ResidentTrainingRecord.STATUS_COMPLETED),
            notes=request.data.get("notes", ""),
            actor=request.user,
        )
        serializer = self.get_serializer(record)
        return Response(serializer.data)


class AcademicPeriodViewSet(viewsets.ModelViewSet):
    queryset = AcademicPeriod.objects.select_related("academic_session").order_by("sort_order", "start_date")
    serializer_class = AcademicPeriodSerializer
    permission_classes = [IsAcademicAdminOrReadOnly]
    filterset_fields = ["academic_session", "period_type", "is_active"]
    search_fields = ["name", "code"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class RotationTemplateViewSet(viewsets.ModelViewSet):
    queryset = RotationTemplate.objects.select_related("program", "department").order_by("name")
    serializer_class = RotationTemplateSerializer
    permission_classes = [IsAcademicAdminOrReadOnly]
    filterset_fields = ["program", "department", "training_year", "is_required", "is_active"]
    search_fields = ["name", "code"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class EvaluationFormTemplateViewSet(viewsets.ModelViewSet):
    queryset = EvaluationFormTemplate.objects.select_related("program", "department").order_by("name")
    serializer_class = EvaluationFormTemplateSerializer
    permission_classes = [IsAcademicAdminOrReadOnly]
    filterset_fields = ["program", "department", "form_type", "is_active"]
    search_fields = ["name", "code"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class LogbookCategoryViewSet(viewsets.ModelViewSet):
    queryset = LogbookCategory.objects.select_related("program", "department").order_by("name")
    serializer_class = LogbookCategorySerializer
    permission_classes = [IsAcademicAdminOrReadOnly]
    filterset_fields = ["program", "department", "category_type", "is_active"]
    search_fields = ["name", "code"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class SupervisorReviewQueueItemViewSet(viewsets.ModelViewSet):
    queryset = SupervisorReviewQueueItem.objects.select_related(
        "resident__user", "supervisor__user", "training_record"
    ).order_by("status", "due_date", "-created_at")
    serializer_class = SupervisorReviewQueueItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["resident", "supervisor", "queue_type", "status"]
    search_fields = [
        "resident__user__username",
        "resident__user__first_name",
        "resident__user__last_name",
        "supervisor__user__username",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) == "ADMIN":
            return queryset
        if getattr(user, "role", None) == "RESIDENT" and hasattr(user, "resident_profile"):
            return queryset.filter(resident=user.resident_profile)
        if getattr(user, "role", None) == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            return queryset.filter(supervisor=user.supervisor_profile)
        if getattr(user, "role", None) == "SUPPORT_STAFF":
            return queryset
        return queryset.none()

    def create(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can create academic review queue items.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = create_review_queue_item(
            resident=serializer.validated_data["resident"],
            supervisor=serializer.validated_data["supervisor"],
            training_record=serializer.validated_data.get("training_record"),
            queue_type=serializer.validated_data["queue_type"],
            due_date=serializer.validated_data.get("due_date"),
            notes=serializer.validated_data.get("notes", ""),
            actor=request.user,
        )
        return Response(self.get_serializer(item).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()
        if not (
            request.user.is_superuser
            or request.user.role == "ADMIN"
            or (request.user.role == "SUPERVISOR" and hasattr(request.user, "supervisor_profile") and item.supervisor_id == request.user.supervisor_profile.id)
        ):
            raise PermissionDenied("You are not allowed to update this review queue item.")
        status_value = request.data.get("status")
        if status_value in {SupervisorReviewQueueItem.STATUS_DONE, SupervisorReviewQueueItem.STATUS_DISMISSED}:
            dismiss_review_queue_item(item=item, actor=request.user, status_value=status_value, notes=request.data.get("notes", ""))
            return Response(self.get_serializer(item).data)
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


class AcademicOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_admin_academic_overview())


class AcademicDataQualityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(get_academic_data_quality())


class AcademicOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "residents": [
                    {"id": row.id, "name": row.user.get_full_name() or row.user.username, "username": row.user.username}
                    for row in ResidentProfile.objects.select_related("user").filter(is_archived=False).order_by("user__first_name", "user__last_name")
                ],
                "supervisors": [
                    {"id": row.id, "name": row.user.get_full_name() or row.user.username, "username": row.user.username}
                    for row in SupervisorProfile.objects.select_related("user").filter(is_archived=False).order_by("user__first_name", "user__last_name")
                ],
                "programs": [{"id": row.id, "name": row.name, "code": row.code} for row in TrainingProgram.objects.filter(active=True).order_by("name")],
                "academic_sessions": [{"id": row.id, "name": row.name, "code": row.code} for row in AcademicSession.objects.filter(active=True).order_by("name")],
                "training_sites": [{"id": row.id, "name": row.name, "code": row.code} for row in Hospital.objects.filter(is_active=True).order_by("name")],
                "departments": [{"id": row.id, "name": row.name, "code": row.code} for row in Department.objects.filter(active=True).order_by("name")],
                "periods": [{"id": row.id, "name": row.name, "code": row.code} for row in AcademicPeriod.objects.filter(is_active=True).order_by("sort_order", "name")],
            }
        )


class ResidentAcademicSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resident_id: int):
        resident = ResidentProfile.objects.select_related("user", "department_ref", "program_ref", "academic_session_ref").get(pk=resident_id)
        if not can_view_resident_profile(request.user, resident):
            raise PermissionDenied("You are not allowed to view this resident academic summary.")
        return Response(get_resident_academic_summary(resident=resident))


class MyResidentAcademicSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "resident_profile"):
            raise PermissionDenied("Resident profile not found.")
        return Response(get_resident_academic_summary(resident=request.user.resident_profile))


class SupervisorAcademicSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, supervisor_id: int):
        supervisor = SupervisorProfile.objects.select_related("user").get(pk=supervisor_id)
        if not can_view_supervisor_profile(request.user, supervisor):
            raise PermissionDenied("You are not allowed to view this supervisor academic summary.")
        return Response(get_supervisor_academic_summary(supervisor=supervisor))


class MySupervisorAcademicSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "supervisor_profile"):
            raise PermissionDenied("Supervisor profile not found.")
        return Response(get_supervisor_academic_summary(supervisor=request.user.supervisor_profile))


class AcademicSeedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can seed pilot academic data.")
        return Response(seed_pilot_academics(actor=request.user))
