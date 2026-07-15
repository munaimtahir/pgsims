from django.core.management.base import BaseCommand

from sims.academics.services import seed_pilot_academics


class Command(BaseCommand):
    help = "Seed Brick 8 pilot academic foundation data."

    def handle(self, *args, **options):
        result = seed_pilot_academics(actor=None)
        for key, value in result.items():
            self.stdout.write(f"{key}: {value}")
