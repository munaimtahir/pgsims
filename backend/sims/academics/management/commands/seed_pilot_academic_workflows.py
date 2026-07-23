from django.core.management.base import BaseCommand

from sims.academics.services import seed_pilot_academic_workflows


class Command(BaseCommand):
    help = "Seed combined Brick 9/10 academic workflows pilot data."

    def handle(self, *args, **options):
        result = seed_pilot_academic_workflows(actor=None)
        for key, value in result.items():
            self.stdout.write(f"{key}: {value}")
