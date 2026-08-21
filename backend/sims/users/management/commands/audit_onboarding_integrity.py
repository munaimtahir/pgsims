from django.core.management.base import BaseCommand
from django.db.models import Count, F

from sims.supervision.models import PendingSupervisorAssignment, ResidentSupervisorAssignment
from sims.users.models import ResidentDocumentRequirement, User


class Command(BaseCommand):
    help = "Report resident supervision/document integrity without mutating data."

    def handle(self, *args, **options):
        residents = User.objects.filter(role="RESIDENT")
        matching = legacy_only = canonical_only = conflicting = 0
        for user in residents.select_related("supervisor"):
            legacy = user.supervisor_id
            assignment = ResidentSupervisorAssignment.objects.filter(
                resident__user=user, assignment_type="PRIMARY", is_active=True
            ).select_related("supervisor__user").first()
            canonical = assignment.supervisor.user_id if assignment else None
            if legacy and canonical and legacy == canonical: matching += 1
            elif legacy and canonical and legacy != canonical: conflicting += 1
            elif legacy: legacy_only += 1
            elif canonical: canonical_only += 1
        duplicate_requirements = ResidentDocumentRequirement.objects.filter(is_active=True).values(
            "document_type", "program_id", "department_id", "stage"
        ).annotate(count=Count("id")).filter(count__gt=1).count()
        pending_with_assignment = PendingSupervisorAssignment.objects.filter(
            status="PENDING", resident__supervisor_assignments__is_active=True
        ).distinct().count()
        resolved_without_assignment = PendingSupervisorAssignment.objects.filter(
            status="RESOLVED", resolved_supervisor__isnull=False
        ).exclude(resident__supervisor_assignments__supervisor_id=F("resolved_supervisor_id")).distinct().count()
        self.stdout.write(self.style.SUCCESS("Onboarding integrity audit"))
        self.stdout.write(f"residents={residents.count()}")
        self.stdout.write(f"supervision_matching={matching}")
        self.stdout.write(f"supervision_legacy_only={legacy_only}")
        self.stdout.write(f"supervision_canonical_only={canonical_only}")
        self.stdout.write(f"supervision_conflicting={conflicting}")
        self.stdout.write(f"pending_with_active_assignment={pending_with_assignment}")
        self.stdout.write(f"resolved_without_matching_assignment={resolved_without_assignment}")
        self.stdout.write(f"duplicate_active_requirements={duplicate_requirements}")
