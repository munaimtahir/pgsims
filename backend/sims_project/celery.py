"""
Celery configuration for SIMS project.

This module sets up Celery for async task processing.
"""

import os

from celery import Celery

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")

app = Celery("sims")

# Load configuration from Django settings with CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks.
# Keep empty here because production uses django-celery-beat DatabaseScheduler.
app.conf.beat_schedule = {}


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup."""
    print(f"Request: {self.request!r}")
