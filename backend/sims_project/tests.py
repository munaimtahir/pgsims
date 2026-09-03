"""Tests for project middleware and utilities."""

import importlib
import os
from io import BytesIO
from unittest import mock
from wsgiref.util import setup_testing_defaults

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework.test import APIClient
import yaml

from .middleware import PerformanceTimingMiddleware

User = get_user_model()


class PerformanceTimingMiddlewareTests(TestCase):
    """Test performance timing middleware."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.middleware = PerformanceTimingMiddleware(lambda r: self._get_response(r))
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            role="admin",
            email="test@test.com",
        )

    def _get_response(self, request):
        """Mock response."""
        from django.http import HttpResponse
        return HttpResponse("OK")

    def test_middleware_adds_timing_header(self):
        """Test that middleware adds X-Response-Time header."""
        request = self.factory.get("/test/")
        request.user = self.user
        
        response = self.middleware(request)
        
        self.assertIn("X-Response-Time", response)
        self.assertTrue(response["X-Response-Time"].endswith("ms"))

    def test_middleware_handles_anonymous_user(self):
        """Test middleware with anonymous user."""
        from django.contrib.auth.models import AnonymousUser
        
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        
        response = self.middleware(request)
        
        self.assertIn("X-Response-Time", response)

    def test_middleware_tracks_post_requests(self):
        """Test middleware with POST request."""
        request = self.factory.post("/test/")
        request.user = self.user

        response = self.middleware(request)

        self.assertIn("X-Response-Time", response)


class OpenAPISchemaGateTests(TestCase):
    """Schema generation must remain wired for the production gate."""

    def setUp(self):
        self.client = APIClient()

    def test_schema_endpoint_returns_openapi_document(self):
        response = self.client.get(reverse("schema"))

        self.assertEqual(response.status_code, 200)
        payload = yaml.safe_load(response.content)
        self.assertEqual(payload["info"]["title"], "PGSIMS API")
        self.assertIn("openapi", payload)
        self.assertIn("/api/auth/login/", payload["paths"])
        self.assertIn("/api/dashboard/resident/", payload["paths"])


class WsgiMediaExposureTests(TestCase):
    """Regression: the production WSGI stack must never serve MEDIA_ROOT unauthenticated.

    sims_project/wsgi.py previously called WhiteNoise's application.add_files() on the
    media directory when running with production settings, which would serve every
    resident document, thesis, synopsis, and workshop certificate straight from the WSGI
    layer with zero authentication - bypassing Django's URL routing (and therefore
    ResidentDocumentViewSet's ownership/role checks) entirely. Protected files must only
    ever be reachable through their authenticated viewset actions.
    """

    def _build_environ(self, path):
        environ = {}
        setup_testing_defaults(environ)
        environ["PATH_INFO"] = path
        environ["REQUEST_METHOD"] = "GET"
        environ["wsgi.input"] = BytesIO(b"")
        return environ

    def _call_wsgi_app(self, application, path):
        environ = self._build_environ(path)
        captured = {}

        def start_response(status, headers, exc_info=None):
            captured["status"] = status
            captured["headers"] = headers

        body = b"".join(application(environ, start_response))
        return captured["status"], body

    def test_production_wsgi_app_never_registers_media_with_whitenoise(self):
        probe_dir = os.path.join(settings.MEDIA_ROOT, "resident_documents")
        os.makedirs(probe_dir, exist_ok=True)
        probe_path = os.path.join(probe_dir, "__wsgi_media_exposure_probe__.txt")
        with open(probe_path, "wb") as fh:
            fh.write(b"should never be publicly servable")

        try:
            with mock.patch.dict(os.environ, {"DEBUG": "False"}):
                wsgi_module = importlib.import_module("sims_project.wsgi")
                importlib.reload(wsgi_module)
                try:
                    application = wsgi_module.application

                    find_file = getattr(application, "find_file", None)
                    if find_file is not None:
                        self.assertIsNone(
                            find_file("/media/resident_documents/__wsgi_media_exposure_probe__.txt"),
                            "WhiteNoise must not have media/ registered - it would serve "
                            "protected resident documents unauthenticated.",
                        )

                    status, body = self._call_wsgi_app(
                        application, "/media/resident_documents/__wsgi_media_exposure_probe__.txt"
                    )
                    self.assertFalse(status.startswith("200"))
                    self.assertNotIn(b"should never be publicly servable", body)
                finally:
                    # Restore a dev-settings wsgi.application for any later importers.
                    importlib.reload(wsgi_module)
        finally:
            os.remove(probe_path)
