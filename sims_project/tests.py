"""Tests for project middleware and utilities."""

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

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
