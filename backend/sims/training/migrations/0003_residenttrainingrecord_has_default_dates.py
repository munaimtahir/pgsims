from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0002_phase6_academic_core"),
    ]

    operations = [
        migrations.AddField(
            model_name="residenttrainingrecord",
            name="has_default_dates",
            field=models.BooleanField(
                default=False,
                help_text="Computed flag set when record uses default/synthetic dates.",
            ),
        ),
    ]
