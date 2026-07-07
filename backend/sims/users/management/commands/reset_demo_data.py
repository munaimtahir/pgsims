from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Iterable

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from sims.academics.models import Department
from sims.audit.models import ActivityLog, AuditReport
from sims.bulk.models import BulkOperation
from sims.notifications.models import Notification, NotificationPreference
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    DeputationPosting,
    LeaveRequest,
    LogbookEntry,
    LogbookReview,
    LogbookThresholdConfig,
    LogbookThresholdSnapshot,
    ProgramMilestone,
    ProgramMilestoneLogbookRequirement,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramPolicy,
    ProgramRotationRequirement,
    ProgramRotationTemplate,
    ResidentMilestoneEligibility,
    ResidentResearchProject,
    ResidentSubmission,
    ResidentThesis,
    ResidentTrainingRecord,
    ResidentWorkshopCompletion,
    RotationAssignment,
    RotationCertificate,
    RotationCompletion,
    SubmissionCertificate,
    SubmissionDocument,
    SubmissionRequirementTemplate,
    SubmissionReview,
    TrainingProgram,
    Workshop,
    WorkshopBlock,
    WorkshopRun,
)
from sims.users.models import (
    DataCorrectionAudit,
    DepartmentMembership,
    HospitalAssignment,
    ResidentProfile,
    SupervisorResidentLink,
    SupervisorProfile,
    SupportStaffProfile,
    AdminProfile,
)

User = get_user_model()


USER_MARKERS = (
    r"\be2e\b",
    r"\btest\b",
    r"\bworkflow[-_ ]?test\b",
    r"\bwf\b",
    r"\bfeature\b",
    r"\bpilot\b",
    r"\bdemo\b",
    r"\bfake\b",
    r"\bdummy\b",
    r"\bsample\b",
    r"\bseed\b",
    r"\bnegative_role_user\b",
    r"\bsupervisor_user\b",
    r"\bresident_user\b",
    r"\bhod_user\b",
    r"\butrmc_admin_user\b",
    r"\butrmc_staff_user\b",
    r"\be2e_admin\b",
    r"\be2e_supervisor\b",
    r"\be2e_pg\b",
    r"\be2e_utrmc_admin\b",
    r"\be2e_utrmc_user\b",
    r"\bpilot_admin\b",
    r"\bpilot_supervisor\b",
    r"\bpilot_pg\b",
    r"\bpilot_resident\b",
    r"\bpilot_utrmc_admin\b",
    r"\bpilot_utrmc_user\b",
    r"\bpg_p6-\w+\b",
    r"\bres_e2e-\w+\b",
    r"\bsup_p6-\w+\b",
    r"\bsup_e2e-\w+\b",
    r"\b\d{10,}\b",
)
EMAIL_MARKERS = (
    r"@test\.com$",
    r"@example\.com$",
    r"@pgsims\.local$",
    r"@demo\.local$",
)
DEPARTMENT_MARKERS = (
    r"\be2e\b",
    r"\btest\b",
    r"\bworkflow[-_ ]?test\b",
    r"\bpilot\b",
    r"\bdemo\b",
    r"\bfeature\b",
    r"\bfake\b",
    r"\bdummy\b",
    r"\bsample\b",
    r"^Department e2e-",
    r"^Test Dept WF-",
    r"^TEST-",
    r"^DEMO-",
    r"^WF-",
)
HOSPITAL_MARKERS = (
    r"\be2e\b",
    r"\btest\b",
    r"\bworkflow[-_ ]?test\b",
    r"\bpilot\b",
    r"\bdemo\b",
    r"\bfeature\b",
    r"\bfake\b",
    r"\bdummy\b",
    r"\bsample\b",
    r"^Hospital e2e-",
    r"^Test Hospital WF-",
    r"^TEST-",
    r"^DEMO-",
    r"^WF-",
)
PROGRAM_MARKERS = (
    r"\be2e\b",
    r"\btest\b",
    r"\bworkflow[-_ ]?test\b",
    r"\bpilot\b",
    r"\bdemo\b",
    r"\bfeature\b",
    r"\bfake\b",
    r"\bdummy\b",
    r"\bsample\b",
    r"^E2E-",
    r"^DEMO-",
    r"^PILOT-",
    r"^ACTIVE-BASELINE",
    r"^WF-",
    r"^PROG-",
    r"^POLI-",
)
WORKSHOP_MARKERS = (
    r"\be2e\b",
    r"\btest\b",
    r"\bworkflow[-_ ]?test\b",
    r"\bpilot\b",
    r"\bdemo\b",
    r"\bfeature\b",
    r"\bfake\b",
    r"\bdummy\b",
    r"\bsample\b",
    r"^DEMO-",
    r"^E2E-",
    r"^WF-",
)
TEXT_MARKER_RE = re.compile(
    r"(e2e|test|workflow[-_ ]?test|wf|feature|pilot|demo|fake|dummy|sample|seed|negative_role_user)",
    re.IGNORECASE,
)


def _text_blob(*values: object) -> str:
    return " ".join(str(value or "") for value in values)


def _matches(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def _json_blob(value: object) -> str:
    try:
        return json.dumps(value, sort_keys=True, default=str)
    except TypeError:
        return str(value)


@dataclass
class DeletionTarget:
    label: str
    queryset: object
    sample_attr: str | None = None

    def count(self) -> int:
        return self.queryset.count()

    def sample_values(self, limit: int = 5) -> list[str]:
        if self.sample_attr is None:
            return []
        values = list(self.queryset.values_list(self.sample_attr, flat=True)[:limit])
        return [str(value) for value in values if value is not None]


class Command(BaseCommand):
    help = "Remove test/demo/pilot data and preserve one usable admin account."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Report the deletion plan without mutating the database. This is the default mode.",
        )
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Execute the deletion after printing the plan.",
        )
        parser.add_argument(
            "--keep-user",
            action="append",
            default=["ADMIN", "pilot_admin"],
            help="Username to preserve even if it matches a purge pattern. Repeatable.",
        )
        parser.add_argument(
            "--keep-email",
            action="append",
            default=["admin@pgsims.local"],
            help="Email address to preserve even if it matches a purge pattern. Repeatable.",
        )

    def handle(self, *args, **options):
        dry_run = bool(options["dry_run"]) or not bool(options["confirm"])
        keep_usernames = {
            value.strip().lower()
            for value in options["keep_user"]
            if isinstance(value, str) and value.strip()
        }
        keep_emails = {
            value.strip().lower()
            for value in options["keep_email"]
            if isinstance(value, str) and value.strip()
        }

        plan = self._build_plan(keep_usernames=keep_usernames, keep_emails=keep_emails)

        self.stdout.write(self.style.WARNING("reset_demo_data plan"))
        self.stdout.write(f"Mode: {'DRY-RUN' if dry_run else 'APPLY'}")
        self.stdout.write(f"Keep usernames: {', '.join(sorted(keep_usernames)) or '(none)'}")
        self.stdout.write(f"Keep emails: {', '.join(sorted(keep_emails)) or '(none)'}")
        self.stdout.write(f"Preserved admin: {plan['protected_admin'] or '(none)'}")
        self.stdout.write("")

        total_count = 0
        for target in plan["targets"]:
            count = target.count()
            total_count += count
            self.stdout.write(f"{target.label}: {count}")
            samples = target.sample_values()
            if samples:
                self.stdout.write(f"  sample: {', '.join(samples)}")

        self.stdout.write("")
        self.stdout.write(f"Total planned deletions: {total_count}")

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry-run complete. Re-run with --confirm to delete."))
            return

        with transaction.atomic():
            for target in plan["targets"]:
                ids = list(target.queryset.values_list("pk", flat=True))
                count = len(ids)
                if not count:
                    continue
                # Chunk deletion to avoid database parameter limits
                for i in range(0, count, 1000):
                    target.queryset.model.objects.filter(pk__in=ids[i:i+1000]).delete()
                self.stdout.write(self.style.SUCCESS(f"Deleted {count} from {target.label}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("reset_demo_data completed successfully."))

    def _build_plan(self, *, keep_usernames: set[str], keep_emails: set[str]) -> dict:
        all_users = list(User.objects.all().order_by("id"))
        protected_users = {
            user.id
            for user in all_users
            if user.username.lower() in keep_usernames or (user.email or "").lower() in keep_emails
        }

        purge_user_ids = {
            user.id
            for user in all_users
            if user.id not in protected_users and self._is_purge_user(user)
        }

        protected_admin = self._select_protected_admin(
            all_users=all_users,
            purge_user_ids=purge_user_ids,
            keep_usernames=keep_usernames,
            keep_emails=keep_emails,
        )
        if protected_admin is None:
            raise CommandError(
                "Refusing to run reset_demo_data because no admin/superuser account would remain. "
                "Use --keep-user or --keep-email to preserve one."
            )
        purge_user_ids.discard(protected_admin.id)

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
        template_ids = set(templates.distinct().values_list("id", flat=True))

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
        program_rotation_requirements = ProgramRotationRequirement.objects.filter(
            program_id__in=purge_program_ids
        ) | ProgramRotationRequirement.objects.filter(department_id__in=purge_department_ids)
        program_rotation_requirements = program_rotation_requirements.distinct()

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

        rotation_completions = RotationCompletion.objects.filter(rotation_id__in=rotation_assignment_ids)
        rotation_completion_ids = set(rotation_completions.values_list("id", flat=True))
        rotation_certificates = RotationCertificate.objects.filter(
            completion_id__in=rotation_completion_ids
        )

        leave_requests = LeaveRequest.objects.filter(resident_training_id__in=training_record_ids)
        deputation_postings = DeputationPosting.objects.filter(resident_training_id__in=training_record_ids)
        resident_theses = ResidentThesis.objects.filter(resident_training_record_id__in=training_record_ids)
        research_projects = ResidentResearchProject.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | ResidentResearchProject.objects.filter(supervisor_id__in=purge_user_ids)
        research_projects = research_projects.distinct()
        workshop_completions = ResidentWorkshopCompletion.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | ResidentWorkshopCompletion.objects.filter(workshop_id__in=purge_workshop_ids) | ResidentWorkshopCompletion.objects.filter(
            workshop_run_id__in=workshop_run_ids
        )
        workshop_completions = workshop_completions.distinct()
        milestone_eligibility = ResidentMilestoneEligibility.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | ResidentMilestoneEligibility.objects.filter(milestone_id__in=milestone_ids)
        milestone_eligibility = milestone_eligibility.distinct()

        logbook_entries = LogbookEntry.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | LogbookEntry.objects.filter(rotation_assignment_id__in=rotation_assignment_ids)
        logbook_entries = logbook_entries.distinct()
        logbook_entry_ids = set(logbook_entries.values_list("id", flat=True))
        logbook_reviews = LogbookReview.objects.filter(entry_id__in=logbook_entry_ids)
        logbook_snapshots = LogbookThresholdSnapshot.objects.filter(
            resident_training_record_id__in=training_record_ids
        ) | LogbookThresholdSnapshot.objects.filter(rotation_assignment_id__in=rotation_assignment_ids)
        logbook_snapshots = logbook_snapshots.distinct()
        logbook_configs = LogbookThresholdConfig.objects.filter(
            program_id__in=purge_program_ids
        ) | LogbookThresholdConfig.objects.filter(department_id__in=purge_department_ids)
        logbook_configs = logbook_configs.distinct()

        submissions = ResidentSubmission.objects.filter(
            resident_training_record_id__in=training_record_ids
        )
        submission_ids = set(submissions.values_list("id", flat=True))
        submission_documents = SubmissionDocument.objects.filter(submission_id__in=submission_ids)
        submission_reviews = SubmissionReview.objects.filter(submission_id__in=submission_ids)
        submission_certificates = SubmissionCertificate.objects.filter(submission_id__in=submission_ids)
        submission_templates = SubmissionRequirementTemplate.objects.filter(
            program_id__in=purge_program_ids
        ) | SubmissionRequirementTemplate.objects.filter(department_id__in=purge_department_ids)
        submission_templates = submission_templates.distinct()

        supervisor_profiles = SupervisorProfile.objects.filter(user_id__in=purge_user_ids)
        support_staff_profiles = SupportStaffProfile.objects.filter(user_id__in=purge_user_ids)
        admin_profiles = AdminProfile.objects.filter(user_id__in=purge_user_ids)
        resident_profiles = ResidentProfile.objects.filter(user_id__in=purge_user_ids)
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
        data_corrections = DataCorrectionAudit.objects.filter(actor_id__in=purge_user_ids)
        notification_preferences = NotificationPreference.objects.filter(user_id__in=purge_user_ids)

        notifications = [
            notification
            for notification in Notification.objects.select_related("recipient", "actor").all().order_by("id")
            if notification.recipient_id in purge_user_ids
            or notification.actor_id in purge_user_ids
            or self._notification_matches(notification)
        ]
        notification_ids = {notification.id for notification in notifications}

        bulk_operations = [
            operation
            for operation in BulkOperation.objects.select_related("user").all().order_by("id")
            if operation.user_id in purge_user_ids or self._bulk_operation_matches(operation)
        ]
        bulk_operation_ids = {operation.id for operation in bulk_operations}

        activity_logs = [
            log
            for log in ActivityLog.objects.select_related("actor").all().order_by("id")
            if log.actor_id in purge_user_ids or self._activity_log_matches(log)
        ]
        activity_log_ids = {log.id for log in activity_logs}

        audit_reports = [
            report
            for report in AuditReport.objects.select_related("created_by").all().order_by("id")
            if report.created_by_id in purge_user_ids or self._audit_report_matches(report)
        ]
        audit_report_ids = {report.id for report in audit_reports}

        history_targets = [
            self._history_target("users_historicaluser", User, purge_user_ids, "username"),
            self._history_target("audit_historicalauditreport", AuditReport, audit_report_ids),
            self._history_target("training_historicaltrainingprogram", TrainingProgram, purge_program_ids, "code"),
            self._history_target(
                "training_historicalprogrampolicy",
                ProgramPolicy,
                set(ProgramPolicy.objects.filter(program_id__in=purge_program_ids).values_list("id", flat=True)),
            ),
            self._history_target("training_historicalprogrammilestone", ProgramMilestone, milestone_ids, "code"),
            self._history_target(
                "training_historicalprogrammilestoneresearchrequirement",
                ProgramMilestoneResearchRequirement,
                set(milestone_research_requirements.values_list("id", flat=True)),
            ),
            self._history_target(
                "training_historicalprogrammilestoneworkshoprequirement",
                ProgramMilestoneWorkshopRequirement,
                set(milestone_workshop_requirements.values_list("id", flat=True)),
            ),
            self._history_target(
                "training_historicalprogrammilestonelogbookrequirement",
                ProgramMilestoneLogbookRequirement,
                set(milestone_logbook_requirements.values_list("id", flat=True)),
            ),
            self._history_target(
                "training_historicalprogramrotationrequirement",
                ProgramRotationRequirement,
                set(program_rotation_requirements.values_list("id", flat=True)),
            ),
            self._history_target(
                "training_historicalprogramrotationtemplate",
                ProgramRotationTemplate,
                template_ids,
                "name",
            ),
            self._history_target("training_historicallogbookthresholdconfig", LogbookThresholdConfig, set(logbook_configs.values_list("id", flat=True))),
            self._history_target("training_historicalresidenttrainingrecord", ResidentTrainingRecord, training_record_ids),
            self._history_target("training_historicalrotationassignment", RotationAssignment, rotation_assignment_ids),
            self._history_target("training_historicalrotationcompletion", RotationCompletion, rotation_completion_ids),
            self._history_target(
                "training_historicalrotationcertificate",
                RotationCertificate,
                set(rotation_certificates.values_list("id", flat=True)),
            ),
            self._history_target("training_historicalleaverequest", LeaveRequest, set(leave_requests.values_list("id", flat=True))),
            self._history_target("training_historicaldeputationposting", DeputationPosting, set(deputation_postings.values_list("id", flat=True))),
            self._history_target("training_historicalresidentresearchproject", ResidentResearchProject, set(research_projects.values_list("id", flat=True))),
            self._history_target("training_historicalresidentthesis", ResidentThesis, set(resident_theses.values_list("id", flat=True))),
            self._history_target(
                "training_historicalresidentworkshopcompletion",
                ResidentWorkshopCompletion,
                set(workshop_completions.values_list("id", flat=True)),
            ),
            self._history_target(
                "training_historicalresidentmilestoneeligibility",
                ResidentMilestoneEligibility,
                set(milestone_eligibility.values_list("id", flat=True)),
            ),
            self._history_target("training_historicallogbookentry", LogbookEntry, logbook_entry_ids),
            self._history_target("training_historicallogbookreview", LogbookReview, set(logbook_reviews.values_list("id", flat=True))),
            self._history_target(
                "training_historicallogbookthresholdsnapshot",
                LogbookThresholdSnapshot,
                set(logbook_snapshots.values_list("id", flat=True)),
            ),
            self._history_target("training_historicalresidentsubmission", ResidentSubmission, submission_ids),
            self._history_target(
                "training_historicalsubmissionrequirementtemplate",
                SubmissionRequirementTemplate,
                set(submission_templates.values_list("id", flat=True)),
            ),
            self._history_target("training_historicalsubmissiondocument", SubmissionDocument, set(submission_documents.values_list("id", flat=True))),
            self._history_target("training_historicalsubmissionreview", SubmissionReview, set(submission_reviews.values_list("id", flat=True))),
            self._history_target("training_historicalsubmissioncertificate", SubmissionCertificate, set(submission_certificates.values_list("id", flat=True))),
            self._history_target("training_historicalworkshop", Workshop, purge_workshop_ids, "code"),
            self._history_target("training_historicalworkshopblock", WorkshopBlock, workshop_block_ids, "name"),
            self._history_target("training_historicalworkshoprun", WorkshopRun, workshop_run_ids),
            self._history_target("users_historicalsupervisorprofile", SupervisorProfile, set(supervisor_profiles.values_list("id", flat=True))),
            self._history_target("users_historicalsupportstaffprofile", SupportStaffProfile, set(support_staff_profiles.values_list("id", flat=True))),
            self._history_target("users_historicaladminprofile", AdminProfile, set(admin_profiles.values_list("id", flat=True))),
            self._history_target("users_historicalresidentprofile", ResidentProfile, set(resident_profiles.values_list("id", flat=True))),
            self._history_target("users_historicaldepartmentmembership", DepartmentMembership, set(department_memberships.values_list("id", flat=True))),
            self._history_target("users_historicalhospitalassignment", HospitalAssignment, set(hospital_assignments.values_list("id", flat=True))),
            self._history_target("users_historicalsupervisorresidentlink", SupervisorResidentLink, set(supervision_links.values_list("id", flat=True))),
        ]

        targets = [
            DeletionTarget("audit_activitylog", ActivityLog.objects.filter(id__in=activity_log_ids)),
            DeletionTarget("audit_auditreport", AuditReport.objects.filter(id__in=audit_report_ids)),
            DeletionTarget("bulk_bulkoperation", BulkOperation.objects.filter(id__in=bulk_operation_ids)),
            DeletionTarget("notifications_notification", Notification.objects.filter(id__in=notification_ids)),
            DeletionTarget("notifications_notificationpreference", notification_preferences),
            DeletionTarget("users_datacorrectionaudit", data_corrections),
            DeletionTarget("training_rotationcertificate", rotation_certificates),
            DeletionTarget("training_rotationcompletion", rotation_completions),
            DeletionTarget("training_submissioncertificate", submission_certificates),
            DeletionTarget("training_submissionreview", submission_reviews),
            DeletionTarget("training_submissiondocument", submission_documents),
            DeletionTarget("training_residentsubmission", submissions),
            DeletionTarget("training_logbookreview", logbook_reviews),
            DeletionTarget("training_logbookentry", logbook_entries),
            DeletionTarget("training_logbookthresholdsnapshot", logbook_snapshots),
            DeletionTarget("training_residentmilestoneeligibility", milestone_eligibility),
            DeletionTarget("training_residentworkshopcompletion", workshop_completions),
            DeletionTarget("training_residentthesis", resident_theses),
            DeletionTarget("training_residentresearchproject", research_projects),
            DeletionTarget("training_leave_request", leave_requests),
            DeletionTarget("training_deputationposting", deputation_postings),
            DeletionTarget("training_rotationassignment", rotation_assignments),
            DeletionTarget("training_workshoprun", workshop_runs),
            DeletionTarget("training_workshopblock", workshop_blocks),
            DeletionTarget("training_programmilestoneworkshoprequirement", milestone_workshop_requirements),
            DeletionTarget("training_programmilestoneresearchrequirement", milestone_research_requirements),
            DeletionTarget("training_programmilestonelogbookrequirement", milestone_logbook_requirements),
            DeletionTarget("training_programrotationrequirement", program_rotation_requirements),
            DeletionTarget("training_programmilestone", milestones),
            DeletionTarget("training_logbookthresholdconfig", logbook_configs),
            DeletionTarget("training_programpolicy", ProgramPolicy.objects.filter(program_id__in=purge_program_ids)),
            DeletionTarget("training_programrotationtemplate", templates),
            DeletionTarget("training_submissionrequirementtemplate", submission_templates),
            DeletionTarget("training_residenttrainingrecord", training_records),
            DeletionTarget("training_workshop", Workshop.objects.filter(id__in=purge_workshop_ids)),
            DeletionTarget("training_trainingprogram", TrainingProgram.objects.filter(id__in=purge_program_ids)),
            DeletionTarget("users_supervisorresidentlink", supervision_links),
            DeletionTarget("users_hospitalassignment", hospital_assignments),
            DeletionTarget("users_departmentmembership", department_memberships),
            DeletionTarget("users_supervisorprofile", supervisor_profiles),
            DeletionTarget("users_supportstaffprofile", support_staff_profiles),
            DeletionTarget("users_adminprofile", admin_profiles),
            DeletionTarget("users_residentprofile", resident_profiles),
            DeletionTarget("users_user", User.objects.filter(id__in=purge_user_ids), "username"),
            DeletionTarget(
                "rotations_hospitaldepartment",
                HospitalDepartment.objects.filter(id__in=hospital_department_ids),
            ),
            DeletionTarget("academics_department", Department.objects.filter(id__in=purge_department_ids), "code"),
            DeletionTarget("rotations_hospital", Hospital.objects.filter(id__in=purge_hospital_ids), "code"),
        ]

        targets.extend([target for target in history_targets if target is not None and target.count() > 0])

        return {
            "targets": [target for target in targets if target.count() > 0],
            "protected_admin": self._describe_user(protected_admin) if protected_admin else None,
        }

    def _select_protected_admin(
        self,
        *,
        all_users: list[User],
        purge_user_ids: set[int],
        keep_usernames: set[str],
        keep_emails: set[str],
    ) -> User | None:
        surviving_admins = [
            user
            for user in all_users
            if user.id not in purge_user_ids and (user.is_superuser or user.role in {"ADMIN", "ADMIN"})
        ]
        if surviving_admins:
            return surviving_admins[0]

        admin_candidates = [
            user
            for user in all_users
            if user.id in purge_user_ids and (user.is_superuser or user.role in {"ADMIN", "ADMIN"})
        ]
        if not admin_candidates:
            return None

        def score(user: User) -> tuple[int, int]:
            username = (user.username or "").lower()
            email = (user.email or "").lower()
            if username == "ADMIN" or email == "admin@pgsims.local":
                return (0, user.id)
            if username == "pilot_admin":
                return (1, user.id)
            return (2, user.id)

        return sorted(admin_candidates, key=score)[0]

    def _is_purge_user(self, user: User) -> bool:
        joined = _text_blob(
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.role,
            user.specialty,
            user.year,
            user.registration_number,
            user.phone_number,
        )
        return _matches(joined, USER_MARKERS) or user.has_placeholder_email

    def _is_purge_department(self, department: Department) -> bool:
        joined = _text_blob(department.code, department.name, department.description)
        return _matches(joined, DEPARTMENT_MARKERS)

    def _is_purge_hospital(self, hospital: Hospital) -> bool:
        joined = _text_blob(hospital.code, hospital.name, hospital.address, hospital.description)
        return _matches(joined, HOSPITAL_MARKERS)

    def _is_purge_program(self, program: TrainingProgram) -> bool:
        joined = _text_blob(program.code, program.name, program.description, program.notes)
        return _matches(joined, PROGRAM_MARKERS)

    def _is_purge_workshop(self, workshop: Workshop) -> bool:
        joined = _text_blob(workshop.code, workshop.name, workshop.description)
        return _matches(joined, WORKSHOP_MARKERS)

    def _notification_matches(self, notification: Notification) -> bool:
        joined = _text_blob(notification.verb, notification.title, notification.body, notification.channel, notification.metadata)
        return bool(TEXT_MARKER_RE.search(joined)) or notification.metadata.get("seed_source") == "seed_demo_data"

    def _bulk_operation_matches(self, operation: BulkOperation) -> bool:
        joined = _text_blob(operation.operation, operation.status, operation.details)
        return bool(TEXT_MARKER_RE.search(joined))

    def _activity_log_matches(self, log: ActivityLog) -> bool:
        joined = _text_blob(log.action, log.verb, log.target_repr, log.metadata)
        return bool(TEXT_MARKER_RE.search(joined))

    def _audit_report_matches(self, report: AuditReport) -> bool:
        joined = _text_blob(report.payload)
        return bool(TEXT_MARKER_RE.search(joined))

    def _describe_user(self, user: User | None) -> str | None:
        if user is None:
            return None
        return f"{user.username} <{user.email or 'no email'}> [{user.role}]"

    def _history_target(
        self,
        label: str,
        model,
        ids: set[int],
        sample_attr: str | None = None,
    ) -> DeletionTarget | None:
        history_model = getattr(model, "history", None)
        if history_model is None or not ids:
            return None
        return DeletionTarget(label, history_model.model.objects.filter(id__in=ids), sample_attr)
