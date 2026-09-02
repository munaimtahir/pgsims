"""Tests for attendance and eligibility API endpoints."""

import io
from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from sims.attendance.models import AttendanceRecord, Session
from sims.users.models import User


class AttendanceAPITests(TestCase):
    """Tests for attendance API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create users
        self.admin = User.objects.create_user(
            username="admin",
            password="testpass",
            role="admin",
            email="admin@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor",
            password="testpass",
            role="supervisor",
            email="supervisor@example.com",
            specialty="surgery",
        )
        self.pg = User.objects.create_user(
            username="pg1",
            password="testpass",
            role="pg",
            email="pg1@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )

        # Create sessions
        self.session1 = Session.objects.create(
            title="Clinical Rotation Day 1",
            session_type="clinical",
            date=date.today() - timedelta(days=5),
            start_time="09:00",
            end_time="17:00",
            status="completed",
        )
        self.session2 = Session.objects.create(
            title="Clinical Rotation Day 2",
            session_type="clinical",
            date=date.today() - timedelta(days=4),
            start_time="09:00",
            end_time="17:00",
            status="completed",
        )
        self.session3 = Session.objects.create(
            title="Clinical Rotation Day 3",
            session_type="clinical",
            date=date.today() - timedelta(days=3),
            start_time="09:00",
            end_time="17:00",
            status="completed",
        )

        # Create some attendance records
        AttendanceRecord.objects.create(user=self.pg, session=self.session1, status="present")
        AttendanceRecord.objects.create(user=self.pg, session=self.session2, status="present")
        # session3 not attended

        self.client = APIClient()

    def test_bulk_upload_csv_success(self):
        """Test successful CSV upload."""
        self.client.force_authenticate(self.supervisor)

        # Create CSV content
        csv_content = f"""session_id,user_id,status,remarks
{self.session3.id},{self.pg.id},present,On time
"""
        csv_file = io.BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "attendance.csv"

        url = reverse("attendance_api:upload")
        response = self.client.post(url, {"file": csv_file}, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success_count"], 1)

        # Verify record was created
        record = AttendanceRecord.objects.get(user=self.pg, session=self.session3)
        self.assertEqual(record.status, "present")

    def test_bulk_upload_pg_denied(self):
        """PG users cannot upload attendance."""
        self.client.force_authenticate(self.pg)

        csv_content = "session_id,user_id,status\n"
        csv_file = io.BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "attendance.csv"

        url = reverse("attendance_api:upload")
        response = self.client.post(url, {"file": csv_file}, format="multipart")

        self.assertEqual(response.status_code, 403)

    def test_bulk_upload_invalid_file_type(self):
        """Upload fails for non-CSV files."""
        self.client.force_authenticate(self.supervisor)

        txt_file = io.BytesIO(b"not a csv")
        txt_file.name = "data.txt"

        url = reverse("attendance_api:upload")
        response = self.client.post(url, {"file": txt_file}, format="multipart")

        self.assertEqual(response.status_code, 400)

    def test_attendance_summary_own(self):
        """PG can view their own attendance summary."""
        self.client.force_authenticate(self.pg)

        url = reverse("attendance_api:summary")
        start = (date.today() - timedelta(days=10)).isoformat()
        end = date.today().isoformat()
        response = self.client.get(url, {"start_date": start, "end_date": end, "period": "custom"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_id"], self.pg.id)
        self.assertEqual(response.data["total_sessions"], 3)
        self.assertEqual(response.data["attended_sessions"], 2)
        self.assertAlmostEqual(response.data["percentage_present"], 66.67, places=1)
        self.assertFalse(response.data["is_eligible"])  # Below 75%

    def test_attendance_summary_supervisor(self):
        """Supervisor can view assigned PG summary."""
        self.client.force_authenticate(self.supervisor)

        url = reverse("attendance_api:summary")
        start = (date.today() - timedelta(days=10)).isoformat()
        end = date.today().isoformat()
        response = self.client.get(
            url,
            {
                "user": self.pg.id,
                "start_date": start,
                "end_date": end,
                "period": "custom",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_id"], self.pg.id)

    def test_attendance_summary_admin(self):
        """Admin can view any user's summary."""
        self.client.force_authenticate(self.admin)

        url = reverse("attendance_api:summary")
        start = (date.today() - timedelta(days=10)).isoformat()
        end = date.today().isoformat()
        response = self.client.get(
            url,
            {
                "user": self.pg.id,
                "start_date": start,
                "end_date": end,
                "period": "custom",
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_attendance_summary_missing_dates(self):
        """Summary requires start_date and end_date."""
        self.client.force_authenticate(self.pg)

        url = reverse("attendance_api:summary")
        response = self.client.get(url, {"period": "custom"})

        self.assertEqual(response.status_code, 400)

    def test_eligibility_threshold(self):
        """Test eligibility calculation with threshold."""
        # Add one more present record to get 100%
        AttendanceRecord.objects.create(user=self.pg, session=self.session3, status="present")

        self.client.force_authenticate(self.pg)

        url = reverse("attendance_api:summary")
        start = (date.today() - timedelta(days=10)).isoformat()
        end = date.today().isoformat()
        response = self.client.get(url, {"start_date": start, "end_date": end, "period": "custom"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["attended_sessions"], 3)
        self.assertEqual(response.data["percentage_present"], 100.0)
        self.assertTrue(response.data["is_eligible"])  # Above 75%
