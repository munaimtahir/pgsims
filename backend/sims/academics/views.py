from datetime import date

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sims.common_permissions import ReadAnyWriteAdminOnly

from django.db.models import Q
from rest_framework.exceptions import ValidationError

from .models import (
    AcademicPeriod,
    AcademicSession,
    Department,
    EvaluationFormTemplate,
    LogbookCategory,
    ResidentTrainingRecord,
    RotationTemplate,
    SupervisorReviewQueueItem,
    EvaluationSubmission,
    EvaluationResponse,
    LogbookEntry,
    ProcedureRecord,
)
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile
from sims.supervision.models import ResidentSupervisorAssignment

from .serializers import (
    AcademicPeriodSerializer,
    EvaluationFormTemplateSerializer,
    LogbookCategorySerializer,
    ResidentTrainingRecordSerializer,
    RotationTemplateSerializer,
    SupervisorReviewQueueItemSerializer,
    EvaluationSubmissionSerializer,
    EvaluationResponseSerializer,
    LogbookEntrySerializer,
    ProcedureRecordSerializer,
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
    create_evaluation_submission,
    update_evaluation_draft,
    submit_evaluation,
    start_evaluation_review,
    approve_evaluation,
    return_evaluation,
    reject_evaluation,
    cancel_evaluation,
    create_logbook_entry,
    update_logbook_draft,
    submit_logbook_entry,
    verify_logbook_entry,
    return_logbook_entry,
    reject_logbook_entry,
    cancel_logbook_entry,
    get_resident_academic_progress,
    get_supervisor_academic_workload,
    get_admin_academic_workflow_overview,
    seed_pilot_academic_workflows,
)



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


class EvaluationSubmissionViewSet(viewsets.ModelViewSet):
    queryset = EvaluationSubmission.objects.all()
    serializer_class = EvaluationSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN" or user.is_superuser:
            return self.queryset
        elif user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            return self.queryset.filter(resident=user.resident_profile)
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            supervised_residents = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                status="ACTIVE"
            ).values_list("resident_id", flat=True)
            return self.queryset.filter(
                Q(supervisor=user.supervisor_profile) | Q(resident_id__in=supervised_residents)
            )
        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "RESIDENT" and user.role != "ADMIN":
            raise PermissionDenied("Only residents or admins can create evaluation submissions.")
        
        if user.role == "RESIDENT":
            if not hasattr(user, "resident_profile"):
                raise ValidationError({"resident": "Resident profile not found."})
            resident = user.resident_profile
        else:
            resident_id = self.request.data.get("resident")
            if not resident_id:
                raise ValidationError({"resident": "Resident field is required."})
            resident = ResidentProfile.objects.get(pk=resident_id)

        template_id = self.request.data.get("template")
        if not template_id:
            raise ValidationError({"template": "Template field is required."})
        template = EvaluationFormTemplate.objects.get(pk=template_id)

        supervisor_id = self.request.data.get("supervisor")
        supervisor = SupervisorProfile.objects.filter(pk=supervisor_id).first() if supervisor_id else None

        period_id = self.request.data.get("academic_period")
        period = AcademicPeriod.objects.filter(pk=period_id).first() if period_id else None

        responses = self.request.data.get("responses", [])

        submission = create_evaluation_submission(
            resident=resident,
            template=template,
            supervisor=supervisor,
            academic_period=period,
            resident_comments=self.request.data.get("resident_comments", ""),
            extra_data=self.request.data.get("extra_data", {}),
            responses=responses,
            actor=user,
        )
        serializer.instance = submission

    def perform_update(self, serializer):
        user = self.request.user
        submission = self.get_object()
        
        if user.role == "RESIDENT":
            if submission.resident.user_id != user.id:
                raise PermissionDenied("You can only edit your own evaluation draft.")
        elif user.role != "ADMIN":
            raise PermissionDenied("You cannot edit this evaluation draft.")

        responses = self.request.data.get("responses")
        
        updated_sub = update_evaluation_draft(
            submission=submission,
            resident_comments=self.request.data.get("resident_comments"),
            supervisor_comments=self.request.data.get("supervisor_comments"),
            score=self.request.data.get("score"),
            max_score=self.request.data.get("max_score"),
            extra_data=self.request.data.get("extra_data"),
            responses=responses,
            actor=user,
        )
        serializer.instance = updated_sub

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        submission = self.get_object()
        if request.user.role == "RESIDENT" and submission.resident.user_id != request.user.id:
            raise PermissionDenied("You can only submit your own evaluations.")
        submit_evaluation(submission=submission, actor=request.user)
        return Response(self.get_serializer(submission).data)

    @action(detail=True, methods=["post"])
    def start_review(self, request, pk=None):
        submission = self.get_object()
        start_evaluation_review(submission=submission, actor=request.user)
        return Response(self.get_serializer(submission).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        submission = self.get_object()
        score = request.data.get("score")
        max_score = request.data.get("max_score")
        approve_evaluation(
            submission=submission,
            supervisor_comments=request.data.get("supervisor_comments", ""),
            score=score,
            max_score=max_score,
            actor=request.user,
        )
        return Response(self.get_serializer(submission).data)

    @action(detail=True, methods=["post"])
    def return_revision(self, request, pk=None):
        submission = self.get_object()
        comments = request.data.get("supervisor_comments")
        if not comments:
            raise ValidationError({"supervisor_comments": "Supervisor comments are required when returning an evaluation."})
        return_evaluation(submission=submission, supervisor_comments=comments, actor=request.user)
        return Response(self.get_serializer(submission).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        submission = self.get_object()
        reject_evaluation(
            submission=submission,
            supervisor_comments=request.data.get("supervisor_comments", ""),
            actor=request.user,
        )
        return Response(self.get_serializer(submission).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        submission = self.get_object()
        if request.user.role == "RESIDENT" and submission.resident.user_id != request.user.id:
            raise PermissionDenied("You can only cancel your own evaluations.")
        cancel_evaluation(submission=submission, actor=request.user)
        return Response(self.get_serializer(submission).data)


class LogbookEntryViewSet(viewsets.ModelViewSet):
    queryset = LogbookEntry.objects.all()
    serializer_class = LogbookEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN" or user.is_superuser:
            return self.queryset
        elif user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            return self.queryset.filter(resident=user.resident_profile)
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            supervised_residents = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                status="ACTIVE"
            ).values_list("resident_id", flat=True)
            return self.queryset.filter(
                Q(supervisor=user.supervisor_profile) | Q(resident_id__in=supervised_residents)
            )
        return self.queryset.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "RESIDENT" and user.role != "ADMIN":
            raise PermissionDenied("Only residents or admins can create logbook entries.")

        if user.role == "RESIDENT":
            if not hasattr(user, "resident_profile"):
                raise ValidationError({"resident": "Resident profile not found."})
            resident = user.resident_profile
        else:
            resident_id = self.request.data.get("resident")
            if not resident_id:
                raise ValidationError({"resident": "Resident field is required."})
            resident = ResidentProfile.objects.get(pk=resident_id)

        category_id = self.request.data.get("category")
        if not category_id:
            raise ValidationError({"category": "Category field is required."})
        category = LogbookCategory.objects.get(pk=category_id)

        supervisor_id = self.request.data.get("supervisor")
        supervisor = SupervisorProfile.objects.filter(pk=supervisor_id).first() if supervisor_id else None

        period_id = self.request.data.get("academic_period")
        period = AcademicPeriod.objects.filter(pk=period_id).first() if period_id else None

        entry_date_str = self.request.data.get("entry_date")
        if not entry_date_str:
            raise ValidationError({"entry_date": "Entry date is required."})
        entry_date = date.fromisoformat(entry_date_str)

        procedure_data = self.request.data.get("procedure_data") or self.request.data.get("procedure_record")

        entry = create_logbook_entry(
            resident=resident,
            category=category,
            entry_date=entry_date,
            title=self.request.data.get("title", ""),
            description=self.request.data.get("description", ""),
            case_identifier=self.request.data.get("case_identifier", ""),
            patient_age=self.request.data.get("patient_age", ""),
            patient_gender=self.request.data.get("patient_gender", ""),
            supervisor=supervisor,
            academic_period=period,
            resident_reflection=self.request.data.get("resident_reflection", ""),
            extra_data=self.request.data.get("extra_data", {}),
            procedure_data=procedure_data,
            actor=user,
        )
        serializer.instance = entry

    def perform_update(self, serializer):
        user = self.request.user
        entry = self.get_object()

        if user.role == "RESIDENT":
            if entry.resident.user_id != user.id:
                raise PermissionDenied("You can only edit your own logbook entry draft.")
        elif user.role != "ADMIN":
            raise PermissionDenied("You cannot edit this logbook entry draft.")

        entry_date = None
        entry_date_str = self.request.data.get("entry_date")
        if entry_date_str:
            entry_date = date.fromisoformat(entry_date_str)

        procedure_data = self.request.data.get("procedure_data") or self.request.data.get("procedure_record")

        updated_entry = update_logbook_draft(
            entry=entry,
            title=self.request.data.get("title"),
            description=self.request.data.get("description"),
            entry_date=entry_date,
            case_identifier=self.request.data.get("case_identifier"),
            patient_age=self.request.data.get("patient_age"),
            patient_gender=self.request.data.get("patient_gender"),
            resident_reflection=self.request.data.get("resident_reflection"),
            supervisor=self.request.data.get("supervisor"),
            academic_period=self.request.data.get("academic_period"),
            extra_data=self.request.data.get("extra_data"),
            procedure_data=procedure_data,
            actor=user,
        )
        serializer.instance = updated_entry

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        entry = self.get_object()
        if request.user.role == "RESIDENT" and entry.resident.user_id != request.user.id:
            raise PermissionDenied("You can only submit your own logbook entries.")
        submit_logbook_entry(entry=entry, actor=request.user)
        return Response(self.get_serializer(entry).data)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        entry = self.get_object()
        verify_logbook_entry(
            entry=entry,
            supervisor_comments=request.data.get("supervisor_comments", ""),
            actor=request.user,
        )
        return Response(self.get_serializer(entry).data)

    @action(detail=True, methods=["post"])
    def return_revision(self, request, pk=None):
        entry = self.get_object()
        comments = request.data.get("supervisor_comments")
        if not comments:
            raise ValidationError({"supervisor_comments": "Supervisor comments are required when returning a logbook entry."})
        return_logbook_entry(entry=entry, supervisor_comments=comments, actor=request.user)
        return Response(self.get_serializer(entry).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        entry = self.get_object()
        reject_logbook_entry(
            entry=entry,
            supervisor_comments=request.data.get("supervisor_comments", ""),
            actor=request.user,
        )
        return Response(self.get_serializer(entry).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        entry = self.get_object()
        if request.user.role == "RESIDENT" and entry.resident.user_id != request.user.id:
            raise PermissionDenied("You can only cancel your own logbook entries.")
        cancel_logbook_entry(entry=entry, actor=request.user)
        return Response(self.get_serializer(entry).data)


class MyAcademicProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "resident_profile"):
            raise PermissionDenied("Resident profile not found.")
        return Response(get_resident_academic_progress(resident=request.user.resident_profile))


class ResidentAcademicProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, resident_id: int):
        resident = ResidentProfile.objects.select_related("user").get(pk=resident_id)
        if not can_view_resident_profile(request.user, resident):
            raise PermissionDenied("You are not allowed to view this resident academic progress.")
        return Response(get_resident_academic_progress(resident=resident))


class SupervisorAcademicWorkloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "supervisor_profile"):
            raise PermissionDenied("Supervisor profile not found.")
        return Response(get_supervisor_academic_workload(supervisor=request.user.supervisor_profile))


class AdminAcademicWorkflowOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access global academic workflow overview.")
        return Response(get_admin_academic_workflow_overview())


class AcademicWorkflowDataQualityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access global data quality checks.")
        return Response(get_academic_data_quality())


class AcademicWorkflowSeedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can seed pilot academic workflows.")
        return Response(seed_pilot_academic_workflows(actor=request.user))


# --- Brick 11: Dashboards, Reports, and Monitoring Views ---

class AdminDashboardMonitoringView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access global monitoring.")
        from sims.academics.reporting import get_admin_monitoring_dashboard
        data = get_admin_monitoring_dashboard()
        return Response(data)


class SupervisorDashboardMonitoringView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, "supervisor_profile"):
            raise PermissionDenied("Supervisor profile not found.")
        from sims.academics.reporting import get_supervisor_monitoring_dashboard
        data = get_supervisor_monitoring_dashboard(request.user.supervisor_profile)
        return Response(data)


class MyProgressMonitoringView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not hasattr(request.user, "resident_profile"):
            raise PermissionDenied("Resident profile not found.")
        from sims.academics.reporting import get_resident_monitoring_my_progress
        data = get_resident_monitoring_my_progress(request.user.resident_profile)
        return Response(data)


class DepartmentMonitoringSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access department summary.")
        from sims.academics.reporting import get_department_monitoring_summary
        return Response(get_department_monitoring_summary())


class ProgramMonitoringSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access program summary.")
        from sims.academics.reporting import get_program_monitoring_summary
        return Response(get_program_monitoring_summary())


class SessionMonitoringSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not (request.user.is_superuser or request.user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access session summary.")
        from sims.academics.reporting import get_session_monitoring_summary
        return Response(get_session_monitoring_summary())


class ResidentProgressReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, resident_id=None):
        user = request.user
        from sims.academics.reporting import get_resident_progress_report
        
        if resident_id is None:
            if user.role == "RESIDENT":
                raise PermissionDenied("Residents cannot access reports listing.")
            elif user.role in ["ADMIN", "SUPPORT_STAFF"] or user.is_superuser:
                if user.role == "SUPPORT_STAFF" and not user.is_superuser:
                    raise PermissionDenied("Support staff blocked by default.")
                residents = ResidentProfile.objects.filter(is_archived=False).select_related("user")
                res_list = []
                for res in residents:
                    res_list.append({
                        "id": res.id,
                        "name": res.user.get_full_name() or res.user.username,
                        "username": res.user.username,
                    })
                return Response(res_list)
            elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
                assigned = ResidentSupervisorAssignment.objects.filter(
                    supervisor=user.supervisor_profile,
                    status="ACTIVE"
                ).select_related("resident__user")
                res_list = []
                for ass in assigned:
                    res_list.append({
                        "id": ass.resident.id,
                        "name": ass.resident.user.get_full_name() or ass.resident.user.username,
                        "username": ass.resident.user.username,
                    })
                return Response(res_list)
            raise PermissionDenied("Not authorized.")
            
        if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            if user.resident_profile.id != resident_id:
                raise PermissionDenied("Residents can only access their own report.")
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            exists = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                resident_id=resident_id,
                status="ACTIVE"
            ).exists()
            if not exists:
                raise PermissionDenied("Supervisors can only view assigned resident progress.")
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        data = get_resident_progress_report(resident_id)
        return Response(data)


class ResidentProgressReportDetailView(ResidentProgressReportView):
    pass


class SupervisorWorkloadReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, supervisor_id=None):
        user = request.user
        from sims.academics.reporting import get_supervisor_workload_report
        
        if supervisor_id is None:
            if user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
                data = get_supervisor_workload_report(user.supervisor_profile.id)
                return Response(data)
            elif user.role in ["ADMIN", "SUPPORT_STAFF"] or user.is_superuser:
                if user.role == "SUPPORT_STAFF" and not user.is_superuser:
                    raise PermissionDenied("Support staff blocked by default.")
                supervisors = SupervisorProfile.objects.filter(is_archived=False).select_related("user")
                sup_list = []
                for sup in supervisors:
                    sup_list.append({
                        "id": sup.id,
                        "name": sup.user.get_full_name() or sup.user.username,
                        "username": sup.user.username,
                    })
                return Response(sup_list)
            raise PermissionDenied("Not authorized.")
            
        if user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            if user.supervisor_profile.id != supervisor_id:
                raise PermissionDenied("Supervisors can only view self workload report.")
        elif user.role == "RESIDENT":
            raise PermissionDenied("Residents cannot access supervisor workload report.")
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        data = get_supervisor_workload_report(supervisor_id)
        return Response(data)


class SupervisorWorkloadReportDetailView(SupervisorWorkloadReportView):
    pass


class EvaluationReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        filters = request.GET.copy()
        from sims.academics.reporting import get_evaluation_report
        
        if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            filters["resident_id"] = user.resident_profile.id
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            assigned_ids = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                status="ACTIVE"
            ).values_list("resident_id", flat=True)
            req_res = filters.get("resident_id")
            if req_res:
                if int(req_res) not in assigned_ids:
                    raise PermissionDenied("You can only query assigned resident evaluations.")
            else:
                filters["supervisor_id"] = user.supervisor_profile.id
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        data = get_evaluation_report(filters)
        return Response(data)


class LogbookReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        filters = request.GET.copy()
        from sims.academics.reporting import get_logbook_report
        
        if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            filters["resident_id"] = user.resident_profile.id
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            assigned_ids = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                status="ACTIVE"
            ).values_list("resident_id", flat=True)
            req_res = filters.get("resident_id")
            if req_res:
                if int(req_res) not in assigned_ids:
                    raise PermissionDenied("You can only query assigned resident logbooks.")
            else:
                filters["supervisor_id"] = user.supervisor_profile.id
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        data = get_logbook_report(filters)
        return Response(data)


class DataQualityReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if not (user.is_superuser or user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access data quality reports.")
        data = get_academic_data_quality()
        return Response(data)


# --- Brick 11: CSV Exports views ---

def generate_csv_response(filename: str, headers: list, rows: list, keys: list):
    import csv
    from django.http import HttpResponse
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(headers)
    for row in rows:
        writer.writerow([row.get(key, "") for key in keys])
    return response


class ResidentProgressExportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        resident_id = request.GET.get("resident_id")
        from sims.academics.reporting import get_resident_progress_report
        
        if resident_id is None:
            if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
                resident_id = user.resident_profile.id
            else:
                raise PermissionDenied("Specify resident_id to export.")
                
        resident_id = int(resident_id)
        if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            if user.resident_profile.id != resident_id:
                raise PermissionDenied("Residents can only export their own progress.")
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            exists = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                resident_id=resident_id,
                status="ACTIVE"
            ).exists()
            if not exists:
                raise PermissionDenied("Supervisors can only export assigned resident progress.")
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        report = get_resident_progress_report(resident_id)
        res = report["resident"]
        prog = report["progress"]
        
        filename = f"resident_progress_{res['username']}.csv"
        headers = ["Resident Name", "Username", "Email", "Program", "Department", "Training Year", "Record Status", "Total Evaluations", "Approved Evaluations", "Total Logbooks", "Verified Logbooks"]
        keys = ["name", "username", "email", "program", "dept", "year", "status", "evals_total", "evals_app", "log_total", "log_ver"]
        rows = [{
            "name": res["name"],
            "username": res["username"],
            "email": res["email"],
            "program": res["program_name"],
            "dept": res["department_name"],
            "year": prog["training_year"],
            "status": prog["training_record_status"],
            "evals_total": prog["evaluations_total"],
            "evals_app": prog["evaluations_approved"],
            "log_total": prog["logbooks_total"],
            "log_ver": prog["logbooks_verified"],
        }]
        return generate_csv_response(filename, headers, rows, keys)


class SupervisorWorkloadExportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        supervisor_id = request.GET.get("supervisor_id")
        from sims.academics.reporting import get_supervisor_workload_report
        
        if supervisor_id is None:
            if user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
                supervisor_id = user.supervisor_profile.id
            else:
                raise PermissionDenied("Specify supervisor_id to export.")
                
        supervisor_id = int(supervisor_id)
        if user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            if user.supervisor_profile.id != supervisor_id:
                raise PermissionDenied("Supervisors can only export self workload.")
        elif user.role == "RESIDENT":
            raise PermissionDenied("Residents cannot export supervisor workload.")
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        report = get_supervisor_workload_report(supervisor_id)
        sup = report["supervisor"]
        wl = report["workload"]
        
        filename = f"supervisor_workload_{sup['username']}.csv"
        headers = ["Supervisor Name", "Username", "Email", "Department", "Assigned Residents Count", "Pending Evaluations", "Pending Logbooks", "Overdue Reviews"]
        keys = ["name", "username", "email", "dept", "residents_count", "pending_evals", "pending_log", "overdue"]
        rows = [{
            "name": sup["name"],
            "username": sup["username"],
            "email": sup["email"],
            "dept": sup["department_name"],
            "residents_count": wl["assigned_residents_count"],
            "pending_evals": wl["pending_evaluation_reviews_count"],
            "pending_log": wl["pending_logbook_reviews_count"],
            "overdue": wl["overdue_reviews_count"],
        }]
        return generate_csv_response(filename, headers, rows, keys)


class EvaluationReportExportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        filters = request.GET.copy()
        from sims.academics.reporting import get_evaluation_report
        
        if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            filters["resident_id"] = user.resident_profile.id
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            assigned_ids = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                status="ACTIVE"
            ).values_list("resident_id", flat=True)
            req_res = filters.get("resident_id")
            if req_res:
                if int(req_res) not in assigned_ids:
                    raise PermissionDenied("You can only query assigned resident evaluations.")
            else:
                filters["supervisor_id"] = user.supervisor_profile.id
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        data = get_evaluation_report(filters)
        
        filename = "evaluation_report.csv"
        headers = ["Resident", "Supervisor", "Template", "Department", "Program", "Session", "Status", "Score", "Max Score", "Submitted At", "Approved At", "Pending Age (Days)"]
        keys = ["resident_name", "supervisor_name", "template_name", "department_name", "program_name", "session_name", "status", "score", "max_score", "submitted_at", "approved_at", "pending_age"]
        return generate_csv_response(filename, headers, data, keys)


class LogbookReportExportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        filters = request.GET.copy()
        from sims.academics.reporting import get_logbook_report
        
        if user.role == "RESIDENT" and hasattr(user, "resident_profile"):
            filters["resident_id"] = user.resident_profile.id
        elif user.role == "SUPERVISOR" and hasattr(user, "supervisor_profile"):
            assigned_ids = ResidentSupervisorAssignment.objects.filter(
                supervisor=user.supervisor_profile,
                status="ACTIVE"
            ).values_list("resident_id", flat=True)
            req_res = filters.get("resident_id")
            if req_res:
                if int(req_res) not in assigned_ids:
                    raise PermissionDenied("You can only query assigned resident logbooks.")
            else:
                filters["supervisor_id"] = user.supervisor_profile.id
        elif user.role == "SUPPORT_STAFF" and not user.is_superuser:
            raise PermissionDenied("Support staff blocked by default.")
            
        data = get_logbook_report(filters)
        
        filename = "logbook_report.csv"
        headers = ["Resident", "Supervisor", "Category", "Type", "Title", "Entry Date", "Status", "Submitted At", "Verified At", "Pending Age (Days)", "Procedure Name", "Procedure Code", "Role Performed", "Complexity", "Outcome"]
        keys = ["resident_name", "supervisor_name", "category_name", "category_type", "title", "entry_date", "status", "submitted_at", "verified_at", "pending_age", "procedure_name", "procedure_code", "role_performed", "complexity", "outcome"]
        return generate_csv_response(filename, headers, data, keys)


class DataQualityReportExportCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        if not (user.is_superuser or user.role == "ADMIN"):
            raise PermissionDenied("Only admins can access data quality reports.")
        data = get_academic_data_quality()
        sections = data.get("sections", [])
        
        filename = "data_quality_report.csv"
        headers = ["Discrepancy Category", "Resident Name/Detail", "Issue details/Notes"]
        keys = ["category", "resident", "details"]
        
        rows = []
        for sec in sections:
            category_label = sec.get("label", "Unknown")
            for item in sec.get("items", []):
                rows.append({
                    "category": category_label,
                    "resident": item.get("resident_name") or item.get("name") or "Unknown",
                    "details": item.get("issue_details") or item.get("notes") or "Missing training records or supervisor links",
                })
        return generate_csv_response(filename, headers, rows, keys)


