"""API views for executing bulk operations."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.bulk.models import BulkOperation
from sims.bulk.serializers import (
    BulkAssignmentSerializer,
    BulkImportSerializer,
    BulkReviewSerializer,
)
from sims.bulk.services import BulkService

User = get_user_model()


def _operation_payload(operation: BulkOperation) -> dict:
    return {
        "operation": operation.operation,
        "status": operation.status,
        "success_count": operation.success_count,
        "failure_count": operation.failure_count,
        "details": operation.details,
        "created_at": operation.created_at,
        "completed_at": operation.completed_at,
    }


class BulkReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = BulkReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = BulkService(request.user)
        operation = service.review_entries(**serializer.validated_data)
        return Response(_operation_payload(operation), status=status.HTTP_200_OK)


class BulkAssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = BulkAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        supervisor = get_object_or_404(
            User.objects.filter(role="supervisor"),
            pk=serializer.validated_data["supervisor_id"],
        )
        service = BulkService(request.user)
        operation = service.assign_supervisor(
            entry_ids=serializer.validated_data["entry_ids"], supervisor=supervisor
        )
        return Response(_operation_payload(operation), status=status.HTTP_200_OK)


class BulkImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        from django.core.exceptions import ValidationError as DjangoValidationError

        serializer = BulkImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        service = BulkService(request.user)

        try:
            operation = service.import_logbook_entries(
                uploaded_file,
                dry_run=serializer.validated_data["dry_run"],
                allow_partial=serializer.validated_data["allow_partial"],
            )
        except DjangoValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(_operation_payload(operation), status=status_code)


__all__ = ["BulkReviewView", "BulkAssignmentView", "BulkImportView"]
