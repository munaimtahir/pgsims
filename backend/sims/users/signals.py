"""User bootstrap signals.

The clean pilot baseline recreates minimal PG/resident accounts by role. Those
accounts need a canonical active training record so resident dashboards and
resident-scoped workflows remain usable without frontend fallbacks.
"""

from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from sims.training.models import ResidentTrainingRecord, TrainingProgram
from .models import User


BASELINE_PROGRAM_CODE = "PILOT-BASELINE"


@receiver(post_save, sender=User)
def ensure_pilot_training_baseline(sender, instance: User, created: bool, **kwargs):
    """Create a deterministic baseline training record for pilot PG/resident users.

    This is intentionally narrow: it only applies to the committed pilot baseline
    usernames used by the runtime reset flow. Regular application users and tests
    are unaffected.
    """

    if not instance.username.startswith("pilot_"):
        return
    if getattr(instance, "role", None) not in {"pg", "resident"}:
        return

    def _bootstrap():
        program, _ = TrainingProgram.objects.get_or_create(
            code=BASELINE_PROGRAM_CODE,
            defaults={
                "name": "Pilot Baseline Program",
                "duration_months": 48,
                "description": "Synthetic program used for clean baseline resident bootstrapping.",
                "degree_type": TrainingProgram.DEGREE_FCPS,
                "notes": "Managed automatically for pilot baseline users.",
                "active": True,
            },
        )
        ResidentTrainingRecord.objects.get_or_create(
            resident_user=instance,
            program=program,
            defaults={
                "start_date": timezone.now().date() - timedelta(days=120),
                "expected_end_date": timezone.now().date() + timedelta(days=48 * 30),
                "current_level": instance.year or "y1",
                "status": ResidentTrainingRecord.STATUS_ACTIVE,
                "locked_program": True,
                "restart_from_scratch_on_change": True,
                "active": True,
                "has_default_dates": True,
                "created_by": instance,
            },
        )

    _bootstrap()
