"""Management command to execute scheduled reports."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from sims.reports.services import ScheduledReportRunner


class Command(BaseCommand):
    help = "Run due scheduled reports"

    def handle(self, *args, **options):
        runner = ScheduledReportRunner()
        count = runner.run_due_reports()
        self.stdout.write(self.style.SUCCESS(f"Processed {count} scheduled reports"))
