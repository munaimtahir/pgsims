"""
Management command: recompute_eligibility

Recomputes all ResidentMilestoneEligibility rows for all active training records.
Safe to run repeatedly (idempotent). Intended as a nightly backstop.

Usage:
    python manage.py recompute_eligibility
    python manage.py recompute_eligibility --rtr-id 42   # single record
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Recompute milestone eligibility snapshots for all active training records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--rtr-id",
            type=int,
            default=None,
            help="If provided, only recompute for the given ResidentTrainingRecord ID.",
        )

    def handle(self, *args, **options):
        from sims.training.models import ResidentTrainingRecord
        from sims.training.eligibility import recompute_for_record

        rtr_id = options.get("rtr_id")

        if rtr_id:
            qs = ResidentTrainingRecord.objects.filter(pk=rtr_id, active=True)
        else:
            qs = ResidentTrainingRecord.objects.filter(active=True).select_related("program")

        total = qs.count()
        self.stdout.write(f"Recomputing eligibility for {total} record(s)…")

        success = 0
        errors = 0
        for rtr in qs.iterator():
            try:
                results = recompute_for_record(rtr)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ RTR {rtr.pk} ({rtr}) — {len(results)} milestone(s) updated"
                    )
                )
                success += 1
            except Exception as exc:
                self.stderr.write(
                    self.style.ERROR(f"  ✗ RTR {rtr.pk} ({rtr}) — ERROR: {exc}")
                )
                errors += 1

        self.stdout.write(
            self.style.SUCCESS(f"\nDone. Success={success}  Errors={errors}")
        )
