"""Seed realistic multi-department demo data for local walkthroughs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.notifications.models import Notification, NotificationPreference
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.eligibility import recompute_for_record
from sims.training.models import (
    DeputationPosting,
    LeaveRequest,
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramPolicy,
    ProgramRotationTemplate,
    ResidentResearchProject,
    ResidentThesis,
    ResidentTrainingRecord,
    ResidentWorkshopCompletion,
    RotationAssignment,
    TrainingProgram,
    Workshop,
    WorkshopBlock,
    WorkshopRun,
)
from sims.users.models import (
    DepartmentMembership,
    HODAssignment,
    HospitalAssignment,
    ResidentProfile,
    StaffProfile,
    SupervisorResidentLink,
    User,
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@sims.com"

DEMO_PASSWORD = "DemoPass123!"
DEMO_EMAIL_DOMAIN = "demo.local"
DEMO_CODE_PREFIX = "DEMO-"

DEMO_HOSPITALS = [
    {
        "code": "DEMO-AH",
        "name": "Allied Hospital Demo",
        "address": "Jail Road, Faisalabad",
        "phone": "+92-41-111-0001",
        "email": "allied.demo@demo.local",
        "description": "High-volume tertiary site seeded for product demonstrations.",
    },
    {
        "code": "DEMO-DHQ",
        "name": "DHQ Hospital Demo",
        "address": "Susan Road, Faisalabad",
        "phone": "+92-41-111-0002",
        "email": "dhq.demo@demo.local",
        "description": "Secondary teaching site seeded for multi-hospital demonstrations.",
    },
]

DEMO_DEPARTMENTS = [
    {
        "code": "DEMO-SURG",
        "name": "General Surgery Demo",
        "description": "Canonical surgery department used by the demo dataset.",
        "specialty": "surgery",
    },
    {
        "code": "DEMO-MED",
        "name": "Internal Medicine Demo",
        "description": "Canonical medicine department used by the demo dataset.",
        "specialty": "medicine",
    },
]

DEMO_MATRIX = {
    "DEMO-AH": ["DEMO-SURG", "DEMO-MED"],
    "DEMO-DHQ": ["DEMO-SURG", "DEMO-MED"],
}

DEMO_OVERSIGHT_USERS = [
    {
        "username": "demo_utrmc_admin",
        "email": "utrmc.admin@demo.local",
        "first_name": "Rida",
        "last_name": "Mansoor",
        "role": "utrmc_admin",
    },
    {
        "username": "demo_utrmc_user",
        "email": "utrmc.readonly@demo.local",
        "first_name": "Hamid",
        "last_name": "Qureshi",
        "role": "utrmc_user",
    },
]

DEMO_STAFF_USERS = [
    {
        "username": "demo_surg_hod",
        "email": "farooq.ahmed@demo.local",
        "first_name": "Farooq",
        "last_name": "Ahmed",
        "role": "supervisor",
        "specialty": "surgery",
        "department_code": "DEMO-SURG",
        "hospital_code": "DEMO-AH",
        "designation": "Professor and HOD",
    },
    {
        "username": "demo_surg_faculty",
        "email": "maria.khan@demo.local",
        "first_name": "Maria",
        "last_name": "Khan",
        "role": "faculty",
        "specialty": "surgery",
        "department_code": "DEMO-SURG",
        "hospital_code": "DEMO-DHQ",
        "designation": "Associate Professor",
    },
    {
        "username": "demo_med_hod",
        "email": "ayesha.khalid@demo.local",
        "first_name": "Ayesha",
        "last_name": "Khalid",
        "role": "supervisor",
        "specialty": "medicine",
        "department_code": "DEMO-MED",
        "hospital_code": "DEMO-DHQ",
        "designation": "Professor and HOD",
    },
    {
        "username": "demo_med_faculty",
        "email": "salman.javed@demo.local",
        "first_name": "Salman",
        "last_name": "Javed",
        "role": "faculty",
        "specialty": "medicine",
        "department_code": "DEMO-MED",
        "hospital_code": "DEMO-AH",
        "designation": "Assistant Professor",
    },
]

DEMO_RESIDENT_USERS = [
    {
        "username": "demo_surg_r1",
        "email": "ali.hamza@demo.local",
        "first_name": "Ali",
        "last_name": "Hamza",
        "role": "resident",
        "specialty": "surgery",
        "year": "1",
        "department_code": "DEMO-SURG",
        "hospital_code": "DEMO-AH",
        "program_code": "DEMO-FCPS-SURG",
        "supervisor_username": "demo_surg_hod",
        "training_level": "Year 1",
        "pgr_id": "PGR-SURG-001",
        "months_in_program": 10,
    },
    {
        "username": "demo_surg_r2",
        "email": "bilal.raza@demo.local",
        "first_name": "Bilal",
        "last_name": "Raza",
        "role": "pg",
        "specialty": "surgery",
        "year": "2",
        "department_code": "DEMO-SURG",
        "hospital_code": "DEMO-DHQ",
        "program_code": "DEMO-FCPS-SURG",
        "supervisor_username": "demo_surg_faculty",
        "training_level": "Year 2",
        "pgr_id": "PGR-SURG-002",
        "months_in_program": 22,
    },
    {
        "username": "demo_surg_r3",
        "email": "hira.aslam@demo.local",
        "first_name": "Hira",
        "last_name": "Aslam",
        "role": "resident",
        "specialty": "surgery",
        "year": "3",
        "department_code": "DEMO-SURG",
        "hospital_code": "DEMO-AH",
        "program_code": "DEMO-FCPS-SURG",
        "supervisor_username": "demo_surg_hod",
        "training_level": "Year 3",
        "pgr_id": "PGR-SURG-003",
        "months_in_program": 34,
    },
    {
        "username": "demo_surg_r4",
        "email": "umar.farid@demo.local",
        "first_name": "Umar",
        "last_name": "Farid",
        "role": "pg",
        "specialty": "surgery",
        "year": "4",
        "department_code": "DEMO-SURG",
        "hospital_code": "DEMO-DHQ",
        "program_code": "DEMO-FCPS-SURG",
        "supervisor_username": "demo_surg_faculty",
        "training_level": "Year 4",
        "pgr_id": "PGR-SURG-004",
        "months_in_program": 46,
    },
    {
        "username": "demo_med_r1",
        "email": "areeba.noor@demo.local",
        "first_name": "Areeba",
        "last_name": "Noor",
        "role": "resident",
        "specialty": "medicine",
        "year": "1",
        "department_code": "DEMO-MED",
        "hospital_code": "DEMO-DHQ",
        "program_code": "DEMO-FCPS-MED",
        "supervisor_username": "demo_med_hod",
        "training_level": "Year 1",
        "pgr_id": "PGR-MED-001",
        "months_in_program": 11,
    },
    {
        "username": "demo_med_r2",
        "email": "saad.malik@demo.local",
        "first_name": "Saad",
        "last_name": "Malik",
        "role": "pg",
        "specialty": "medicine",
        "year": "2",
        "department_code": "DEMO-MED",
        "hospital_code": "DEMO-AH",
        "program_code": "DEMO-FCPS-MED",
        "supervisor_username": "demo_med_faculty",
        "training_level": "Year 2",
        "pgr_id": "PGR-MED-002",
        "months_in_program": 23,
    },
    {
        "username": "demo_med_r3",
        "email": "fatima.sheikh@demo.local",
        "first_name": "Fatima",
        "last_name": "Sheikh",
        "role": "resident",
        "specialty": "medicine",
        "year": "3",
        "department_code": "DEMO-MED",
        "hospital_code": "DEMO-DHQ",
        "program_code": "DEMO-FCPS-MED",
        "supervisor_username": "demo_med_hod",
        "training_level": "Year 3",
        "pgr_id": "PGR-MED-003",
        "months_in_program": 35,
    },
    {
        "username": "demo_med_r4",
        "email": "usman.shah@demo.local",
        "first_name": "Usman",
        "last_name": "Shah",
        "role": "pg",
        "specialty": "medicine",
        "year": "4",
        "department_code": "DEMO-MED",
        "hospital_code": "DEMO-AH",
        "program_code": "DEMO-FCPS-MED",
        "supervisor_username": "demo_med_faculty",
        "training_level": "Year 4",
        "pgr_id": "PGR-MED-004",
        "months_in_program": 47,
    },
]

DEMO_PROGRAMS = [
    {
        "code": "DEMO-FCPS-SURG",
        "name": "FCPS General Surgery Demo",
        "department_code": "DEMO-SURG",
        "degree_type": TrainingProgram.DEGREE_FCPS,
        "duration_months": 48,
        "description": "Seeded surgery program for screenshots, workflows, and walkthroughs.",
        "policy": {
            "allow_program_change": False,
            "program_change_requires_restart": True,
            "min_active_months_before_imm": 18,
            "imm_allowed_from_month": 24,
            "final_allowed_from_month": 42,
            "exception_rules_text": "Demo data only.",
        },
    },
    {
        "code": "DEMO-FCPS-MED",
        "name": "FCPS Internal Medicine Demo",
        "department_code": "DEMO-MED",
        "degree_type": TrainingProgram.DEGREE_FCPS,
        "duration_months": 48,
        "description": "Seeded medicine program for screenshots, workflows, and walkthroughs.",
        "policy": {
            "allow_program_change": False,
            "program_change_requires_restart": True,
            "min_active_months_before_imm": 18,
            "imm_allowed_from_month": 24,
            "final_allowed_from_month": 42,
            "exception_rules_text": "Demo data only.",
        },
    },
]

DEMO_PROGRAM_TEMPLATES = {
    "DEMO-FCPS-SURG": [
        {
            "name": "General Surgery Ward",
            "department_code": "DEMO-SURG",
            "duration_weeks": 12,
            "sequence_order": 1,
            "year_index": 1,
        },
        {
            "name": "Emergency Surgery and Trauma",
            "department_code": "DEMO-SURG",
            "duration_weeks": 8,
            "sequence_order": 2,
            "year_index": 2,
        },
        {
            "name": "Surgical ICU and Peri-Operative Care",
            "department_code": "DEMO-SURG",
            "duration_weeks": 8,
            "sequence_order": 3,
            "year_index": 3,
        },
    ],
    "DEMO-FCPS-MED": [
        {
            "name": "General Medicine Ward",
            "department_code": "DEMO-MED",
            "duration_weeks": 12,
            "sequence_order": 1,
            "year_index": 1,
        },
        {
            "name": "Cardiology and HDU",
            "department_code": "DEMO-MED",
            "duration_weeks": 8,
            "sequence_order": 2,
            "year_index": 2,
        },
        {
            "name": "Critical Care Medicine",
            "department_code": "DEMO-MED",
            "duration_weeks": 8,
            "sequence_order": 3,
            "year_index": 3,
        },
    ],
}

DEMO_WORKSHOPS = [
    {
        "code": "DEMO-RESM",
        "name": "Research Methods and Biostatistics",
        "description": "Core research workshop for milestone progression.",
    },
    {
        "code": "DEMO-SSAFE",
        "name": "Surgical Safety Bootcamp",
        "description": "Final-year surgical readiness workshop.",
    },
    {
        "code": "DEMO-ACLS",
        "name": "ACLS Refresher",
        "description": "Final-year medicine readiness workshop.",
    },
]


@dataclass(frozen=True)
class RotationStatusPlan:
    status: str
    note: str


FUTURE_ROTATION_STATUS_PLANS = [
    RotationStatusPlan(
        status=RotationAssignment.STATUS_SUBMITTED,
        note="Awaiting department review for the next block.",
    ),
    RotationStatusPlan(
        status=RotationAssignment.STATUS_APPROVED,
        note="Approved and ready for the upcoming block.",
    ),
    RotationStatusPlan(
        status=RotationAssignment.STATUS_RETURNED,
        note="Returned for date clarification before approval.",
    ),
    RotationStatusPlan(
        status=RotationAssignment.STATUS_DRAFT,
        note="Prepared draft for the next block.",
    ),
]


class Command(BaseCommand):
    help = "Seed realistic multi-hospital demo data while preserving admin/admin123."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing demo-coded data before reseeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self._reset_demo_entities()

        today = timezone.now().date()
        now = timezone.now()

        admin = self._ensure_admin_user()
        hospitals = self._upsert_hospitals()
        departments = self._upsert_departments()
        hospital_departments = self._upsert_hospital_departments(
            hospitals=hospitals,
            departments=departments,
        )
        users = self._upsert_users(
            admin=admin,
            hospitals=hospitals,
            departments=departments,
        )
        self._seed_staff_profiles(users=users)
        self._seed_department_memberships(
            admin=admin,
            users=users,
            departments=departments,
        )
        self._seed_hospital_assignments(
            admin=admin,
            users=users,
            hospital_departments=hospital_departments,
        )
        self._seed_hod_assignments(
            admin=admin,
            users=users,
            departments=departments,
        )
        self._seed_supervision_links(
            admin=admin,
            users=users,
            departments=departments,
        )

        workshops = self._upsert_workshops(users=users, today=today)
        programs = self._upsert_programs(departments=departments)
        templates = self._upsert_program_rotation_templates(
            programs=programs,
            departments=departments,
            hospitals=hospitals,
        )

        resident_training = self._seed_resident_training_records(
            admin=admin,
            users=users,
            programs=programs,
            today=today,
        )
        self._seed_rotation_assignments(
            admin=admin,
            users=users,
            resident_training=resident_training,
            hospital_departments=hospital_departments,
            templates=templates,
            today=today,
            now=now,
        )
        self._seed_leave_requests(
            approvers=users,
            resident_training=resident_training,
            today=today,
        )
        self._seed_deputation_postings(
            approvers=users,
            resident_training=resident_training,
            today=today,
        )
        self._seed_research_and_thesis(
            resident_training=resident_training,
            users=users,
            now=now,
        )
        self._seed_workshop_completions(
            resident_training=resident_training,
            workshops=workshops,
            today=today,
        )
        self._seed_notifications(users=users, admin=admin)

        eligibility_rows = 0
        for record in resident_training.values():
            eligibility_rows += len(recompute_for_record(record))

        demo_user_count = User.objects.filter(
            username__startswith="demo_",
            is_archived=False,
        ).count()
        self.stdout.write(self.style.SUCCESS("seed_demo_data completed successfully."))
        self.stdout.write(f"Admin login: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
        self.stdout.write(f"Shared demo user password: {DEMO_PASSWORD}")
        self.stdout.write(f"Demo users seeded: {demo_user_count + 1}")
        self.stdout.write(
            f"Demo hospitals seeded: {Hospital.objects.filter(code__startswith=DEMO_CODE_PREFIX).count()}"
        )
        self.stdout.write(
            f"Demo departments seeded: {Department.objects.filter(code__startswith=DEMO_CODE_PREFIX).count()}"
        )
        self.stdout.write(
            "Hospital-department links: "
            f"{HospitalDepartment.objects.filter(hospital__code__startswith=DEMO_CODE_PREFIX).count()}"
        )
        self.stdout.write(
            f"Resident training records: {ResidentTrainingRecord.objects.filter(program__code__startswith=DEMO_CODE_PREFIX).count()}"
        )
        self.stdout.write(
            f"Rotation assignments: {RotationAssignment.objects.filter(resident_training__program__code__startswith=DEMO_CODE_PREFIX).count()}"
        )
        self.stdout.write(
            f"Workshop completions: {ResidentWorkshopCompletion.objects.filter(resident_training_record__program__code__startswith=DEMO_CODE_PREFIX).count()}"
        )
        self.stdout.write(f"Eligibility snapshots recomputed: {eligibility_rows}")
        self.stdout.write("Sample logins:")
        self.stdout.write(f"  - demo_utrmc_admin / {DEMO_PASSWORD}")
        self.stdout.write(f"  - demo_surg_hod / {DEMO_PASSWORD}")
        self.stdout.write(f"  - demo_med_r4 / {DEMO_PASSWORD}")

    def _reset_demo_entities(self):
        Notification.objects.filter(metadata__seed_source="seed_demo_data").delete()
        ResidentWorkshopCompletion.objects.filter(
            resident_training_record__program__code__startswith=DEMO_CODE_PREFIX
        ).delete()
        WorkshopRun.objects.filter(block__workshop__code__startswith=DEMO_CODE_PREFIX).delete()
        WorkshopBlock.objects.filter(workshop__code__startswith=DEMO_CODE_PREFIX).delete()
        Workshop.objects.filter(code__startswith=DEMO_CODE_PREFIX).delete()
        ProgramRotationTemplate.objects.filter(program__code__startswith=DEMO_CODE_PREFIX).delete()
        TrainingProgram.objects.filter(code__startswith=DEMO_CODE_PREFIX).delete()
        Department.objects.filter(code__startswith=DEMO_CODE_PREFIX).delete()
        Hospital.objects.filter(code__startswith=DEMO_CODE_PREFIX).delete()
        User.objects.filter(email__iendswith=f"@{DEMO_EMAIL_DOMAIN}").delete()

    def _ensure_admin_user(self):
        user = User.objects.filter(username=ADMIN_USERNAME).first()
        if user is None:
            user = User(username=ADMIN_USERNAME, email=ADMIN_EMAIL)
        user.email = ADMIN_EMAIL
        user.first_name = "Admin"
        user.last_name = "User"
        user.role = "admin"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_archived = False
        user.set_password(ADMIN_PASSWORD)
        user.save()
        NotificationPreference.for_user(user)
        return user

    def _upsert_hospitals(self):
        hospitals = {}
        for spec in DEMO_HOSPITALS:
            hospital, _ = Hospital.objects.update_or_create(
                code=spec["code"],
                defaults={
                    "name": spec["name"],
                    "address": spec["address"],
                    "phone": spec["phone"],
                    "email": spec["email"],
                    "description": spec["description"],
                    "is_active": True,
                },
            )
            hospitals[spec["code"]] = hospital
        return hospitals

    def _upsert_departments(self):
        departments = {}
        for spec in DEMO_DEPARTMENTS:
            department, _ = Department.objects.update_or_create(
                code=spec["code"],
                defaults={
                    "name": spec["name"],
                    "description": spec["description"],
                    "active": True,
                },
            )
            departments[spec["code"]] = department
        return departments

    def _upsert_hospital_departments(self, hospitals, departments):
        hospital_departments = {}
        for hospital_code, department_codes in DEMO_MATRIX.items():
            for department_code in department_codes:
                hospital_department, _ = HospitalDepartment.objects.update_or_create(
                    hospital=hospitals[hospital_code],
                    department=departments[department_code],
                    defaults={"is_active": True},
                )
                hospital_departments[(hospital_code, department_code)] = hospital_department
        return hospital_departments

    def _upsert_users(self, admin, hospitals, departments):
        users = {ADMIN_USERNAME: admin}

        for spec in DEMO_OVERSIGHT_USERS + DEMO_STAFF_USERS + DEMO_RESIDENT_USERS:
            user = User.objects.filter(username=spec["username"]).first()
            if user is None:
                user = User(username=spec["username"])
            user.email = spec["email"]
            user.first_name = spec["first_name"]
            user.last_name = spec["last_name"]
            user.role = spec["role"]
            user.specialty = spec.get("specialty")
            user.year = spec.get("year")
            user.registration_number = spec.get("pgr_id") or f"STAFF-{spec['username'].upper()}"
            user.phone_number = "+92-300-0000000"
            user.created_by = admin
            user.modified_by = admin
            user.is_active = True
            user.is_archived = False
            user.home_hospital = hospitals.get(spec.get("hospital_code"))
            user.home_department = departments.get(spec.get("department_code"))
            supervisor_username = spec.get("supervisor_username")
            user.supervisor = users.get(supervisor_username) if supervisor_username else None
            user.set_password(DEMO_PASSWORD)
            user.save()
            NotificationPreference.for_user(user)
            users[user.username] = user

        return users

    def _seed_staff_profiles(self, users):
        for spec in DEMO_STAFF_USERS:
            StaffProfile.objects.update_or_create(
                user=users[spec["username"]],
                defaults={
                    "designation": spec["designation"],
                    "phone": "+92-300-1111111",
                    "active": True,
                },
            )

    def _seed_department_memberships(self, admin, users, departments):
        for spec in DEMO_STAFF_USERS + DEMO_RESIDENT_USERS:
            member_type = "resident" if spec["role"] in {"resident", "pg"} else spec["role"]
            DepartmentMembership.objects.update_or_create(
                user=users[spec["username"]],
                department=departments[spec["department_code"]],
                defaults={
                    "member_type": member_type,
                    "is_primary": True,
                    "active": True,
                    "start_date": timezone.now().date() - timedelta(days=400),
                    "end_date": None,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

    def _seed_hospital_assignments(self, admin, users, hospital_departments):
        for spec in DEMO_STAFF_USERS:
            HospitalAssignment.objects.update_or_create(
                user=users[spec["username"]],
                hospital_department=hospital_departments[
                    (spec["hospital_code"], spec["department_code"])
                ],
                defaults={
                    "assignment_type": HospitalAssignment.ASSIGNMENT_FACULTY_SITE,
                    "start_date": timezone.now().date() - timedelta(days=365),
                    "end_date": None,
                    "active": True,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

        for spec in DEMO_RESIDENT_USERS:
            HospitalAssignment.objects.update_or_create(
                user=users[spec["username"]],
                hospital_department=hospital_departments[
                    (spec["hospital_code"], spec["department_code"])
                ],
                defaults={
                    "assignment_type": HospitalAssignment.ASSIGNMENT_PRIMARY_TRAINING,
                    "start_date": timezone.now().date() - timedelta(days=spec["months_in_program"] * 30),
                    "end_date": None,
                    "active": True,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

    def _seed_hod_assignments(self, admin, users, departments):
        hod_map = {
            "DEMO-SURG": "demo_surg_hod",
            "DEMO-MED": "demo_med_hod",
        }
        today = timezone.now().date()
        for department_code, username in hod_map.items():
            department = departments[department_code]
            hod_user = users[username]
            department.head = hod_user
            department.save(update_fields=["head"])
            HODAssignment.objects.update_or_create(
                department=department,
                active=True,
                defaults={
                    "hod_user": hod_user,
                    "start_date": today - timedelta(days=365),
                    "end_date": None,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

    def _seed_supervision_links(self, admin, users, departments):
        today = timezone.now().date()
        for spec in DEMO_RESIDENT_USERS:
            SupervisorResidentLink.objects.update_or_create(
                supervisor_user=users[spec["supervisor_username"]],
                resident_user=users[spec["username"]],
                department=departments[spec["department_code"]],
                defaults={
                    "start_date": today - timedelta(days=300),
                    "end_date": None,
                    "active": True,
                    "created_by": admin,
                    "updated_by": admin,
                },
            )

    def _upsert_programs(self, departments):
        programs = {}
        for spec in DEMO_PROGRAMS:
            program, _ = TrainingProgram.objects.update_or_create(
                code=spec["code"],
                defaults={
                    "name": spec["name"],
                    "duration_months": spec["duration_months"],
                    "description": spec["description"],
                    "degree_type": spec["degree_type"],
                    "department": departments[spec["department_code"]],
                    "notes": "Seeded by seed_demo_data.",
                    "active": True,
                },
            )
            ProgramPolicy.objects.update_or_create(
                program=program,
                defaults=spec["policy"],
            )
            programs[spec["code"]] = program

        for code, program in programs.items():
            imm, _ = ProgramMilestone.objects.update_or_create(
                program=program,
                code=ProgramMilestone.CODE_IMM,
                defaults={
                    "name": "Intermediate Module Milestone",
                    "recommended_month": 24,
                    "is_active": True,
                },
            )
            final, _ = ProgramMilestone.objects.update_or_create(
                program=program,
                code=ProgramMilestone.CODE_FINAL,
                defaults={
                    "name": "Final Examination Readiness",
                    "recommended_month": 42,
                    "is_active": True,
                },
            )
            ProgramMilestoneResearchRequirement.objects.update_or_create(
                milestone=imm,
                defaults={
                    "requires_synopsis_approved": True,
                    "requires_synopsis_submitted_to_university": False,
                    "requires_thesis_submitted": False,
                },
            )
            ProgramMilestoneResearchRequirement.objects.update_or_create(
                milestone=final,
                defaults={
                    "requires_synopsis_approved": True,
                    "requires_synopsis_submitted_to_university": False,
                    "requires_thesis_submitted": True,
                },
            )
            imm.workshop_requirements.all().delete()
            final.workshop_requirements.all().delete()
            research_methods = Workshop.objects.filter(code="DEMO-RESM").first()
            final_workshop_code = "DEMO-SSAFE" if code.endswith("SURG") else "DEMO-ACLS"
            final_workshop = Workshop.objects.filter(code=final_workshop_code).first()
            if research_methods is not None:
                ProgramMilestoneWorkshopRequirement.objects.update_or_create(
                    milestone=imm,
                    workshop=research_methods,
                    defaults={"required_count": 1},
                )
            if final_workshop is not None:
                ProgramMilestoneWorkshopRequirement.objects.update_or_create(
                    milestone=final,
                    workshop=final_workshop,
                    defaults={"required_count": 1},
                )

        return programs

    def _upsert_program_rotation_templates(self, programs, departments, hospitals):
        templates = {}
        for program_code, specs in DEMO_PROGRAM_TEMPLATES.items():
            program = programs[program_code]
            for spec in specs:
                template, _ = ProgramRotationTemplate.objects.update_or_create(
                    program=program,
                    name=spec["name"],
                    defaults={
                        "department": departments[spec["department_code"]],
                        "duration_weeks": spec["duration_weeks"],
                        "required": True,
                        "sequence_order": spec["sequence_order"],
                        "active": True,
                        "year_index": spec["year_index"],
                        "phase_index": 1,
                        "block_index": spec["sequence_order"],
                        "is_mandatory": True,
                        "min_duration_weeks": spec["duration_weeks"],
                        "requirements_json": {"seed_source": "seed_demo_data"},
                    },
                )
                template.allowed_hospitals.set(list(hospitals.values()))
                templates[(program_code, spec["name"])] = template
        return templates

    def _upsert_workshops(self, users, today):
        workshops = {}
        facilitators = {
            "DEMO-RESM": users["demo_med_faculty"],
            "DEMO-SSAFE": users["demo_surg_hod"],
            "DEMO-ACLS": users["demo_med_hod"],
        }
        for spec in DEMO_WORKSHOPS:
            workshop, _ = Workshop.objects.update_or_create(
                code=spec["code"],
                defaults={
                    "name": spec["name"],
                    "description": spec["description"],
                    "is_active": True,
                },
            )
            block, _ = WorkshopBlock.objects.update_or_create(
                workshop=workshop,
                name="Main Cohort",
                defaults={"capacity": 40},
            )
            WorkshopRun.objects.update_or_create(
                block=block,
                run_date=today - timedelta(days=120),
                defaults={
                    "facilitator": facilitators[spec["code"]],
                    "status": WorkshopRun.STATUS_COMPLETED,
                    "notes": "Seeded demo workshop run.",
                },
            )
            workshops[spec["code"]] = workshop
        return workshops

    def _seed_resident_training_records(self, admin, users, programs, today):
        records = {}
        year_map = {"1": "y1", "2": "y2", "3": "y3", "4": "y4"}
        for spec in DEMO_RESIDENT_USERS:
            resident = users[spec["username"]]
            training_start = today - timedelta(days=spec["months_in_program"] * 30)
            training_end = training_start + timedelta(days=48 * 30)
            ResidentProfile.objects.update_or_create(
                user=resident,
                defaults={
                    "pgr_id": spec["pgr_id"],
                    "training_start": training_start,
                    "training_end": training_end,
                    "training_level": spec["training_level"],
                    "active": True,
                },
            )
            record, _ = ResidentTrainingRecord.objects.update_or_create(
                resident_user=resident,
                program=programs[spec["program_code"]],
                defaults={
                    "start_date": training_start,
                    "expected_end_date": training_end,
                    "current_level": year_map[spec["year"]],
                    "status": ResidentTrainingRecord.STATUS_ACTIVE,
                    "locked_program": True,
                    "restart_from_scratch_on_change": True,
                    "active": True,
                    "created_by": admin,
                },
            )
            records[spec["username"]] = record
        return records

    def _seed_rotation_assignments(
        self,
        admin,
        users,
        resident_training,
        hospital_departments,
        templates,
        today,
        now,
    ):
        alternate_hospital = {
            "DEMO-AH": "DEMO-DHQ",
            "DEMO-DHQ": "DEMO-AH",
        }
        template_names = {
            "DEMO-FCPS-SURG": [
                "General Surgery Ward",
                "Emergency Surgery and Trauma",
                "Surgical ICU and Peri-Operative Care",
            ],
            "DEMO-FCPS-MED": [
                "General Medicine Ward",
                "Cardiology and HDU",
                "Critical Care Medicine",
            ],
        }

        for index, spec in enumerate(DEMO_RESIDENT_USERS):
            record = resident_training[spec["username"]]
            department_code = spec["department_code"]
            home_hospital_code = spec["hospital_code"]
            future_hospital_code = alternate_hospital[home_hospital_code]
            program_code = spec["program_code"]

            completed_template = templates[(program_code, template_names[program_code][0])]
            active_template = templates[(program_code, template_names[program_code][1])]
            future_template = templates[(program_code, template_names[program_code][2])]

            RotationAssignment.objects.update_or_create(
                resident_training=record,
                template=completed_template,
                defaults={
                    "hospital_department": hospital_departments[(home_hospital_code, department_code)],
                    "start_date": today - timedelta(days=220),
                    "end_date": today - timedelta(days=136),
                    "status": RotationAssignment.STATUS_COMPLETED,
                    "notes": "Completed block seeded for historical demo context.",
                    "requested_by": admin,
                    "approved_by_hod": users[spec["supervisor_username"]],
                    "approved_by_utrmc": users["demo_utrmc_admin"],
                    "submitted_at": now - timedelta(days=230),
                    "approved_at": now - timedelta(days=225),
                    "completed_at": now - timedelta(days=136),
                    "return_reason": "",
                    "reject_reason": "",
                },
            )

            RotationAssignment.objects.update_or_create(
                resident_training=record,
                template=active_template,
                defaults={
                    "hospital_department": hospital_departments[(future_hospital_code, department_code)],
                    "start_date": today - timedelta(days=21),
                    "end_date": today + timedelta(days=35),
                    "status": RotationAssignment.STATUS_ACTIVE,
                    "notes": "Current active rotation seeded for dashboard schedule.",
                    "requested_by": admin,
                    "approved_by_hod": users[spec["supervisor_username"]],
                    "approved_by_utrmc": users["demo_utrmc_admin"],
                    "submitted_at": now - timedelta(days=30),
                    "approved_at": now - timedelta(days=25),
                    "completed_at": None,
                    "return_reason": "",
                    "reject_reason": "",
                },
            )

            plan = FUTURE_ROTATION_STATUS_PLANS[index % len(FUTURE_ROTATION_STATUS_PLANS)]
            future_defaults = {
                "hospital_department": hospital_departments[(home_hospital_code, department_code)],
                "start_date": today + timedelta(days=49),
                "end_date": today + timedelta(days=112),
                "status": plan.status,
                "notes": plan.note,
                "requested_by": admin,
                "approved_by_hod": None,
                "approved_by_utrmc": None,
                "submitted_at": None,
                "approved_at": None,
                "completed_at": None,
                "return_reason": "",
                "reject_reason": "",
            }
            if plan.status in {
                RotationAssignment.STATUS_SUBMITTED,
                RotationAssignment.STATUS_APPROVED,
                RotationAssignment.STATUS_RETURNED,
            }:
                future_defaults["submitted_at"] = now - timedelta(days=3)
            if plan.status == RotationAssignment.STATUS_APPROVED:
                future_defaults["approved_by_hod"] = users[spec["supervisor_username"]]
                future_defaults["approved_by_utrmc"] = users["demo_utrmc_admin"]
                future_defaults["approved_at"] = now - timedelta(days=2)
            if plan.status == RotationAssignment.STATUS_RETURNED:
                future_defaults["return_reason"] = (
                    "Please align the requested dates with the next hospital block."
                )

            RotationAssignment.objects.update_or_create(
                resident_training=record,
                template=future_template,
                defaults=future_defaults,
            )

    def _seed_leave_requests(self, approvers, resident_training, today):
        leave_specs = [
            ("demo_surg_r1", LeaveRequest.TYPE_ANNUAL, LeaveRequest.STATUS_APPROVED, 18, 22),
            ("demo_surg_r2", LeaveRequest.TYPE_STUDY, LeaveRequest.STATUS_SUBMITTED, 35, 37),
            ("demo_med_r1", LeaveRequest.TYPE_CASUAL, LeaveRequest.STATUS_DRAFT, 12, 12),
            ("demo_med_r2", LeaveRequest.TYPE_SICK, LeaveRequest.STATUS_APPROVED, -18, -14),
        ]
        for username, leave_type, status_value, start_offset, end_offset in leave_specs:
            defaults = {
                "leave_type": leave_type,
                "start_date": today + timedelta(days=start_offset),
                "end_date": today + timedelta(days=end_offset),
                "reason": "Seeded leave request for demo schedule coverage.",
                "status": status_value,
                "approved_by": None,
                "approved_at": None,
                "reject_reason": "",
            }
            if status_value == LeaveRequest.STATUS_APPROVED:
                defaults["approved_by"] = approvers["demo_utrmc_admin"]
                defaults["approved_at"] = timezone.now() - timedelta(days=1)
            LeaveRequest.objects.update_or_create(
                resident_training=resident_training[username],
                leave_type=leave_type,
                start_date=defaults["start_date"],
                defaults=defaults,
            )

    def _seed_deputation_postings(self, approvers, resident_training, today):
        posting_specs = [
            (
                "demo_surg_r4",
                DeputationPosting.TYPE_OFF_SERVICE,
                DeputationPosting.STATUS_APPROVED,
                "Punjab Institute of Cardiology",
                "Lahore",
                65,
                118,
            ),
            (
                "demo_med_r3",
                DeputationPosting.TYPE_DEPUTATION,
                DeputationPosting.STATUS_SUBMITTED,
                "Medical ICU Exchange",
                "Rawalpindi",
                42,
                84,
            ),
            (
                "demo_med_r4",
                DeputationPosting.TYPE_OFF_SERVICE,
                DeputationPosting.STATUS_COMPLETED,
                "Hepatology Service",
                "Lahore",
                -120,
                -70,
            ),
        ]
        for username, posting_type, status_value, institution, city, start_offset, end_offset in posting_specs:
            defaults = {
                "posting_type": posting_type,
                "institution_name": institution,
                "city": city,
                "start_date": today + timedelta(days=start_offset),
                "end_date": today + timedelta(days=end_offset),
                "status": status_value,
                "notes": "Seeded off-service posting for demo walkthroughs.",
                "approved_by": None,
                "approved_at": None,
                "reject_reason": "",
            }
            if status_value in {DeputationPosting.STATUS_APPROVED, DeputationPosting.STATUS_COMPLETED}:
                defaults["approved_by"] = approvers["demo_utrmc_admin"]
                defaults["approved_at"] = timezone.now() - timedelta(days=14)
            DeputationPosting.objects.update_or_create(
                resident_training=resident_training[username],
                institution_name=institution,
                start_date=defaults["start_date"],
                defaults=defaults,
            )

    def _seed_research_and_thesis(self, resident_training, users, now):
        topic_by_department = {
            "surgery": "Enhanced Recovery After Emergency Laparotomy",
            "medicine": "Improving Sepsis Bundle Compliance in High-Dependency Units",
        }
        for spec in DEMO_RESIDENT_USERS:
            record = resident_training[spec["username"]]
            status_value = ResidentResearchProject.STATUS_DRAFT
            supervisor_feedback = ""
            submitted_to_supervisor_at = None
            synopsis_approved_at = None
            submitted_to_university_at = None
            accepted_at = None
            university_submission_ref = ""

            if spec["year"] == "2":
                status_value = ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR
                submitted_to_supervisor_at = now - timedelta(days=14)
                supervisor_feedback = "Seeded for supervisor review queue."
            elif spec["year"] == "3":
                status_value = ResidentResearchProject.STATUS_APPROVED_SUPERVISOR
                submitted_to_supervisor_at = now - timedelta(days=40)
                synopsis_approved_at = now - timedelta(days=28)
                supervisor_feedback = "Approved after minor revisions."
            elif spec["username"] in {"demo_surg_r4", "demo_med_r4"}:
                status_value = ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY
                submitted_to_supervisor_at = now - timedelta(days=90)
                synopsis_approved_at = now - timedelta(days=75)
                submitted_to_university_at = now - timedelta(days=45)
                accepted_at = now - timedelta(days=20)
                university_submission_ref = f"UNI-{record.id:04d}"
                supervisor_feedback = "Accepted for final evaluation."

            ResidentResearchProject.objects.update_or_create(
                resident_training_record=record,
                defaults={
                    "title": topic_by_department[spec["specialty"]],
                    "topic_area": "Clinical Governance",
                    "supervisor": users[spec["supervisor_username"]],
                    "status": status_value,
                    "supervisor_feedback": supervisor_feedback,
                    "submitted_to_supervisor_at": submitted_to_supervisor_at,
                    "synopsis_approved_at": synopsis_approved_at,
                    "submitted_to_university_at": submitted_to_university_at,
                    "accepted_at": accepted_at,
                    "university_submission_ref": university_submission_ref,
                },
            )

            thesis_status = ResidentThesis.STATUS_NOT_STARTED
            submitted_at = None
            final_submission_ref = ""
            notes = "Seeded thesis placeholder."
            if spec["year"] == "3":
                thesis_status = ResidentThesis.STATUS_IN_PROGRESS
                notes = "Draft chapters and supervisor comments in progress."
            elif spec["year"] == "4":
                thesis_status = ResidentThesis.STATUS_SUBMITTED
                submitted_at = now - timedelta(days=10)
                final_submission_ref = f"TH-{record.id:04d}"
                notes = "Submitted thesis packet seeded for final milestone coverage."

            ResidentThesis.objects.update_or_create(
                resident_training_record=record,
                defaults={
                    "status": thesis_status,
                    "submitted_at": submitted_at,
                    "final_submission_ref": final_submission_ref,
                    "notes": notes,
                },
            )

    def _seed_workshop_completions(self, resident_training, workshops, today):
        for spec in DEMO_RESIDENT_USERS:
            record = resident_training[spec["username"]]
            if spec["year"] in {"2", "3", "4"}:
                ResidentWorkshopCompletion.objects.update_or_create(
                    resident_training_record=record,
                    workshop=workshops["DEMO-RESM"],
                    defaults={
                        "workshop_run": workshops["DEMO-RESM"].blocks.first().runs.first(),
                        "completed_at": today - timedelta(days=150),
                        "source": ResidentWorkshopCompletion.SOURCE_SYSTEM,
                        "notes": "Seeded core research workshop completion.",
                    },
                )
            if spec["year"] == "4" and spec["specialty"] == "surgery":
                ResidentWorkshopCompletion.objects.update_or_create(
                    resident_training_record=record,
                    workshop=workshops["DEMO-SSAFE"],
                    defaults={
                        "workshop_run": workshops["DEMO-SSAFE"].blocks.first().runs.first(),
                        "completed_at": today - timedelta(days=45),
                        "source": ResidentWorkshopCompletion.SOURCE_SYSTEM,
                        "notes": "Seeded final-year surgery workshop completion.",
                    },
                )
            if spec["year"] == "4" and spec["specialty"] == "medicine":
                ResidentWorkshopCompletion.objects.update_or_create(
                    resident_training_record=record,
                    workshop=workshops["DEMO-ACLS"],
                    defaults={
                        "workshop_run": workshops["DEMO-ACLS"].blocks.first().runs.first(),
                        "completed_at": today - timedelta(days=40),
                        "source": ResidentWorkshopCompletion.SOURCE_SYSTEM,
                        "notes": "Seeded final-year medicine workshop completion.",
                    },
                )

    def _seed_notifications(self, users, admin):
        for username in [*users]:
            user = users[username]
            NotificationPreference.for_user(user)
            if user.username == ADMIN_USERNAME:
                continue
            Notification.objects.update_or_create(
                recipient=user,
                verb="demo-seeded",
                title="Demo workspace ready",
                channel=Notification.CHANNEL_IN_APP,
                defaults={
                    "actor": admin,
                    "body": (
                        "Your account has seeded rotations, research, workshops, and "
                        "organization links for demonstration use."
                    ),
                    "metadata": {
                        "seed_source": "seed_demo_data",
                        "username": user.username,
                    },
                },
            )

        Notification.objects.update_or_create(
            recipient=admin,
            verb="demo-refresh",
            title="Demo data refreshed",
            channel=Notification.CHANNEL_IN_APP,
            defaults={
                "actor": admin,
                "body": "Canonical demo data has been refreshed successfully.",
                "metadata": {
                    "seed_source": "seed_demo_data",
                    "dataset": "multi-hospital-demo",
                },
            },
        )
