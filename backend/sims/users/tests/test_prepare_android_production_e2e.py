from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase


class PrepareAndroidProductionE2ECommandTests(SimpleTestCase):
    @patch.dict("os.environ", {"PGSIMS_ENVIRONMENT": "staging"}, clear=False)
    def test_refuses_any_non_production_environment(self):
        with self.assertRaisesMessage(CommandError, "refuses to run outside"):
            call_command("prepare_android_production_e2e")

    @patch.dict("os.environ", {"PGSIMS_ENVIRONMENT": "production"}, clear=False)
    def test_requires_an_external_strong_password(self):
        with self.assertRaisesMessage(CommandError, "16+ character password"):
            call_command("prepare_android_production_e2e")
