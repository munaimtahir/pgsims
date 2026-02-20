# Generated manually for adding urology specialty

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_historicaluser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="specialty",
            field=models.CharField(
                blank=True,
                choices=[
                    ("medicine", "Internal Medicine"),
                    ("surgery", "Surgery"),
                    ("pediatrics", "Pediatrics"),
                    ("gynecology", "Gynecology & Obstetrics"),
                    ("orthopedics", "Orthopedics"),
                    ("cardiology", "Cardiology"),
                    ("neurology", "Neurology"),
                    ("urology", "Urology"),
                    ("psychiatry", "Psychiatry"),
                    ("dermatology", "Dermatology"),
                    ("radiology", "Radiology"),
                    ("anesthesia", "Anesthesia"),
                    ("pathology", "Pathology"),
                    ("microbiology", "Microbiology"),
                    ("pharmacology", "Pharmacology"),
                    ("community_medicine", "Community Medicine"),
                    ("forensic_medicine", "Forensic Medicine"),
                    ("other", "Other"),
                ],
                help_text="Medical specialty (required for PGs and Supervisors)",
                max_length=100,
                null=True,
            ),
        ),
    ]
