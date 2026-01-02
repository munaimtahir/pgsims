"""Health check views for monitoring and observability."""

import logging

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)


@never_cache
@require_GET
def healthz(request):
    """
    Comprehensive health check endpoint.
    
    Checks:
    - Database connectivity
    - Cache connectivity (Redis)
    - Basic application status
    
    Returns:
    - 200 OK if all checks pass
    - 503 Service Unavailable if any check fails
    """
    health_status = {
        "status": "healthy",
        "checks": {},
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check cache
    try:
        cache_key = "healthz_test"
        cache.set(cache_key, "test_value", 10)
        if cache.get(cache_key) == "test_value":
            health_status["checks"]["cache"] = "ok"
        else:
            health_status["checks"]["cache"] = "error: cache read/write failed"
            health_status["status"] = "unhealthy"
        cache.delete(cache_key)
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        health_status["checks"]["cache"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Celery check (optional, basic ping)
    try:
        from celery import current_app
        
        # Try to get Celery stats with a short timeout
        stats = current_app.control.inspect(timeout=1.0).stats()
        if stats:
            health_status["checks"]["celery"] = "ok"
        else:
            health_status["checks"]["celery"] = "warning: no workers found"
    except Exception as e:
        logger.warning(f"Celery health check failed (may be expected if not running): {e}")
        health_status["checks"]["celery"] = "not available"
    
    # Return appropriate status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return JsonResponse(health_status, status=status_code)


@never_cache
@require_GET
def readiness(request):
    """
    Readiness probe for Kubernetes/container orchestration.
    Similar to healthz but may have different criteria.
    """
    return healthz(request)


@never_cache
@require_GET
def liveness(request):
    """
    Liveness probe for Kubernetes/container orchestration.
    Returns 200 as long as the application is running.
    """
    return JsonResponse({"status": "alive"})
