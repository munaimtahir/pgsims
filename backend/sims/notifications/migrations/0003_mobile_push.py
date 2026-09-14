from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("notifications", "0002_initial")]
    operations = [
        migrations.AlterField(model_name="notification", name="channel", field=models.CharField(choices=[("email", "Email"), ("in_app", "In-App"), ("push", "Push")], default="in_app", max_length=20)),
        migrations.AddField(model_name="notificationpreference", name="push_enabled", field=models.BooleanField(default=True)),
        migrations.CreateModel(
            name="MobileDevice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.TextField(unique=True)), ("platform", models.CharField(default="android", max_length=16)),
                ("active", models.BooleanField(default=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="mobile_devices", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="mobiledevice", index=models.Index(fields=["user", "active"], name="notificatio_user_id_9df594_idx")),
    ]
