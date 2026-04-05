from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0003_residenttrainingrecord_has_default_dates"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalresidenttrainingrecord",
            name="has_default_dates",
            field=models.BooleanField(
                default=False,
                help_text="Computed flag set when record uses default/synthetic dates.",
            ),
        ),
    ]
