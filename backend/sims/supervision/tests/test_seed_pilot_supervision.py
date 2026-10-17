from unittest.mock import patch

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_seed_pilot_supervision_exits_without_required_masters():
    """The command is safe when its prerequisite pilot masters are absent."""
    from sims.supervision.management.commands import seed_pilot_supervision

    with patch.object(seed_pilot_supervision, "call_command") as seeded:
        with patch.object(seed_pilot_supervision.Hospital.objects, "filter") as hospitals:
            hospitals.return_value.first.return_value = None
            call_command("seed_pilot_supervision")

    seeded.assert_called_once_with("seed_pilot_masters")
