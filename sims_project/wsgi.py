"""
WSGI config for sims_project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/

SIMS - Postgraduate Medical Training System
A comprehensive platform for managing postgraduate medical training,
rotations, certificates, workshops, logbooks, and clinical cases.

Created: 2025-05-29 16:22:43 UTC
Author: SMIB2012
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

# Get the WSGI application
application = get_wsgi_application()

# Production-specific WSGI configuration
if not os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true':
    # Production optimizations
    try:
        # Enable compression and static file serving optimizations
        from whitenoise import WhiteNoise
        application = WhiteNoise(application, root=BASE_DIR / 'staticfiles')
        application.add_files(BASE_DIR / 'media', prefix='/media/')
    except ImportError:
        # WhiteNoise not available, continue without it
        pass
    
    # Add application monitoring (if available)
    try:
        # Example: New Relic monitoring
        import newrelic.agent
        application = newrelic.agent.WSGIApplicationWrapper(application)
    except ImportError:
        pass
    
    try:
        # Example: Sentry error monitoring
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
        
        sentry_sdk.init(
            dsn=os.environ.get('SENTRY_DSN'),
            integrations=[DjangoIntegration()],
            traces_sample_rate=0.1,
            send_default_pii=True
        )
        application = SentryWsgiMiddleware(application)
    except ImportError:
        pass

# Health check endpoint for load balancers
def health_check_app(environ, start_response):
    """Simple health check for load balancers"""
    if environ['PATH_INFO'] == '/health/':
        status = '200 OK'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'OK']
    return None

# Wrap the main application with health check
class HealthCheckMiddleware:
    def __init__(self, application):
        self.application = application
    
    def __call__(self, environ, start_response):
        # Handle health check requests
        if environ['PATH_INFO'] == '/health/':
            status = '200 OK'
            headers = [('Content-Type', 'text/plain')]
            start_response(status, headers)
            return [b'OK']
        
        # Handle all other requests with the main application
        return self.application(environ, start_response)

# Apply health check middleware
application = HealthCheckMiddleware(application)

# Logging configuration for WSGI
import logging
logger = logging.getLogger('sims.wsgi')
logger.info('SIMS WSGI application initialized successfully')