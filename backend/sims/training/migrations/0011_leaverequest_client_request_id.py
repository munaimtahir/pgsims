from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("training", "0010_add_actual_end_date")]

    operations = [
        migrations.AddField(
            model_name="leaverequest",
            name="client_request_id",
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="historicalleaverequest",
            name="client_request_id",
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
    ]
