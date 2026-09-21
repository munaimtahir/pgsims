"""Additive, replay-safe fixtures for the three existing demonstration identities."""

import json
from datetime import timedelta
from io import BytesIO
from unittest.mock import patch
from uuid import NAMESPACE_URL, uuid5

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.test import override_settings
from django.utils import timezone
from PIL import Image, ImageDraw
from rest_framework.test import APIRequestFactory, force_authenticate

from sims.academics import services
from sims.academics.models import (
    AcademicPeriod,
    EvaluationFormTemplate,
    EvaluationSubmission,
    LogbookCategory,
    LogbookEntry,
    SupervisorReviewQueueItem,
)
from sims.academics.views import EvaluationSubmissionViewSet, LogbookEntryViewSet
from sims.audit.models import ActivityLog
from sims.rotations.models import HospitalDepartment
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import LeaveRequest, ResidentTrainingRecord, RotationAssignment
from sims.training.views import LeaveRequestViewSet, RotationAssignmentViewSet
from sims.users.models import ResidentDocument, User
from sims.users.onboarding_api import ResidentDocumentViewSet
from django.core.files.uploadedfile import SimpleUploadedFile

DATASET = "DEMO-THREE-ACCOUNTS-V1"
STATES = {
    "logbook": ["SUBMITTED", "SUBMITTED", "RETURNED", "VERIFIED"],
    "evaluation": ["SUBMITTED", "SUBMITTED", "RETURNED", "APPROVED"],
    "leave": ["SUBMITTED", "SUBMITTED", "DRAFT", "APPROVED"],
    "rotation": ["SUBMITTED", "SUBMITTED", "APPROVED", "ACTIVE"],
    "document": ["PENDING_REVIEW", "PENDING_REVIEW", "REUPLOAD_REQUIRED", "VERIFIED"],
}


class Command(BaseCommand):
    help = "Preview/apply/verify additive demo records for admin, supervisor and resident only."

    def add_arguments(self, parser):
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument("--dry-run", action="store_true")
        mode.add_argument("--apply", action="store_true")
        mode.add_argument("--verify", action="store_true")

    def handle(self, *args, **options):
        self.created_files = []
        created = 0
        try:
            # Locks serialize concurrent applies. Preview/verify perform SELECTs only.
            with override_settings(
                EMAIL_BACKEND="django.core.mail.backends.dummy.EmailBackend", FCM_ENABLED=False
            ):
                with transaction.atomic():
                    self.preflight(lock=options["apply"])
                    inventory = self.inventory()
                    self.schedule(inventory)
                    if options["apply"]:
                        self.configuration()
                        storage = ResidentDocument._meta.get_field("file").storage
                        save = storage.save

                        def track_save(*args, **kwargs):
                            name = save(*args, **kwargs)
                            self.created_files.append((storage, name))
                            return name

                        # Track storage writes separately: database rollback cannot undo files.
                        with patch.object(storage, "save", side_effect=track_save):
                            for kind, states in STATES.items():
                                for index, state in enumerate(states, 1):
                                    if inventory[(kind, index)] is None:
                                        self.create_example(kind, index, state)
                                        created += 1
                        inventory = self.inventory()
                    rows = self.rows(inventory)
                    access = (
                        self.verify_access(inventory)
                        if options["apply"] or options["verify"]
                        else {}
                    )
                    result = {
                        "dataset": DATASET,
                        "mode": (
                            "apply"
                            if options["apply"]
                            else "verify" if options["verify"] else "dry-run"
                        ),
                        "accounts": {name: user.pk for name, user in self.users.items()},
                        "resident_profile_id": self.resident.pk,
                        "supervisor_profile_id": self.supervisor.pk,
                        "training_record_id": self.training.pk,
                        "assignment_id": self.assignment.pk,
                        "created": created,
                        "existing": sum(obj is not None for obj in inventory.values()),
                        "missing": sum(obj is None for obj in inventory.values()),
                        "records": rows,
                        "read_access_checks": access,
                        "pending_academic_queue_count": SupervisorReviewQueueItem.objects.filter(
                            resident=self.resident, supervisor=self.supervisor, status="PENDING"
                        ).count(),
                    }
                    if options["verify"] and result["missing"]:
                        raise CommandError(
                            f"Incomplete dataset: {result['missing']} missing records."
                        )
        except Exception:
            for storage, name in self.created_files:
                storage.delete(name)
            raise
        self.stdout.write(json.dumps(result, indent=2, default=str))

    def preflight(self, *, lock):
        self.users = {}
        for name, role, relation in [
            ("admin", "ADMIN", "admin_profile"),
            ("supervisor", "SUPERVISOR", "supervisor_profile"),
            ("resident", "RESIDENT", "resident_profile"),
        ]:
            qs = User.objects.select_for_update() if lock else User.objects.all()
            user = qs.filter(username=name, role=role, is_active=True).first()
            if user is None or not hasattr(user, relation):
                raise CommandError(f"Need existing active {name}/{role} with its correct profile.")
            self.users[name] = user
        self.resident = self.users["resident"].resident_profile
        self.supervisor = self.users["supervisor"].supervisor_profile
        training = ResidentTrainingRecord.objects.filter(
            resident_user=self.users["resident"], active=True
        )
        if training.count() != 1:
            raise CommandError("Exactly one existing active resident training record is required.")
        self.training = training.get()
        assignments = ResidentSupervisorAssignment.objects.filter(
            resident=self.resident, assignment_type="PRIMARY", is_active=True, status="ACTIVE"
        )
        if assignments.count() != 1 or assignments.get().supervisor_id != self.supervisor.pk:
            raise CommandError("The existing primary assignment must link resident to supervisor.")
        self.assignment = assignments.get()
        self.today = timezone.localdate()
        if self.training.status != "ACTIVE" or not self.training.start_date <= self.today:
            raise CommandError("Training must be active and already started.")
        self.end = self.training.expected_end_date
        if not self.end or self.end <= self.today:
            raise CommandError(
                "Training needs a future expected end date; no profile dates will be changed."
            )
        matrix = HospitalDepartment.objects.filter(
            hospital_id=self.resident.hospital_id,
            is_active=True,
            hospital__is_active=True,
            department__active=True,
        ).order_by("pk")
        self.matrix = (
            matrix.filter(department_id=self.resident.department_ref_id).first() or matrix.first()
        )
        if self.matrix is None:
            raise CommandError(
                "Need an existing active hospital/department placement at the resident's hospital."
            )

    @staticmethod
    def key(kind, index):
        return f"{DATASET}:{kind}:{index}"

    def inventory(self):
        result = {}
        for kind in STATES:
            for index in range(1, 5):
                key = self.key(kind, index)
                if kind in ("logbook", "evaluation", "document"):
                    model = {
                        "logbook": LogbookEntry,
                        "evaluation": EvaluationSubmission,
                        "document": ResidentDocument,
                    }[kind]
                    qs = model.objects.filter(
                        extra_data__demo_dataset=DATASET, extra_data__demo_key=key
                    )
                elif kind == "leave":
                    qs = LeaveRequest.objects.filter(client_request_id=uuid5(NAMESPACE_URL, key))
                else:
                    qs = RotationAssignment.objects.filter(notes__startswith=f"[{key}] ")
                if qs.count() > 1:
                    raise CommandError(f"Duplicate marker: {key}; refusing to guess.")
                obj = qs.first()
                if obj:
                    correct = (
                        obj.resident_id == self.resident.pk
                        if kind in ("logbook", "evaluation", "document")
                        else obj.resident_training_id == self.training.pk
                    )
                    if not correct or (
                        kind in ("logbook", "evaluation")
                        and obj.supervisor_id != self.supervisor.pk
                    ):
                        raise CommandError(f"Demo ownership mismatch: {key}.")
                result[(kind, index)] = obj
        return result

    def schedule(self, inventory):
        occupied = list(
            RotationAssignment.objects.filter(resident_training=self.training)
            .exclude(status__in=["CANCELLED", "REJECTED"])
            .values_list("start_date", "end_date")
        )
        occupied += list(
            LeaveRequest.objects.filter(resident_training=self.training)
            .exclude(status="REJECTED")
            .values_list("start_date", "end_date")
        )
        self.dates = {}

        def reserve(key, start, length, latest):
            while start + timedelta(days=length - 1) <= latest:
                end = start + timedelta(days=length - 1)
                if not any(start <= b and end >= a for a, b in occupied):
                    occupied.append((start, end))
                    self.dates[key] = (start, end)
                    return
                start += timedelta(days=1)
            raise CommandError(f"No non-overlapping training dates for {key}.")

        # Active teaching rotation is deliberately in the recent past, ready to complete.
        order = (
            [("rotation", 4)]
            + [("rotation", i) for i in range(1, 4)]
            + [("leave", i) for i in range(1, 5)]
        )
        for kind, index in order:
            key = (kind, index)
            if inventory[key]:
                self.dates[key] = (inventory[key].start_date, inventory[key].end_date)
            elif kind == "rotation" and index == 4:
                reserve(
                    key,
                    max(self.training.start_date, self.today - timedelta(days=90)),
                    7,
                    self.today - timedelta(days=1),
                )
            else:
                reserve(
                    key, self.today + timedelta(days=2), 7 if kind == "rotation" else 2, self.end
                )

    def configuration(self):
        self.category = (
            LogbookCategory.objects.filter(is_active=True, category_type="PROCEDURE")
            .order_by("pk")
            .first()
        )
        if not self.category:
            self.category, _ = LogbookCategory.objects.get_or_create(
                code="DEMO-3-PROCEDURE",
                defaults={
                    "name": "Three-account demo procedures",
                    "category_type": "PROCEDURE",
                    "description": DATASET,
                },
            )
        self.template = (
            EvaluationFormTemplate.objects.filter(is_active=True, form_type="SUPERVISOR_REVIEW")
            .order_by("pk")
            .first()
        )
        if not self.template:
            self.template, _ = EvaluationFormTemplate.objects.get_or_create(
                code="DEMO-3-REVIEW",
                defaults={
                    "name": "Three-account demo review",
                    "form_type": "SUPERVISOR_REVIEW",
                    "description": DATASET,
                    "schema": {
                        "fields": [
                            {"key": "clinical_skills", "label": "Clinical skills", "type": "number"}
                        ]
                    },
                },
            )
        self.period = (
            AcademicPeriod.objects.filter(
                is_active=True, start_date__lte=self.today, end_date__gte=self.today
            )
            .order_by("pk")
            .first()
        )
        if not self.period:
            self.period, _ = AcademicPeriod.objects.get_or_create(
                code="DEMO-3-PERIOD",
                defaults={
                    "name": "Three-account demo period",
                    "start_date": self.training.start_date,
                    "end_date": self.end,
                },
            )

    def request(self, viewset, action, actor, data=None, pk=None, multipart=False):
        request = APIRequestFactory().post(
            "/demo-seed/", data or {}, format="multipart" if multipart else "json"
        )
        force_authenticate(request, user=self.users[actor])
        response = viewset.as_view({"post": action})(request, **({"pk": pk} if pk else {}))
        if response.status_code >= 400:
            raise CommandError(
                f"{viewset.__name__}.{action}: {response.status_code} {response.data}"
            )
        return response.data

    def create_example(self, kind, index, desired):
        key = self.key(kind, index)
        metadata = {"demo_dataset": DATASET, "demo_key": key}
        resident_user, supervisor_user = self.users["resident"], self.users["supervisor"]
        if kind == "logbook":
            title = [
                "Urinary catheterization",
                "Diagnostic cystoscopy",
                "Ureteric stent insertion",
                "Supervised case discussion",
            ][index - 1]
            obj = services.create_logbook_entry(
                resident=self.resident,
                category=self.category,
                supervisor=self.supervisor,
                academic_period=self.period,
                entry_date=max(self.training.start_date, self.today - timedelta(days=index)),
                title=f"[{key}] {title}",
                description="Synthetic teaching example; no actual patient.",
                case_identifier=f"DEMO-3-{index}",
                resident_reflection="Practised safe preparation and discussed the learning objectives.",
                extra_data=metadata,
                procedure_data={
                    "procedure_name": title,
                    "role_performed": "ASSISTED",
                    "complexity": "LOW",
                    "outcome": "Synthetic successful outcome",
                },
                actor=resident_user,
            )
            services.submit_logbook_entry(entry=obj, actor=resident_user)
            if desired == "RETURNED":
                services.return_logbook_entry(
                    entry=obj,
                    supervisor_comments="Clarify your role and add a learning point, then resubmit.",
                    actor=supervisor_user,
                )
            elif desired == "VERIFIED":
                services.verify_logbook_entry(
                    entry=obj,
                    supervisor_comments="Demonstration case reviewed and verified.",
                    actor=supervisor_user,
                )
        elif kind == "evaluation":
            responses = []
            for field in self.template.schema.get("fields", []):
                field_type = field.get("type", "text")
                responses.append(
                    {
                        "field_key": field["key"],
                        "field_label": field.get("label", field["key"]),
                        "field_type": field_type,
                        "value_number": 4 if field_type in ("number", "rating", "score") else None,
                        "value_text": (
                            "Synthetic demo reflection"
                            if field_type not in ("number", "rating", "score")
                            else ""
                        ),
                    }
                )
            obj = services.create_evaluation_submission(
                resident=self.resident,
                template=self.template,
                supervisor=self.supervisor,
                academic_period=self.period,
                resident_comments=f"[{key}] Clinical learning review {index}",
                extra_data=metadata,
                responses=responses,
                actor=resident_user,
            )
            services.submit_evaluation(submission=obj, actor=resident_user)
            if desired == "RETURNED":
                services.return_evaluation(
                    submission=obj,
                    supervisor_comments="Add a specific action plan and resubmit.",
                    actor=supervisor_user,
                )
            elif desired == "APPROVED":
                services.start_evaluation_review(submission=obj, actor=supervisor_user)
                services.approve_evaluation(
                    submission=obj,
                    supervisor_comments="Demo objectives achieved.",
                    score=4,
                    max_score=5,
                    actor=supervisor_user,
                )
        elif kind in ("leave", "rotation"):
            start, end = self.dates[(kind, index)]
            data = {
                "resident_training": self.training.pk,
                "start_date": str(start),
                "end_date": str(end),
            }
            if kind == "leave":
                view = LeaveRequestViewSet
                data.update(
                    leave_type=LeaveRequest.TYPE_STUDY,
                    reason=f"[{key}] Synthetic teaching leave {index}",
                    client_request_id=str(uuid5(NAMESPACE_URL, key)),
                )
                actor = "resident"
            else:
                view = RotationAssignmentViewSet
                data.update(
                    hospital_department=self.matrix.pk,
                    notes=f"[{key}] Synthetic teaching placement {index}",
                )
                actor = "admin"
            pk = self.request(view, "create", actor, data)["id"]
            if desired != "DRAFT":
                self.request(view, "submit", actor, pk=pk)
            if desired in ("APPROVED", "ACTIVE"):
                self.request(
                    view,
                    "approve" if kind == "leave" else "utrmc_approve",
                    "supervisor" if kind == "leave" else "admin",
                    pk=pk,
                )
            if desired == "ACTIVE":
                self.request(view, "activate", "admin", pk=pk)
            obj = (LeaveRequest if kind == "leave" else RotationAssignment).objects.get(pk=pk)
        else:
            obj = ResidentDocument.objects.create(
                resident=self.resident,
                title=f"[{key}] Synthetic attachment {index}",
                document_type=f"DEMO_3_{index}",
                extra_data=metadata,
            )
            output = BytesIO()
            picture = Image.new("RGB", (800, 220), "white")
            draw = ImageDraw.Draw(picture)
            draw.text((25, 30), "DEMONSTRATION ONLY - NOT A REAL DOCUMENT", fill="black")
            draw.text((25, 75), key, fill="black")
            draw.text(
                (25, 120),
                "Synthetic attachment for the existing resident demo profile.",
                fill="black",
            )
            picture.save(output, format="PNG")
            self.request(
                ResidentDocumentViewSet,
                "upload",
                "resident",
                {
                    "file": SimpleUploadedFile(
                        f"demo-three-{index}.png", output.getvalue(), content_type="image/png"
                    )
                },
                pk=obj.pk,
                multipart=True,
            )
            if desired in ("VERIFIED", "REUPLOAD_REQUIRED"):
                self.request(
                    ResidentDocumentViewSet,
                    "review",
                    "admin",
                    {
                        "status": desired,
                        "remarks": (
                            "Please upload a clearer demo image."
                            if desired == "REUPLOAD_REQUIRED"
                            else "Synthetic attachment verified."
                        ),
                    },
                    pk=obj.pk,
                )
        ActivityLog.log(
            actor=self.users["admin"],
            action="create",
            verb="DEMO_RECORD_CREATED",
            target=obj,
            metadata=metadata,
        )

    def rows(self, inventory):
        rows = []
        for (kind, index), obj in inventory.items():
            row = {
                "key": self.key(kind, index),
                "feature": kind,
                "id": obj.pk if obj else None,
                "status": obj.status if obj else "MISSING",
                "planned_initial_status": STATES[kind][index - 1],
            }
            if kind in ("rotation", "leave"):
                row.update(zip(("start_date", "end_date"), self.dates[(kind, index)]))
            rows.append(row)
        return rows

    def verify_access(self, inventory):
        """Exercise the same read handlers used by both clients without consuming tasks."""
        checks = {}
        viewsets = {
            "logbook": LogbookEntryViewSet,
            "evaluation": EvaluationSubmissionViewSet,
            "leave": LeaveRequestViewSet,
            "rotation": RotationAssignmentViewSet,
            "document": ResidentDocumentViewSet,
        }
        for role, user in self.users.items():
            checks[role] = 0
            for (kind, index), obj in inventory.items():
                if obj is None:
                    continue
                request = APIRequestFactory().get("/demo-verify/")
                force_authenticate(request, user=user)
                response = viewsets[kind].as_view({"get": "retrieve"})(request, pk=obj.pk)
                if response.status_code != 200:
                    raise CommandError(
                        f"{role} cannot read {self.key(kind, index)}: {response.status_code}."
                    )
                if kind == "document" and (
                    not obj.file or not obj.file.storage.exists(obj.file.name)
                ):
                    raise CommandError(f"Missing demo attachment: {self.key(kind, index)}.")
                checks[role] += 1
        return checks
