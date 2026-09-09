"""Seed marked, repeatable workflow records for the institutional Urology demo."""

from datetime import date, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from sims.academics.models import AcademicPeriod, EvaluationFormTemplate, LogbookCategory
from sims.academics.services import (
    approve_evaluation,
    create_evaluation_submission,
    create_logbook_entry,
    return_evaluation,
    return_logbook_entry,
    start_evaluation_review,
    submit_evaluation,
    submit_logbook_entry,
    verify_logbook_entry,
)
from sims.rotations.models import HospitalDepartment
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import (
    DeputationPosting,
    LeaveRequest,
    ResidentResearchProject,
    ResidentTrainingRecord,
    RotationAssignment,
)
from sims.users.models import ResidentDocument, ResidentDocumentRequirement, ResidentProfile


MARKER = "[DEMO-UROLOGY-20260910]"
DATASET = "urology_institutional_demo_20260910"


class Command(BaseCommand):
    help = "Seed idempotent, clearly marked Urology supervisor approval demo records."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Validate and report without writing.")
        parser.add_argument("--cleanup", action="store_true", help="Delete only records created by this seeder.")

    def handle(self, *args, **options):
        if options["dry_run"] and options["cleanup"]:
            raise CommandError("Use either --dry-run or --cleanup, not both.")
        if options["cleanup"]:
            with transaction.atomic():
                result = self.cleanup()
            self.report(result)
            return
        with transaction.atomic():
            result = self.seed(dry_run=options["dry_run"])
            if options["dry_run"]:
                transaction.set_rollback(True)
        self.report(result)

    def report(self, result):
        for key, value in result.items():
            self.stdout.write(f"{key}: {value}")

    def residents(self):
        qs = ResidentProfile.objects.filter(
            user__is_active=True,
            program_ref__code="MS-URO",
        ).select_related("user", "program_ref")
        return [
            profile
            for profile in qs.order_by("user__username", "user_id")
            if ResidentSupervisorAssignment.objects.filter(
                resident=profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                status="ACTIVE",
            ).select_related("supervisor__user").exists()
        ]

    def assignment(self, resident):
        return ResidentSupervisorAssignment.objects.filter(
            resident=resident,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            status="ACTIVE",
        ).select_related("supervisor__user").first()

    def marker(self, **extra):
        return {"demo_seed": True, "demo_dataset": DATASET, **extra}

    def seed(self, *, dry_run=False):
        residents = self.residents()
        if len(residents) < 9:
            raise CommandError(f"Need at least 9 assigned MS-URO residents; found {len(residents)}.")

        result = {
            "dataset": DATASET,
            "eligible_ms_residents": len(residents),
            "logbook_pending": 0,
            "logbook_approved": 0,
            "logbook_returned": 0,
            "evaluation_pending": 0,
            "evaluation_approved": 0,
            "evaluation_returned": 0,
            "research_pending": 0,
            "research_approved": 0,
            "research_returned": 0,
            "leave_records": 0,
            "rotation_pending": 0,
            "rotation_approved": 0,
            "deputation_records": 0,
            "documents_available": ResidentDocumentRequirement.objects.filter(is_active=True).count(),
            "dry_run": dry_run,
        }

        category = self.get_category(dry_run)
        template = self.get_template(dry_run)
        period = self.get_period(dry_run)

        procedures = [
            ("Urinary catheterization", "Performed under supervision", "PENDING"),
            ("Diagnostic cystoscopy", "Assisted under supervision", "PENDING"),
            ("Ureteric stent insertion", "Performed under supervision", "PENDING"),
            ("Suprapubic catheterization", "Performed under supervision", "PENDING"),
            ("Ureteroscopy and lithotripsy", "Performed under supervision", "APPROVED"),
            ("TURP", "Assisted under supervision", "RETURNED"),
        ]
        for index, (procedure, role, desired) in enumerate(procedures):
            resident = residents[index]
            if dry_run:
                result[f"logbook_{index + 1}"] = f"{resident.user.username}: {desired}"
                result[f"logbook_{desired.lower()}"] += 1
                continue
            existing = self.marked_logbook(resident, procedure)
            if existing:
                result[f"logbook_{desired.lower()}"] += int(existing.status == {"PENDING": "SUBMITTED", "APPROVED": "VERIFIED", "RETURNED": "RETURNED"}[desired])
                continue
            assignment = self.assignment(resident)
            entry = create_logbook_entry(
                resident=resident,
                category=category,
                entry_date=date(2026, 9, 1) - timedelta(days=index * 2),
                title=f"{procedure} {MARKER}",
                description=f"Synthetic de-identified Urology teaching case. {MARKER}",
                case_identifier=f"DEMO-URO-{index + 1:03d}",
                patient_age="Adult",
                patient_gender="Not recorded",
                supervisor=assignment.supervisor,
                resident_reflection="Demonstration record for supervised procedural learning.",
                extra_data=self.marker(workflow="logbook", stable_key=f"logbook-{index + 1}"),
                procedure_data={
                    "procedure_name": procedure,
                    "procedure_code": f"DEMO-URO-PROC-{index + 1:02d}",
                    "role_performed": "PERFORMED_UNDER_SUPERVISION" if "Performed" in role else "ASSISTED",
                    "complexity": "MODERATE",
                    "outcome": "Completed without complication (synthetic demo record).",
                },
                actor=resident.user,
            )
            submit_logbook_entry(entry=entry, actor=resident.user)
            if desired == "APPROVED":
                verify_logbook_entry(entry=entry, supervisor_comments="Procedure reviewed. Appropriate level of participation documented.", actor=assignment.supervisor.user)
                result["logbook_approved"] += 1
            elif desired == "RETURNED":
                return_logbook_entry(entry=entry, supervisor_comments="Please clarify your operative role and complete the procedure details before resubmission.", actor=assignment.supervisor.user)
                result["logbook_returned"] += 1
            else:
                result["logbook_pending"] += 1

        for index, desired in enumerate(("PENDING", "PENDING", "APPROVED", "RETURNED")):
            resident = residents[index + 2]
            if dry_run:
                result[f"evaluation_{index + 1}"] = f"{resident.user.username}: {desired}"
                result[f"evaluation_{desired.lower()}"] += 1
                continue
            submission = self.marked_evaluation(resident, index)
            if submission:
                result[f"evaluation_{desired.lower()}"] += 1
                continue
            assignment = self.assignment(resident)
            submission = create_evaluation_submission(
                resident=resident,
                template=template,
                supervisor=assignment.supervisor,
                academic_period=period,
                resident_comments=f"Periodic Urology progress review. {MARKER}",
                extra_data=self.marker(workflow="evaluation", stable_key=f"evaluation-{index + 1}"),
                responses=[
                    {"field_key": "clinical_skills", "field_label": "Clinical Skills", "field_type": "number", "value_number": 4.0 + (index / 10)},
                    {"field_key": "professionalism", "field_label": "Professionalism", "field_type": "number", "value_number": 4.5},
                ],
                actor=resident.user,
            )
            submit_evaluation(submission=submission, actor=resident.user)
            if desired == "APPROVED":
                start_evaluation_review(submission=submission, actor=assignment.supervisor.user)
                approve_evaluation(submission=submission, supervisor_comments="Strong clinical progress demonstrated.", score=4.5, max_score=5, actor=assignment.supervisor.user)
                result["evaluation_approved"] += 1
            elif desired == "RETURNED":
                return_evaluation(submission=submission, supervisor_comments="Please add a clearer reflection and action plan before resubmission.", actor=assignment.supervisor.user)
                result["evaluation_returned"] += 1
            else:
                result["evaluation_pending"] += 1

        research_specs = (("PENDING", 6), ("RETURNED", 7), ("APPROVED", 8))
        for desired, index in research_specs:
            resident = residents[index]
            if dry_run:
                result[f"research_{desired.lower()}"] += 1
                continue
            training = ResidentTrainingRecord.objects.filter(resident_user=resident.user, active=True).first()
            if not training:
                continue
            project = ResidentResearchProject.objects.filter(
                resident_training_record=training,
                title__endswith=MARKER,
            ).first()
            if not project:
                if ResidentResearchProject.objects.filter(resident_training_record=training).exists():
                    continue
                assignment = self.assignment(resident)
                project = ResidentResearchProject.objects.create(
                    resident_training_record=training,
                    title=f"Urological outcomes in supervised stone disease {MARKER}",
                    topic_area="Endourology",
                    supervisor=assignment.supervisor.user,
                    status=ResidentResearchProject.STATUS_DRAFT,
                )
                project.transition_to(ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR, actor=resident.user)
                if desired == "APPROVED":
                    project.transition_to(ResidentResearchProject.STATUS_APPROVED_SUPERVISOR, actor=assignment.supervisor.user)
                elif desired == "RETURNED":
                    project.supervisor_feedback = "Please refine the methodology and resubmit the synopsis."
                    project.save(update_fields=["supervisor_feedback", "updated_at"])
                    project.transition_to(ResidentResearchProject.STATUS_DRAFT, actor=assignment.supervisor.user)
            result[f"research_{desired.lower()}"] += 1

        # Leave and deputation are admin/UTRMC approval workflows, not supervisor queues.
        for index, desired in enumerate(("SUBMITTED", "APPROVED", "REJECTED")):
            resident = residents[index]
            if not dry_run:
                training = ResidentTrainingRecord.objects.filter(resident_user=resident.user, active=True).first()
                if training and not LeaveRequest.objects.filter(reason__contains=MARKER, resident_training=training).exists():
                    LeaveRequest.objects.create(
                        resident_training=training, leave_type=LeaveRequest.TYPE_STUDY,
                        start_date=date(2026, 9, 15) + timedelta(days=index * 3),
                        end_date=date(2026, 9, 16) + timedelta(days=index * 3),
                        reason=f"Academic leave request for demonstration approval. {MARKER}",
                        status=desired,
                    )
            result["leave_records"] += 1

        rotation_specs = (("SUBMITTED", 9), ("APPROVED", 10))
        template_names = ("Part II — General Surgery", "Renal Transplantation")
        for index, (desired, resident_index) in enumerate(rotation_specs):
            resident = residents[resident_index]
            result_key = "rotation_pending" if desired == "SUBMITTED" else "rotation_approved"
            if dry_run:
                result[result_key] += 1
                continue
            training = ResidentTrainingRecord.objects.filter(resident_user=resident.user, active=True).first()
            hospital_department = HospitalDepartment.objects.filter(
                hospital=resident.hospital,
                department__name__icontains="General Surgery" if index == 0 else "Urology",
            ).first()
            template = resident.program_ref.rotation_templates.filter(name=template_names[index], active=True).first()
            if not training or not hospital_department or not template:
                continue
            if not RotationAssignment.objects.filter(notes__contains=MARKER, resident_training=training).exists():
                assignment = self.assignment(resident)
                start = date(2026, 10, 1) + timedelta(days=index * 70)
                RotationAssignment.objects.create(
                    resident_training=training,
                    hospital_department=hospital_department,
                    template=template,
                    start_date=start,
                    end_date=start + timedelta(days=template.duration_weeks * 7),
                    status=desired,
                    notes=f"Curriculum rotation approval demonstration. {MARKER}",
                    requested_by=resident.user,
                    approved_by_hod=assignment.supervisor.user if desired == "APPROVED" else None,
                    approved_at=timezone.now() if desired == "APPROVED" else None,
                    submitted_at=timezone.now(),
                )
            result[result_key] += 1

        return result

    def get_category(self, dry_run):
        if dry_run:
            return LogbookCategory(name="demo", code="DEMO")
        return LogbookCategory.objects.get_or_create(
            code="DEMO-UROLOGY-PROCEDURES",
            defaults={"name": "Urology Demonstration Procedures", "category_type": LogbookCategory.TYPE_PROCEDURE, "description": MARKER},
        )[0]

    def get_template(self, dry_run):
        if dry_run:
            return EvaluationFormTemplate(name="demo", code="DEMO", form_type=EvaluationFormTemplate.TYPE_SUPERVISOR_REVIEW)
        return EvaluationFormTemplate.objects.get_or_create(
            code="DEMO-UROLOGY-SUPERVISOR-REVIEW",
            defaults={"name": "Urology Demonstration Supervisor Review", "form_type": EvaluationFormTemplate.TYPE_SUPERVISOR_REVIEW, "description": MARKER, "schema": {"fields": [{"key": "clinical_skills", "label": "Clinical Skills", "type": "number"}]}},
        )[0]

    def get_period(self, dry_run):
        if dry_run:
            return AcademicPeriod(name="demo", code="DEMO")
        return AcademicPeriod.objects.get_or_create(
            code="DEMO-UROLOGY-2026",
            defaults={"name": "Urology Demonstration Period 2026", "start_date": date(2026, 7, 1), "end_date": date(2027, 6, 30), "sort_order": 99},
        )[0]

    def marked_logbook(self, resident, procedure):
        from sims.academics.models import LogbookEntry
        return LogbookEntry.objects.filter(resident=resident, title__contains=procedure, extra_data__demo_seed=True).first()

    def marked_evaluation(self, resident, index):
        from sims.academics.models import EvaluationSubmission
        return EvaluationSubmission.objects.filter(resident=resident, extra_data__stable_key=f"evaluation-{index + 1}").first()

    def cleanup(self):
        from sims.academics.models import EvaluationSubmission, LogbookEntry
        result = {}
        result["logbook_entries"] = LogbookEntry.objects.filter(extra_data__demo_seed=True).delete()[0]
        result["evaluation_submissions"] = EvaluationSubmission.objects.filter(extra_data__demo_seed=True).delete()[0]
        result["research_projects"] = ResidentResearchProject.objects.filter(title__endswith=MARKER).delete()[0]
        result["leave_requests"] = LeaveRequest.objects.filter(reason__contains=MARKER).delete()[0]
        result["rotation_assignments"] = RotationAssignment.objects.filter(notes__contains=MARKER).delete()[0]
        result["deputation_postings"] = DeputationPosting.objects.filter(notes__contains=MARKER).delete()[0]
        result["documents"] = ResidentDocument.objects.filter(extra_data__demo_seed=True).delete()[0]
        result["demo_category"] = LogbookCategory.objects.filter(code="DEMO-UROLOGY-PROCEDURES").delete()[0]
        result["demo_template"] = EvaluationFormTemplate.objects.filter(code="DEMO-UROLOGY-SUPERVISOR-REVIEW").delete()[0]
        result["demo_period"] = AcademicPeriod.objects.filter(code="DEMO-UROLOGY-2026").delete()[0]
        return result
