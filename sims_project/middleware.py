"""Custom middleware for performance monitoring and debugging."""

import json
import logging
import os
import time

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("sims.performance")


class HostDebugMiddleware(MiddlewareMixin):
    """
    Debug middleware to capture Host header and ALLOWED_HOSTS for Bad Request 400 diagnostics.
    """

    LOG_PATH = "/opt/sims_project/.cursor/debug.log"

    def process_request(self, request):
        host = request.META.get("HTTP_HOST", request.get_raw_host())
        # #region agent log
        try:
            payload = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "H1",
                "location": "sims_project/middleware.py:HostDebugMiddleware",
                "message": "Host header captured",
                "data": {
                    "host": host,
                    "allowed_hosts": settings.ALLOWED_HOSTS,
                    "debug": settings.DEBUG,
                },
                "timestamp": int(time.time() * 1000),
            }
            with open(self.LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
        except Exception:
            # Avoid impacting request handling if logging fails
            pass
        # #endregion


class PerformanceTimingMiddleware(MiddlewareMixin):
    """Middleware to track request/response timing for performance monitoring."""

    def process_request(self, request):
        """Mark the start time of the request."""
        request._start_time = time.perf_counter()

    def process_response(self, request, response):
        """Calculate and log request duration."""
        if hasattr(request, "_start_time"):
            duration_ms = int((time.perf_counter() - request._start_time) * 1000)
            response["X-Response-Time"] = f"{duration_ms}ms"
            
            # Log slow requests (> 1000ms)
            if duration_ms > 1000:
                logger.warning(
                    f"Slow request: {request.method} {request.path} took {duration_ms}ms",
                    extra={
                        "method": request.method,
                        "path": request.path,
                        "duration_ms": duration_ms,
                        "user": getattr(request.user, "username", "anonymous"),
                    },
                )
            else:
                logger.debug(
                    f"{request.method} {request.path} - {duration_ms}ms",
                    extra={
                        "method": request.method,
                        "path": request.path,
                        "duration_ms": duration_ms,
                    },
                )
        
        return response
