from __future__ import annotations

from datetime import date
from typing import Any

from django.db import transaction
from django.db.models import Count, Q
from rest_framework.exceptions import ValidationError

from sims.academics.models import (
    AcademicPeriod,
    EvaluationFormTemplate,
    LogbookCategory,
    ResidentTrainingRecord,
    RotationTemplate,
    SupervisorReviewQueueItem,
)
from sims.audit.models import ActivityLog
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import (
    get_resident_supervision_summary,
    get_supervisor_resident_summary,
)
from sims.users.models import ResidentProfile, SupervisorProfile


def _serialize_training_record(record: ResidentTrainingRecord | None) -> dict[str, Any] | None:
    if not record:
        return None
    return {
        "id": record.id,
        "status": record.status,
        "is_active": record.is_active,
        "training_year": record.training_year,
        "start_date": record.start_date,
        "expected_end_date": record.expected_end_date,
        "actual_end_date": record.actual_end_date,
        "program": {
            "id": record.program_id,
            "name": record.program.name if record.program else None,
            "code": record.program.code if record.program else None,
        },
        "academic_session": {
            "id": record.academic_session_id,
            "name": record.academic_session.name if record.academic_session else None,
            "code": record.academic_session.code if record.academic_session else None,
        },
        "training_site": {
            "id": record.training_site_id,
            "name": record.training_site.name if record.training_site else None,
        },
        "department": {
            "id": record.department_id,
            "name": record.department.name if record.department else None,
            "code": record.department.code if record.department else None,
        },
        "notes": record.notes,
    }


def _serialize_supervision_assignment(assignment: ResidentSupervisorAssignment | None) -> dict[str, Any] | None:
    if not assignment:
        return None
    return {
        "id": assignment.id,
        "assignment_type": assignment.assignment_type,
        "status": assignment.status,
        "start_date": assignment.start_date,
        "end_date": assignment.end_date,
        "supervisor": {
            "id": assignment.supervisor_id,
            "name": assignment.supervisor.user.get_full_name() or assignment.supervisor.user.username,
            "username": assignment.supervisor.user.username,
            "department": assignment.supervisor.department_ref.name if assignment.supervisor.department_ref else None,
            "designation": assignment.supervisor.designation_ref.name if assignment.supervisor.designation_ref else None,
            "email": assignment.supervisor.official_email or assignment.supervisor.email or None,
            "phone": assignment.supervisor.phone or None,
        },
    }


def _serialize_resident_profile(profile: ResidentProfile) -> dict[str, Any]:
    return {
        "id": profile.id,
        "name": profile.user.get_full_name() or profile.user.username,
        "username": profile.user.username,
        "department": profile.department_ref.name if profile.department_ref else None,
        "program": profile.program_ref.name if profile.program_ref else None,
        "academic_session": profile.academic_session_ref.name if profile.academic_session_ref else None,
    }


def _serialize_review_item(item: SupervisorReviewQueueItem) -> dict[str, Any]:
    return {
        "id": item.id,
        "resident_id": item.resident_id,
        "resident_name": item.resident.user.get_full_name() or item.resident.user.username,
        "supervisor_id": item.supervisor_id,
        "supervisor_name": item.supervisor.user.get_full_name() or item.supervisor.user.username,
        "training_record_id": item.training_record_id,
        "queue_type": item.queue_type,
        "status": item.status,
        "due_date": item.due_date,
        "notes": item.notes,
    }


def _prefill_training_record_fields(
    *,
    resident: ResidentProfile,
    program=None,
    academic_session=None,
    training_site=None,
    department=None,
) -> dict[str, Any]:
    return {
        "program": program or resident.program_ref,
        "academic_session": academic_session or resident.academic_session_ref,
        "training_site": training_site or resident.hospital,
        "department": department or resident.department_ref,
    }


def _validate_training_record_consistency(*, resident: ResidentProfile, program, academic_session, training_site, department):
    if department and resident.department_ref and department.id != resident.department_ref.id:
        raise ValidationError({"department": "Training record department does not match resident profile department."})
    if program and resident.program_ref and program.id != resident.program_ref.id:
        raise ValidationError({"program": "Training record program does not match resident profile program."})
    if academic_session and resident.academic_session_ref and academic_session.code != resident.academic_session_ref.code:
        raise ValidationError({"academic_session": "Training record session does not match resident profile session."})
    if training_site and resident.hospital and training_site.id != resident.hospital.id:
        raise ValidationError({"training_site": "Training site does not match resident profile hospital."})


@transaction.atomic
def create_training_record(
    *,
    resident: ResidentProfile,
    program=None,
    academic_session=None,
    training_site=None,
    department=None,
    start_date=None,
    expected_end_date=None,
    training_year=None,
    notes: str = "",
    actor=None,
) -> ResidentTrainingRecord:
    if resident.user.role != "RESIDENT":
        raise ValidationError({"resident": "Training records can only be created for resident profiles."})

    if ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).exists():
        raise ValidationError({"resident": "Resident already has an active training record."})

    fields = _prefill_training_record_fields(
        resident=resident,
        program=program,
        academic_session=academic_session,
        training_site=training_site,
        department=department,
    )
    _validate_training_record_consistency(resident=resident, **fields)

    record = ResidentTrainingRecord.objects.create(
        resident=resident,
        program=fields["program"],
        academic_session=fields["academic_session"],
        training_site=fields["training_site"],
        department=fields["department"],
        start_date=start_date,
        expected_end_date=expected_end_date,
        training_year=training_year,
        notes=notes,
        status=ResidentTrainingRecord.STATUS_ACTIVE,
        is_active=True,
        created_by=actor,
        updated_by=actor,
    )
    ActivityLog.log(
        actor=actor,
        action="create",
        verb="TRAINING_RECORD_CREATED",
        target=record,
        metadata={"resident_id": resident.id, "training_record_id": record.id, "source": "academics_service"},
    )
    return record


@transaction.atomic
def update_training_record(*, record: ResidentTrainingRecord, actor=None, **changes) -> ResidentTrainingRecord:
    before = _serialize_training_record(record)
    for field in [
        "program",
        "academic_session",
        "training_site",
        "department",
        "start_date",
        "expected_end_date",
        "actual_end_date",
        "training_year",
        "status",
        "notes",
        "is_active",
    ]:
        if field in changes:
            setattr(record, field, changes[field])
    _validate_training_record_consistency(
        resident=record.resident,
        program=record.program,
        academic_session=record.academic_session,
        training_site=record.training_site,
        department=record.department,
    )
    record.updated_by = actor
    record.save()
    ActivityLog.log(
        actor=actor,
        action="update",
        verb="TRAINING_RECORD_UPDATED",
        target=record,
        metadata={"before": before, "after": _serialize_training_record(record)},
    )
    return record


@transaction.atomic
def close_training_record(*, record: ResidentTrainingRecord, actual_end_date: date | None, status_value: str, notes: str = "", actor=None):
    if not record.is_active:
        raise ValidationError({"record": "Training record is already inactive."})
    record.actual_end_date = actual_end_date
    record.status = status_value
    record.is_active = False
    if notes:
        record.notes = f"{record.notes}\n{notes}".strip()
    record.updated_by = actor
    record.save()
    ActivityLog.log(
        actor=actor,
        action="update",
        verb="TRAINING_RECORD_CLOSED",
        target=record,
        metadata={"training_record_id": record.id, "actual_end_date": str(actual_end_date) if actual_end_date else None},
    )
    return record


def get_resident_academic_summary(*, resident: ResidentProfile) -> dict[str, Any]:
    record = (
        ResidentTrainingRecord.objects.select_related("program", "academic_session", "training_site", "department")
        .filter(resident=resident, is_active=True)
        .first()
    )
    supervision = get_resident_supervision_summary(resident=resident)
    pending_reviews = SupervisorReviewQueueItem.objects.filter(resident=resident, status=SupervisorReviewQueueItem.STATUS_PENDING).count()
    missing_items: list[str] = []
    if not record:
        missing_items.append("active_training_record")
    if not supervision["active_primary"]:
        missing_items.append("primary_supervisor")
    return {
        "resident": _serialize_resident_profile(resident),
        "training_record": _serialize_training_record(record),
        "supervision": {
            "primary_supervisor": _serialize_supervision_assignment(supervision["active_primary"]),
            "co_supervisors": [_serialize_supervision_assignment(item) for item in supervision["active_co_supervisors"]],
        },
        "review_queue": {
            "pending_count": pending_reviews,
            "items": [_serialize_review_item(item) for item in SupervisorReviewQueueItem.objects.filter(resident=resident).select_related("resident__user", "supervisor__user", "training_record")[:10]],
        },
        "readiness": {
            "has_active_training_record": bool(record),
            "has_primary_supervisor": bool(supervision["active_primary"]),
            "missing_items": missing_items,
        },
    }


def get_supervisor_academic_summary(*, supervisor: SupervisorProfile) -> dict[str, Any]:
    supervision = get_supervisor_resident_summary(supervisor=supervisor)
    resident_ids = [
        assignment.resident_id
        for assignment in supervision["active_primary_residents"] + supervision["active_co_supervised_residents"]
    ]
    resident_ids = sorted(set(resident_ids))
    active_records = {
        row.resident_id: row
        for row in ResidentTrainingRecord.objects.select_related("resident__user", "program", "department", "academic_session")
        .filter(resident_id__in=resident_ids, is_active=True)
    }
    pending_queue = SupervisorReviewQueueItem.objects.filter(
        supervisor=supervisor,
        status=SupervisorReviewQueueItem.STATUS_PENDING,
    ).select_related("resident__user", "training_record")
    residents = []
    for assignment in supervision["active_primary_residents"]:
        record = active_records.get(assignment.resident_id)
        residents.append(
            {
                "resident_id": assignment.resident_id,
                "name": assignment.resident.user.get_full_name() or assignment.resident.user.username,
                "username": assignment.resident.user.username,
                "program": record.program.name if record and record.program else assignment.resident.program_ref.name if assignment.resident.program_ref else None,
                "training_record_id": record.id if record else None,
                "training_year": record.training_year if record else None,
                "status": record.status if record else "MISSING_TRAINING_RECORD",
            }
        )
    residents_missing_records = [
        item for item in residents if item["training_record_id"] is None
    ]
    return {
        "supervisor": {
            "id": supervisor.id,
            "name": supervisor.user.get_full_name() or supervisor.user.username,
            "username": supervisor.user.username,
        },
        "assigned_residents": residents,
        "summary": {
            "assigned_residents": len(resident_ids),
            "active_training_records": len(active_records),
            "residents_missing_training_records": len(residents_missing_records),
            "pending_review_queue_items": pending_queue.count(),
        },
        "review_queue": [_serialize_review_item(item) for item in pending_queue[:20]],
        "residents_missing_training_records": residents_missing_records,
    }


def get_admin_academic_overview() -> dict[str, Any]:
    active_records = ResidentTrainingRecord.objects.filter(is_active=True).count()
    pending_review_items = SupervisorReviewQueueItem.objects.filter(status=SupervisorReviewQueueItem.STATUS_PENDING).count()
    data_quality = get_academic_data_quality()
    return {
        "cards": {
            "active_training_records": active_records,
            "residents_without_training_record": data_quality["summary"]["residents_without_training_record"],
            "residents_without_primary_supervisor": data_quality["summary"]["residents_without_primary_supervisor"],
            "pending_review_queue_items": pending_review_items,
            "active_academic_periods": AcademicPeriod.objects.filter(is_active=True).count(),
            "active_evaluation_templates": EvaluationFormTemplate.objects.filter(is_active=True).count(),
            "active_logbook_categories": LogbookCategory.objects.filter(is_active=True).count(),
            "data_quality_warnings": sum(data_quality["summary"].values()),
        }
    }


def get_academic_data_quality() -> dict[str, Any]:
    today = date.today()
    residents = ResidentProfile.objects.select_related("user", "department_ref", "program_ref", "hospital")
    active_records = list(
        ResidentTrainingRecord.objects.select_related("resident__user", "program", "academic_session", "department", "training_site")
    )
    record_map: dict[int, list[ResidentTrainingRecord]] = {}
    for record in active_records:
        record_map.setdefault(record.resident_id, []).append(record)

    def resident_item(profile: ResidentProfile) -> dict[str, Any]:
        return {
            "resident_id": profile.id,
            "name": profile.user.get_full_name() or profile.user.username,
            "username": profile.user.username,
            "link": f"/residents/{profile.user_id}",
        }

    sections: list[dict[str, Any]] = []

    def add_section(key: str, label: str, items: list[dict[str, Any]]):
        sections.append({"key": key, "label": label, "count": len(items), "items": items})

    without_record = [resident_item(r) for r in residents if not any(row.is_active for row in record_map.get(r.id, []))]
    add_section("residents_without_training_record", "Residents without Training Record", without_record)

    multiple_active = [resident_item(r) for r in residents if sum(1 for row in record_map.get(r.id, []) if row.is_active) > 1]
    add_section("residents_with_multiple_active_training_records", "Residents with Multiple Active Training Records", multiple_active)

    missing_program = []
    missing_session = []
    missing_department = []
    missing_site = []
    no_primary = []
    inactive_resident = []
    incomplete_profile = []
    department_mismatch = []
    program_mismatch = []
    active_with_actual_end = []
    completed_without_actual_end = []

    primary_resident_ids = set(
        ResidentSupervisorAssignment.objects.filter(
            is_active=True,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
        ).values_list("resident_id", flat=True)
    )

    for record in active_records:
        profile = record.resident
        if record.is_active and not record.program:
            missing_program.append(resident_item(profile))
        if record.is_active and not record.academic_session:
            missing_session.append(resident_item(profile))
        if record.is_active and not record.department:
            missing_department.append(resident_item(profile))
        if record.is_active and not record.training_site:
            missing_site.append(resident_item(profile))
        if record.is_active and record.resident_id not in primary_resident_ids:
            no_primary.append(resident_item(profile))
        if not profile.user.is_active or profile.user.is_archived:
            inactive_resident.append(resident_item(profile))
        if profile.profile_status != "COMPLETE":
            incomplete_profile.append(resident_item(profile))
        if record.department and profile.department_ref and record.department_id != profile.department_ref.id:
            department_mismatch.append(resident_item(profile))
        if record.program and profile.program_ref and record.program_id != profile.program_ref.id:
            program_mismatch.append(resident_item(profile))
        if record.is_active and record.actual_end_date:
            active_with_actual_end.append(resident_item(profile))
        if record.status == ResidentTrainingRecord.STATUS_COMPLETED and not record.actual_end_date:
            completed_without_actual_end.append(resident_item(profile))

    add_section("training_records_missing_program", "Training Records Missing Program", missing_program)
    add_section("training_records_missing_academic_session", "Training Records Missing Academic Session", missing_session)
    add_section("training_records_missing_department", "Training Records Missing Department", missing_department)
    add_section("training_records_missing_training_site", "Training Records Missing Hospital / Training Site", missing_site)
    add_section("training_records_without_primary_supervisor", "Training Records without Primary Supervisor", no_primary)
    add_section("training_records_linked_to_inactive_resident", "Training Records Linked to Inactive Resident", inactive_resident)
    add_section("training_records_linked_to_incomplete_resident_profile", "Training Records Linked to Incomplete Resident Profile", incomplete_profile)
    add_section("training_record_department_mismatch", "Training Record Department Mismatch", department_mismatch)
    add_section("training_record_program_mismatch", "Training Record Program Mismatch", program_mismatch)
    add_section("active_training_record_with_actual_end_date", "Active Training Record with Actual End Date", active_with_actual_end)
    add_section("completed_training_record_without_actual_end_date", "Completed Training Record without Actual End Date", completed_without_actual_end)

    overdue_queue = [
        _serialize_review_item(item)
        for item in SupervisorReviewQueueItem.objects.select_related("resident__user", "supervisor__user")
        .filter(status=SupervisorReviewQueueItem.STATUS_PENDING, due_date__lt=today)
    ]
    add_section("pending_review_queue_items_overdue", "Pending Review Queue Items Overdue", overdue_queue)

    supervisors_with_residents_no_queue = []
    supervisor_summary = SupervisorProfile.objects.filter(
        resident_assignments__is_active=True,
    ).annotate(
        assigned_count=Count("resident_assignments", distinct=True),
        pending_queue_count=Count(
            "review_queue_items",
            filter=Q(review_queue_items__status=SupervisorReviewQueueItem.STATUS_PENDING),
            distinct=True,
        ),
    ).select_related("user")
    for supervisor in supervisor_summary:
        if supervisor.assigned_count > 0 and supervisor.pending_queue_count == 0:
            supervisors_with_residents_no_queue.append(
                {
                    "supervisor_id": supervisor.id,
                    "name": supervisor.user.get_full_name() or supervisor.user.username,
                    "username": supervisor.user.username,
                    "link": f"/supervisors/{supervisor.user_id}",
                }
            )
    add_section(
        "supervisors_with_assigned_residents_but_no_review_queue_items",
        "Supervisors with Assigned Residents but No Review Queue Items",
        supervisors_with_residents_no_queue,
    )

    summary = {section["key"]: section["count"] for section in sections}
    summary["review_items_pending"] = SupervisorReviewQueueItem.objects.filter(status=SupervisorReviewQueueItem.STATUS_PENDING).count()
    summary["residents_without_primary_supervisor"] = len(no_primary)
    summary["residents_without_training_record"] = len(without_record)
    return {"summary": summary, "sections": sections}


@transaction.atomic
def create_review_queue_item(*, resident: ResidentProfile, supervisor: SupervisorProfile, training_record: ResidentTrainingRecord | None = None, queue_type: str, due_date=None, notes: str = "", actor=None) -> SupervisorReviewQueueItem:
    item = SupervisorReviewQueueItem.objects.create(
        resident=resident,
        supervisor=supervisor,
        training_record=training_record,
        queue_type=queue_type,
        due_date=due_date,
        notes=notes,
        created_by=actor,
        updated_by=actor,
    )
    ActivityLog.log(
        actor=actor,
        action="create",
        verb="REVIEW_QUEUE_ITEM_CREATED",
        target=item,
        metadata={"resident_id": resident.id, "supervisor_id": supervisor.id, "training_record_id": training_record.id if training_record else None},
    )
    return item


@transaction.atomic
def dismiss_review_queue_item(*, item: SupervisorReviewQueueItem, actor=None, status_value: str = SupervisorReviewQueueItem.STATUS_DISMISSED, notes: str = "") -> SupervisorReviewQueueItem:
    item.status = status_value
    if notes:
        item.notes = f"{item.notes}\n{notes}".strip()
    item.updated_by = actor
    item.save()
    ActivityLog.log(
        actor=actor,
        action="update",
        verb="REVIEW_QUEUE_ITEM_DISMISSED" if status_value == SupervisorReviewQueueItem.STATUS_DISMISSED else "REVIEW_QUEUE_ITEM_DONE",
        target=item,
        metadata={"review_queue_item_id": item.id, "status": item.status},
    )
    return item


@transaction.atomic
def seed_pilot_academics(*, actor=None) -> dict[str, int]:
    created = {
        "periods": 0,
        "training_records": 0,
        "rotation_templates": 0,
        "evaluation_templates": 0,
        "logbook_categories": 0,
        "review_queue_items": 0,
    }
    for code, name, order in [
        ("AY-2026-Y1", "Year 1 - Session 2026", 1),
        ("AY-2026-Y2", "Year 2 - Session 2026", 2),
    ]:
        _, was_created = AcademicPeriod.objects.get_or_create(
            code=code,
            defaults={"name": name, "start_date": date(2026, 7, 1), "end_date": date(2027, 6, 30), "sort_order": order, "created_by": actor, "updated_by": actor},
        )
        created["periods"] += int(was_created)
    ActivityLog.log(actor=actor, action="create", verb="PILOT_ACADEMICS_SEEDED", metadata=created)
    return created
