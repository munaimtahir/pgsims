from django.test import TestCase
from django.contrib.auth import get_user_model
from sims.notifications.services import NotificationService
from sims.notifications.models import Notification, NotificationPreference
from unittest.mock import patch, MagicMock

User = get_user_model()

class NotificationServicesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="notify_user", email="test@example.com")
        self.actor = User.objects.create_user(username="actor_user")
        self.service = NotificationService(actor=self.actor)

    @patch("sims.notifications.services.render_to_string")
    def test_send_in_app_success(self, mock_render):
        mock_render.return_value = "Notification body content"
        
        results = list(self.service.send(
            recipient=self.user,
            verb="test_verb",
            title="Test Title",
            template="test_template",
            channels=[Notification.CHANNEL_IN_APP]
        ))
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].delivered)
        
        notification = Notification.objects.last()
        self.assertEqual(notification.recipient, self.user)
        self.assertEqual(notification.actor, self.actor)
        self.assertEqual(notification.title, "Test Title")
        self.assertEqual(notification.body, "Notification body content")

    @patch("sims.notifications.services.EmailMultiAlternatives")
    @patch("sims.notifications.services.render_to_string")
    def test_send_email_success(self, mock_render, mock_email_class):
        mock_render.return_value = "Email content"
        mock_email = MagicMock()
        mock_email_class.return_value = mock_email
        
        results = list(self.service.send(
            recipient=self.user,
            verb="test_email",
            title="Email Subject",
            template="email_template",
            channels=[Notification.CHANNEL_EMAIL]
        ))
        
        self.assertTrue(results[0].delivered)
        mock_email.send.assert_called_once()

    def test_send_disabled_channel(self):
        pref = NotificationPreference.for_user(self.user)
        pref.email_enabled = False
        pref.save()
        
        results = list(self.service.send(
            recipient=self.user,
            verb="test",
            title="T",
            template="t",
            channels=[Notification.CHANNEL_EMAIL]
        ))
        
        self.assertFalse(results[0].delivered)
        self.assertEqual(results[0].error, "channel-disabled")

    def test_serialise_metadata(self):
        context = {
            "str": "val",
            "int": 123,
            "obj": self.user,
            "date": timezone.now()
        }
        # Accessing private method for coverage
        serialised = self.service._serialise_metadata(context)
        
        self.assertEqual(serialised["str"], "val")
        self.assertEqual(serialised["int"], 123)
        self.assertEqual(serialised["obj_id"], self.user.pk)
        self.assertIsInstance(serialised["date"], str)

    @patch("sims.notifications.services.NotificationService.send")
    def test_upcoming_rotation_deadlines(self, mock_send):
        from sims.training.models import TrainingProgram, ResidentTrainingRecord, RotationAssignment
        from sims.rotations.models import Hospital, HospitalDepartment
        from sims.academics.models import Department
        from datetime import date, timedelta
        
        program = TrainingProgram.objects.create(name="P", code="P", duration_months=12)
        rtr = ResidentTrainingRecord.objects.create(resident_user=self.user, program=program, start_date=date.today())
        hospital = Hospital.objects.create(name="H", code="H")
        dept = Department.objects.create(name="D", code="D")
        hdept = HospitalDepartment.objects.create(hospital=hospital, department=dept)
        
        # Ending in 2 days
        rotation = RotationAssignment.objects.create(
            resident_training=rtr,
            hospital_department=hdept,
            start_date=date.today() - timedelta(days=20),
            end_date=date.today() + timedelta(days=2),
            status=RotationAssignment.STATUS_ACTIVE
        )
        
        count = self.service.upcoming_rotation_deadlines(days=3)
        self.assertEqual(count, 1)
        mock_send.assert_called_once()
        
from django.utils import timezone
