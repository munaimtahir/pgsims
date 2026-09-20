from django.db import migrations


DEFAULT_REQUIREMENTS = (
    {
        "document_type": "CNIC",
        "display_name": "CNIC Copy",
        "description": "A clear copy of the resident's CNIC or national identity document.",
        "display_order": 1,
    },
    {
        "document_type": "PMDC_CERTIFICATE",
        "display_name": "PMDC Registration Certificate",
        "description": "A copy of the resident's current PMDC registration certificate.",
        "display_order": 2,
    },
)


def seed_default_requirements(apps, schema_editor):
    Requirement = apps.get_model("users", "ResidentDocumentRequirement")
    for values in DEFAULT_REQUIREMENTS:
        Requirement.objects.get_or_create(
            document_type=values["document_type"],
            program=None,
            department=None,
            defaults={
                **values,
                "stage": "ONBOARDING",
                "is_required": True,
                "is_active": True,
            },
        )


def remove_default_requirements(apps, schema_editor):
    Requirement = apps.get_model("users", "ResidentDocumentRequirement")
    Requirement.objects.filter(
        document_type__in=[item["document_type"] for item in DEFAULT_REQUIREMENTS],
        program__isnull=True,
        department__isnull=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("users", "0015_historicalresidentprofile_review_note_and_more")]

    operations = [migrations.RunPython(seed_default_requirements, remove_default_requirements)]
