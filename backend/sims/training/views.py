"""
Training & Rotations API views.

RBAC summary:
  TrainingProgram / ProgramRotationTemplate  → admin | utrmc_admin (write); authenticated (read)
  ResidentTrainingRecord                     → admin | utrmc_admin (write); resident sees own
  RotationAssignment                         → DRAFT/SUBMITTED by utrmc_admin|admin; state machine actions role-gated
  LeaveRequest / DeputationPosting           → resident creates; approvers approve
"""
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sims.common_permissions import IsUTRMCAdmin, IsTechAdmin

from .models import (
    TrainingProgram,
    ProgramRotationTemplate,
    ResidentTrainingRecord,
    RotationAssignment,
    LeaveRequest,
    DeputationPosting,
)
from .serializers import (
    TrainingProgramSerializer,
    ProgramRotationTemplateSerializer,
    ResidentTrainingRecordSerializer,
    RotationAssignmentSerializer,
    LeaveRequestSerializer,
    DeputationPostingSerializer,
)


def _is_admin_or_utrmc_admin(user):
    return getattr(user, "role", None) in {"admin", "utrmc_admin"} or getattr(user, "is_superuser", False)


def _is_supervisor_or_hod(user):
    return getattr(user, "role", None) in {"supervisor", "faculty"}


def _is_resident(user):
    return getattr(user, "role", None) in {"pg", "resident"}


# ---------------------------------------------------------------------------
# Training Program CRUD
# ---------------------------------------------------------------------------

class TrainingProgramViewSet(viewsets.ModelViewSet):
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get("active"):
            qs = qs.filter(active=True)
        return qs

    def check_write_permissions(self, request):
        if not _is_admin_or_utrmc_admin(request.user):
            self.permission_denied(request, message="Only admin or utrmc_admin can modify programs.")

    def create(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().destroy(request, *args, **kwargs)


class ProgramRotationTemplateViewSet(viewsets.ModelViewSet):
    queryset = ProgramRotationTemplate.objects.select_related(
        "program", "department"
    ).prefetch_related("allowed_hospitals")
    serializer_class = ProgramRotationTemplateSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["program", "required", "active"]

    def get_queryset(self):
        qs = super().get_queryset()
        program_id = self.request.query_params.get("program")
        if program_id:
            qs = qs.filter(program_id=program_id)
        return qs

    def check_write_permissions(self, request):
        if not _is_admin_or_utrmc_admin(request.user):
            self.permission_denied(request, message="Only admin or utrmc_admin can modify templates.")

    def create(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().destroy(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# Resident Training Records
# ---------------------------------------------------------------------------

class ResidentTrainingRecordViewSet(viewsets.ModelViewSet):
    serializer_class = ResidentTrainingRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = ResidentTrainingRecord.objects.select_related(
            "resident_user", "program", "created_by"
        )
        if _is_resident(user):
            return qs.filter(resident_user=user)
        if _is_admin_or_utrmc_admin(user):
            return qs.all()
        # supervisors see residents they supervise
        if _is_supervisor_or_hod(user):
            from sims.users.models import SupervisorResidentLink
            supervised_ids = SupervisorResidentLink.objects.filter(
                supervisor_user=user, active=True
            ).values_list("resident_user_id", flat=True)
            return qs.filter(resident_user_id__in=supervised_ids)
        return qs.none()

    def check_write_permissions(self, request):
        if not _is_admin_or_utrmc_admin(request.user):
            self.permission_denied(request, message="Only admin or utrmc_admin can manage training records.")

    def create(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_write_permissions(request)
        return super().destroy(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# Rotation Assignments with full state machine
# ---------------------------------------------------------------------------

class RotationAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = RotationAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = RotationAssignment.objects.select_related(
            "resident_training__resident_user",
            "resident_training__program",
            "hospital_department__hospital",
            "hospital_department__department",
            "template",
            "requested_by",
            "approved_by_hod",
            "approved_by_utrmc",
        )
        # Filter params
        qp = self.request.query_params
        if qp.get("status"):
            qs = qs.filter(status=qp["status"])
        if qp.get("resident"):
            qs = qs.filter(resident_training__resident_user_id=qp["resident"])
        if qp.get("department"):
            qs = qs.filter(hospital_department__department_id=qp["department"])
        if qp.get("hospital"):
            qs = qs.filter(hospital_department__hospital_id=qp["hospital"])
        if qp.get("start_date_from"):
            qs = qs.filter(start_date__gte=qp["start_date_from"])
        if qp.get("start_date_to"):
            qs = qs.filter(start_date__lte=qp["start_date_to"])

        if _is_resident(user):
            return qs.filter(resident_training__resident_user=user)
        if _is_admin_or_utrmc_admin(user):
            return qs.all()
        if _is_supervisor_or_hod(user):
            from sims.users.models import HODAssignment, DepartmentMembership
            hod_dept_ids = HODAssignment.objects.filter(
                hod_user=user, active=True
            ).values_list("department_id", flat=True)
            member_dept_ids = DepartmentMembership.objects.filter(
                user=user, active=True
            ).values_list("department_id", flat=True)
            dept_ids = set(list(hod_dept_ids) + list(member_dept_ids))
            return qs.filter(hospital_department__department_id__in=dept_ids)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save(
            requested_by=self.request.user,
            status=RotationAssignment.STATUS_DRAFT,
        )

    def check_create_permission(self, request):
        if not _is_admin_or_utrmc_admin(request.user):
            self.permission_denied(request, message="Only admin or utrmc_admin can create rotation assignments.")

    def create(self, request, *args, **kwargs):
        self.check_create_permission(request)
        return super().create(request, *args, **kwargs)

    def check_edit_permission(self, request, instance):
        if _is_admin_or_utrmc_admin(request.user):
            return
        self.permission_denied(request, message="Only admin or utrmc_admin can edit rotation assignments.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_edit_permission(request, instance)
        if instance.status not in {RotationAssignment.STATUS_DRAFT, RotationAssignment.STATUS_RETURNED}:
            return Response(
                {"detail": "Can only edit DRAFT or RETURNED assignments."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_edit_permission(request, instance)
        if instance.status not in {RotationAssignment.STATUS_DRAFT, RotationAssignment.STATUS_RETURNED}:
            return Response(
                {"detail": "Can only edit DRAFT or RETURNED assignments."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().partial_update(request, *args, **kwargs)

    # ---- State machine actions ----

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        obj = self.get_object()
        if not (_is_admin_or_utrmc_admin(request.user) or
                obj.resident_training.resident_user == request.user):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != RotationAssignment.STATUS_DRAFT:
            return Response(
                {"detail": f"Cannot submit from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = RotationAssignment.STATUS_SUBMITTED
        obj.submitted_at = timezone.now()
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"], url_path="hod-approve")
    def hod_approve(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != RotationAssignment.STATUS_SUBMITTED:
            return Response(
                {"detail": f"Cannot HOD-approve from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = RotationAssignment.STATUS_APPROVED
        obj.approved_by_hod = request.user
        obj.approved_at = timezone.now()
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"], url_path="utrmc-approve")
    def utrmc_approve(self, request, pk=None):
        obj = self.get_object()
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Only admin/utrmc_admin can UTRMC-approve."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status not in {RotationAssignment.STATUS_SUBMITTED, RotationAssignment.STATUS_APPROVED}:
            return Response(
                {"detail": f"Cannot UTRMC-approve from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = RotationAssignment.STATUS_APPROVED
        obj.approved_by_utrmc = request.user
        if not obj.approved_at:
            obj.approved_at = timezone.now()
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        obj = self.get_object()
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != RotationAssignment.STATUS_APPROVED:
            return Response(
                {"detail": f"Cannot activate from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = RotationAssignment.STATUS_ACTIVE
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        obj = self.get_object()
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != RotationAssignment.STATUS_ACTIVE:
            return Response(
                {"detail": f"Cannot complete from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = RotationAssignment.STATUS_COMPLETED
        obj.completed_at = timezone.now()
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def returned(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status not in {RotationAssignment.STATUS_SUBMITTED, RotationAssignment.STATUS_APPROVED}:
            return Response(
                {"detail": f"Cannot return from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reason = request.data.get("reason", "")
        obj.status = RotationAssignment.STATUS_RETURNED
        obj.return_reason = reason
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status not in {
            RotationAssignment.STATUS_SUBMITTED, RotationAssignment.STATUS_APPROVED
        }:
            return Response(
                {"detail": f"Cannot reject from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reason = request.data.get("reason", "")
        obj.status = RotationAssignment.STATUS_REJECTED
        obj.reject_reason = reason
        obj.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)


# ---------------------------------------------------------------------------
# Leave Requests
# ---------------------------------------------------------------------------

class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = LeaveRequest.objects.select_related(
            "resident_training__resident_user", "approved_by"
        )
        qp = self.request.query_params
        if qp.get("status"):
            qs = qs.filter(status=qp["status"])
        if _is_resident(user):
            return qs.filter(resident_training__resident_user=user)
        if _is_admin_or_utrmc_admin(user):
            return qs.all()
        if _is_supervisor_or_hod(user):
            from sims.users.models import SupervisorResidentLink
            supervised_ids = SupervisorResidentLink.objects.filter(
                supervisor_user=user, active=True
            ).values_list("resident_user_id", flat=True)
            return qs.filter(resident_training__resident_user_id__in=supervised_ids)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        if not (_is_resident(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        obj = self.get_object()
        if not (_is_resident(request.user) and obj.resident_training.resident_user == request.user
                or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != LeaveRequest.STATUS_DRAFT:
            return Response(
                {"detail": f"Cannot submit from {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = LeaveRequest.STATUS_SUBMITTED
        obj.save()
        return Response(LeaveRequestSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != LeaveRequest.STATUS_SUBMITTED:
            return Response(
                {"detail": f"Cannot approve from {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = LeaveRequest.STATUS_APPROVED
        obj.approved_by = request.user
        obj.approved_at = timezone.now()
        obj.save()
        return Response(LeaveRequestSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != LeaveRequest.STATUS_SUBMITTED:
            return Response(
                {"detail": f"Cannot reject from {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reason = request.data.get("reason", "")
        obj.status = LeaveRequest.STATUS_REJECTED
        obj.reject_reason = reason
        obj.save()
        return Response(LeaveRequestSerializer(obj, context={"request": request}).data)


# ---------------------------------------------------------------------------
# Deputation / Off-service Postings
# ---------------------------------------------------------------------------

class DeputationPostingViewSet(viewsets.ModelViewSet):
    serializer_class = DeputationPostingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = DeputationPosting.objects.select_related(
            "resident_training__resident_user", "approved_by"
        )
        qp = self.request.query_params
        if qp.get("status"):
            qs = qs.filter(status=qp["status"])
        if _is_resident(user):
            return qs.filter(resident_training__resident_user=user)
        if _is_admin_or_utrmc_admin(user):
            return qs.all()
        if _is_supervisor_or_hod(user):
            from sims.users.models import SupervisorResidentLink
            supervised_ids = SupervisorResidentLink.objects.filter(
                supervisor_user=user, active=True
            ).values_list("resident_user_id", flat=True)
            return qs.filter(resident_training__resident_user_id__in=supervised_ids)
        return qs.none()

    def create(self, request, *args, **kwargs):
        if not (_is_resident(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != DeputationPosting.STATUS_SUBMITTED:
            return Response(
                {"detail": f"Cannot approve from {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = DeputationPosting.STATUS_APPROVED
        obj.approved_by = request.user
        obj.approved_at = timezone.now()
        obj.save()
        return Response(DeputationPostingSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != DeputationPosting.STATUS_SUBMITTED:
            return Response(
                {"detail": f"Cannot reject from {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reason = request.data.get("reason", "")
        obj.status = DeputationPosting.STATUS_REJECTED
        obj.reject_reason = reason
        obj.save()
        return Response(DeputationPostingSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        obj = self.get_object()
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status != DeputationPosting.STATUS_APPROVED:
            return Response(
                {"detail": f"Cannot complete from {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = DeputationPosting.STATUS_COMPLETED
        obj.save()
        return Response(DeputationPostingSerializer(obj, context={"request": request}).data)


# ---------------------------------------------------------------------------
# Approval Inboxes & Roster Views
# ---------------------------------------------------------------------------

from rest_framework.views import APIView


class RotationApprovalInboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = RotationAssignment.objects.select_related(
            "resident_training__resident_user",
            "resident_training__program",
            "hospital_department__hospital",
            "hospital_department__department",
        )
        if _is_admin_or_utrmc_admin(user):
            qs = qs.filter(
                status__in=[RotationAssignment.STATUS_SUBMITTED, RotationAssignment.STATUS_APPROVED]
            )
        elif _is_supervisor_or_hod(user):
            from sims.users.models import HODAssignment, DepartmentMembership
            hod_dept_ids = HODAssignment.objects.filter(
                hod_user=user, active=True
            ).values_list("department_id", flat=True)
            member_dept_ids = DepartmentMembership.objects.filter(
                user=user, active=True
            ).values_list("department_id", flat=True)
            dept_ids = set(list(hod_dept_ids) + list(member_dept_ids))
            qs = qs.filter(
                status=RotationAssignment.STATUS_SUBMITTED,
                hospital_department__department_id__in=dept_ids,
            )
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = RotationAssignmentSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class LeaveApprovalInboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = LeaveRequest.objects.select_related(
            "resident_training__resident_user"
        ).filter(status=LeaveRequest.STATUS_SUBMITTED)
        if _is_admin_or_utrmc_admin(user):
            pass  # see all
        elif _is_supervisor_or_hod(user):
            from sims.users.models import SupervisorResidentLink
            supervised_ids = SupervisorResidentLink.objects.filter(
                supervisor_user=user, active=True
            ).values_list("resident_user_id", flat=True)
            qs = qs.filter(resident_training__resident_user_id__in=supervised_ids)
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LeaveRequestSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class MyRotationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        qs = RotationAssignment.objects.filter(
            resident_training__resident_user=request.user
        ).select_related(
            "hospital_department__hospital",
            "hospital_department__department",
            "template",
        ).order_by("-start_date")
        serializer = RotationAssignmentSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class MyLeavesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        qs = LeaveRequest.objects.filter(
            resident_training__resident_user=request.user
        ).order_by("-start_date")
        serializer = LeaveRequestSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class SupervisorPendingRotationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (_is_supervisor_or_hod(user) or _is_admin_or_utrmc_admin(user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if _is_admin_or_utrmc_admin(user):
            qs = RotationAssignment.objects.filter(
                status=RotationAssignment.STATUS_SUBMITTED
            )
        else:
            from sims.users.models import HODAssignment, DepartmentMembership
            hod_dept_ids = HODAssignment.objects.filter(
                hod_user=user, active=True
            ).values_list("department_id", flat=True)
            member_dept_ids = DepartmentMembership.objects.filter(
                user=user, active=True
            ).values_list("department_id", flat=True)
            dept_ids = set(list(hod_dept_ids) + list(member_dept_ids))
            qs = RotationAssignment.objects.filter(
                status=RotationAssignment.STATUS_SUBMITTED,
                hospital_department__department_id__in=dept_ids,
            )
        qs = qs.select_related(
            "resident_training__resident_user",
            "hospital_department__hospital",
            "hospital_department__department",
        )
        serializer = RotationAssignmentSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


# =============================================================================
# Phase 6 Views — Program Policy, Milestones, Research, Thesis,
#                 Workshops, Eligibility
# =============================================================================

from .models import (
    ProgramPolicy,
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramMilestoneLogbookRequirement,
    ResidentResearchProject,
    ResidentThesis,
    Workshop,
    WorkshopBlock,
    WorkshopRun,
    ResidentWorkshopCompletion,
    ResidentMilestoneEligibility,
)
from .serializers import (
    ProgramPolicySerializer,
    ProgramMilestoneSerializer,
    ProgramMilestoneResearchRequirementSerializer,
    ProgramMilestoneWorkshopRequirementSerializer,
    ProgramMilestoneLogbookRequirementSerializer,
    ResidentResearchProjectSerializer,
    ResidentThesisSerializer,
    WorkshopSerializer,
    WorkshopBlockSerializer,
    WorkshopRunSerializer,
    ResidentWorkshopCompletionSerializer,
    ResidentMilestoneEligibilitySerializer,
)


# ------------------------------------------------------------------
# Program Policy
# ------------------------------------------------------------------

class ProgramPolicyView(APIView):
    """GET + PUT/PATCH the policy for a specific program. Admin/UTRMC-admin only."""
    permission_classes = [IsAuthenticated]

    def _get_program(self, program_id):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(TrainingProgram, pk=program_id)

    def get(self, request, program_id):
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=403)
        program = self._get_program(program_id)
        policy, _ = ProgramPolicy.objects.get_or_create(program=program)
        return Response(ProgramPolicySerializer(policy).data)

    def put(self, request, program_id):
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=403)
        program = self._get_program(program_id)
        policy, _ = ProgramPolicy.objects.get_or_create(program=program)
        serializer = ProgramPolicySerializer(policy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ------------------------------------------------------------------
# Program Milestones
# ------------------------------------------------------------------

class ProgramMilestoneViewSet(viewsets.ModelViewSet):
    """CRUD for milestones of a given program. Admin/UTRMC-admin only."""
    serializer_class = ProgramMilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProgramMilestone.objects.filter(
            program_id=self.kwargs["program_id"]
        ).prefetch_related(
            "research_requirement",
            "workshop_requirements__workshop",
            "logbook_requirements",
        )

    def perform_create(self, serializer):
        if not _is_admin_or_utrmc_admin(self.request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        program = TrainingProgram.objects.get(pk=self.kwargs["program_id"])
        serializer.save(program=program)

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def check_write_permission(self, request):
        if not _is_admin_or_utrmc_admin(request.user):
            self.permission_denied(request, message="Admin or UTRMC admin required.")

    def update(self, request, *args, **kwargs):
        self.check_write_permission(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.check_write_permission(request)
        return super().destroy(request, *args, **kwargs)


class MilestoneResearchRequirementView(APIView):
    """GET + PUT research requirements for a milestone."""
    permission_classes = [IsAuthenticated]

    def _get_milestone(self, milestone_id):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(ProgramMilestone, pk=milestone_id)

    def get(self, request, milestone_id):
        m = self._get_milestone(milestone_id)
        req, _ = ProgramMilestoneResearchRequirement.objects.get_or_create(milestone=m)
        return Response(ProgramMilestoneResearchRequirementSerializer(req).data)

    def put(self, request, milestone_id):
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=403)
        m = self._get_milestone(milestone_id)
        req, _ = ProgramMilestoneResearchRequirement.objects.get_or_create(milestone=m)
        serializer = ProgramMilestoneResearchRequirementSerializer(req, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ------------------------------------------------------------------
# Research Project
# ------------------------------------------------------------------

def _get_active_rtr(user):
    """Return the user's active ResidentTrainingRecord or raise 404."""
    from django.shortcuts import get_object_or_404
    return get_object_or_404(ResidentTrainingRecord, resident_user=user, active=True)


class ResidentResearchProjectView(APIView):
    """
    GET / POST / PATCH own research project.
    Residents manage their own project; supervisors can view their assigned residents'.
    """
    permission_classes = [IsAuthenticated]

    def _get_project_or_none(self, rtr):
        try:
            return rtr.research_project
        except ResidentResearchProject.DoesNotExist:
            return None

    def get(self, request, rtr_id=None):
        if rtr_id:
            rtr = ResidentTrainingRecord.objects.get(pk=rtr_id)
        else:
            rtr = _get_active_rtr(request.user)
        project = self._get_project_or_none(rtr)
        if project is None:
            return Response({"detail": "No research project found."}, status=404)
        return Response(ResidentResearchProjectSerializer(project, context={"request": request}).data)

    def post(self, request):
        rtr = _get_active_rtr(request.user)
        if hasattr(rtr, "research_project"):
            return Response({"detail": "Research project already exists. Use PATCH to update."}, status=400)
        serializer = ResidentResearchProjectSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(resident_training_record=rtr)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        rtr = _get_active_rtr(request.user)
        project = self._get_project_or_none(rtr)
        if project is None:
            return Response({"detail": "No research project found."}, status=404)
        if project.status not in (
            ResidentResearchProject.STATUS_DRAFT,
        ):
            return Response({"detail": "Research project can only be edited in Draft status."}, status=400)
        serializer = ResidentResearchProjectSerializer(
            project, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResearchProjectActionView(APIView):
    """State machine transition endpoints for research project."""
    permission_classes = [IsAuthenticated]

    VALID_ACTIONS = {
        "submit-to-supervisor": ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
        "supervisor-approve": ResidentResearchProject.STATUS_APPROVED_SUPERVISOR,
        "submit-to-university": ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
        "accept-by-university": ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
        "return-to-draft": ResidentResearchProject.STATUS_DRAFT,
    }

    def post(self, request, action):
        new_status = self.VALID_ACTIONS.get(action)
        if new_status is None:
            return Response({"detail": f"Unknown action '{action}'."}, status=400)

        user = request.user

        if action == "submit-to-supervisor":
            rtr = _get_active_rtr(user)
            project = rtr.research_project
        elif action in ("supervisor-approve", "return-to-draft"):
            # Supervisor approves/returns
            if not _is_supervisor_or_hod(user) and not _is_admin_or_utrmc_admin(user):
                return Response({"detail": "Supervisor/admin role required."}, status=403)
            project_id = request.data.get("project_id")
            if not project_id:
                return Response({"detail": "project_id required."}, status=400)
            project = ResidentResearchProject.objects.get(pk=project_id)
            if action == "supervisor-approve":
                feedback = request.data.get("feedback", "")
                project.supervisor_feedback = feedback
                project.supervisor = user
                project.save()
        elif action in ("submit-to-university", "accept-by-university"):
            # Resident submits; UTRMC accepts
            if action == "submit-to-university":
                rtr = _get_active_rtr(user)
                project = rtr.research_project
            else:
                if not _is_admin_or_utrmc_admin(user):
                    return Response({"detail": "UTRMC admin required."}, status=403)
                project_id = request.data.get("project_id")
                project = ResidentResearchProject.objects.get(pk=project_id)
                ref = request.data.get("university_submission_ref", "")
                if ref:
                    project.university_submission_ref = ref
                    project.save()
        else:
            return Response({"detail": "Unknown action."}, status=400)

        try:
            project.transition_to(new_status, actor=user)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=400)

        return Response(
            ResidentResearchProjectSerializer(project, context={"request": request}).data
        )


# ------------------------------------------------------------------
# Thesis
# ------------------------------------------------------------------

class ResidentThesisView(APIView):
    """GET / POST / PATCH own thesis record."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rtr = _get_active_rtr(request.user)
        try:
            thesis = rtr.thesis
        except ResidentThesis.DoesNotExist:
            return Response({"detail": "No thesis record found."}, status=404)
        return Response(ResidentThesisSerializer(thesis, context={"request": request}).data)

    def post(self, request):
        rtr = _get_active_rtr(request.user)
        if hasattr(rtr, "thesis"):
            return Response({"detail": "Thesis already exists. Use PATCH to update."}, status=400)
        serializer = ResidentThesisSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(
            resident_training_record=rtr,
            status=ResidentThesis.STATUS_IN_PROGRESS,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        rtr = _get_active_rtr(request.user)
        try:
            thesis = rtr.thesis
        except ResidentThesis.DoesNotExist:
            return Response({"detail": "No thesis record found."}, status=404)
        serializer = ResidentThesisSerializer(
            thesis, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ThesisSubmitView(APIView):
    """POST to submit thesis (transitions status to SUBMITTED)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.utils import timezone
        rtr = _get_active_rtr(request.user)
        try:
            thesis = rtr.thesis
        except ResidentThesis.DoesNotExist:
            return Response({"detail": "No thesis record found."}, status=404)
        if thesis.status == ResidentThesis.STATUS_SUBMITTED:
            return Response({"detail": "Thesis already submitted."}, status=400)
        if not thesis.thesis_file:
            return Response({"detail": "Upload thesis file before submitting."}, status=400)
        thesis.status = ResidentThesis.STATUS_SUBMITTED
        thesis.submitted_at = timezone.now()
        ref = request.data.get("final_submission_ref")
        if ref:
            thesis.final_submission_ref = ref
        thesis.save()
        return Response(ResidentThesisSerializer(thesis, context={"request": request}).data)


# ------------------------------------------------------------------
# Workshop Completions (always available — manual upload)
# ------------------------------------------------------------------

class MyWorkshopCompletionsView(APIView):
    """Resident's own workshop completion records."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rtr = _get_active_rtr(request.user)
        qs = rtr.workshop_completions.select_related("workshop").order_by("-completed_at")
        serializer = ResidentWorkshopCompletionSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})

    def post(self, request):
        rtr = _get_active_rtr(request.user)
        serializer = ResidentWorkshopCompletionSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(resident_training_record=rtr)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyWorkshopCompletionDetailView(APIView):
    """GET / DELETE a single workshop completion record."""
    permission_classes = [IsAuthenticated]

    def _get_completion(self, request, pk):
        from django.shortcuts import get_object_or_404
        rtr = _get_active_rtr(request.user)
        return get_object_or_404(ResidentWorkshopCompletion, pk=pk, resident_training_record=rtr)

    def get(self, request, pk):
        obj = self._get_completion(request, pk)
        return Response(ResidentWorkshopCompletionSerializer(obj, context={"request": request}).data)

    def delete(self, request, pk):
        obj = self._get_completion(request, pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------------------------------------------------------------
# Workshops (management) — only exposed if WORKSHOP_MANAGEMENT_ENABLED
# ------------------------------------------------------------------

class WorkshopViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only list of workshops (always visible)."""
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]
    queryset = Workshop.objects.filter(is_active=True).order_by("name")


# ------------------------------------------------------------------
# Eligibility
# ------------------------------------------------------------------

class MyEligibilityView(APIView):
    """Resident's own eligibility snapshot (IMM + FINAL)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rtr = _get_active_rtr(request.user)
        # Trigger recompute on-demand for freshness
        try:
            from sims.training.eligibility import recompute_for_record
            recompute_for_record(rtr)
        except Exception:
            pass

        qs = ResidentMilestoneEligibility.objects.filter(
            resident_training_record=rtr
        ).select_related("milestone")
        serializer = ResidentMilestoneEligibilitySerializer(qs, many=True, context={"request": request})
        return Response({
            "resident_training_record": rtr.id,
            "program": {"id": rtr.program_id, "code": rtr.program.code, "name": rtr.program.name},
            "current_month_index": rtr.current_month_index(),
            "eligibilities": serializer.data,
        })


class UTRMCEligibilityView(APIView):
    """UTRMC/admin view: list eligibility with optional filters."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Permission denied."}, status=403)

        qs = ResidentMilestoneEligibility.objects.select_related(
            "resident_training_record__resident_user",
            "resident_training_record__program",
            "milestone",
        )

        # Optional filters
        program_id = request.query_params.get("program")
        milestone_code = request.query_params.get("milestone_code")
        eli_status = request.query_params.get("status")

        if program_id:
            qs = qs.filter(resident_training_record__program_id=program_id)
        if milestone_code:
            qs = qs.filter(milestone__code=milestone_code)
        if eli_status:
            qs = qs.filter(status=eli_status)

        serializer = ResidentMilestoneEligibilitySerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class SupervisorResearchApprovalsView(APIView):
    """Supervisor inbox: pending research projects awaiting approval."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=403)

        # Find all pending research projects for residents supervised by this user
        if _is_admin_or_utrmc_admin(request.user):
            qs = ResidentResearchProject.objects.filter(
                status=ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR
            )
        else:
            qs = ResidentResearchProject.objects.filter(
                status=ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
                resident_training_record__resident_user__supervisor=request.user,
            )

        qs = qs.select_related(
            "resident_training_record__resident_user",
            "resident_training_record__program",
            "supervisor",
        )
        serializer = ResidentResearchProjectSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class SystemSettingsView(APIView):
    """Read-only system settings for the frontend (toggles, labels, etc.)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.conf import settings
        return Response({
            "WORKSHOP_MANAGEMENT_ENABLED": getattr(settings, "WORKSHOP_MANAGEMENT_ENABLED", False),
            "ANALYTICS_ENABLED": getattr(settings, "ANALYTICS_ENABLED", True),
        })


# =============================================================================
# Phase 6B/6C — Resident & Supervisor Summary Endpoints
# =============================================================================

class ResidentSummaryView(APIView):
    """Single-call summary for the resident command-center dashboard."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        user = request.user
        if not _is_resident(user) and not _is_admin_or_utrmc_admin(user):
            return Response({"detail": "Resident access required."}, status=403)

        rtr = _get_active_rtr(user)
        today = timezone.now().date()

        # --- Training record ---
        training_data = {
            "program_code": rtr.program.code,
            "program_name": rtr.program.name,
            "degree_type": rtr.program.degree_type,
            "start_date": rtr.start_date.isoformat(),
            "current_month_index": rtr.current_month_index(),
        }

        # --- Rotations (current + next) ---
        rotations_qs = RotationAssignment.objects.filter(
            resident_training=rtr,
            status__in={
                RotationAssignment.STATUS_ACTIVE,
                RotationAssignment.STATUS_APPROVED,
                RotationAssignment.STATUS_SUBMITTED,
                RotationAssignment.STATUS_DRAFT,
                RotationAssignment.STATUS_COMPLETED,
            },
        ).select_related(
            "hospital_department__hospital",
            "hospital_department__department",
        ).order_by("start_date")

        current_rotation = None
        next_rotation = None
        for r in rotations_qs:
            active = r.status in {RotationAssignment.STATUS_ACTIVE, RotationAssignment.STATUS_APPROVED}
            if active and r.start_date <= today and r.end_date >= today:
                current_rotation = {
                    "id": r.id,
                    "department": r.hospital_department.department.name,
                    "hospital": r.hospital_department.hospital.name,
                    "start_date": r.start_date.isoformat(),
                    "end_date": r.end_date.isoformat(),
                    "status": r.status,
                }
            elif active and r.start_date > today and next_rotation is None:
                next_rotation = {
                    "id": r.id,
                    "department": r.hospital_department.department.name,
                    "hospital": r.hospital_department.hospital.name,
                    "start_date": r.start_date.isoformat(),
                    "end_date": r.end_date.isoformat(),
                    "status": r.status,
                }

        # All rotations for schedule (chronological)
        all_rotations = []
        for r in rotations_qs:
            all_rotations.append({
                "id": r.id,
                "department": r.hospital_department.department.name,
                "hospital": r.hospital_department.hospital.name,
                "start_date": r.start_date.isoformat(),
                "end_date": r.end_date.isoformat(),
                "status": r.status,
            })

        # --- Leaves ---
        leaves_qs = LeaveRequest.objects.filter(resident_training=rtr)
        leaves_active = leaves_qs.filter(status=LeaveRequest.STATUS_APPROVED).count()
        leaves_pending = leaves_qs.filter(status=LeaveRequest.STATUS_SUBMITTED).count()
        leaves_list = list(
            leaves_qs.values("id", "leave_type", "start_date", "end_date", "status")
            .order_by("-start_date")
        )
        for item in leaves_list:
            if item["start_date"]:
                item["start_date"] = item["start_date"].isoformat()
            if item["end_date"]:
                item["end_date"] = item["end_date"].isoformat()

        # --- Postings ---
        postings_qs = DeputationPosting.objects.filter(resident_training=rtr)
        postings_active = postings_qs.filter(status=DeputationPosting.STATUS_APPROVED).count()
        postings_pending = postings_qs.filter(status=DeputationPosting.STATUS_SUBMITTED).count()

        # --- Research ---
        try:
            research = rtr.research_project
            research_data = {
                "status": research.status,
                "supervisor_name": (
                    research.supervisor.get_full_name() or research.supervisor.username
                ) if research.supervisor else None,
                "synopsis_uploaded": bool(research.synopsis_file),
                "university_submitted": research.status in (
                    ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
                    ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
                ),
            }
        except ResidentResearchProject.DoesNotExist:
            research_data = {
                "status": None,
                "supervisor_name": None,
                "synopsis_uploaded": False,
                "university_submitted": False,
            }

        # --- Thesis ---
        try:
            thesis = rtr.thesis
            thesis_data = {
                "status": thesis.status,
                "submitted_at": thesis.submitted_at.isoformat() if thesis.submitted_at else None,
            }
        except ResidentThesis.DoesNotExist:
            thesis_data = {"status": ResidentThesis.STATUS_NOT_STARTED, "submitted_at": None}

        # --- Workshops ---
        completions_qs = ResidentWorkshopCompletion.objects.filter(
            resident_training_record=rtr
        ).select_related("workshop").order_by("completed_at")
        completions = list(completions_qs)

        milestones = ProgramMilestone.objects.filter(
            program=rtr.program, is_active=True
        ).prefetch_related("workshop_requirements")
        imm_ws_req = 0
        final_ws_req = 0
        for ms in milestones:
            total = sum(wr.required_count for wr in ms.workshop_requirements.all())
            if ms.code == "IMM":
                imm_ws_req = total
            elif ms.code == "FINAL":
                final_ws_req = total

        workshops_data = {
            "total_completed": len(completions),
            "required_for_imm": imm_ws_req,
            "required_for_final": final_ws_req,
            "completed_list": [
                {
                    "id": c.id,
                    "workshop_name": c.workshop.name,
                    "completed_at": c.completed_at.isoformat() if c.completed_at else None,
                }
                for c in completions
            ],
        }

        # --- Eligibility (recompute + snapshot) ---
        try:
            from sims.training.eligibility import recompute_for_record
            recompute_for_record(rtr)
        except Exception:
            pass

        eligibility_qs = ResidentMilestoneEligibility.objects.filter(
            resident_training_record=rtr
        ).select_related("milestone")

        imm_eli = {"status": None, "reasons": []}
        final_eli = {"status": None, "reasons": []}
        for eli in eligibility_qs:
            reasons = sorted(eli.reasons_json) if isinstance(eli.reasons_json, list) else []
            entry = {"status": eli.status, "reasons": reasons}
            if eli.milestone.code == "IMM":
                imm_eli = entry
            elif eli.milestone.code == "FINAL":
                final_eli = entry

        return Response({
            "training_record": training_data,
            "rotation": {"current": current_rotation, "next": next_rotation},
            "schedule": all_rotations,
            "leaves": {
                "active_count": leaves_active,
                "pending_count": leaves_pending,
                "list": leaves_list,
            },
            "postings": {"active_count": postings_active, "pending_count": postings_pending},
            "research": research_data,
            "thesis": thesis_data,
            "workshops": workshops_data,
            "eligibility": {"IMM": imm_eli, "FINAL": final_eli},
        })


class SupervisorSummaryView(APIView):
    """Single-call summary for the supervisor dashboard."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        user = request.user
        if not _is_supervisor_or_hod(user) and not _is_admin_or_utrmc_admin(user):
            return Response({"detail": "Supervisor access required."}, status=403)

        # ---- Determine scoped resident users ----
        from sims.users.models import SupervisorResidentLink, User as SIMSUser

        if _is_admin_or_utrmc_admin(user):
            resident_users = list(
                SIMSUser.objects.filter(role__in=["pg", "resident"], is_active=True)
            )
        else:
            links = SupervisorResidentLink.objects.filter(
                supervisor_user=user, active=True
            ).select_related("resident_user")
            resident_users = [ln.resident_user for ln in links]

        resident_ids = [u.id for u in resident_users]

        # ---- Active training records ----
        rtrs = list(
            ResidentTrainingRecord.objects.filter(
                resident_user_id__in=resident_ids, active=True
            ).select_related("resident_user", "program")
        )
        rtr_ids = [r.id for r in rtrs]
        rtr_by_id = {r.id: r for r in rtrs}

        # ---- Pending approval counts ----
        pending_rotations = RotationAssignment.objects.filter(
            resident_training_id__in=rtr_ids,
            status=RotationAssignment.STATUS_SUBMITTED,
        ).count()

        pending_leaves = LeaveRequest.objects.filter(
            resident_training_id__in=rtr_ids,
            status=LeaveRequest.STATUS_SUBMITTED,
        ).count()

        if _is_admin_or_utrmc_admin(user):
            pending_research = ResidentResearchProject.objects.filter(
                status=ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
            ).count()
        else:
            pending_research = ResidentResearchProject.objects.filter(
                status=ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
                resident_training_record_id__in=rtr_ids,
            ).count()

        # ---- Current rotations ----
        today = timezone.now().date()
        active_statuses = {RotationAssignment.STATUS_ACTIVE, RotationAssignment.STATUS_APPROVED}
        cur_rotations = RotationAssignment.objects.filter(
            resident_training_id__in=rtr_ids,
            status__in=active_statuses,
            start_date__lte=today,
            end_date__gte=today,
        ).select_related("hospital_department__department", "hospital_department__hospital")
        rotation_map = {
            r.resident_training_id: (
                f"{r.hospital_department.department.name}"
                f" @ {r.hospital_department.hospital.name}"
            )
            for r in cur_rotations
        }

        # ---- Eligibility ----
        eligibilities = ResidentMilestoneEligibility.objects.filter(
            resident_training_record_id__in=rtr_ids
        ).select_related("milestone")
        eli_map = {}
        for eli in eligibilities:
            eli_map.setdefault(eli.resident_training_record_id, {})[eli.milestone.code] = eli.status

        # ---- Research status ----
        research_qs = ResidentResearchProject.objects.filter(
            resident_training_record_id__in=rtr_ids
        )
        research_map = {rp.resident_training_record_id: rp.status for rp in research_qs}

        # ---- Build residents list (sorted by display name) ----
        rtrs_sorted = sorted(
            rtrs,
            key=lambda r: (r.resident_user.get_full_name() or r.resident_user.username).lower(),
        )
        residents_list = []
        for rtr in rtrs_sorted:
            rtr_eli = eli_map.get(rtr.id, {})
            residents_list.append({
                "id": rtr.resident_user_id,
                "rtr_id": rtr.id,
                "name": rtr.resident_user.get_full_name() or rtr.resident_user.username,
                "program": rtr.program.name,
                "current_rotation": rotation_map.get(rtr.id),
                "imm_status": rtr_eli.get("IMM"),
                "final_status": rtr_eli.get("FINAL"),
                "research_status": research_map.get(rtr.id),
            })

        return Response({
            "pending": {
                "rotation_approvals": pending_rotations,
                "leave_approvals": pending_leaves,
                "research_approvals": pending_research,
            },
            "residents": residents_list,
        })


class SupervisorResidentProgressView(APIView):
    """Read-only progress snapshot for a specific resident (supervisor/admin view)."""
    permission_classes = [IsAuthenticated]

    def get(self, request, resident_id):
        user = request.user
        if not _is_supervisor_or_hod(user) and not _is_admin_or_utrmc_admin(user):
            return Response({"detail": "Permission denied."}, status=403)

        from django.shortcuts import get_object_or_404
        from sims.users.models import User as SIMSUser
        resident = get_object_or_404(SIMSUser, pk=resident_id)
        rtr = get_object_or_404(ResidentTrainingRecord, resident_user=resident, active=True)

        from django.utils import timezone
        today = timezone.now().date()

        # Training record
        training_data = {
            "program_code": rtr.program.code,
            "program_name": rtr.program.name,
            "degree_type": rtr.program.degree_type,
            "start_date": rtr.start_date.isoformat(),
            "current_month_index": rtr.current_month_index(),
        }

        # Current rotation
        current_rotation = None
        cur = RotationAssignment.objects.filter(
            resident_training=rtr,
            status__in={RotationAssignment.STATUS_ACTIVE, RotationAssignment.STATUS_APPROVED},
            start_date__lte=today,
            end_date__gte=today,
        ).select_related("hospital_department__department", "hospital_department__hospital").first()
        if cur:
            current_rotation = {
                "department": cur.hospital_department.department.name,
                "hospital": cur.hospital_department.hospital.name,
                "start_date": cur.start_date.isoformat(),
                "end_date": cur.end_date.isoformat(),
                "status": cur.status,
            }

        # Research
        try:
            research = rtr.research_project
            research_data = {"status": research.status, "title": research.title}
        except ResidentResearchProject.DoesNotExist:
            research_data = {"status": None, "title": None}

        # Thesis
        try:
            thesis = rtr.thesis
            thesis_data = {"status": thesis.status}
        except ResidentThesis.DoesNotExist:
            thesis_data = {"status": ResidentThesis.STATUS_NOT_STARTED}

        # Workshops
        ws_count = ResidentWorkshopCompletion.objects.filter(resident_training_record=rtr).count()

        # Eligibility
        try:
            from sims.training.eligibility import recompute_for_record
            recompute_for_record(rtr)
        except Exception:
            pass
        eligibilities = ResidentMilestoneEligibility.objects.filter(
            resident_training_record=rtr
        ).select_related("milestone")
        imm_eli = {"status": None, "reasons": []}
        final_eli = {"status": None, "reasons": []}
        for eli in eligibilities:
            reasons = sorted(eli.reasons_json) if isinstance(eli.reasons_json, list) else []
            entry = {"status": eli.status, "reasons": reasons}
            if eli.milestone.code == "IMM":
                imm_eli = entry
            elif eli.milestone.code == "FINAL":
                final_eli = entry

        return Response({
            "resident": {
                "id": resident.id,
                "name": resident.get_full_name() or resident.username,
                "username": resident.username,
            },
            "training_record": training_data,
            "current_rotation": current_rotation,
            "research": research_data,
            "thesis": thesis_data,
            "workshops": {"total_completed": ws_count},
            "eligibility": {"IMM": imm_eli, "FINAL": final_eli},
        })
