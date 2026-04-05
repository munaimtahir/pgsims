from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_data_correction_flags"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="datacorrectionaudit",
            old_name="users_dataco_entity__0fc19f_idx",
            new_name="users_datac_entity__308bcb_idx",
        ),
        migrations.RenameIndex(
            model_name="datacorrectionaudit",
            old_name="users_dataco_actor_i_5aa07d_idx",
            new_name="users_datac_actor_i_b92e94_idx",
        ),
        migrations.RenameIndex(
            model_name="datacorrectionaudit",
            old_name="users_dataco_field_n_12a34f_idx",
            new_name="users_datac_field_n_611183_idx",
        ),
        migrations.AlterField(
            model_name="historicaluser",
            name="data_issues",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Computed list of data quality issue codes for this user.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaluser",
            name="has_placeholder_email",
            field=models.BooleanField(
                default=False,
                help_text="True when email appears to be a placeholder value.",
            ),
        ),
        migrations.AlterField(
            model_name="historicaluser",
            name="is_complete_profile",
            field=models.BooleanField(
                default=False,
                help_text="Computed data quality flag for resident/admin correction workflows.",
            ),
        ),
    ]
