"""
Celery configuration for SIMS project.

This module sets up Celery for async task processing.
"""

import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")

app = Celery("sims")

# Load configuration from Django settings with CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    # Example: Generate daily reports at 2 AM
    "generate-daily-reports": {
        "task": "sims.reports.tasks.generate_daily_reports",
        "schedule": crontab(hour=2, minute=0),
    },
    # Example: Clean up old notifications weekly
    "cleanup-old-notifications": {
        "task": "sims.notifications.tasks.cleanup_old_notifications",
        "schedule": crontab(day_of_week=0, hour=3, minute=0),  # Sunday at 3 AM
    },
    # Example: Calculate monthly attendance summaries
    "calculate-monthly-attendance": {
        "task": "sims.attendance.tasks.calculate_monthly_summaries",
        "schedule": crontab(day_of_month=1, hour=1, minute=0),  # 1st of month at 1 AM
    },
}


@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup."""
    print(f"Request: {self.request!r}")
