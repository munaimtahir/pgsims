from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Iterable

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import QuerySet, TextField
from django.db.models.functions import Cast

from sims.academics.models import Department
from sims.audit.models import ActivityLog
from sims.notifications.models import Notification, NotificationPreference
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    DeputationPosting,
    LeaveRequest,
    ProgramMilestone,
    ProgramMilestoneLogbookRequirement,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramPolicy,
    ProgramRotationTemplate,
    ResidentMilestoneEligibility,
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
)

User = get_user_model()

USER_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^demo_",
        r"^e2e_",
        r"(^|[_-])(demo|e2e|test|dummy|sample|seed)([_-]|$)",
        r"^(pg|res|sup)_p6-",
        r"^(pg|res|sup)_e2e-",
    )
]
EMAIL_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"@demo\.local$",
        r"@pgsims\.local$",
        r"@test\.com$",
        r"@example\.com$",
    )
]
DEPARTMENT_CODE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^DEMO-",
        r"^D\d{8}$",
        r"^TD\d+",
        r"^SD\d+",
    )
]
DEPARTMENT_NAME_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bdemo\b",
        r"\btest dept\b",
        r"\bscreenshot dept\b",
        r"\be2e-",
    )
]
HOSPITAL_CODE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^DEMO-",
        r"^H\d{8}$",
        r"^TH\d+",
        r"^SH\d+",
    )
]
HOSPITAL_NAME_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bdemo\b",
        r"\btest hospital\b",
        r"\bscreenshot hospital\b",
        r"\be2e-",
    )
]
PROGRAM_CODE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^DEMO-",
        r"^E2E-",
        r"^PROG-",
        r"^POLI-",
    )
]
WORKSHOP_CODE_PATTERNS = [re.compile(r"^DEMO-", re.IGNORECASE)]
TEXT_MARKERS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bdemo\b",
        r"\be2e\b",
        r"\bseed_demo_data\b",
        r"\bscreenshot\b",
        r"\btest\b",
        r"\bwf-\d+\b",
    )
]


@dataclass
class DeletionTarget:
    label: str
    queryset: QuerySet
    sample_attr: str | None = None

    def count(self) -> int:
        return self.queryset.count()

    def sample_values(self, limit: int = 10) -> list[str]:
        if self.sample_attr is None:
            return []
        values = list(self.queryset.values_list(self.sample_attr, flat=True)[:limit])
        return [str(value) for value in values]


def _matches_any(value: str | None, patterns: Iterable[re.Pattern[str]]) -> bool:
    text = (value or "").strip()
    return any(pattern.search(text) for pattern in patterns)
class Command(BaseCommand):
    help = (
        "Remove non-production demo/E2E runtime data while preserving canonical org "
        "structure and explicitly kept admin users. Defaults to dry-run."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Execute deletions. Without this flag the command only reports what would be removed.",
        )
        parser.add_argument(
            "--keep-username",
            action="append",
            default=["admin"],
            help="Username to preserve even if it matches a purge pattern. Repeatable.",
        )

    def handle(self, *args, **options):
        keep_usernames = {username.strip() for username in options["keep_username"] if username.strip()}
        plan = self._build_plan(keep_usernames=keep_usernames)

        self.stdout.write(self.style.WARNING("Pilot cleanup plan"))
        self.stdout.write(f"Mode: {'APPLY' if options['apply'] else 'DRY-RUN'}")
        self.stdout.write(f"Keep usernames: {', '.join(sorted(keep_usernames)) or '(none)'}")
        self.stdout.write("")

        for target in plan["targets"]:
            self.stdout.write(f"{target.label}: {target.count()}")
            samples = target.sample_values()
            if samples:
                self.stdout.write(f"  sample: {', '.join(samples)}")

        self.stdout.write("")
        self.stdout.write("Manual review")
        for label, values in plan["manual_review"].items():
            rendered = ", ".join(values) if values else "(none)"
            self.stdout.write(f"{label}: {rendered}")

        if not options["apply"]:
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("Dry-run complete. Re-run with --apply to execute the purge."))
            return

        with transaction.atomic():
            for target in plan["targets"]:
                object_ids = list(target.queryset.values_list("pk", flat=True))
                deleted_count = len(object_ids)
                if deleted_count:
                    target.queryset.model.objects.filter(pk__in=object_ids).delete()
                self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} from {target.label}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Pilot runtime cleanup completed."))

    def _build_plan(self, *, keep_usernames: set[str]) -> dict:
        purge_users = [
            user
            for user in User.objects.all().order_by("id")
            if user.username not in keep_usernames and self._is_purge_user(user)
        ]
        purge_user_ids = {user.id for user in purge_users}

        purge_departments = [
            department
            for department in Department.objects.all().order_by("id")
            if self._is_purge_department(department)
        ]
        purge_department_ids = {department.id for department in purge_departments}

        purge_hospitals = [
            hospital
            for hospital in Hospital.objects.all().order_by("id")
            if self._is_purge_hospital(hospital)
        ]
        purge_hospital_ids = {hospital.id for hospital in purge_hospitals}

        purge_programs = [
            program
            for program in TrainingProgram.objects.all().order_by("id")
            if self._is_purge_program(program)
        ]
        purge_program_ids = {program.id for program in purge_programs}

        purge_workshops = [
            workshop
            for workshop in Workshop.objects.all().order_by("id")
            if self._is_purge_workshop(workshop)
        ]
        purge_workshop_ids = {workshop.id for workshop in purge_workshops}

        hospital_departments = HospitalDepartment.objects.filter(
            hospital_id__in=purge_hospital_ids
        ) | HospitalDepartment.objects.filter(department_id__in=purge_department_ids)
        hospital_department_ids = set(hospital_departments.values_list("id", flat=True))

        templates = ProgramRotationTemplate.objects.filter(program_id__in=purge_program_ids) | ProgramRotationTemplate.objects.filter(
            department_id__in=purge_department_ids
        )
        templates = templates.distinct()
        template_ids = set(templates.values_list("id", flat=True))

        policies = ProgramPolicy.objects.filter(program_id__in=purge_program_ids)

        milestones = ProgramMilestone.objects.filter(program_id__in=purge_program_ids)
        milestone_ids = set(milestones.values_list("id", flat=True))

        milestone_research_requirements = ProgramMilestoneResearchRequirement.objects.filter(
            milestone_id__in=milestone_ids
        )
        milestone_workshop_requirements = ProgramMilestoneWorkshopRequirement.objects.filter(
            milestone_id__in=milestone_ids
        ) | ProgramMilestoneWorkshopRequirement.objects.filter(workshop_id__in=purge_workshop_ids)
        milestone_workshop_requirements = milestone_workshop_requirements.distinct()
        milestone_logbook_requirements = ProgramMilestoneLogbookRequirement.objects.filter(
            milestone_id__in=milestone_ids
        )

        workshop_blocks = WorkshopBlock.objects.filter(workshop_id__in=purge_workshop_ids)
        workshop_block_ids = set(workshop_blocks.values_list("id", flat=True))
        workshop_runs = WorkshopRun.objects.filter(block_id__in=workshop_block_ids) | WorkshopRun.objects.filter(
            facilitator_id__in=purge_user_ids
        )
        workshop_runs = workshop_runs.distinct()
        workshop_run_ids = set(workshop_runs.values_list("id", flat=True))

        training_records = ResidentTrainingRecord.objects.filter(
            resident_user_id__in=purge_user_ids
        ) | ResidentTrainingRecord.objects.filter(program_id__in=purge_program_ids)
        training_records = training_records.distinct()
        training_record_ids = set(training_records.values_list("id", flat=True))

        rotation_assignments = RotationAssignment.objects.filter(
            resident_training_id__in=training_record_ids
        ) | RotationAssignment.objects.filter(hospital_department_id__in=hospital_department_ids) | RotationAssignment.objects.filter(
            template_id__in=template_ids
        )
        rotation_assignments = rotation_assignments.distinct()
        rotation_assignment_ids = set(rotation_assignments.values_list("id", flat=True))

        leave_requests = LeaveRequest.objects.filter(resident_training_id__in=training_record_ids)
        leave_request_ids = set(leave_requests.values_list("id", flat=True))

        deputation_postings = DeputationPosting.objects.filter(resident_training_id__in=training_record_ids)
        deputation_posting_ids = set(deputation_postings.values_list("id", flat=True))

        research_projects = ResidentResearchProject.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | ResidentResearchProject.objects.filter(supervisor_id__in=purge_user_ids)
        research_projects = research_projects.distinct()
        research_project_ids = set(research_projects.values_list("id", flat=True))

        resident_theses = ResidentThesis.objects.filter(resident_training_record_id__in=training_record_ids)
        resident_thesis_ids = set(resident_theses.values_list("id", flat=True))

        workshop_completions = ResidentWorkshopCompletion.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | ResidentWorkshopCompletion.objects.filter(workshop_id__in=purge_workshop_ids) | ResidentWorkshopCompletion.objects.filter(
            workshop_run_id__in=workshop_run_ids
        )
        workshop_completions = workshop_completions.distinct()
        workshop_completion_ids = set(workshop_completions.values_list("id", flat=True))

        milestone_eligibility = ResidentMilestoneEligibility.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | ResidentMilestoneEligibility.objects.filter(milestone_id__in=milestone_ids)
        milestone_eligibility = milestone_eligibility.distinct()

        department_memberships = DepartmentMembership.objects.filter(user_id__in=purge_user_ids) | DepartmentMembership.objects.filter(
            department_id__in=purge_department_ids
        )
        department_memberships = department_memberships.distinct()

        hospital_assignments = HospitalAssignment.objects.filter(user_id__in=purge_user_ids) | HospitalAssignment.objects.filter(
            hospital_department_id__in=hospital_department_ids
        )
        hospital_assignments = hospital_assignments.distinct()

        supervision_links = SupervisorResidentLink.objects.filter(
            supervisor_user_id__in=purge_user_ids
        ) | SupervisorResidentLink.objects.filter(resident_user_id__in=purge_user_ids) | SupervisorResidentLink.objects.filter(
            department_id__in=purge_department_ids
        )
        supervision_links = supervision_links.distinct()

        hod_assignments = HODAssignment.objects.filter(hod_user_id__in=purge_user_ids) | HODAssignment.objects.filter(
            department_id__in=purge_department_ids
        )
        hod_assignments = hod_assignments.distinct()

        staff_profiles = StaffProfile.objects.filter(user_id__in=purge_user_ids)
        resident_profiles = ResidentProfile.objects.filter(user_id__in=purge_user_ids)

        notifications = Notification.objects.filter(recipient_id__in=purge_user_ids) | Notification.objects.filter(
            actor_id__in=purge_user_ids
        ) | Notification.objects.filter(verb__in=["demo-seeded", "demo-refresh"]) | Notification.objects.filter(
            metadata__seed_source="seed_demo_data"
        )
        notifications = notifications.distinct()
        notification_preferences = NotificationPreference.objects.filter(user_id__in=purge_user_ids)

        activity_logs = [
            log
            for log in ActivityLog.objects.annotate(meta_text=Cast("metadata", output_field=TextField()))
            if log.actor_id in purge_user_ids
            or _matches_any(log.target_repr, TEXT_MARKERS)
            or _matches_any(getattr(log, "meta_text", ""), TEXT_MARKERS)
        ]
        activity_log_ids = {log.id for log in activity_logs}

        history_targets = [
            DeletionTarget(
                "users_historicaluser",
                User.history.model.objects.filter(id__in=purge_user_ids),
                "username",
            ),
            DeletionTarget(
                "training_historicaltrainingprogram",
                TrainingProgram.history.model.objects.filter(id__in=purge_program_ids),
                "code",
            ),
            DeletionTarget(
                "training_historicalprogramrotationtemplate",
                ProgramRotationTemplate.history.model.objects.filter(id__in=template_ids),
                "name",
            ),
            DeletionTarget(
                "training_historicalprogrammilestone",
                ProgramMilestone.history.model.objects.filter(id__in=milestone_ids),
                "code",
            ),
            DeletionTarget(
                "training_historicalprogrammilestoneresearchrequirement",
                ProgramMilestoneResearchRequirement.history.model.objects.filter(
                    id__in=milestone_research_requirements.values_list("id", flat=True)
                ),
            ),
            DeletionTarget(
                "training_historicalprogrammilestoneworkshoprequirement",
                ProgramMilestoneWorkshopRequirement.history.model.objects.filter(
                    id__in=milestone_workshop_requirements.values_list("id", flat=True)
                ),
            ),
            DeletionTarget(
                "training_historicalprogrammilestonelogbookrequirement",
                ProgramMilestoneLogbookRequirement.history.model.objects.filter(
                    id__in=milestone_logbook_requirements.values_list("id", flat=True)
                ),
            ),
            DeletionTarget(
                "training_historicalresidenttrainingrecord",
                ResidentTrainingRecord.history.model.objects.filter(id__in=training_record_ids),
            ),
            DeletionTarget(
                "training_historicalrotationassignment",
                RotationAssignment.history.model.objects.filter(id__in=rotation_assignment_ids),
            ),
            DeletionTarget(
                "training_historicalleaverequest",
                LeaveRequest.history.model.objects.filter(id__in=leave_request_ids),
            ),
            DeletionTarget(
                "training_historicaldeputationposting",
                DeputationPosting.history.model.objects.filter(id__in=deputation_posting_ids),
            ),
            DeletionTarget(
                "training_historicalresidentresearchproject",
                ResidentResearchProject.history.model.objects.filter(id__in=research_project_ids),
            ),
            DeletionTarget(
                "training_historicalresidentthesis",
                ResidentThesis.history.model.objects.filter(id__in=resident_thesis_ids),
            ),
            DeletionTarget(
                "training_historicalresidentworkshopcompletion",
                ResidentWorkshopCompletion.history.model.objects.filter(id__in=workshop_completion_ids),
            ),
            DeletionTarget(
                "training_historicalworkshop",
                Workshop.history.model.objects.filter(id__in=purge_workshop_ids),
                "code",
            ),
            DeletionTarget(
                "training_historicalworkshopblock",
                WorkshopBlock.history.model.objects.filter(id__in=workshop_block_ids),
                "name",
            ),
            DeletionTarget(
                "training_historicalworkshoprun",
                WorkshopRun.history.model.objects.filter(id__in=workshop_run_ids),
            ),
        ]

        targets = [
            DeletionTarget("audit_activitylog", ActivityLog.objects.filter(id__in=activity_log_ids)),
            DeletionTarget("notifications_notification", notifications, "verb"),
            DeletionTarget("notifications_notificationpreference", notification_preferences),
            DeletionTarget("training_residentmilestoneeligibility", milestone_eligibility),
            DeletionTarget("training_residentworkshopcompletion", workshop_completions),
            DeletionTarget("training_residentthesis", resident_theses),
            DeletionTarget("training_residentresearchproject", research_projects),
            DeletionTarget("training_leaverequest", leave_requests),
            DeletionTarget("training_deputationposting", deputation_postings),
            DeletionTarget("training_rotationassignment", rotation_assignments),
            DeletionTarget("training_workshoprun", workshop_runs),
            DeletionTarget("training_workshopblock", workshop_blocks),
            DeletionTarget("training_programmilestoneworkshoprequirement", milestone_workshop_requirements),
            DeletionTarget("training_programmilestoneresearchrequirement", milestone_research_requirements),
            DeletionTarget("training_programmilestonelogbookrequirement", milestone_logbook_requirements),
            DeletionTarget("training_programmilestone", milestones, "code"),
            DeletionTarget("training_programpolicy", policies),
            DeletionTarget("training_programrotationtemplate", templates, "name"),
            DeletionTarget("training_residenttrainingrecord", training_records),
            DeletionTarget("training_workshop", Workshop.objects.filter(id__in=purge_workshop_ids), "code"),
            DeletionTarget("training_trainingprogram", TrainingProgram.objects.filter(id__in=purge_program_ids), "code"),
            DeletionTarget("users_supervisorresidentlink", supervision_links),
            DeletionTarget("users_hodassignment", hod_assignments),
            DeletionTarget("users_hospitalassignment", hospital_assignments),
            DeletionTarget("users_departmentmembership", department_memberships),
            DeletionTarget("users_staffprofile", staff_profiles),
            DeletionTarget("users_residentprofile", resident_profiles),
            DeletionTarget("users_user", User.objects.filter(id__in=purge_user_ids), "username"),
            DeletionTarget(
                "rotations_hospitaldepartment",
                HospitalDepartment.objects.filter(id__in=hospital_department_ids),
            ),
            DeletionTarget("academics_department", Department.objects.filter(id__in=purge_department_ids), "code"),
            DeletionTarget("rotations_hospital", Hospital.objects.filter(id__in=purge_hospital_ids), "code"),
        ]
        targets.extend(history_targets)

        manual_review_users = [
            user.username
            for user in User.objects.exclude(id__in=purge_user_ids).order_by("username")
            if user.username not in keep_usernames and user.role == "admin"
        ]
        manual_review_programs = [
            program.code
            for program in TrainingProgram.objects.exclude(id__in=purge_program_ids).order_by("code")
        ]

        return {
            "targets": [target for target in targets if target.count() > 0],
            "manual_review": {
                "admin_users_to_keep": sorted(keep_usernames),
                "nonpurged_admin_users": manual_review_users,
                "nonpurged_programs": manual_review_programs,
            },
        }

    def _is_purge_user(self, user) -> bool:
        return _matches_any(user.username, USER_PATTERNS) or _matches_any(user.email, EMAIL_PATTERNS)

    def _is_purge_department(self, department: Department) -> bool:
        return _matches_any(department.code, DEPARTMENT_CODE_PATTERNS) or _matches_any(
            department.name, DEPARTMENT_NAME_PATTERNS
        )

    def _is_purge_hospital(self, hospital: Hospital) -> bool:
        return _matches_any(hospital.code, HOSPITAL_CODE_PATTERNS) or _matches_any(
            hospital.name, HOSPITAL_NAME_PATTERNS
        )

    def _is_purge_program(self, program: TrainingProgram) -> bool:
        return _matches_any(program.code, PROGRAM_CODE_PATTERNS)

    def _is_purge_workshop(self, workshop: Workshop) -> bool:
        return _matches_any(workshop.code, WORKSHOP_CODE_PATTERNS)
