from __future__ import annotations

from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from sims.analytics.models import AnalyticsDailyRollup, AnalyticsEvent


class Command(BaseCommand):
    help = "Build analytics daily rollups (idempotent) for a date range."

    def add_arguments(self, parser):
        parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
        parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
        parser.add_argument(
            "--yesterday",
            action="store_true",
            help="Roll up yesterday only (default when no range is supplied).",
        )

    def handle(self, *args, **options):
        start_date, end_date = self._resolve_range(options)
        self.stdout.write(
            self.style.NOTICE(
                f"Rebuilding analytics rollups for {start_date.isoformat()} -> {end_date.isoformat()}"
            )
        )

        rows = (
            AnalyticsEvent.objects.filter(occurred_at__date__gte=start_date, occurred_at__date__lte=end_date)
            .annotate(day=TruncDate("occurred_at"))
            .values("day", "event_type", "department_id", "hospital_id")
            .annotate(total=Count("id"))
            .order_by()
        )
        rebuilt = 0
        with transaction.atomic():
            for row in rows:
                AnalyticsDailyRollup.objects.update_or_create(
                    day=row["day"],
                    event_type=row["event_type"],
                    department_id=row["department_id"],
                    hospital_id=row["hospital_id"],
                    defaults={"count": int(row["total"]), "extra": {}},
                )
                rebuilt += 1

        self.stdout.write(self.style.SUCCESS(f"Rollup rows updated: {rebuilt}"))

    def _resolve_range(self, options: dict) -> tuple[date, date]:
        if options.get("start_date") and options.get("end_date"):
            start_date = datetime.fromisoformat(options["start_date"]).date()
            end_date = datetime.fromisoformat(options["end_date"]).date()
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            return start_date, end_date
        yesterday = timezone.now().date() - timedelta(days=1)
        return yesterday, yesterday
