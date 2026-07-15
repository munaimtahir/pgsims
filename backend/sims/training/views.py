"""
Training & Rotations API views.

RBAC summary:
  TrainingProgram / ProgramRotationTemplate  → admin | utrmc_admin (write); authenticated (read)
  ResidentTrainingRecord                     → admin | utrmc_admin (write); resident sees own
  RotationAssignment                         → DRAFT/SUBMITTED by utrmc_admin|admin; state machine actions role-gated
  LeaveRequest / DeputationPosting           → resident creates; approvers approve
"""
from datetime import timedelta

from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as DRFValidationError

from sims.rotations.services import evaluate_rotation_override_policy

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
    return getattr(user, "role", None) in {"ADMIN", "ADMIN"} or getattr(user, "is_superuser", False)


def _is_utrmc_viewer(user):
    return getattr(user, "role", None) in {"ADMIN", "ADMIN", "SUPPORT_STAFF"} or getattr(user, "is_superuser", False)


def _is_supervisor_or_hod(user):
    return getattr(user, "role", None) in {"SUPERVISOR", "SUPERVISOR"}


def _is_resident(user):
    return getattr(user, "role", None) in {"RESIDENT", "RESIDENT"}


class TrainingEmptySchemaSerializer(serializers.Serializer):
    pass


def _get_supervised_resident_ids(user):
    from sims.supervision.models import ResidentSupervisorAssignment
    from sims.users.models import User as SIMSUser

    resident_ids = set()

    # 1. New spine assignments (via ResidentSupervisorAssignment)
    try:
        profile = user.supervisor_profile
        if profile:
            new_ids = ResidentSupervisorAssignment.objects.filter(
                supervisor=profile,
                is_active=True
            ).values_list("resident__user_id", flat=True)
            resident_ids.update(new_ids)
    except Exception:
        pass

    # 2. Legacy direct User.supervisor FK is retained only as a narrow compatibility fallback.
    direct_ids = SIMSUser.objects.filter(
        supervisor=user,
        role="RESIDENT"
    ).values_list("id", flat=True)
    resident_ids.update(direct_ids)

    return resident_ids


def _get_rotation_scope(user):
    from sims.users.models import DepartmentMembership, SupervisorProfile

    supervised_ids = _get_supervised_resident_ids(user)
    hod_dept_ids = []
    try:
        profile = user.supervisor_profile
        if profile.designation_ref == "HOD" and profile.department_ref_id:
            hod_dept_ids = [profile.department_ref_id]
    except SupervisorProfile.DoesNotExist:
        pass
    member_dept_ids = DepartmentMembership.objects.filter(
        user=user, active=True
    ).values_list("department_id", flat=True)
    dept_ids = set(hod_dept_ids).union(set(member_dept_ids))
    return supervised_ids, dept_ids


def _serialize_supervisor_profile(profile):
    if not profile:
        return None
    return {
        "id": profile.id,
        "name": profile.user.get_full_name() or profile.user.username,
        "username": profile.user.username,
        "email": profile.email or profile.official_email or profile.user.email or "",
        "phone": profile.phone or "",
        "designation": profile.designation_ref.name if profile.designation_ref else "",
        "department": profile.department_ref.name if profile.department_ref else "",
        "training_site": profile.hospital.name if profile.hospital else "",
    }


def _serialize_resident_profile(profile):
    if not profile:
        return None
    return {
        "id": profile.id,
        "name": profile.user.get_full_name() or profile.user.username,
        "username": profile.user.username,
        "email": profile.email or profile.user.email or "",
        "phone": profile.phone or "",
        "department": profile.department_ref.name if profile.department_ref else "",
        "training_site": profile.hospital.name if profile.hospital else "",
    }


def _serialize_assignment(assignment):
    if not assignment:
        return None
    return {
        "id": assignment.id,
        "assignment_type": assignment.assignment_type,
        "status": assignment.status,
        "start_date": assignment.start_date.isoformat() if assignment.start_date else None,
        "end_date": assignment.end_date.isoformat() if assignment.end_date else None,
        "notes": assignment.notes,
        "reason_for_change": assignment.reason_for_change,
        "supervisor": _serialize_supervisor_profile(assignment.supervisor),
        "resident": _serialize_resident_profile(assignment.resident),
    }


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
            supervised_ids = _get_supervised_resident_ids(user)
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
            supervised_ids, dept_ids = _get_rotation_scope(user)
            return qs.filter(
                Q(resident_training__resident_user_id__in=supervised_ids)
                | Q(hospital_department__department_id__in=dept_ids)
            ).distinct()
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
        if obj.status not in {
            RotationAssignment.STATUS_DRAFT,
            RotationAssignment.STATUS_RETURNED,
        }:
            return Response(
                {"detail": f"Cannot submit from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.status = RotationAssignment.STATUS_SUBMITTED
        obj.submitted_at = timezone.now()
        obj.return_reason = ""
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
        policy = evaluate_rotation_override_policy(
            obj.resident_training.resident_user,
            obj.hospital_department.hospital,
            obj.hospital_department.department,
        )
        if policy.requires_utrmc_approval and not obj.approved_by_utrmc_id:
            return Response(
                {"detail": "UTRMC approval is required before activating this rotation."},
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
        completion, _ = RotationCompletion.objects.get_or_create(rotation=obj)
        completion.status = RotationCompletion.STATUS_PENDING_UTRMC_VERIFICATION
        completion.confirmed_by = request.user
        completion.confirmed_at = completion.confirmed_at or timezone.now()
        completion.verification_submitted_at = timezone.now()
        completion.save()
        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"], url_path="review-application")
    def review_application(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status not in {RotationAssignment.STATUS_SUBMITTED, RotationAssignment.STATUS_APPROVED}:
            return Response(
                {"detail": f"Cannot review application from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        decision = request.data.get("action")
        reason = (request.data.get("reason") or "").strip()
        if decision not in {"approve", "redirect", "defer", "reject"}:
            return Response(
                {"detail": "action must be one of: approve, redirect, defer, reject."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if decision == "approve":
            obj.status = RotationAssignment.STATUS_APPROVED
            obj.approved_by_hod = request.user
            obj.approved_at = timezone.now()
            if reason:
                obj.notes = f"{obj.notes}\nApproval note: {reason}".strip()
            obj.save()
        elif decision == "redirect":
            target_hospital_department = request.data.get("hospital_department")
            if not target_hospital_department:
                return Response(
                    {"detail": "hospital_department is required when action=redirect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            obj.hospital_department_id = int(target_hospital_department)
            obj.status = RotationAssignment.STATUS_APPROVED
            obj.approved_by_hod = request.user
            obj.approved_at = timezone.now()
            redirect_note = "Redirected by supervisor/HOD."
            if reason:
                redirect_note = f"{redirect_note} {reason}"
            obj.notes = f"{obj.notes}\n{redirect_note}".strip()
            obj.save()
        elif decision == "defer":
            obj.status = RotationAssignment.STATUS_RETURNED
            obj.return_reason = reason or "Deferred by supervisor/HOD."
            obj.save()
        else:  # reject
            obj.status = RotationAssignment.STATUS_REJECTED
            obj.reject_reason = reason or "Rejected by supervisor/HOD."
            obj.save()

        return Response(RotationAssignmentSerializer(obj, context={"request": request}).data)

    @action(detail=True, methods=["post"], url_path="confirm-completion")
    def confirm_completion(self, request, pk=None):
        obj = self.get_object()
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if obj.status not in {
            RotationAssignment.STATUS_ACTIVE,
            RotationAssignment.STATUS_APPROVED,
            RotationAssignment.STATUS_COMPLETED,
        }:
            return Response(
                {"detail": f"Cannot confirm completion from status {obj.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        now = timezone.now()
        if obj.status != RotationAssignment.STATUS_COMPLETED:
            obj.status = RotationAssignment.STATUS_COMPLETED
            obj.completed_at = now
            obj.save(update_fields=["status", "completed_at", "updated_at"])

        completion, _ = RotationCompletion.objects.get_or_create(rotation=obj)
        completion.status = RotationCompletion.STATUS_PENDING_UTRMC_VERIFICATION
        completion.confirmed_by = request.user
        completion.confirmed_at = now
        completion.verification_submitted_at = now
        completion.notes = (request.data.get("notes") or completion.notes or "").strip()
        completion.save()

        certificate, created = RotationCertificate.objects.get_or_create(
            completion=completion,
            defaults={
                "certificate_number": f"ROT-{obj.id}-{now.strftime('%Y%m%d%H%M%S')}",
                "issued_by": request.user,
            },
        )
        if not created and not certificate.issued_by_id:
            certificate.issued_by = request.user
            certificate.save(update_fields=["issued_by"])

        return Response(
            {
                "rotation": RotationAssignmentSerializer(obj, context={"request": request}).data,
                "completion": RotationCompletionSerializer(completion, context={"request": request}).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="verify-completion")
    def verify_completion(self, request, pk=None):
        obj = self.get_object()
        if not _is_admin_or_utrmc_admin(request.user):
            return Response(
                {"detail": "Only admin/utrmc_admin can verify rotation completion."},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            completion = obj.completion
        except RotationCompletion.DoesNotExist:
            return Response({"detail": "Rotation completion record not found."}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        completion.status = RotationCompletion.STATUS_VERIFIED
        completion.verified_by = request.user
        completion.verified_at = now
        completion.save()

        certificate, _ = RotationCertificate.objects.get_or_create(
            completion=completion,
            defaults={
                "certificate_number": f"ROT-{obj.id}-{now.strftime('%Y%m%d%H%M%S')}",
                "issued_by": request.user,
            },
        )
        certificate.status = RotationCertificate.STATUS_VERIFIED
        certificate.verified_by = request.user
        certificate.verified_at = now
        if not certificate.issued_by_id:
            certificate.issued_by = request.user
        certificate.save()

        return Response(RotationCompletionSerializer(completion, context={"request": request}).data)

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
            supervised_ids = _get_supervised_resident_ids(user)
            return qs.filter(resident_training__resident_user_id__in=supervised_ids)
        return qs.none()

    def perform_create(self, serializer):
        user = self.request.user
        if _is_resident(user):
            requested_rtr = serializer.validated_data.get("resident_training")
            if requested_rtr is None:
                raise DRFValidationError({"resident_training": "This field is required."})
            if requested_rtr.resident_user_id != user.id:
                self.permission_denied(
                    self.request,
                    message="Residents can only create leave for their own training record.",
                )
            serializer.save()
            return
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
            supervised_ids = _get_supervised_resident_ids(user)
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
from drf_spectacular.utils import extend_schema


@extend_schema(responses={200: None})
class RotationApprovalInboxView(APIView):
    serializer_class = RotationAssignmentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: None})
    @extend_schema(operation_id="api_my_workshop_completions_list")
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
            supervised_ids, dept_ids = _get_rotation_scope(user)
            qs = qs.filter(status=RotationAssignment.STATUS_SUBMITTED).filter(
                Q(resident_training__resident_user_id__in=supervised_ids)
                | Q(hospital_department__department_id__in=dept_ids)
            ).distinct()
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = RotationAssignmentSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


@extend_schema(responses={200: None})
class LeaveApprovalInboxView(APIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: None})
    def get(self, request):
        user = request.user
        qs = LeaveRequest.objects.select_related(
            "resident_training__resident_user"
        ).filter(status=LeaveRequest.STATUS_SUBMITTED)
        if _is_admin_or_utrmc_admin(user):
            pass  # see all
        elif _is_supervisor_or_hod(user):
            supervised_ids = _get_supervised_resident_ids(user)
            qs = qs.filter(resident_training__resident_user_id__in=supervised_ids)
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        serializer = LeaveRequestSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


@extend_schema(responses={200: None})
class MyRotationsView(APIView):
    serializer_class = RotationAssignmentSerializer
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


@extend_schema(responses={200: None})
class MyLeavesView(APIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        qs = LeaveRequest.objects.filter(
            resident_training__resident_user=request.user
        ).order_by("-start_date")
        serializer = LeaveRequestSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


@extend_schema(responses={200: None})
class SupervisorPendingRotationsView(APIView):
    serializer_class = RotationAssignmentSerializer
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
            supervised_ids, dept_ids = _get_rotation_scope(user)
            qs = RotationAssignment.objects.filter(
                status=RotationAssignment.STATUS_SUBMITTED,
            ).filter(
                Q(resident_training__resident_user_id__in=supervised_ids)
                | Q(hospital_department__department_id__in=dept_ids)
            ).distinct()
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
    LogbookThresholdConfig,
    LogbookEntry,
    LogbookReview,
    LogbookThresholdSnapshot,
    SubmissionRequirementTemplate,
    ResidentSubmission,
    SubmissionDocument,
    SubmissionReview,
    SubmissionCertificate,
    ProgramRotationRequirement,
    RotationCompletion,
    RotationCertificate,
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
    LogbookThresholdConfigSerializer,
    LogbookEntrySerializer,
    LogbookReviewSerializer,
    LogbookThresholdSnapshotSerializer,
    SubmissionRequirementTemplateSerializer,
    ResidentSubmissionSerializer,
    SubmissionDocumentSerializer,
    SubmissionReviewSerializer,
    SubmissionCertificateSerializer,
    ProgramRotationRequirementSerializer,
    RotationCompletionSerializer,
    RotationCertificateSerializer,
)


# ------------------------------------------------------------------
# Program Policy
# ------------------------------------------------------------------

@extend_schema(responses={200: None})
class ProgramPolicyView(APIView):
    """GET + PUT/PATCH the policy for a specific program. Admin/UTRMC-admin only."""
    serializer_class = ProgramPolicySerializer
    permission_classes = [IsAuthenticated]

    def _get_program(self, program_id):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(TrainingProgram, pk=program_id)

    def get(self, request, program_id):
        if not _is_utrmc_viewer(request.user):
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
        if getattr(self, "swagger_fake_view", False):
            return ProgramMilestone.objects.none()
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


@extend_schema(responses={200: None})
class MilestoneResearchRequirementView(APIView):
    """GET + PUT research requirements for a milestone."""
    serializer_class = ProgramMilestoneResearchRequirementSerializer
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


def _get_active_rtr_or_none(user):
    """Return the user's active ResidentTrainingRecord if one exists."""
    return ResidentTrainingRecord.objects.filter(resident_user=user, active=True).first()


@extend_schema(responses={200: None})
class ResidentResearchProjectView(APIView):
    """
    GET / POST / PATCH own research project.
    Residents manage their own project; supervisors can view their assigned residents'.
    """
    serializer_class = ResidentResearchProjectSerializer
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

    @extend_schema(operation_id="api_my_workshop_completions_create")
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


@extend_schema(responses={200: None})
class ResearchProjectActionView(APIView):
    """State machine transition endpoints for research project."""
    serializer_class = TrainingEmptySchemaSerializer
    permission_classes = [IsAuthenticated]

    VALID_ACTIONS = {
        "submit-to-supervisor": ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
        "supervisor-approve": ResidentResearchProject.STATUS_APPROVED_SUPERVISOR,
        "supervisor-return": ResidentResearchProject.STATUS_DRAFT,
        "submit-to-university": ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
        "accept-by-university": ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
        # Backward-compatible alias retained for existing clients.
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
        elif action in ("supervisor-approve", "supervisor-return", "return-to-draft"):
            # Supervisor approves/returns
            if not _is_supervisor_or_hod(user) and not _is_admin_or_utrmc_admin(user):
                return Response({"detail": "Supervisor/admin role required."}, status=403)
            project_id = request.data.get("project_id")
            if not project_id:
                return Response({"detail": "project_id required."}, status=400)
            project = ResidentResearchProject.objects.get(pk=project_id)
            if action in ("supervisor-approve", "supervisor-return", "return-to-draft"):
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

@extend_schema(responses={200: None})
class ResidentThesisView(APIView):
    """GET / POST / PATCH own thesis record."""
    serializer_class = ResidentThesisSerializer
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


@extend_schema(responses={200: None})
class ThesisSubmitView(APIView):
    """POST to submit thesis (transitions status to SUBMITTED)."""
    serializer_class = TrainingEmptySchemaSerializer
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

@extend_schema(responses={200: None})
class MyWorkshopCompletionsView(APIView):
    """Resident's own workshop completion records."""
    serializer_class = ResidentWorkshopCompletionSerializer
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


@extend_schema(responses={200: None})
class MyWorkshopCompletionDetailView(APIView):
    """GET / DELETE a single workshop completion record."""
    serializer_class = ResidentWorkshopCompletionSerializer
    permission_classes = [IsAuthenticated]

    def _get_completion(self, request, pk):
        from django.shortcuts import get_object_or_404
        rtr = _get_active_rtr(request.user)
        return get_object_or_404(ResidentWorkshopCompletion, pk=pk, resident_training_record=rtr)

    @extend_schema(operation_id="api_my_workshop_completion_retrieve")
    def get(self, request, pk):
        obj = self._get_completion(request, pk)
        return Response(ResidentWorkshopCompletionSerializer(obj, context={"request": request}).data)

    @extend_schema(operation_id="api_my_workshop_completion_destroy")
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

@extend_schema(responses={200: None})
class MyEligibilityView(APIView):
    """Resident's own eligibility snapshot (IMM + FINAL)."""
    serializer_class = TrainingEmptySchemaSerializer
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


@extend_schema(responses={200: None})
class UTRMCEligibilityView(APIView):
    """UTRMC/admin view: list eligibility with optional filters."""
    serializer_class = ResidentMilestoneEligibilitySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_utrmc_viewer(request.user):
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


@extend_schema(responses={200: None})
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


@extend_schema(responses={200: None})
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

@extend_schema(responses={200: None})
class ResidentSummaryView(APIView):
    """Single-call summary for the resident command-center dashboard."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        user = request.user
        if not _is_resident(user) and not _is_admin_or_utrmc_admin(user):
            return Response({"detail": "Resident access required."}, status=403)

        rtr = _get_active_rtr_or_none(user)
        if rtr is None:
            from sims.supervision.services import get_resident_supervision_summary
            resident_profile = getattr(user, "resident_profile", None)
            resident_supervision = get_resident_supervision_summary(resident=resident_profile)
            return Response({
                "training_record": None,
                "rotation": {"current": None, "next": None},
                "schedule": [],
                "leaves": {"active_count": 0, "pending_count": 0, "list": []},
                "postings": {"active_count": 0, "pending_count": 0},
                "research": {
                    "status": None,
                    "supervisor_name": None,
                    "synopsis_uploaded": False,
                    "university_submitted": False,
                },
                "thesis": {"status": "NOT_STARTED", "submitted_at": None},
                "workshops": {
                    "total_completed": 0,
                    "required_for_imm": 0,
                    "required_for_final": 0,
                    "completed_list": [],
                },
                "eligibility": {
                    "IMM": {"status": None, "reasons": []},
                    "FINAL": {"status": None, "reasons": []},
                },
                "supervision": {
                    "active_primary": _serialize_assignment(resident_supervision["active_primary"]),
                    "active_co_supervisors": [
                        _serialize_assignment(item) for item in resident_supervision["active_co_supervisors"]
                    ],
                    "past_assignments": [
                        _serialize_assignment(item) for item in resident_supervision["past_assignments"]
                    ],
                },
            })
        today = timezone.now().date()

        # --- Training record ---
        training_data = {
            "id": rtr.id,
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
                RotationAssignment.STATUS_RETURNED,
                RotationAssignment.STATUS_REJECTED,
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

        from sims.supervision.services import get_resident_supervision_summary
        resident_profile = getattr(user, "resident_profile", None)
        resident_supervision = get_resident_supervision_summary(resident=resident_profile)
        supervision_data = {
            "active_primary": _serialize_assignment(resident_supervision["active_primary"]),
            "active_co_supervisors": [
                _serialize_assignment(item) for item in resident_supervision["active_co_supervisors"]
            ],
            "past_assignments": [
                _serialize_assignment(item) for item in resident_supervision["past_assignments"]
            ],
        }

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
            "supervision": supervision_data,
        })


@extend_schema(responses={200: None})
class SupervisorSummaryView(APIView):
    """Single-call summary for the supervisor dashboard."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        user = request.user
        if not _is_supervisor_or_hod(user) and not _is_admin_or_utrmc_admin(user):
            return Response({"detail": "Supervisor access required."}, status=403)

        # ---- Determine scoped resident users ----
        from sims.users.models import User as SIMSUser

        if _is_admin_or_utrmc_admin(user):
            resident_users = list(
                SIMSUser.objects.filter(role__in=["RESIDENT", "RESIDENT"], is_active=True)
            )
        else:
            resident_users = list(
                SIMSUser.objects.filter(id__in=_get_supervised_resident_ids(user))
            )

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

        from sims.supervision.services import get_supervisor_resident_summary
        supervisor_profile = getattr(user, "supervisor_profile", None)
        supervisor_supervision = get_supervisor_resident_summary(supervisor=supervisor_profile)
        supervision_data = {
            "active_primary_residents": [
                _serialize_assignment(item) for item in supervisor_supervision["active_primary_residents"]
            ],
            "active_co_supervised_residents": [
                _serialize_assignment(item) for item in supervisor_supervision["active_co_supervised_residents"]
            ],
            "past_assigned_residents": [
                _serialize_assignment(item) for item in supervisor_supervision["past_assigned_residents"]
            ],
        }

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
            "supervision": supervision_data,
        })


@extend_schema(responses={200: None})
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
            "RESIDENT": {
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


def _is_hod(user):
    from sims.users.models import SupervisorProfile
    try:
        profile = user.supervisor_profile
        return profile.designation_ref == "HOD"
    except SupervisorProfile.DoesNotExist:
        return False


def _get_hod_department_ids(user):
    from sims.users.models import SupervisorProfile
    try:
        profile = user.supervisor_profile
        if profile.designation_ref == "HOD" and profile.department_ref_id:
            return {profile.department_ref_id}
    except SupervisorProfile.DoesNotExist:
        pass
    return set()


def _get_department_resident_ids(department_ids):
    if not department_ids:
        return set()
    from sims.users.models import User as SIMSUser

    return set(
        SIMSUser.objects.filter(
            role__in=["RESIDENT", "RESIDENT"],
            is_active=True,
            is_archived=False,
            home_department_id__in=department_ids,
        ).values_list("id", flat=True)
    )


def _can_access_resident_training(user, resident_training):
    if _is_admin_or_utrmc_admin(user):
        return True
    if _is_resident(user):
        return resident_training.resident_user_id == user.id
    if _is_supervisor_or_hod(user):
        supervised_ids = _get_supervised_resident_ids(user)
        if resident_training.resident_user_id in supervised_ids:
            return True
        dept_ids = _get_hod_department_ids(user)
        return bool(
            dept_ids and resident_training.resident_user.home_department_id in dept_ids
        )
    return False


def _get_submission_requirements(rtr, submission_type):
    resident = rtr.resident_user
    return SubmissionRequirementTemplate.objects.filter(
        submission_type=submission_type,
        active=True,
        is_required=True,
    ).filter(
        Q(program__isnull=True) | Q(program=rtr.program)
    ).filter(
        Q(department__isnull=True) | Q(department=resident.home_department)
    ).order_by("sort_order", "title")


def _evaluate_logbook_thresholds(rtr, persist=True):
    today = timezone.now().date()
    resident = rtr.resident_user
    base_entries = LogbookEntry.objects.filter(
        resident_training_record=rtr,
        status=LogbookEntry.STATUS_APPROVED,
    )
    configs = LogbookThresholdConfig.objects.filter(
        is_active=True
    ).filter(
        Q(program__isnull=True) | Q(program=rtr.program)
    ).filter(
        Q(department__isnull=True) | Q(department=resident.home_department)
    )

    snapshots_payload = []
    for config in configs:
        if config.mode == LogbookThresholdConfig.MODE_PER_ROTATION:
            rotations = RotationAssignment.objects.filter(
                resident_training=rtr,
                status__in=[
                    RotationAssignment.STATUS_ACTIVE,
                    RotationAssignment.STATUS_APPROVED,
                    RotationAssignment.STATUS_COMPLETED,
                ],
            )
            if not rotations.exists():
                payload = {
                    "threshold_config_id": config.id,
                    "rotation_assignment_id": None,
                    "window_start": None,
                    "window_end": None,
                    "approved_entries": 0,
                    "required_entries": config.min_approved_entries,
                    "is_met": False,
                }
                snapshots_payload.append(payload)
                if persist:
                    LogbookThresholdSnapshot.objects.update_or_create(
                        resident_training_record=rtr,
                        threshold_config=config,
                        rotation_assignment=None,
                        window_start=None,
                        window_end=None,
                        defaults={
                            "approved_entries": payload["approved_entries"],
                            "required_entries": payload["required_entries"],
                            "is_met": payload["is_met"],
                        },
                    )
                continue

            for rotation in rotations:
                approved_entries = base_entries.filter(rotation_assignment=rotation).count()
                payload = {
                    "threshold_config_id": config.id,
                    "rotation_assignment_id": rotation.id,
                    "window_start": rotation.start_date,
                    "window_end": rotation.end_date,
                    "approved_entries": approved_entries,
                    "required_entries": config.min_approved_entries,
                    "is_met": approved_entries >= config.min_approved_entries,
                }
                snapshots_payload.append(payload)
                if persist:
                    LogbookThresholdSnapshot.objects.update_or_create(
                        resident_training_record=rtr,
                        threshold_config=config,
                        rotation_assignment=rotation,
                        window_start=rotation.start_date,
                        window_end=rotation.end_date,
                        defaults={
                            "approved_entries": payload["approved_entries"],
                            "required_entries": payload["required_entries"],
                            "is_met": payload["is_met"],
                        },
                    )
        else:
            period_days = config.period_days or 30
            window_start = today - timedelta(days=period_days - 1)
            approved_entries = base_entries.filter(
                approved_at__date__gte=window_start,
                approved_at__date__lte=today,
            ).count()
            payload = {
                "threshold_config_id": config.id,
                "rotation_assignment_id": None,
                "window_start": window_start,
                "window_end": today,
                "approved_entries": approved_entries,
                "required_entries": config.min_approved_entries,
                "is_met": approved_entries >= config.min_approved_entries,
            }
            snapshots_payload.append(payload)
            if persist:
                LogbookThresholdSnapshot.objects.update_or_create(
                    resident_training_record=rtr,
                    threshold_config=config,
                    rotation_assignment=None,
                    window_start=window_start,
                    window_end=today,
                    defaults={
                        "approved_entries": payload["approved_entries"],
                        "required_entries": payload["required_entries"],
                        "is_met": payload["is_met"],
                    },
                )

    overall_met = bool(snapshots_payload) and all(item["is_met"] for item in snapshots_payload)
    return {
        "overall_met": overall_met,
        "count": len(snapshots_payload),
        "items": snapshots_payload,
    }


class LogbookEntryViewSet(viewsets.ModelViewSet):
    serializer_class = LogbookEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = LogbookEntry.objects.select_related(
            "resident_training_record__resident_user",
            "rotation_assignment",
            "reviewed_by",
        ).prefetch_related("reviews")
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)

        if _is_resident(user):
            return qs.filter(resident_training_record__resident_user=user)
        if _is_admin_or_utrmc_admin(user):
            return qs.all()
        if _is_supervisor_or_hod(user):
            supervised_ids = _get_supervised_resident_ids(user)
            dept_ids = _get_hod_department_ids(user)
            return qs.filter(
                Q(resident_training_record__resident_user_id__in=supervised_ids)
                | Q(resident_training_record__resident_user__home_department_id__in=dept_ids)
            ).distinct()
        return qs.none()

    def perform_create(self, serializer):
        user = self.request.user
        if _is_resident(user):
            rtr = _get_active_rtr(user)
            serializer.save(resident_training_record=rtr, created_by=user)
            return
        if _is_admin_or_utrmc_admin(user):
            serializer.save(created_by=user)
            return
        raise DRFValidationError("Only residents/admin can create logbook entries.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not _can_access_resident_training(request.user, instance.resident_training_record):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if _is_resident(request.user) and instance.status not in {
            LogbookEntry.STATUS_DRAFT,
            LogbookEntry.STATUS_RETURNED,
        }:
            return Response(
                {"detail": "Entry can only be edited in draft/returned status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        entry = self.get_object()
        if not (_is_admin_or_utrmc_admin(request.user) or (
            _is_resident(request.user) and entry.resident_training_record.resident_user_id == request.user.id
        )):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if entry.status not in {LogbookEntry.STATUS_DRAFT, LogbookEntry.STATUS_RETURNED}:
            return Response(
                {"detail": f"Cannot submit from {entry.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        entry.status = LogbookEntry.STATUS_SUBMITTED
        entry.submitted_at = timezone.now()
        entry.supervisor_feedback = ""
        entry.save()
        return Response(LogbookEntrySerializer(entry, context={"request": request}).data)

    def _review_entry(self, request, entry):
        if not (_is_supervisor_or_hod(request.user) or _is_admin_or_utrmc_admin(request.user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if not _can_access_resident_training(request.user, entry.resident_training_record):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if entry.status != LogbookEntry.STATUS_SUBMITTED:
            return Response(
                {"detail": f"Cannot review from {entry.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        action_name = request.data.get("action")
        feedback = (request.data.get("feedback") or request.data.get("supervisor_feedback") or "").strip()
        now = timezone.now()
        if action_name == "approved":
            entry.status = LogbookEntry.STATUS_APPROVED
            entry.approved_at = now
            review_action = LogbookReview.ACTION_APPROVED
        elif action_name == "returned":
            entry.status = LogbookEntry.STATUS_RETURNED
            entry.returned_at = now
            review_action = LogbookReview.ACTION_RETURNED
        else:
            return Response(
                {"detail": "action must be 'approved' or 'returned'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        entry.reviewed_by = request.user
        entry.supervisor_feedback = feedback
        entry.save()
        LogbookReview.objects.create(
            entry=entry,
            reviewer=request.user,
            action=review_action,
            comments=feedback,
        )
        return Response(LogbookEntrySerializer(entry, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        entry = self.get_object()
        return self._review_entry(request, entry)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        entry = self.get_object()
        return self._review_entry(request, entry)


@extend_schema(responses={200: None})
class LogbookReviewQueueView(APIView):
    serializer_class = LogbookEntrySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = LogbookEntry.objects.filter(status=LogbookEntry.STATUS_SUBMITTED).select_related(
            "resident_training_record__resident_user",
            "rotation_assignment",
        )
        if _is_admin_or_utrmc_admin(user):
            pass
        elif _is_supervisor_or_hod(user):
            supervised_ids = _get_supervised_resident_ids(user)
            dept_ids = _get_hod_department_ids(user)
            qs = qs.filter(
                Q(resident_training_record__resident_user_id__in=supervised_ids)
                | Q(resident_training_record__resident_user__home_department_id__in=dept_ids)
            ).distinct()
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        data = LogbookEntrySerializer(qs, many=True, context={"request": request}).data
        return Response({"count": qs.count(), "results": data})


class LogbookThresholdConfigViewSet(viewsets.ModelViewSet):
    serializer_class = LogbookThresholdConfigSerializer
    permission_classes = [IsAuthenticated]
    queryset = LogbookThresholdConfig.objects.select_related("program", "department", "configured_by")

    def _check_write(self, request):
        if _is_admin_or_utrmc_admin(request.user):
            return
        if _is_supervisor_or_hod(request.user) and _is_hod(request.user):
            return
        self.permission_denied(request, message="Only admin/utrmc_admin/HOD can modify threshold config.")

    def perform_create(self, serializer):
        serializer.save(configured_by=self.request.user)

    def create(self, request, *args, **kwargs):
        self._check_write(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._check_write(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_write(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_write(request)
        return super().destroy(request, *args, **kwargs)


@extend_schema(responses={200: None})
class LogbookMyThresholdView(APIView):
    serializer_class = TrainingEmptySchemaSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr(request.user)
        _evaluate_logbook_thresholds(rtr, persist=True)
        snapshots = LogbookThresholdSnapshot.objects.filter(
            resident_training_record=rtr
        ).select_related("threshold_config", "rotation_assignment")
        serializer = LogbookThresholdSnapshotSerializer(snapshots, many=True, context={"request": request})
        return Response(
            {
                "count": snapshots.count(),
                "results": serializer.data,
                "overall_met": bool(serializer.data) and all(item["is_met"] for item in serializer.data),
            }
        )


class SubmissionRequirementTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionRequirementTemplateSerializer
    permission_classes = [IsAuthenticated]
    queryset = SubmissionRequirementTemplate.objects.select_related(
        "program", "department", "created_by"
    )

    def get_queryset(self):
        qs = super().get_queryset()
        qp = self.request.query_params
        if qp.get("submission_type"):
            qs = qs.filter(submission_type=qp["submission_type"])
        if qp.get("program"):
            qs = qs.filter(program_id=qp["program"])
        if qp.get("department"):
            qs = qs.filter(department_id=qp["department"])
        if qp.get("active") in {"true", "false"}:
            qs = qs.filter(active=qp["active"] == "true")
        return qs

    def _check_write(self, request):
        if _is_admin_or_utrmc_admin(request.user):
            return
        if _is_supervisor_or_hod(request.user) and _is_hod(request.user):
            return
        self.permission_denied(
            request,
            message="Only admin/utrmc_admin/HOD can modify submission requirements.",
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        self._check_write(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._check_write(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_write(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_write(request)
        return super().destroy(request, *args, **kwargs)


@extend_schema(responses={200: None})
class _ResidentSubmissionBaseView(APIView):
    serializer_class = ResidentSubmissionSerializer
    permission_classes = [IsAuthenticated]
    submission_type = None

    def _get_submission(self, rtr):
        return ResidentSubmission.objects.filter(
            resident_training_record=rtr,
            submission_type=self.submission_type,
        ).first()

    def get(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr(request.user)
        submission = self._get_submission(rtr)
        if not submission:
            return Response({"detail": "No submission found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ResidentSubmissionSerializer(submission, context={"request": request}).data)

    def post(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr(request.user)
        existing = self._get_submission(rtr)
        if existing:
            return Response(
                {"detail": "Submission already exists. Use PATCH to update."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        submission = ResidentSubmission.objects.create(
            resident_training_record=rtr,
            submission_type=self.submission_type,
            status=ResidentSubmission.STATUS_DRAFT,
            feedback=(request.data.get("feedback") or "").strip(),
        )
        return Response(
            ResidentSubmissionSerializer(submission, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr(request.user)
        submission = self._get_submission(rtr)
        if not submission:
            return Response({"detail": "No submission found."}, status=status.HTTP_404_NOT_FOUND)
        if submission.status not in {ResidentSubmission.STATUS_DRAFT, ResidentSubmission.STATUS_RETURNED}:
            return Response(
                {"detail": "Submission can only be edited in draft/returned status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        submission.feedback = (request.data.get("feedback") or submission.feedback or "").strip()
        submission.save(update_fields=["feedback", "updated_at"])
        return Response(ResidentSubmissionSerializer(submission, context={"request": request}).data)


class SynopsisSubmissionView(_ResidentSubmissionBaseView):
    submission_type = ResidentSubmission.TYPE_SYNOPSIS


class ThesisSubmissionView(_ResidentSubmissionBaseView):
    submission_type = ResidentSubmission.TYPE_THESIS


@extend_schema(responses={200: None})
class _SubmissionDocumentsBaseView(APIView):
    serializer_class = SubmissionDocumentSerializer
    permission_classes = [IsAuthenticated]
    submission_type = None

    def post(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr(request.user)
        submission, _ = ResidentSubmission.objects.get_or_create(
            resident_training_record=rtr,
            submission_type=self.submission_type,
            defaults={"status": ResidentSubmission.STATUS_DRAFT},
        )
        if submission.status not in {ResidentSubmission.STATUS_DRAFT, ResidentSubmission.STATUS_RETURNED}:
            return Response(
                {"detail": "Documents can only be uploaded in draft/returned status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        upload = request.FILES.get("file")
        if not upload:
            return Response({"detail": "file is required."}, status=status.HTTP_400_BAD_REQUEST)
        requirement_id = request.data.get("requirement")
        requirement = None
        if requirement_id:
            requirement = SubmissionRequirementTemplate.objects.filter(
                pk=requirement_id,
                submission_type=self.submission_type,
                active=True,
            ).first()
            if not requirement:
                return Response({"detail": "Invalid requirement."}, status=status.HTTP_400_BAD_REQUEST)
        document = SubmissionDocument.objects.create(
            submission=submission,
            requirement=requirement,
            file=upload,
            original_filename=upload.name,
            uploaded_by=request.user,
            is_active=True,
        )
        return Response(
            SubmissionDocumentSerializer(document, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class SynopsisSubmissionDocumentsView(_SubmissionDocumentsBaseView):
    submission_type = ResidentSubmission.TYPE_SYNOPSIS


class ThesisSubmissionDocumentsView(_SubmissionDocumentsBaseView):
    submission_type = ResidentSubmission.TYPE_THESIS


@extend_schema(responses={200: None})
class _SubmissionSubmitBaseView(APIView):
    serializer_class = ResidentSubmissionSerializer
    permission_classes = [IsAuthenticated]
    submission_type = None

    def post(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr(request.user)
        submission = ResidentSubmission.objects.filter(
            resident_training_record=rtr,
            submission_type=self.submission_type,
        ).first()
        if not submission:
            return Response({"detail": "Create submission first."}, status=status.HTTP_400_BAD_REQUEST)
        if submission.status not in {ResidentSubmission.STATUS_DRAFT, ResidentSubmission.STATUS_RETURNED}:
            return Response(
                {"detail": f"Cannot submit from status {submission.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        required_requirements = list(_get_submission_requirements(rtr, self.submission_type))
        required_ids = {item.id for item in required_requirements}
        uploaded_ids = set(
            submission.documents.filter(
                is_active=True,
                requirement_id__in=required_ids,
            ).values_list("requirement_id", flat=True)
        )
        missing = [item for item in required_requirements if item.id not in uploaded_ids]
        if missing:
            return Response(
                {
                    "detail": "All required documents must be uploaded before submission.",
                    "missing_requirements": SubmissionRequirementTemplateSerializer(missing, many=True).data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission.status = ResidentSubmission.STATUS_SUBMITTED
        submission.submitted_at = timezone.now()
        submission.feedback = ""
        submission.save()
        SubmissionReview.objects.create(
            submission=submission,
            reviewer=request.user,
            action=SubmissionReview.ACTION_SUBMITTED,
            comments="Submitted for completeness review.",
        )
        return Response(ResidentSubmissionSerializer(submission, context={"request": request}).data)


class SynopsisSubmissionSubmitView(_SubmissionSubmitBaseView):
    submission_type = ResidentSubmission.TYPE_SYNOPSIS


class ThesisSubmissionSubmitView(_SubmissionSubmitBaseView):
    submission_type = ResidentSubmission.TYPE_THESIS


@extend_schema(responses={200: None})
class _SubmissionReviewQueueBaseView(APIView):
    serializer_class = ResidentSubmissionSerializer
    permission_classes = [IsAuthenticated]
    submission_type = None

    def get(self, request):
        user = request.user
        qs = ResidentSubmission.objects.filter(
            submission_type=self.submission_type,
            status__in=[ResidentSubmission.STATUS_SUBMITTED, ResidentSubmission.STATUS_UNDER_REVIEW],
        ).select_related(
            "resident_training_record__resident_user",
            "resident_training_record__program",
        )
        if _is_admin_or_utrmc_admin(user) or user.role == "SUPPORT_STAFF":
            pass
        elif _is_supervisor_or_hod(user):
            supervised_ids = _get_supervised_resident_ids(user)
            dept_ids = _get_hod_department_ids(user)
            qs = qs.filter(
                Q(resident_training_record__resident_user_id__in=supervised_ids)
                | Q(resident_training_record__resident_user__home_department_id__in=dept_ids)
            ).distinct()
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResidentSubmissionSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class SynopsisReviewQueueView(_SubmissionReviewQueueBaseView):
    submission_type = ResidentSubmission.TYPE_SYNOPSIS


class ThesisReviewQueueView(_SubmissionReviewQueueBaseView):
    submission_type = ResidentSubmission.TYPE_THESIS


@extend_schema(responses={200: None})
class _SubmissionReviewActionBaseView(APIView):
    serializer_class = ResidentSubmissionSerializer
    permission_classes = [IsAuthenticated]
    submission_type = None

    def post(self, request, submission_id):
        user = request.user
        if user.role == "SUPPORT_STAFF":
            return Response({"detail": "Read-only role."}, status=status.HTTP_403_FORBIDDEN)
        if not (_is_supervisor_or_hod(user) or _is_admin_or_utrmc_admin(user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        submission = ResidentSubmission.objects.filter(
            pk=submission_id,
            submission_type=self.submission_type,
        ).select_related("resident_training_record__resident_user", "resident_training_record__program").first()
        if not submission:
            return Response({"detail": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)
        if not _can_access_resident_training(user, submission.resident_training_record):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        action_name = request.data.get("action")
        comments = (request.data.get("comments") or request.data.get("feedback") or "").strip()
        now = timezone.now()

        if action_name == "start-review":
            if submission.status not in {
                ResidentSubmission.STATUS_SUBMITTED,
                ResidentSubmission.STATUS_UNDER_REVIEW,
            }:
                return Response(
                    {"detail": f"Cannot start review from status {submission.status}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            submission.status = ResidentSubmission.STATUS_UNDER_REVIEW
            submission.under_review_at = now
            review_action = SubmissionReview.ACTION_UNDER_REVIEW
        elif action_name == "return":
            if submission.status not in {
                ResidentSubmission.STATUS_SUBMITTED,
                ResidentSubmission.STATUS_UNDER_REVIEW,
            }:
                return Response(
                    {"detail": f"Cannot return from status {submission.status}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            submission.status = ResidentSubmission.STATUS_RETURNED
            submission.returned_at = now
            review_action = SubmissionReview.ACTION_RETURNED
        elif action_name == "verify":
            if submission.status not in {
                ResidentSubmission.STATUS_SUBMITTED,
                ResidentSubmission.STATUS_UNDER_REVIEW,
                ResidentSubmission.STATUS_VERIFIED,
            }:
                return Response(
                    {"detail": f"Cannot verify from status {submission.status}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            certificate_number = (
                f"{submission.submission_type[:3]}-{submission.id}-{now.strftime('%Y%m%d%H%M%S')}"
            )
            certificate, _ = SubmissionCertificate.objects.get_or_create(
                submission=submission,
                defaults={
                    "certificate_number": certificate_number,
                    "issued_by": user,
                    "status": SubmissionCertificate.STATUS_ISSUED,
                },
            )
            if not certificate.issued_by_id:
                certificate.issued_by = user
                certificate.save(update_fields=["issued_by"])
            submission.status = ResidentSubmission.STATUS_CERTIFICATE_ISSUED
            submission.verified_at = now
            submission.certificate_issued_at = now
            review_action = SubmissionReview.ACTION_CERTIFICATE_ISSUED
            if submission.submission_type == ResidentSubmission.TYPE_THESIS:
                try:
                    thesis = submission.resident_training_record.thesis
                except ResidentThesis.DoesNotExist:
                    thesis = None
                if thesis and thesis.status != ResidentThesis.STATUS_SUBMITTED:
                    thesis.status = ResidentThesis.STATUS_SUBMITTED
                    thesis.submitted_at = thesis.submitted_at or now
                    thesis.save()
        else:
            return Response(
                {"detail": "action must be one of: start-review, return, verify."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission.reviewed_by = user
        submission.feedback = comments
        submission.save()
        SubmissionReview.objects.create(
            submission=submission,
            reviewer=user,
            action=review_action,
            comments=comments,
        )
        return Response(ResidentSubmissionSerializer(submission, context={"request": request}).data)


class SynopsisReviewActionView(_SubmissionReviewActionBaseView):
    submission_type = ResidentSubmission.TYPE_SYNOPSIS


class ThesisReviewActionView(_SubmissionReviewActionBaseView):
    submission_type = ResidentSubmission.TYPE_THESIS


@extend_schema(responses={200: None})
class SubmissionCertificatesView(APIView):
    serializer_class = SubmissionCertificateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = SubmissionCertificate.objects.select_related(
            "submission__resident_training_record__resident_user",
            "submission",
            "issued_by",
            "verified_by",
        )
        submission_type = request.query_params.get("submission_type")
        if submission_type:
            qs = qs.filter(submission__submission_type=submission_type)

        if _is_resident(user):
            qs = qs.filter(submission__resident_training_record__resident_user=user)
        elif _is_admin_or_utrmc_admin(user) or user.role == "SUPPORT_STAFF":
            pass
        elif _is_supervisor_or_hod(user):
            supervised_ids = _get_supervised_resident_ids(user)
            dept_ids = _get_hod_department_ids(user)
            qs = qs.filter(
                Q(submission__resident_training_record__resident_user_id__in=supervised_ids)
                | Q(submission__resident_training_record__resident_user__home_department_id__in=dept_ids)
            ).distinct()
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = SubmissionCertificateSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


class ProgramRotationRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramRotationRequirementSerializer
    permission_classes = [IsAuthenticated]
    queryset = ProgramRotationRequirement.objects.select_related("program", "department")

    def _check_write(self, request):
        if _is_admin_or_utrmc_admin(request.user):
            return
        if _is_supervisor_or_hod(request.user) and _is_hod(request.user):
            return
        self.permission_denied(
            request,
            message="Only admin/utrmc_admin/HOD can manage rotation requirements.",
        )

    def create(self, request, *args, **kwargs):
        self._check_write(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._check_write(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_write(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_write(request)
        return super().destroy(request, *args, **kwargs)


@extend_schema(responses={200: None})
class RotationCompletionsView(APIView):
    serializer_class = RotationCompletionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = RotationCompletion.objects.select_related(
            "rotation__resident_training__resident_user",
            "rotation__hospital_department__hospital",
            "rotation__hospital_department__department",
            "confirmed_by",
            "verified_by",
            "certificate",
        )
        status_param = request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        if _is_resident(user):
            qs = qs.filter(rotation__resident_training__resident_user=user)
        elif _is_admin_or_utrmc_admin(user) or user.role == "SUPPORT_STAFF":
            pass
        elif _is_supervisor_or_hod(user):
            supervised_ids = _get_supervised_resident_ids(user)
            dept_ids = _get_hod_department_ids(user)
            qs = qs.filter(
                Q(rotation__resident_training__resident_user_id__in=supervised_ids)
                | Q(rotation__resident_training__resident_user__home_department_id__in=dept_ids)
                | Q(rotation__hospital_department__department_id__in=dept_ids)
            ).distinct()
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RotationCompletionSerializer(qs, many=True, context={"request": request})
        return Response({"count": qs.count(), "results": serializer.data})


@extend_schema(responses={200: None})
class RotationCompletionVerifyView(APIView):
    serializer_class = RotationCompletionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, completion_id):
        if not _is_admin_or_utrmc_admin(request.user):
            return Response({"detail": "Only admin/utrmc_admin can verify."}, status=status.HTTP_403_FORBIDDEN)
        completion = RotationCompletion.objects.select_related("rotation").filter(pk=completion_id).first()
        if not completion:
            return Response({"detail": "Completion not found."}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        completion.status = RotationCompletion.STATUS_VERIFIED
        completion.verified_by = request.user
        completion.verified_at = now
        completion.save()

        certificate, _ = RotationCertificate.objects.get_or_create(
            completion=completion,
            defaults={
                "certificate_number": f"ROT-{completion.rotation_id}-{now.strftime('%Y%m%d%H%M%S')}",
                "issued_by": request.user,
            },
        )
        certificate.status = RotationCertificate.STATUS_VERIFIED
        certificate.verified_by = request.user
        certificate.verified_at = now
        if not certificate.issued_by_id:
            certificate.issued_by = request.user
        certificate.save()

        return Response(RotationCompletionSerializer(completion, context={"request": request}).data)


@extend_schema(responses={200: None})
class ResidentOperationalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not _is_resident(request.user):
            return Response({"detail": "Residents only."}, status=status.HTTP_403_FORBIDDEN)
        rtr = _get_active_rtr_or_none(request.user)
        if rtr is None:
            return Response(
                {
                    "training_record_id": None,
                    "logbook": {
                        "total": 0,
                        "draft": 0,
                        "submitted": 0,
                        "returned": 0,
                        "approved": 0,
                        "threshold": {"overall_met": False, "overall_reasons": []},
                    },
                    "submissions": {"synopsis": None, "thesis": None},
                    "certificates": [],
                    "readiness": {
                        "logbook_threshold_met": False,
                        "synopsis_certificate_issued": False,
                        "thesis_certificate_issued": False,
                        "required_rotations_verified": False,
                        "required_rotation_count": 0,
                        "verified_rotation_count": 0,
                    },
                    "pending_actions": [],
                }
            )

        logbook_qs = LogbookEntry.objects.filter(resident_training_record=rtr)
        logbook_counts = {
            "total": logbook_qs.count(),
            "draft": logbook_qs.filter(status=LogbookEntry.STATUS_DRAFT).count(),
            "submitted": logbook_qs.filter(status=LogbookEntry.STATUS_SUBMITTED).count(),
            "returned": logbook_qs.filter(status=LogbookEntry.STATUS_RETURNED).count(),
            "approved": logbook_qs.filter(status=LogbookEntry.STATUS_APPROVED).count(),
        }
        threshold_summary = _evaluate_logbook_thresholds(rtr, persist=True)

        synopsis_submission = ResidentSubmission.objects.filter(
            resident_training_record=rtr, submission_type=ResidentSubmission.TYPE_SYNOPSIS
        ).first()
        thesis_submission = ResidentSubmission.objects.filter(
            resident_training_record=rtr, submission_type=ResidentSubmission.TYPE_THESIS
        ).first()

        certificates = []
        for cert in SubmissionCertificate.objects.filter(
            submission__resident_training_record=rtr
        ).select_related("submission"):
            certificates.append(
                {
                    "type": f"{cert.submission.submission_type.lower()}_submission",
                    "certificate_number": cert.certificate_number,
                    "issued_at": cert.issued_at,
                    "status": cert.status,
                }
            )
        for cert in RotationCertificate.objects.filter(
            completion__rotation__resident_training=rtr
        ).select_related("completion__rotation"):
            certificates.append(
                {
                    "type": "rotation_completion",
                    "certificate_number": cert.certificate_number,
                    "issued_at": cert.issued_at,
                    "status": cert.status,
                    "rotation_id": cert.completion.rotation_id,
                }
            )

        required_rotation_count = ProgramRotationRequirement.objects.filter(
            program=rtr.program, is_mandatory=True
        ).count()
        verified_rotation_count = RotationCompletion.objects.filter(
            rotation__resident_training=rtr,
            status=RotationCompletion.STATUS_VERIFIED,
        ).count()

        readiness = {
            "logbook_threshold_met": threshold_summary["overall_met"],
            "synopsis_certificate_issued": bool(
                synopsis_submission and synopsis_submission.status == ResidentSubmission.STATUS_CERTIFICATE_ISSUED
            ),
            "thesis_certificate_issued": bool(
                thesis_submission and thesis_submission.status == ResidentSubmission.STATUS_CERTIFICATE_ISSUED
            ),
            "required_rotations_verified": required_rotation_count > 0 and verified_rotation_count >= required_rotation_count,
            "required_rotation_count": required_rotation_count,
            "verified_rotation_count": verified_rotation_count,
        }

        pending_actions = []
        if logbook_counts["returned"] > 0:
            pending_actions.append(f"{logbook_counts['returned']} logbook entries returned for revision")
        if logbook_counts["draft"] > 0:
            pending_actions.append(f"{logbook_counts['draft']} logbook drafts pending submission")
        if synopsis_submission and synopsis_submission.status == ResidentSubmission.STATUS_RETURNED:
            pending_actions.append("Synopsis submission returned for missing/incomplete documents")
        if thesis_submission and thesis_submission.status == ResidentSubmission.STATUS_RETURNED:
            pending_actions.append("Thesis submission returned for missing/incomplete documents")

        return Response(
            {
                "training_record_id": rtr.id,
                "logbook": {
                    **logbook_counts,
                    "threshold": threshold_summary,
                },
                "submissions": {
                    "synopsis": ResidentSubmissionSerializer(synopsis_submission).data if synopsis_submission else None,
                    "thesis": ResidentSubmissionSerializer(thesis_submission).data if thesis_submission else None,
                },
                "certificates": certificates,
                "readiness": readiness,
                "pending_actions": pending_actions,
            }
        )


@extend_schema(responses={200: None})
class SupervisorOperationalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not (_is_supervisor_or_hod(user) or _is_admin_or_utrmc_admin(user)):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        if _is_admin_or_utrmc_admin(user):
            resident_ids = set(
                ResidentTrainingRecord.objects.filter(active=True).values_list("resident_user_id", flat=True)
            )
        else:
            resident_ids = _get_supervised_resident_ids(user)
            dept_ids = _get_hod_department_ids(user)
            resident_ids |= _get_department_resident_ids(dept_ids)

        rtrs = ResidentTrainingRecord.objects.filter(
            active=True, resident_user_id__in=resident_ids
        ).select_related("resident_user", "program")
        rtr_ids = list(rtrs.values_list("id", flat=True))

        pending_logbook = LogbookEntry.objects.filter(
            resident_training_record_id__in=rtr_ids,
            status=LogbookEntry.STATUS_SUBMITTED,
        ).count()
        returned_logbook = LogbookEntry.objects.filter(
            resident_training_record_id__in=rtr_ids,
            status=LogbookEntry.STATUS_RETURNED,
        ).count()
        pending_rotations = RotationAssignment.objects.filter(
            resident_training_id__in=rtr_ids,
            status=RotationAssignment.STATUS_SUBMITTED,
        ).count()
        pending_synopsis = ResidentSubmission.objects.filter(
            resident_training_record_id__in=rtr_ids,
            submission_type=ResidentSubmission.TYPE_SYNOPSIS,
            status__in=[ResidentSubmission.STATUS_SUBMITTED, ResidentSubmission.STATUS_UNDER_REVIEW],
        ).count()
        pending_thesis = ResidentSubmission.objects.filter(
            resident_training_record_id__in=rtr_ids,
            submission_type=ResidentSubmission.TYPE_THESIS,
            status__in=[ResidentSubmission.STATUS_SUBMITTED, ResidentSubmission.STATUS_UNDER_REVIEW],
        ).count()

        residents = []
        lagging = []
        for rtr in rtrs:
            threshold = _evaluate_logbook_thresholds(rtr, persist=False)
            resident_row = {
                "resident_id": rtr.resident_user_id,
                "resident_name": rtr.resident_user.get_full_name() or rtr.resident_user.username,
                "program": rtr.program.name,
                "logbook_approved": LogbookEntry.objects.filter(
                    resident_training_record=rtr, status=LogbookEntry.STATUS_APPROVED
                ).count(),
                "pending_reviews": LogbookEntry.objects.filter(
                    resident_training_record=rtr, status=LogbookEntry.STATUS_SUBMITTED
                ).count(),
                "threshold_met": threshold["overall_met"],
            }
            residents.append(resident_row)
            if not threshold["overall_met"]:
                lagging.append(resident_row)

        return Response(
            {
                "assigned_residents": len(resident_ids),
                "pending_logbook_reviews": pending_logbook,
                "returned_logbook_queue": returned_logbook,
                "pending_rotation_applications": pending_rotations,
                "pending_synopsis_reviews": pending_synopsis,
                "pending_thesis_reviews": pending_thesis,
                "residents": residents,
                "lagging_residents": lagging,
                "is_hod": _is_hod(user),
            }
        )





@extend_schema(responses={200: None})
class UTRMCOperationalDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not _is_utrmc_viewer(user):
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        resident_qs = ResidentTrainingRecord.objects.filter(active=True).select_related(
            "resident_user", "program"
        )
        search = (request.query_params.get("search") or "").strip().lower()
        if search:
            resident_qs = resident_qs.filter(
                Q(resident_user__username__icontains=search)
                | Q(resident_user__first_name__icontains=search)
                | Q(resident_user__last_name__icontains=search)
            )
        resident_ids = list(resident_qs.values_list("id", flat=True))

        readiness_rows = []
        for rtr in resident_qs[:200]:
            threshold = _evaluate_logbook_thresholds(rtr, persist=False)
            synopsis_ok = ResidentSubmission.objects.filter(
                resident_training_record=rtr,
                submission_type=ResidentSubmission.TYPE_SYNOPSIS,
                status=ResidentSubmission.STATUS_CERTIFICATE_ISSUED,
            ).exists()
            thesis_ok = ResidentSubmission.objects.filter(
                resident_training_record=rtr,
                submission_type=ResidentSubmission.TYPE_THESIS,
                status=ResidentSubmission.STATUS_CERTIFICATE_ISSUED,
            ).exists()
            required_rotations = ProgramRotationRequirement.objects.filter(
                program=rtr.program, is_mandatory=True
            ).count()
            verified_rotations = RotationCompletion.objects.filter(
                rotation__resident_training=rtr,
                status=RotationCompletion.STATUS_VERIFIED,
            ).count()
            readiness_rows.append(
                {
                    "resident_id": rtr.resident_user_id,
                    "resident_name": rtr.resident_user.get_full_name() or rtr.resident_user.username,
                    "program": rtr.program.name,
                    "logbook_threshold_met": threshold["overall_met"],
                    "synopsis_certificate_issued": synopsis_ok,
                    "thesis_certificate_issued": thesis_ok,
                    "required_rotation_count": required_rotations,
                    "verified_rotation_count": verified_rotations,
                    "rotation_requirement_met": required_rotations > 0 and verified_rotations >= required_rotations,
                }
            )

        return Response(
            {
                "cross_department_overview": {
                    "active_residents": resident_qs.count(),
                    "program_count": TrainingProgram.objects.filter(active=True).count(),
                    "pending_logbook_reviews": LogbookEntry.objects.filter(
                        status=LogbookEntry.STATUS_SUBMITTED
                    ).count(),
                },
                "pending_synopsis_reviews": ResidentSubmission.objects.filter(
                    submission_type=ResidentSubmission.TYPE_SYNOPSIS,
                    status__in=[ResidentSubmission.STATUS_SUBMITTED, ResidentSubmission.STATUS_UNDER_REVIEW],
                ).count(),
                "pending_thesis_reviews": ResidentSubmission.objects.filter(
                    submission_type=ResidentSubmission.TYPE_THESIS,
                    status__in=[ResidentSubmission.STATUS_SUBMITTED, ResidentSubmission.STATUS_UNDER_REVIEW],
                ).count(),
                "pending_rotation_completion_verifications": RotationCompletion.objects.filter(
                    status=RotationCompletion.STATUS_PENDING_UTRMC_VERIFICATION
                ).count(),
                "resident_milestone_readiness": readiness_rows,
                "readiness_summary": {
                    "fully_ready_count": sum(
                        1
                        for row in readiness_rows
                        if row["logbook_threshold_met"]
                        and row["synopsis_certificate_issued"]
                        and row["thesis_certificate_issued"]
                        and row["rotation_requirement_met"]
                    ),
                    "total_rows": len(readiness_rows),
                },
            }
        )
