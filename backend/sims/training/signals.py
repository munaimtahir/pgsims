"""
Django signals for the training app.

Triggers eligibility recomputation whenever research project,
thesis, or workshop completion records change.
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _recompute_if_record_active(rtr):
    if rtr is None:
        return
    try:
        from sims.training.eligibility import recompute_for_record
        recompute_for_record(rtr)
    except Exception as exc:
        logger.warning("Eligibility recompute failed for rtr=%s: %s", rtr, exc)


@receiver(post_save, sender="training.ResidentResearchProject")
def on_research_project_save(sender, instance, **kwargs):
    _recompute_if_record_active(instance.resident_training_record)


@receiver(post_save, sender="training.ResidentThesis")
def on_thesis_save(sender, instance, **kwargs):
    _recompute_if_record_active(instance.resident_training_record)


@receiver(post_save, sender="training.ResidentWorkshopCompletion")
def on_workshop_completion_save(sender, instance, **kwargs):
    _recompute_if_record_active(instance.resident_training_record)
