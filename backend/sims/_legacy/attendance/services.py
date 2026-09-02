"""Services for attendance processing and eligibility calculation."""

import csv
import io
import os
from datetime import datetime
from typing import Dict

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import AttendanceRecord, EligibilitySummary, Session

User = get_user_model()


def get_attendance_threshold() -> float:
    """Get attendance threshold from environment or default to 75%."""
    return float(os.environ.get("ATTENDANCE_THRESHOLD", "75.0"))


def process_csv_upload(csv_file, uploaded_by) -> Dict:
    """
    Process CSV file for bulk attendance upload.

    Expected CSV format:
    session_id,user_id,status,check_in_time,remarks

    Returns dict with success count, error count, and error messages.
    """
    errors = []
    success_count = 0

    try:
        # Read CSV content
        content = csv_file.read().decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(content))

        # Validate headers
        required_headers = {"session_id", "user_id", "status"}
        if not required_headers.issubset(set(csv_reader.fieldnames)):
            return {
                "success": False,
                "success_count": 0,
                "error_count": 1,
                "errors": [f"CSV must contain columns: {', '.join(required_headers)}"],
            }

        with transaction.atomic():
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (header is 1)
                try:
                    # Get session
                    session = Session.objects.get(pk=int(row["session_id"]))

                    # Get user
                    user = User.objects.get(pk=int(row["user_id"]))

                    # Validate status
                    status = row["status"].strip().lower()
                    valid_statuses = ["present", "absent", "late", "excused"]
                    if status not in valid_statuses:
                        errors.append(
                            f"Row {row_num}: Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                        )
                        continue

                    # Parse check-in time if provided
                    check_in_time = None
                    if row.get("check_in_time"):
                        try:
                            check_in_time = datetime.fromisoformat(row["check_in_time"])
                        except ValueError:
                            errors.append(
                                f"Row {row_num}: Invalid check_in_time format. Use ISO format (YYYY-MM-DD HH:MM:SS)"
                            )
                            continue

                    # Create or update attendance record
                    record, created = AttendanceRecord.objects.update_or_create(
                        user=user,
                        session=session,
                        defaults={
                            "status": status,
                            "check_in_time": check_in_time,
                            "remarks": row.get("remarks", ""),
                            "recorded_by": uploaded_by,
                        },
                    )
                    success_count += 1

                except Session.DoesNotExist:
                    errors.append(f"Row {row_num}: Session with ID {row['session_id']} not found")
                except User.DoesNotExist:
                    errors.append(f"Row {row_num}: User with ID {row['user_id']} not found")
                except ValueError as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                except Exception as e:
                    errors.append(f"Row {row_num}: Unexpected error - {str(e)}")

    except Exception as e:
        return {
            "success": False,
            "success_count": 0,
            "error_count": 1,
            "errors": [f"Failed to parse CSV file: {str(e)}"],
        }

    return {
        "success": len(errors) == 0,
        "success_count": success_count,
        "error_count": len(errors),
        "errors": errors,
    }


def calculate_attendance_summary(user, start_date, end_date, period="custom") -> Dict:
    """
    Calculate attendance summary for a user over a date range.

    Returns dict with attendance statistics and eligibility status.
    """
    # Get sessions in the date range
    sessions = Session.objects.filter(
        date__gte=start_date, date__lte=end_date, status__in=["completed", "ongoing"]
    )

    total_sessions = sessions.count()

    # Get attendance records for the user
    attendance_records = AttendanceRecord.objects.filter(user=user, session__in=sessions)

    # Count attended (present or late)
    attended = attendance_records.filter(status__in=["present", "late"]).count()

    # Count by status
    present_count = attendance_records.filter(status="present").count()
    late_count = attendance_records.filter(status="late").count()
    absent_count = attendance_records.filter(status="absent").count()
    excused_count = attendance_records.filter(status="excused").count()

    # Calculate percentage
    if total_sessions > 0:
        percentage_present = round((attended / total_sessions) * 100, 2)
    else:
        percentage_present = 0.0

    # Check eligibility
    threshold = get_attendance_threshold()
    is_eligible = percentage_present >= threshold

    # Create or update eligibility summary
    summary, created = EligibilitySummary.objects.update_or_create(
        user=user,
        period=period,
        start_date=start_date,
        end_date=end_date,
        defaults={
            "total_sessions": total_sessions,
            "attended_sessions": attended,
            "percentage_present": percentage_present,
            "is_eligible": is_eligible,
            "threshold_percentage": threshold,
        },
    )

    return {
        "user_id": user.id,
        "username": user.username,
        "full_name": user.get_full_name(),
        "period": period,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_sessions": total_sessions,
        "attended_sessions": attended,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "excused_count": excused_count,
        "percentage_present": percentage_present,
        "threshold_percentage": threshold,
        "is_eligible": is_eligible,
    }
