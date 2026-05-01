from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from unittest.mock import patch
from sims.users.decorators import (
    admin_required, supervisor_required, pg_required,
    supervisor_or_admin_required
)

User = get_user_model()

@admin_required
def mock_admin_view(request):
    return HttpResponse("OK")

@supervisor_required
def mock_supervisor_view(request):
    return HttpResponse("OK")

@pg_required
def mock_pg_view(request):
    return HttpResponse("OK")

@supervisor_or_admin_required
def mock_supervisor_or_admin_view(request):
    return HttpResponse("OK")

class DecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.pg = User.objects.create_user(username="pg", role="pg")
        self.supervisor = User.objects.create_user(username="sup", role="supervisor")
        self.admin = User.objects.create_user(username="admin", role="admin")

    @patch("django.contrib.messages.error")
    def test_admin_required(self, mock_msg):
        request = self.factory.get("/")
        request.user = self.admin
        self.assertEqual(mock_admin_view(request).status_code, 200)

        request.user = self.pg
        with self.assertRaises(PermissionDenied):
            mock_admin_view(request)
        self.assertTrue(mock_msg.called)

    @patch("django.contrib.messages.error")
    def test_supervisor_required(self, mock_msg):
        request = self.factory.get("/")
        request.user = self.supervisor
        self.assertEqual(mock_supervisor_view(request).status_code, 200)

        request.user = self.pg
        with self.assertRaises(PermissionDenied):
            mock_supervisor_view(request)
        self.assertTrue(mock_msg.called)

    @patch("django.contrib.messages.error")
    def test_pg_required(self, mock_msg):
        request = self.factory.get("/")
        request.user = self.pg
        self.assertEqual(mock_pg_view(request).status_code, 200)

        request.user = self.admin
        with self.assertRaises(PermissionDenied):
            mock_pg_view(request)
        self.assertTrue(mock_msg.called)

    @patch("django.contrib.messages.error")
    def test_supervisor_or_admin_required(self, mock_msg):
        request = self.factory.get("/")
        request.user = self.supervisor
        self.assertEqual(mock_supervisor_or_admin_view(request).status_code, 200)

        request.user = self.admin
        self.assertEqual(mock_supervisor_or_admin_view(request).status_code, 200)

        request.user = self.pg
        with self.assertRaises(PermissionDenied):
            mock_supervisor_or_admin_view(request)
        self.assertTrue(mock_msg.called)
