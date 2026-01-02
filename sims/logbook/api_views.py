"""API views for logbook supervisor verification workflow."""

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.logbook.models import LogbookEntry

User = get_user_model()


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


__all__ = ["PendingLogbookEntriesView", "VerifyLogbookEntryView"]
