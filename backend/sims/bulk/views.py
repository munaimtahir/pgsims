"""API views for executing bulk operations."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.http import HttpResponse
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
    DepartmentImportSerializer,
    ResidentImportSerializer,
    SupervisorImportSerializer,
    TraineeImportSerializer,
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


def _track_bulk_event(request, *, event_type, resource, operation=None, error_code=None):
    pass  # analytics module removed


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
        _track_bulk_event(request, event_type="data.import.started", resource="logbook")

        try:
            operation = service.import_logbook_entries(
                uploaded_file,
                dry_run=serializer.validated_data["dry_run"],
                allow_partial=serializer.validated_data["allow_partial"],
            )
        except DjangoValidationError as e:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="logbook",
                error_code="validation_error",
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if operation.status == BulkOperation.STATUS_COMPLETED:
            _track_bulk_event(
                request,
                event_type="data.import.completed",
                resource="logbook",
                operation=operation,
            )
        else:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="logbook",
                operation=operation,
                error_code="operation_failed",
            )

        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(_operation_payload(operation), status=status_code)


class BulkTraineeImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        from django.core.exceptions import ValidationError as DjangoValidationError

        serializer = TraineeImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        service = BulkService(request.user)
        _track_bulk_event(request, event_type="data.import.started", resource="trainees")

        try:
            operation = service.import_trainees(
                uploaded_file,
                dry_run=serializer.validated_data["dry_run"],
                allow_partial=serializer.validated_data["allow_partial"],
            )
        except DjangoValidationError as e:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="trainees",
                error_code="validation_error",
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if operation.status == BulkOperation.STATUS_COMPLETED:
            _track_bulk_event(
                request,
                event_type="data.import.completed",
                resource="trainees",
                operation=operation,
            )
        else:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="trainees",
                operation=operation,
                error_code="operation_failed",
            )

        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(_operation_payload(operation), status=status_code)


class BulkSupervisorImportView(APIView):
    """
    Bulk import view for supervisors/faculty.

    Accepts CSV or Excel files with supervisor data.
    Creates accounts with role 'supervisor' and generates passwords.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        from django.core.exceptions import ValidationError as DjangoValidationError

        serializer = SupervisorImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        service = BulkService(request.user)
        _track_bulk_event(request, event_type="data.import.started", resource="supervisors")

        try:
            operation = service.import_supervisors(
                uploaded_file,
                dry_run=serializer.validated_data["dry_run"],
                allow_partial=serializer.validated_data["allow_partial"],
                generate_passwords=serializer.validated_data.get("generate_passwords", True),
            )
        except DjangoValidationError as e:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="supervisors",
                error_code="validation_error",
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if operation.status == BulkOperation.STATUS_COMPLETED:
            _track_bulk_event(
                request,
                event_type="data.import.completed",
                resource="supervisors",
                operation=operation,
            )
        else:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="supervisors",
                operation=operation,
                error_code="operation_failed",
            )

        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(_operation_payload(operation), status=status_code)


class BulkResidentImportView(APIView):
    """
    Bulk import view for residents/postgraduates.

    Accepts CSV or Excel files with resident data.
    Creates accounts with role 'pg' and links to supervisors.
    Handles cases where supervisors don't exist (based on allow_partial setting).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        from django.core.exceptions import ValidationError as DjangoValidationError

        serializer = ResidentImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        service = BulkService(request.user)
        _track_bulk_event(request, event_type="data.import.started", resource="residents")

        try:
            operation = service.import_residents(
                uploaded_file,
                dry_run=serializer.validated_data["dry_run"],
                allow_partial=serializer.validated_data["allow_partial"],
                generate_passwords=serializer.validated_data.get("generate_passwords", True),
            )
        except DjangoValidationError as e:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="residents",
                error_code="validation_error",
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if operation.status == BulkOperation.STATUS_COMPLETED:
            _track_bulk_event(
                request,
                event_type="data.import.completed",
                resource="residents",
                operation=operation,
            )
        else:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="residents",
                operation=operation,
                error_code="operation_failed",
            )

        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(_operation_payload(operation), status=status_code)


class BulkDepartmentImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        if getattr(request.user, "role", None) != "admin":
            return Response({"detail": "Only admins can import departments."}, status=403)

        serializer = DepartmentImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = BulkService(request.user)
        _track_bulk_event(request, event_type="data.import.started", resource="departments")
        operation = service.import_departments(
            serializer.validated_data["file"],
            dry_run=serializer.validated_data["dry_run"],
            allow_partial=serializer.validated_data["allow_partial"],
        )
        if operation.status == BulkOperation.STATUS_COMPLETED:
            _track_bulk_event(
                request,
                event_type="data.import.completed",
                resource="departments",
                operation=operation,
            )
        else:
            _track_bulk_event(
                request,
                event_type="data.import.failed",
                resource="departments",
                operation=operation,
                error_code="operation_failed",
            )
        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(_operation_payload(operation), status=status_code)


class BulkExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, resource: str) -> HttpResponse:
        from django.core.exceptions import ValidationError as DjangoValidationError

        if getattr(request.user, "role", None) not in {"admin", "utrmc_admin"}:
            return Response({"detail": "Only admins can export bulk datasets."}, status=403)
        export_format = request.query_params.get("file_format", "xlsx").lower()
        service = BulkService(request.user)
        _track_bulk_event(request, event_type="data.export.started", resource=resource)
        try:
            export_file = service.export_dataset(resource=resource, export_format=export_format)
        except DjangoValidationError as exc:
            _track_bulk_event(
                request,
                event_type="data.export.failed",
                resource=resource,
                error_code="validation_error",
            )
            return Response({"detail": str(exc)}, status=400)
        _track_bulk_event(request, event_type="data.export.completed", resource=resource)
        response = HttpResponse(export_file.content, content_type=export_file.content_type)
        response["Content-Disposition"] = f'attachment; filename="{export_file.filename}"'
        return response


# ---------------------------------------------------------------------------
# NEW unified import endpoint: /api/bulk/import/<entity>/<action>/
# action = "dry-run" | "apply"
# entity = hospitals | matrix | supervision-links | departments | supervisors | residents | trainees

_ENTITY_METHOD_MAP = {
    "hospitals": "import_hospitals",
    "matrix": "import_hospital_departments",
    "supervision-links": "import_supervision_links",
    "departments": "import_departments",
    "supervisors": "import_supervisors",
    "residents": "import_residents",
    "trainees": "import_trainees",
    # Training module
    "training-programs": "import_training_programs",
    "rotation-templates": "import_rotation_templates",
    "resident-training-records": "import_resident_training_records",
}

_ALLOWED_ROLES = {"admin", "utrmc_admin"}


class BulkImportEntityView(APIView):
    """Unified import endpoint.

    POST /api/bulk/import/<entity>/dry-run/   — validate only
    POST /api/bulk/import/<entity>/apply/     — write to DB
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, entity: str, action: str) -> Response:
        from django.core.exceptions import ValidationError as DjangoValidationError

        if getattr(request.user, "role", None) not in _ALLOWED_ROLES:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        if action not in {"dry-run", "apply"}:
            return Response({"detail": "action must be 'dry-run' or 'apply'."}, status=status.HTTP_400_BAD_REQUEST)

        method_name = _ENTITY_METHOD_MAP.get(entity)
        if not method_name:
            return Response({"detail": f"Unknown entity '{entity}'."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        dry_run = (action == "dry-run")
        try:
            service = BulkService(request.user)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        _track_bulk_event(request, event_type="data.import.started", resource=entity)
        try:
            operation = getattr(service, method_name)(
                uploaded_file,
                dry_run=dry_run,
                allow_partial=True,
            )
        except DjangoValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        payload = _operation_payload(operation)
        payload["dry_run"] = dry_run
        status_code = (
            status.HTTP_200_OK
            if operation.status == BulkOperation.STATUS_COMPLETED
            else status.HTTP_400_BAD_REQUEST
        )
        return Response(payload, status=status_code)


__all__ = [
    "BulkReviewView",
    "BulkAssignmentView",
    "BulkImportView",
    "BulkTraineeImportView",
    "BulkSupervisorImportView",
    "BulkResidentImportView",
    "BulkDepartmentImportView",
    "BulkExportView",
    "BulkImportEntityView",
]
