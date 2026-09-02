import logging

from django.db import migrations

logger = logging.getLogger(__name__)


def link_training_records(apps, schema_editor):
    ATR = apps.get_model("academics", "ResidentTrainingRecord")
    TTR = apps.get_model("training", "ResidentTrainingRecord")
    SupervisorReviewQueueItem = apps.get_model("academics", "SupervisorReviewQueueItem")
    EvaluationSubmission = apps.get_model("academics", "EvaluationSubmission")
    LogbookEntry = apps.get_model("academics", "LogbookEntry")

    dependents = [SupervisorReviewQueueItem, EvaluationSubmission, LogbookEntry]
    conflicts = []

    valid_training_statuses = {c[0] for c in TTR._meta.get_field("status").choices}

    for row in ATR.objects.all():
        resident_user_id = row.resident.user_id
        target = TTR.objects.filter(resident_user_id=resident_user_id).first()

        if target is not None:
            programs_set = row.program_id is not None and target.program_id is not None
            consistent = not programs_set or row.program_id == target.program_id
            if not consistent:
                conflicts.append(
                    f"academics.ResidentTrainingRecord id={row.id} resident_user_id={resident_user_id} "
                    f"program_id={row.program_id} conflicts with existing training.ResidentTrainingRecord "
                    f"id={target.id} program_id={target.program_id}; creating a separate linked record "
                    f"instead of merging."
                )
                target = None

        if target is None:
            target = TTR.objects.create(
                resident_user_id=resident_user_id,
                program_id=row.program_id,
                academic_session_id=row.academic_session_id,
                training_site_id=row.training_site_id,
                department_id=row.department_id,
                start_date=row.start_date or row.created_at.date(),
                expected_end_date=row.expected_end_date,
                status=row.status if row.status in valid_training_statuses else "ACTIVE",
                extra_data=row.extra_data or {},
                created_by_id=row.created_by_id,
                updated_by_id=row.updated_by_id,
            )

        for model in dependents:
            model.objects.filter(training_record_id=row.id).update(training_record_new_id=target.id)

    if conflicts:
        logger.warning(
            "academics->training ResidentTrainingRecord link conflicts (%d): %s",
            len(conflicts),
            "; ".join(conflicts),
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0009_add_training_record_new"),
    ]

    operations = [
        migrations.RunPython(link_training_records, noop_reverse),
    ]
