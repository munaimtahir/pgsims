from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0010_link_training_record_new"),
    ]

    operations = [
        # Drop the old FKs pointing at academics.ResidentTrainingRecord.
        migrations.RemoveField(model_name="supervisorreviewqueueitem", name="training_record"),
        migrations.RemoveField(model_name="historicalsupervisorreviewqueueitem", name="training_record"),
        migrations.RemoveField(model_name="evaluationsubmission", name="training_record"),
        migrations.RemoveField(model_name="historicalevaluationsubmission", name="training_record"),
        migrations.RemoveField(model_name="logbookentry", name="training_record"),
        migrations.RemoveField(model_name="historicallogbookentry", name="training_record"),
        # Rename the new FKs (pointing at training.ResidentTrainingRecord) into place.
        migrations.RenameField(
            model_name="supervisorreviewqueueitem", old_name="training_record_new", new_name="training_record"
        ),
        migrations.RenameField(
            model_name="historicalsupervisorreviewqueueitem",
            old_name="training_record_new",
            new_name="training_record",
        ),
        migrations.RenameField(
            model_name="evaluationsubmission", old_name="training_record_new", new_name="training_record"
        ),
        migrations.RenameField(
            model_name="historicalevaluationsubmission",
            old_name="training_record_new",
            new_name="training_record",
        ),
        migrations.RenameField(
            model_name="logbookentry", old_name="training_record_new", new_name="training_record"
        ),
        migrations.RenameField(
            model_name="historicallogbookentry", old_name="training_record_new", new_name="training_record"
        ),
    ]
