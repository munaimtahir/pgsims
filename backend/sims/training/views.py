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
