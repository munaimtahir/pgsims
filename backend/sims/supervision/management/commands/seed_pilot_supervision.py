from datetime import date
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.users.models import ResidentProfile, SupervisorProfile
from sims.users.services import create_user_with_profile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import create_supervisor_assignment

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds pilot supervision assignments idempotently for training and verification."

    def handle(self, *args, **options):
        self.stdout.write("Ensuring pilot master data is seeded...")
        call_command("seed_pilot_masters")

        allied_hosp = Hospital.objects.filter(code="ALLIED").first()
        med_dept = Department.objects.filter(code="MED").first()

        if not allied_hosp or not med_dept:
            self.stdout.write(
                self.style.ERROR("Required master data (ALLIED, MED) not found. Seeding aborted.")
            )
            return

        self.stdout.write("Ensuring pilot users are seeded...")
        
        # 1. Pilot Residents
        residents_info = [
            {"username": "pgr001", "full_name": "Dr. Ahmad Ali", "email": "pgr001@fmu.edu.pk"},
            {"username": "pgr002", "full_name": "Dr. Fatima Zahra", "email": "pgr002@fmu.edu.pk"},
            {"username": "pgr003", "full_name": "Dr. Usman Khan", "email": "pgr003@fmu.edu.pk"},
        ]
        
        residents = []
        for info in residents_info:
            user = User.objects.filter(username=info["username"]).first()
            if not user:
                user = create_user_with_profile(
                    role="RESIDENT",
                    username=info["username"],
                    password="password123",
                    full_name=info["full_name"],
                    email=info["email"],
                    profile_payload={
                        "hospital_id": allied_hosp.id,
                        "department_ref_id": med_dept.id,
                    }
                )
            # Ensure profile fields are set and profile status is complete
            profile = user.resident_profile
            profile.hospital = allied_hosp
            profile.department_ref = med_dept
            profile.profile_status = "COMPLETE"
            profile.completed_schema_version = 1
            profile.save()
            user.is_profile_complete = True
            user.save()
            residents.append(profile)

        # 2. Pilot Supervisors
        supervisors_info = [
            {"username": "sup001", "full_name": "Prof. Khalid Mahmood", "email": "sup001@fmu.edu.pk"},
            {"username": "sup002", "full_name": "Dr. Sajid Raza", "email": "sup002@fmu.edu.pk"},
        ]
        
        supervisors = []
        for info in supervisors_info:
            user = User.objects.filter(username=info["username"]).first()
            if not user:
                user = create_user_with_profile(
                    role="SUPERVISOR",
                    username=info["username"],
                    password="password123",
                    full_name=info["full_name"],
                    email=info["email"],
                    profile_payload={
                        "hospital_id": allied_hosp.id,
                        "department_ref_id": med_dept.id,
                    }
                )
            profile = user.supervisor_profile
            profile.hospital = allied_hosp
            profile.department_ref = med_dept
            profile.profile_status = "COMPLETE"
            profile.completed_schema_version = 1
            profile.save()
            user.is_profile_complete = True
            user.save()
            supervisors.append(profile)

        self.stdout.write("Ensuring pilot supervision mappings...")

        with transaction.atomic():
            # Clear old active mappings for seeded users to ensure idempotency
            ResidentSupervisorAssignment.objects.filter(
                resident__in=residents,
                supervisor__in=supervisors,
            ).delete()

            # Assign Primary Supervisor: pgr001 -> sup001
            create_supervisor_assignment(
                resident=residents[0],
                supervisor=supervisors[0],
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                start_date=date(2026, 1, 1),
                notes="Seeded Pilot Primary Supervisor",
            )

            # Assign Primary Supervisor: pgr002 -> sup001
            create_supervisor_assignment(
                resident=residents[1],
                supervisor=supervisors[0],
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                start_date=date(2026, 1, 1),
                notes="Seeded Pilot Primary Supervisor",
            )

            # Assign Primary Supervisor: pgr003 -> sup002
            create_supervisor_assignment(
                resident=residents[2],
                supervisor=supervisors[1],
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                start_date=date(2026, 1, 1),
                notes="Seeded Pilot Primary Supervisor",
            )

            # Assign Co-Supervisor: pgr001 -> sup002
            create_supervisor_assignment(
                resident=residents[0],
                supervisor=supervisors[1],
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
                start_date=date(2026, 2, 1),
                notes="Seeded Pilot Co-Supervisor",
            )

        self.stdout.write(self.style.SUCCESS("Supervision pilot data seeded successfully."))
