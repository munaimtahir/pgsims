"""API views for attendance and eligibility management."""

from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import calculate_attendance_summary, process_csv_upload

User = get_user_model()


class BulkAttendanceUploadView(APIView):
    """
    POST /api/attendance/upload/

    Bulk CSV upload for attendance records.

    Requires supervisor or admin role.
    Accepts CSV file with columns: session_id,user_id,status,check_in_time,remarks
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request: Request) -> Response:
        user = request.user

        # Only supervisors and admins can upload attendance
        if getattr(user, "role", None) not in ["supervisor", "admin"]:
            raise PermissionDenied("Only supervisors and admins can upload attendance")

        # Get uploaded file
        if "file" not in request.FILES:
            raise ValidationError({"file": "CSV file is required"})

        csv_file = request.FILES["file"]

        # Validate file type
        if not csv_file.name.endswith(".csv"):
            raise ValidationError({"file": "File must be a CSV file"})

        # Process the CSV
        result = process_csv_upload(csv_file, user)

        # Create audit event
        try:
            from sims.audit.services import log_action

            log_action(
                user=user,
                action="bulk_attendance_upload",
                details={
                    "filename": csv_file.name,
                    "success_count": result["success_count"],
                    "error_count": result["error_count"],
                },
            )
        except ImportError:
            pass

        if result["success"]:
            return Response(
                {
                    "message": f"Successfully uploaded {result['success_count']} attendance records",
                    "success_count": result["success_count"],
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "message": "Upload completed with errors",
                    "success_count": result["success_count"],
                    "error_count": result["error_count"],
                    "errors": result["errors"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class AttendanceSummaryView(APIView):
    """
    GET /api/attendance/summary/

    Get attendance summary for a user over a date range.

    Query parameters:
    - user: user ID (optional for admins/supervisors, defaults to self)
    - period: 'monthly', 'quarterly', 'semester', 'yearly', or 'custom'
    - start_date: YYYY-MM-DD (required for custom period)
    - end_date: YYYY-MM-DD (required for custom period)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        acting_user = request.user

        # Get target user
        user_id = request.query_params.get("user")
        if user_id:
            try:
                target_user = User.objects.get(pk=int(user_id))
            except (User.DoesNotExist, ValueError):
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check permission
            if getattr(acting_user, "role", None) == "supervisor":
                if target_user.supervisor_id != acting_user.id:
                    raise PermissionDenied("You can only view summaries for your assigned PGs")
            elif getattr(acting_user, "role", None) not in ["admin"]:
                if target_user.id != acting_user.id:
                    raise PermissionDenied("You can only view your own summary")
        else:
            target_user = acting_user

        # Get period and date range
        period = request.query_params.get("period", "custom")
        valid_periods = ["monthly", "quarterly", "semester", "yearly", "custom"]
        if period not in valid_periods:
            raise ValidationError({"period": f"Period must be one of: {', '.join(valid_periods)}"})

        # Parse dates
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            raise ValidationError({"date_range": "Both start_date and end_date are required"})

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError({"date_format": "Dates must be in YYYY-MM-DD format"})

        if start_date > end_date:
            raise ValidationError({"date_range": "start_date must be before end_date"})

        # Calculate summary
        summary = calculate_attendance_summary(target_user, start_date, end_date, period)

        return Response(summary)


__all__ = ["BulkAttendanceUploadView", "AttendanceSummaryView"]
