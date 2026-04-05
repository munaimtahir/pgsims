from __future__ import annotations

from django.db import migrations, models


def backfill_data_quality_flags(apps, schema_editor):
    User = apps.get_model("users", "User")
    ResidentTrainingRecord = apps.get_model("training", "ResidentTrainingRecord")
    SupervisorResidentLink = apps.get_model("users", "SupervisorResidentLink")
    ResidentProfile = apps.get_model("users", "ResidentProfile")

    default_dates = {"2026-01-01"}

    for user in User.objects.filter(role__in=["resident", "pg"]).iterator():
        issues = []
        email = (user.email or "").strip().lower()
        if not email:
            issues.append("missing_email")
        elif "placeholder" in email or email.endswith("@pilot-placeholder.local"):
            issues.append("placeholder_email")

        if not (user.year or "").strip():
            issues.append("missing_year")

        profile = ResidentProfile.objects.filter(user=user).first()
        if not profile:
            issues.append("missing_resident_profile")
        else:
            if not profile.training_start:
                issues.append("missing_training_start")
            elif profile.training_start.isoformat() in default_dates:
                issues.append("default_training_start")

        has_default_training = False
        for record in ResidentTrainingRecord.objects.filter(resident_user=user):
            has_default = (
                (not bool(record.start_date))
                or (record.start_date and record.start_date.isoformat() in default_dates)
            )
            if has_default:
                has_default_training = True
            record.has_default_dates = has_default
            record.save(update_fields=["has_default_dates"])

        for link in SupervisorResidentLink.objects.filter(resident_user=user):
            has_default_link = (
                (not bool(link.start_date))
                or (link.start_date and link.start_date.isoformat() in default_dates)
            )
            link.has_default_dates = has_default_link
            link.save(update_fields=["has_default_dates"])

        user.has_placeholder_email = "placeholder_email" in issues
        user.data_issues = sorted(set(issues))
        user.is_complete_profile = not issues and not has_default_training
        user.save(update_fields=["has_placeholder_email", "data_issues", "is_complete_profile"])


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0003_residenttrainingrecord_has_default_dates"),
        ("users", "0003_alter_historicaluser_year_alter_user_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_complete_profile",
            field=models.BooleanField(
                default=False,
                help_text="Computed data quality flag for resident/admin correction workflows.",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="has_placeholder_email",
            field=models.BooleanField(
                default=False,
                help_text="True when email appears to be a placeholder value.",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="data_issues",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Computed list of data quality issue codes for this user.",
            ),
        ),
        migrations.AddField(
            model_name="historicaluser",
            name="is_complete_profile",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="historicaluser",
            name="has_placeholder_email",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="historicaluser",
            name="data_issues",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="supervisorresidentlink",
            name="has_default_dates",
            field=models.BooleanField(
                default=False,
                help_text="Computed flag set when this link uses default/synthetic dates.",
            ),
        ),
        migrations.CreateModel(
            name="DataCorrectionAudit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entity_type", models.CharField(max_length=50)),
                ("entity_id", models.CharField(max_length=64)),
                ("field_name", models.CharField(max_length=100)),
                ("old_value", models.TextField(blank=True)),
                ("new_value", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.SET_NULL,
                        related_name="data_corrections_made",
                        to="users.user",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="datacorrectionaudit",
            index=models.Index(fields=["entity_type", "entity_id", "created_at"], name="users_dataco_entity__0fc19f_idx"),
        ),
        migrations.AddIndex(
            model_name="datacorrectionaudit",
            index=models.Index(fields=["actor", "created_at"], name="users_dataco_actor_i_5aa07d_idx"),
        ),
        migrations.AddIndex(
            model_name="datacorrectionaudit",
            index=models.Index(fields=["field_name", "created_at"], name="users_dataco_field_n_12a34f_idx"),
        ),
        migrations.RunPython(backfill_data_quality_flags, migrations.RunPython.noop),
    ]
