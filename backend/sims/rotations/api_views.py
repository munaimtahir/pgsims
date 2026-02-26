"""API views for rotations endpoints."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.rotations.api_serializers import (
    HospitalDepartmentSerializer,
    HospitalSerializer,
    RotationSummarySerializer,
)
from sims.rotations.models import Hospital, HospitalDepartment, Rotation
from sims.common_permissions import (
    CanApproveRotationOverride,
    IsPGUser,
    IsUTRMCAdminUser,
    ReadAnyWriteAdminOnly,
    ReadAnyWriteAdminOrUTRMCAdmin,
)
from sims.rotations.services import approve_rotation_override

User = get_user_model()


class HospitalViewSet(viewsets.ModelViewSet):
    """Reference-data CRUD for hospitals (authenticated read, admin/UTRMC admin write)."""

    queryset = Hospital.objects.all().order_by("name")
    serializer_class = HospitalSerializer
    permission_classes = [ReadAnyWriteAdminOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or getattr(user, "role", None) in {"admin", "utrmc_admin"}:
            return qs
        return qs.filter(is_active=True)


class HospitalDepartmentViewSet(viewsets.ModelViewSet):
    """Hospital/Department matrix governance API (UTRMC admin write)."""

    queryset = HospitalDepartment.objects.select_related("hospital", "department").order_by(
        "hospital__name",
        "department__name",
    )
    serializer_class = HospitalDepartmentSerializer
    permission_classes = [ReadAnyWriteAdminOrUTRMCAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or getattr(user, "role", None) in {"admin", "utrmc_admin"}:
            return qs
        return qs.filter(is_active=True, hospital__is_active=True, department__active=True)


class PGMyRotationsListView(APIView):
    """
    List rotations for authenticated PG user.
    
    GET /api/rotations/my/
    Returns all rotations for the authenticated PG user.
    Authentication: Required (PG role only)
    """

    permission_classes = [permissions.IsAuthenticated, IsPGUser]

    def get(self, request: Request) -> Response:
        queryset = (
            Rotation.objects.filter(pg=request.user)
            .select_related(
                "department",
                "hospital",
                "supervisor",
                "approved_by",
                "utrmc_approved_by",
                "source_department",
                "source_hospital",
                "pg__home_hospital",
                "pg__home_department",
            )
            .order_by("-start_date")
        )
        serializer = RotationSummarySerializer(queryset, many=True)
        return Response({"count": len(serializer.data), "results": serializer.data})


class PGMyRotationDetailView(APIView):
    """
    Get details of a specific rotation for authenticated PG user.
    
    GET /api/rotations/my/<id>/
    Returns a single rotation for the authenticated PG user.
    Authentication: Required (PG role only)
    """

    permission_classes = [permissions.IsAuthenticated, IsPGUser]

    def get(self, request: Request, pk: int) -> Response:
        rotation = get_object_or_404(
            Rotation.objects.select_related(
                "department",
                "hospital",
                "supervisor",
                "approved_by",
                "utrmc_approved_by",
                "source_department",
                "source_hospital",
                "pg__home_hospital",
                "pg__home_department",
            ),
            pk=pk,
            pg=request.user,
        )
        serializer = RotationSummarySerializer(rotation)
        return Response(serializer.data)


class UTRMCRotationOverrideApproveView(APIView):
    """
    PATCH /api/rotations/<id>/utrmc-approve/

    Approve a rotation override that requires UTRMC approval.
    """

    permission_classes = [permissions.IsAuthenticated, IsUTRMCAdminUser, CanApproveRotationOverride]

    def patch(self, request: Request, pk: int) -> Response:
        rotation = get_object_or_404(
            Rotation.objects.select_related(
                "pg__home_hospital",
                "pg__home_department",
                "department",
                "hospital",
            ),
            pk=pk,
        )
        if not request.data.get("override_reason") and not rotation.override_reason:
            return Response(
                {"error": "override_reason is required before approval"},
                status=400,
            )
        if request.data.get("override_reason"):
            rotation.override_reason = str(request.data["override_reason"]).strip()
            rotation.save(update_fields=["override_reason", "updated_at"])

        try:
            policy = approve_rotation_override(rotation=rotation, approver=request.user)
        except PermissionError as exc:
            raise PermissionDenied(str(exc)) from exc
        except ValueError as exc:
            return Response({"error": str(exc)}, status=400)

        rotation.refresh_from_db()
        return Response(
            {
                "id": rotation.id,
                "requires_utrmc_approval": policy.requires_utrmc_approval,
                "override_reason": rotation.override_reason,
                "utrmc_approved_by": rotation.utrmc_approved_by_id,
                "utrmc_approved_at": (
                    rotation.utrmc_approved_at.isoformat() if rotation.utrmc_approved_at else None
                ),
            }
        )
