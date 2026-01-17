"""API views for logbook supervisor verification workflow."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.logbook.models import LogbookEntry
from sims.logbook.api_serializers import (
    PGLogbookEntrySerializer,
    PGLogbookEntryWriteSerializer,
)
from sims.common_permissions import IsPGUser

User = get_user_model()


class LogbookEntryPagination(PageNumberPagination):
    """Pagination class for logbook entries."""
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class PendingLogbookEntriesView(APIView):
    """
    GET /api/logbook/pending/

    Returns logbook entries pending verification, scoped by supervisor role.
    - Supervisors see entries from their assigned PGs
    - Admins see all pending entries
    - PGs cannot access this endpoint
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user

        # Only supervisors and admins can view pending entries
        if getattr(user, "role", None) not in ["supervisor", "admin"]:
            raise PermissionDenied("Only supervisors and admins can view pending entries")

        # Build queryset based on role
        if user.is_superuser or getattr(user, "role", None) == "admin":
            queryset = LogbookEntry.objects.filter(status="pending")
        else:  # supervisor
            supervised_users = User.objects.filter(supervisor=user)
            queryset = LogbookEntry.objects.filter(status="pending", pg__in=supervised_users)

        # Select related to reduce queries
        queryset = queryset.select_related(
            "pg", "supervisor", "rotation", "rotation__department"
        ).order_by("-submitted_to_supervisor_at", "-date")

        # Serialize data
        data = []
        for entry in queryset:
            data.append(
                {
                    "id": entry.id,
                    "case_title": entry.case_title,
                    "date": entry.date.isoformat() if entry.date else None,
                    "user": {
                        "id": entry.pg.id,
                        "username": entry.pg.username,
                        "full_name": entry.pg.get_full_name(),
                    },
                    "rotation": {
                        "id": entry.rotation.id if entry.rotation else None,
                        "department": (entry.rotation.department.name if entry.rotation else None),
                    },
                    "submitted_at": (
                        entry.submitted_to_supervisor_at.isoformat()
                        if entry.submitted_to_supervisor_at
                        else None
                    ),
                    "status": entry.status,
                }
            )

        return Response({"count": len(data), "results": data})


class VerifyLogbookEntryView(APIView):
    """
    PATCH /api/logbook/<id>/verify/

    Verifies (approves) a logbook entry.
    - Sets verified_by and verified_at
    - Changes status to 'approved'
    - Triggers notification and audit event

    Request body (optional):
    {
        "feedback": "Additional supervisor feedback"
    }
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, pk: int) -> Response:
        user = request.user

        # Only supervisors and admins can verify entries
        if getattr(user, "role", None) not in ["supervisor", "admin"]:
            raise PermissionDenied("Only supervisors and admins can verify entries")

        # Get the logbook entry
        try:
            entry = LogbookEntry.objects.select_related("pg", "supervisor").get(pk=pk)
        except LogbookEntry.DoesNotExist:
            return Response({"error": "Logbook entry not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check permission - supervisors can only verify their assigned PGs
        if getattr(user, "role", None) == "supervisor":
            if entry.pg.supervisor_id != user.id:
                raise PermissionDenied("You can only verify entries from your assigned PGs")

        # Cannot verify already verified entries
        if entry.verified_by is not None:
            return Response(
                {"error": "Entry is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update entry
        entry.verified_by = user
        entry.verified_at = timezone.now()
        entry.status = "approved"
        entry.supervisor_action_at = timezone.now()

        # Add optional feedback
        feedback = request.data.get("feedback")
        if feedback:
            entry.supervisor_comments = feedback

        entry.save()

        # Create notification (if notifications app exists)
        try:
            from sims.notifications.services import create_notification

            create_notification(
                recipient=entry.pg,
                title="Logbook Entry Verified",
                body=f"Your logbook entry '{entry.case_title}' has been verified by {user.get_full_name()}.",
                notification_type="logbook_verified",
            )
        except ImportError:
            pass  # Notifications not available

        # Create audit event (if audit app exists)
        try:
            from sims.audit.services import log_action

            log_action(
                user=user,
                action="logbook_verified",
                details={
                    "entry_id": entry.id,
                    "entry_title": entry.case_title,
                    "pg_user_id": entry.pg.id,
                },
            )
        except ImportError:
            pass  # Audit not available

        return Response(
            {
                "id": entry.id,
                "case_title": entry.case_title,
                "status": entry.status,
                "verified_by": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.get_full_name(),
                },
                "verified_at": entry.verified_at.isoformat(),
                "message": "Entry verified successfully",
            }
        )


class PGLogbookEntryListCreateView(APIView):
    """
    List and create PG logbook entries.
    
    GET /api/logbook/my/
    Returns paginated list of logbook entries for the authenticated PG user.
    Authentication: Required (PG role only)
    
    POST /api/logbook/my/
    Creates a new draft logbook entry for the authenticated PG user.
    Authentication: Required (PG role only)
    """

    permission_classes = [permissions.IsAuthenticated, IsPGUser]
    pagination_class = LogbookEntryPagination

    def get(self, request: Request) -> Response:
        queryset = LogbookEntry.objects.filter(pg=request.user).order_by("-date", "-updated_at")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PGLogbookEntrySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = PGLogbookEntrySerializer(queryset, many=True)
        return Response({"count": len(serializer.data), "results": serializer.data})

    def post(self, request: Request) -> Response:
        serializer = PGLogbookEntryWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        entry = serializer.save(pg=request.user, status="draft")
        response_serializer = PGLogbookEntrySerializer(entry)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class PGLogbookEntryDetailView(APIView):
    """
    Update a PG logbook entry.
    
    PATCH /api/logbook/my/<id>/
    Updates an existing draft logbook entry for the authenticated PG user.
    Only draft entries can be edited.
    Authentication: Required (PG role only)
    """

    permission_classes = [permissions.IsAuthenticated, IsPGUser]

    def patch(self, request: Request, pk: int) -> Response:
        entry = get_object_or_404(LogbookEntry, pk=pk, pg=request.user)
        if entry.status != "draft":
            return Response(
                {"error": f'Cannot edit entry with status "{entry.status}". Only draft entries can be edited.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PGLogbookEntryWriteSerializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = PGLogbookEntrySerializer(entry)
        return Response(response_serializer.data)


class PGLogbookEntrySubmitView(APIView):
    """
    Submit a PG logbook entry for review.
    
    POST /api/logbook/my/<id>/submit/
    Submits a draft logbook entry for supervisor review.
    Changes status from 'draft' to 'pending'.
    Authentication: Required (PG role only)
    """

    permission_classes = [permissions.IsAuthenticated, IsPGUser]

    def post(self, request: Request, pk: int) -> Response:
        entry = get_object_or_404(LogbookEntry, pk=pk, pg=request.user)

        if entry.status != "draft":
            return Response(
                {"error": f'Cannot submit entry with status "{entry.status}". Only draft entries can be submitted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure that either the entry already has a supervisor or the PG user has one assigned.
        # The actual supervisor assignment is handled by the LogbookEntry model's save() method.
        if not (entry.supervisor or getattr(request.user, "supervisor", None)):
            return Response(
                {"error": "No supervisor assigned to submit this entry"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        entry.status = "pending"
        entry.save()
        response_serializer = PGLogbookEntrySerializer(entry)
        return Response(response_serializer.data)


__all__ = [
    "PendingLogbookEntriesView",
    "VerifyLogbookEntryView",
    "PGLogbookEntryListCreateView",
    "PGLogbookEntryDetailView",
    "PGLogbookEntrySubmitView",
]
