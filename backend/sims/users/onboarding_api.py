from datetime import date

from django.db import transaction
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.audit.models import ActivityLog
from sims.supervision.models import PendingSupervisorAssignment
from sims.supervision.services import create_supervisor_assignment
from .models import ResidentDocument, ResidentDocumentRequirement, ResidentProfile, SupervisorProfile
from rest_framework import serializers


class ResidentDocumentRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentDocumentRequirement
        fields = "__all__"


class ResidentDocumentRequirementViewSet(viewsets.ModelViewSet):
    queryset = ResidentDocumentRequirement.objects.all()
    serializer_class = ResidentDocumentRequirementSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        if not _admin(self.request.user): raise PermissionDenied()
        serializer.save()

    def perform_update(self, serializer):
        if not _admin(self.request.user): raise PermissionDenied()
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not _admin(request.user): raise PermissionDenied()
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return Response(status=204)


class ResidentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentDocument
        fields = "__all__"
        read_only_fields = ["resident", "status", "verified_by", "verified_at", "uploaded_at", "updated_at"]

DECLARATION_TEXT = (
    "I confirm that the information provided is correct and that the documents uploaded by me are authentic "
    "and belong to me. I understand that any deferred required documents remain pending and must be uploaded when available."
)


def _admin(user):
    return bool(user.is_authenticated and (user.is_superuser or user.role == "ADMIN"))


def _resident_profile(user):
    profile = getattr(user, "resident_profile", None)
    if not profile:
        raise PermissionDenied("Resident profile is required.")
    return profile


def _requirements_for(profile):
    qs = ResidentDocumentRequirement.objects.filter(is_active=True)
    return qs.filter(program__isnull=True, department__isnull=True) | qs.filter(program=profile.program_ref, department__isnull=True) | qs.filter(department=profile.department_ref, program__isnull=True) | qs.filter(program=profile.program_ref, department=profile.department_ref)


def get_resident_onboarding_state(user):
    profile = getattr(user, "resident_profile", None)
    if not profile:
        return {"password_change_required": user.must_change_password, "profile_complete": False, "onboarding_complete": False, "pending_upload_count": 0, "pending_uploads": [], "pending_supervisor_link": None}
    requirements = _requirements_for(profile).distinct().order_by("display_order", "display_name")
    fulfillments = []
    for requirement in requirements:
        document, _ = ResidentDocument.objects.get_or_create(
            resident=profile, requirement=requirement,
            defaults={"document_type": requirement.document_type, "title": requirement.display_name},
        )
        fulfillments.append(document)
    pending = [d for d in fulfillments if d.status in {ResidentDocument.STATUS_DEFERRED, ResidentDocument.STATUS_REUPLOAD_REQUIRED}]
    pending_link = profile.pending_supervisor_assignments.filter(status=PendingSupervisorAssignment.STATUS_PENDING).first()
    return {
        "password_change_required": user.must_change_password,
        "profile_complete": user.is_profile_complete,
        "onboarding_complete": bool(user.is_profile_complete and profile.declaration_accepted),
        "pending_upload_count": len(pending),
        "pending_uploads": [{"requirement_id": d.requirement_id, "document_id": d.id, "document_type": d.document_type, "display_name": d.title, "stage": d.requirement.stage, "status": d.status, "verification_remarks": d.verification_remarks} for d in pending],
        "pending_supervisor_link": {"id": pending_link.id, "name": pending_link.supervisor_name_text, "status": pending_link.status} if pending_link else None,
    }


class ResidentOnboardingStateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(get_resident_onboarding_state(request.user))

    def post(self, request):
        profile = _resident_profile(request.user)
        if not request.data.get("accepted"):
            return Response({"detail": "Declaration must be accepted."}, status=400)
        profile.declaration_accepted = True
        profile.declaration_accepted_at = timezone.now()
        profile.save(update_fields=["declaration_accepted", "declaration_accepted_at", "updated_at"])
        ActivityLog.log(actor=request.user, action="update", verb="ONBOARDING_COMPLETED", target=profile, metadata={"source": "resident_onboarding"})
        return Response(get_resident_onboarding_state(request.user))


class ResidentDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = ResidentDocumentSerializer
    http_method_names = ["get", "post", "head", "options"]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ResidentDocument.objects.select_related("resident__user", "requirement")
        if _admin(self.request.user):
            resident_id = self.request.query_params.get("resident")
            return qs.filter(resident_id=resident_id) if resident_id else qs
        return qs.filter(resident__user=self.request.user)

    def list(self, request, *args, **kwargs):
        documents = list(self.get_queryset().order_by("requirement__stage", "requirement__display_order", "title"))
        return Response([self._data(d) for d in documents])

    def _data(self, d):
        return {"id": d.id, "resident_id": d.resident_id, "requirement_id": d.requirement_id, "document_type": d.document_type, "title": d.title, "stage": d.requirement.stage if d.requirement else "OPTIONAL", "status": d.status, "original_filename": d.original_filename, "verification_remarks": d.verification_remarks, "file": d.file.url if d.file else None}

    @action(detail=True, methods=["post"])
    def defer(self, request, pk=None):
        document = self.get_object()
        if _admin(request.user) or document.resident.user_id != request.user.id:
            if not _admin(request.user): raise PermissionDenied()
        document.status = ResidentDocument.STATUS_DEFERRED
        document.save(update_fields=["status", "updated_at"])
        ActivityLog.log(actor=request.user, action="update", verb="ATTACHMENT_DEFERRED", target=document, metadata={"requirement_id": document.requirement_id})
        return Response(self._data(document))

    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser, FormParser])
    def upload(self, request, pk=None):
        document = self.get_object()
        if not _admin(request.user) and document.resident.user_id != request.user.id:
            raise PermissionDenied()
        uploaded = request.FILES.get("file")
        if not uploaded: return Response({"detail": "file is required"}, status=400)
        if uploaded.size > 10 * 1024 * 1024: return Response({"detail": "File must be 10MB or smaller."}, status=400)
        document.file = uploaded
        document.original_filename = uploaded.name[:255]
        document.status = ResidentDocument.STATUS_PENDING_REVIEW
        document.uploaded_at = timezone.now()
        document.save()
        ActivityLog.log(actor=request.user, action="update", verb="DOCUMENT_UPLOADED", target=document, metadata={"requirement_id": document.requirement_id})
        return Response(self._data(document))

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        if not _admin(request.user): raise PermissionDenied()
        document = self.get_object()
        status_value = request.data.get("status")
        if status_value not in {ResidentDocument.STATUS_VERIFIED, ResidentDocument.STATUS_REUPLOAD_REQUIRED}:
            return Response({"detail": "status must be VERIFIED or REUPLOAD_REQUIRED"}, status=400)
        document.status = status_value
        document.verified_by = request.user
        document.verified_at = timezone.now()
        document.verification_remarks = request.data.get("remarks", "")
        document.save()
        ActivityLog.log(actor=request.user, action="update", verb="DOCUMENT_VERIFIED" if status_value == ResidentDocument.STATUS_VERIFIED else "REUPLOAD_REQUESTED", target=document, metadata={"remarks": document.verification_remarks})
        return Response(self._data(document))


class PendingSupervisorViewSet(viewsets.ModelViewSet):
    class PendingSupervisorSerializer(serializers.ModelSerializer):
        class Meta:
            model = PendingSupervisorAssignment
            fields = "__all__"
            read_only_fields = ["status", "resolved_supervisor", "resolved_by", "resolved_at"]

    serializer_class = PendingSupervisorSerializer
    http_method_names = ["get", "post", "head", "options"]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not _admin(self.request.user): raise PermissionDenied()
        return PendingSupervisorAssignment.objects.select_related("resident__user", "resident__program_ref", "resident__department_ref", "resolved_supervisor__user")

    def list(self, request, *args, **kwargs):
        return Response([{"id": p.id, "resident_id": p.resident_id, "resident": p.resident.user.get_full_name(), "program": getattr(p.resident.program_ref, "name", None), "department": getattr(p.resident.department_ref, "name", None), "supervisor_name": p.supervisor_name_text, "created_at": p.created_at, "status": p.status} for p in self.get_queryset()])

    @action(detail=True, methods=["post"], url_path="resolve")
    def resolve(self, request, pk=None):
        if not _admin(request.user): raise PermissionDenied()
        pending = self.get_object()
        supervisor_id = request.data.get("supervisor_id")
        supervisor = SupervisorProfile.objects.filter(pk=supervisor_id, user__role="SUPERVISOR").first()
        if not supervisor: return Response({"detail": "Supervisor not found."}, status=400)
        with transaction.atomic():
            assignment = create_supervisor_assignment(resident=pending.resident, supervisor=supervisor, assignment_type="PRIMARY", start_date=date.today(), actor=request.user, notes="Resolved from pending supervisor request")
            pending.status = PendingSupervisorAssignment.STATUS_RESOLVED
            pending.resolved_supervisor = supervisor
            pending.resolved_by = request.user
            pending.resolved_at = timezone.now()
            pending.save()
        return Response({"pending_id": pending.id, "assignment_id": assignment.id, "status": pending.status})

    @action(detail=True, methods=["post"], url_path="create-supervisor")
    def create_supervisor(self, request, pk=None):
        if not _admin(request.user): raise PermissionDenied()
        pending = self.get_object()
        from .services import create_user_with_profile
        from django.core.exceptions import ValidationError
        try:
            supervisor_user = create_user_with_profile(
                role="SUPERVISOR",
                full_name=(request.data.get("full_name") or pending.supervisor_name_text).strip(),
                email=request.data.get("email") or pending.email_text,
                phone=request.data.get("phone") or pending.phone_text,
                profile_payload={
                    "pmdc_no": request.data.get("pmdc_no") or pending.pmdc_number_text,
                    "department_ref": request.data.get("department_ref"),
                    "hospital": request.data.get("hospital"),
                },
                actor=request.user,
                source="pending_supervisor_resolution",
            )
        except (ValidationError, Exception) as exc:
            return Response({"detail": str(exc)}, status=400)
        supervisor = supervisor_user.supervisor_profile
        with transaction.atomic():
            assignment = create_supervisor_assignment(resident=pending.resident, supervisor=supervisor, assignment_type="PRIMARY", start_date=date.today(), actor=request.user, notes="Auto-linked after supervisor creation")
            pending.status = PendingSupervisorAssignment.STATUS_RESOLVED
            pending.resolved_supervisor = supervisor
            pending.resolved_by = request.user
            pending.resolved_at = timezone.now()
            pending.save()
        return Response({"pending_id": pending.id, "assignment_id": assignment.id, "supervisor_user_id": supervisor_user.id, "username": supervisor_user.username, "temporary_password": "pgfmu123", "status": pending.status}, status=201)
