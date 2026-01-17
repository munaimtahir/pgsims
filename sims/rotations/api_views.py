"""API views for rotations endpoints."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.rotations.api_serializers import RotationSummarySerializer
from sims.rotations.models import Rotation
from sims.rotations.permissions import IsPGUser

User = get_user_model()


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
            .select_related("department", "hospital", "supervisor")
            .order_by("-start_date")
        )
        serializer = RotationSummarySerializer(queryset, many=True)
        return Response({"count": queryset.count(), "results": serializer.data})


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
            Rotation.objects.select_related("department", "hospital", "supervisor"),
            pk=pk,
            pg=request.user,
        )
        serializer = RotationSummarySerializer(rotation)
        return Response(serializer.data)
