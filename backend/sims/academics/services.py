from __future__ import annotations

from datetime import date
from typing import Any

from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from sims.academics.models import (
    AcademicPeriod,
    EvaluationFormTemplate,
    LogbookCategory,
    ResidentTrainingRecord,
    RotationTemplate,
    SupervisorReviewQueueItem,
    EvaluationSubmission,
    EvaluationResponse,
    LogbookEntry,
    ProcedureRecord,
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

    # Combined Brick 9/10 Extra Data Quality checks
    active_res_with_record_ids = ResidentTrainingRecord.objects.filter(is_active=True).values_list("resident_id", flat=True)
    res_with_evals_ids = EvaluationSubmission.objects.values_list("resident_id", flat=True).distinct()
    res_no_evals = [
        resident_item(r) for r in residents 
        if r.id in active_res_with_record_ids and r.id not in res_with_evals_ids
    ]
    add_section("residents_with_active_record_no_evaluations", "Residents with Active Record but No Evaluations", res_no_evals)

    submitted_no_sup = [
        {"id": ev.id, "resident_id": ev.resident_id, "name": ev.resident.user.username, "link": f"/academics/evaluations/{ev.id}"}
        for ev in EvaluationSubmission.objects.filter(status="SUBMITTED", supervisor=None).select_related("resident__user")
    ]
    add_section("submitted_evaluations_without_supervisor", "Submitted Evaluations without Supervisor", submitted_no_sup)

    seven_days_ago = timezone.now() - timezone.timedelta(days=7)
    pending_beyond_threshold = [
        {"id": ev.id, "resident_id": ev.resident_id, "name": ev.resident.user.username, "link": f"/academics/evaluations/{ev.id}"}
        for ev in EvaluationSubmission.objects.filter(status="SUBMITTED", submitted_at__lt=seven_days_ago).select_related("resident__user")
    ]
    add_section("pending_evaluations_beyond_threshold", "Pending Evaluations Beyond 7 Days", pending_beyond_threshold)

    approved_missing_dates = [
        {"id": ev.id, "resident_id": ev.resident_id, "name": ev.resident.user.username, "link": f"/academics/evaluations/{ev.id}"}
        for ev in EvaluationSubmission.objects.filter(status="APPROVED").filter(Q(reviewed_at=None) | Q(approved_at=None)).select_related("resident__user")
    ]
    add_section("approved_evaluations_missing_timestamps", "Approved Evaluations Missing Review/Approval Date", approved_missing_dates)

    returned_no_comments = [
        {"id": ev.id, "resident_id": ev.resident_id, "name": ev.resident.user.username, "link": f"/academics/evaluations/{ev.id}"}
        for ev in EvaluationSubmission.objects.filter(status="RETURNED", supervisor_comments="").select_related("resident__user")
    ]
    add_section("returned_evaluations_without_supervisor_comments", "Returned Evaluations without Supervisor Comments", returned_no_comments)

    inactive_template_evals = [
        {"id": ev.id, "resident_id": ev.resident_id, "name": ev.resident.user.username, "link": f"/academics/evaluations/{ev.id}"}
        for ev in EvaluationSubmission.objects.filter(template__is_active=False).select_related("resident__user")
    ]
    add_section("evaluations_linked_to_inactive_template", "Evaluations Linked to Inactive Template", inactive_template_evals)

    eval_no_active_record = [
        {"id": ev.id, "resident_id": ev.resident_id, "name": ev.resident.user.username, "link": f"/academics/evaluations/{ev.id}"}
        for ev in EvaluationSubmission.objects.select_related("resident__user")
        if ev.resident_id not in active_res_with_record_ids
    ]
    add_section("evaluations_without_active_training_record", "Evaluations for Residents without Active Training Record", eval_no_active_record)

    evals_unassigned_supervisor = []
    for ev in EvaluationSubmission.objects.filter(status__in=["SUBMITTED", "UNDER_REVIEW", "APPROVED", "REJECTED"]).select_related("resident", "supervisor"):
        if ev.supervisor_id:
            assigned = ResidentSupervisorAssignment.objects.filter(
                resident=ev.resident,
                supervisor=ev.supervisor,
                status="ACTIVE"
            ).exists()
            if not assigned:
                evals_unassigned_supervisor.append({
                    "id": ev.id,
                    "resident_id": ev.resident_id,
                    "supervisor_id": ev.supervisor_id,
                    "link": f"/academics/evaluations/{ev.id}"
                })
    add_section("evaluation_supervisor_unassigned", "Evaluations Reviewed by Unassigned Supervisor", evals_unassigned_supervisor)

    res_with_logbooks_ids = LogbookEntry.objects.values_list("resident_id", flat=True).distinct()
    res_no_logbooks = [
        resident_item(r) for r in residents
        if r.id in active_res_with_record_ids and r.id not in res_with_logbooks_ids
    ]
    add_section("residents_with_active_record_no_logbooks", "Residents with Active Record but No Logbooks", res_no_logbooks)

    logbooks_no_sup = [
        {"id": le.id, "resident_id": le.resident_id, "name": le.resident.user.username, "link": f"/academics/logbook/{le.id}"}
        for le in LogbookEntry.objects.filter(status="SUBMITTED", supervisor=None).select_related("resident__user")
    ]
    add_section("submitted_logbooks_without_supervisor", "Submitted Logbook Entries without Supervisor", logbooks_no_sup)

    pending_logbooks_beyond_threshold = [
        {"id": le.id, "resident_id": le.resident_id, "name": le.resident.user.username, "link": f"/academics/logbook/{le.id}"}
        for le in LogbookEntry.objects.filter(status="SUBMITTED", submitted_at__lt=seven_days_ago).select_related("resident__user")
    ]
    add_section("pending_logbooks_beyond_threshold", "Pending Logbook Entries Beyond 7 Days", pending_logbooks_beyond_threshold)

    verified_missing_date = [
        {"id": le.id, "resident_id": le.resident_id, "name": le.resident.user.username, "link": f"/academics/logbook/{le.id}"}
        for le in LogbookEntry.objects.filter(status="VERIFIED", verified_at=None).select_related("resident__user")
    ]
    add_section("verified_logbooks_missing_timestamp", "Verified Logbook Entries Missing Timestamp", verified_missing_date)

    returned_logbook_no_comments = [
        {"id": le.id, "resident_id": le.resident_id, "name": le.resident.user.username, "link": f"/academics/logbook/{le.id}"}
        for le in LogbookEntry.objects.filter(status="RETURNED", supervisor_comments="").select_related("resident__user")
    ]
    add_section("returned_logbooks_without_supervisor_comments", "Returned Logbooks without Supervisor Comments", returned_logbook_no_comments)

    inactive_cat_logbooks = [
        {"id": le.id, "resident_id": le.resident_id, "name": le.resident.user.username, "link": f"/academics/logbook/{le.id}"}
        for le in LogbookEntry.objects.filter(category__is_active=False).select_related("resident__user")
    ]
    add_section("logbooks_linked_to_inactive_category", "Logbook Entries Linked to Inactive Category", inactive_cat_logbooks)

    logbook_no_active_record = [
        {"id": le.id, "resident_id": le.resident_id, "name": le.resident.user.username, "link": f"/academics/logbook/{le.id}"}
        for le in LogbookEntry.objects.select_related("resident__user")
        if le.resident_id not in active_res_with_record_ids
    ]
    add_section("logbooks_without_active_training_record", "Logbooks for Residents without Active Training Record", logbook_no_active_record)

    logbooks_unassigned_supervisor = []
    for le in LogbookEntry.objects.filter(status__in=["SUBMITTED", "VERIFIED", "REJECTED"]).select_related("resident", "supervisor"):
        if le.supervisor_id:
            assigned = ResidentSupervisorAssignment.objects.filter(
                resident=le.resident,
                supervisor=le.supervisor,
                status="ACTIVE"
            ).exists()
            if not assigned:
                logbooks_unassigned_supervisor.append({
                    "id": le.id,
                    "resident_id": le.resident_id,
                    "supervisor_id": le.supervisor_id,
                    "link": f"/academics/logbook/{le.id}"
                })
    add_section("logbook_supervisor_unassigned", "Logbooks Verified by Unassigned Supervisor", logbooks_unassigned_supervisor)

    res_below_minimum = []
    min_req_categories = LogbookCategory.objects.filter(is_active=True, minimum_required__gt=0)
    for res in residents:
        if res.id in active_res_with_record_ids:
            for cat in min_req_categories:
                cat_entries = LogbookEntry.objects.filter(resident=res, category=cat, status="VERIFIED").count()
                if cat_entries < cat.minimum_required:
                    res_below_minimum.append({
                        "resident_id": res.id,
                        "name": res.user.username,
                        "category_name": cat.name,
                        "verified_count": cat_entries,
                        "minimum_required": cat.minimum_required,
                    })
    add_section("residents_below_minimum_logbook_requirement", "Residents Below Minimum Logbook Requirement", res_below_minimum)

    res_no_activity = []
    for res in residents:
        if res.id in active_res_with_record_ids:
            has_approved_eval = EvaluationSubmission.objects.filter(resident=res, status="APPROVED").exists()
            has_verified_log = LogbookEntry.objects.filter(resident=res, status="VERIFIED").exists()
            if not has_approved_eval and not has_verified_log:
                res_no_activity.append(resident_item(res))
    add_section("residents_without_verified_academic_activity", "Residents without Verified Academic Activity", res_no_activity)

    res_with_returned = []
    for res in residents:
        if res.id in active_res_with_record_ids:
            has_returned_eval = EvaluationSubmission.objects.filter(resident=res, status="RETURNED").exists()
            has_returned_log = LogbookEntry.objects.filter(resident=res, status="RETURNED").exists()
            if has_returned_eval or has_returned_log:
                res_with_returned.append(resident_item(res))
    add_section("residents_with_pending_returned_items", "Residents with Pending Returned Items", res_with_returned)

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


# Combined Brick 9/10 Workflow Service logic
@transaction.atomic
def create_evaluation_submission(
    *,
    resident: ResidentProfile,
    template: EvaluationFormTemplate,
    supervisor: SupervisorProfile | None = None,
    academic_period: AcademicPeriod | None = None,
    resident_comments: str = "",
    extra_data: dict | None = None,
    responses: list[dict] | None = None,
    actor=None,
) -> EvaluationSubmission:
    training_record = ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).first()
    if not training_record:
        raise ValidationError({"resident": "Resident does not have an active training record."})

    primary_assignment = ResidentSupervisorAssignment.objects.filter(
        resident=resident,
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
        status="ACTIVE",
    ).first()

    is_admin = actor and actor.role == "ADMIN"
    if not primary_assignment and not is_admin:
        raise ValidationError({"resident": "Resident does not have an active primary supervisor."})

    resolved_supervisor = supervisor
    if resolved_supervisor:
        is_assigned = ResidentSupervisorAssignment.objects.filter(
            resident=resident,
            supervisor=resolved_supervisor,
            status="ACTIVE",
        ).exists()
        if not is_assigned and not is_admin:
            raise ValidationError({"supervisor": "Supervisor is not assigned to this resident."})
    else:
        if primary_assignment:
            resolved_supervisor = primary_assignment.supervisor

    submission = EvaluationSubmission.objects.create(
        resident=resident,
        training_record=training_record,
        template=template,
        supervisor=resolved_supervisor,
        academic_period=academic_period,
        status="DRAFT",
        resident_comments=resident_comments,
        extra_data=extra_data or {},
        created_by=actor,
        updated_by=actor,
    )

    if responses:
        for idx, resp in enumerate(responses):
            EvaluationResponse.objects.create(
                submission=submission,
                field_key=resp.get("field_key", ""),
                field_label=resp.get("field_label", ""),
                field_type=resp.get("field_type", ""),
                value_text=resp.get("value_text", ""),
                value_number=resp.get("value_number"),
                value_json=resp.get("value_json", {}),
                sort_order=resp.get("sort_order", idx),
            )

    ActivityLog.log(
        actor=actor,
        action="create",
        verb="EVALUATION_CREATED",
        target=submission,
        metadata={"resident_id": resident.id, "submission_id": submission.id, "old_status": None, "new_status": "DRAFT"},
    )
    return submission


@transaction.atomic
def update_evaluation_draft(
    *,
    submission: EvaluationSubmission,
    resident_comments: str | None = None,
    supervisor_comments: str | None = None,
    score: float | None = None,
    max_score: float | None = None,
    extra_data: dict | None = None,
    responses: list[dict] | None = None,
    actor=None,
) -> EvaluationSubmission:
    if submission.status not in ["DRAFT", "RETURNED"]:
        raise ValidationError({"status": "Cannot update evaluation unless it is in DRAFT or RETURNED status."})

    if resident_comments is not None:
        submission.resident_comments = resident_comments
    if supervisor_comments is not None:
        submission.supervisor_comments = supervisor_comments
    if score is not None:
        submission.score = score
    if max_score is not None:
        submission.max_score = max_score
    if extra_data is not None:
        submission.extra_data.update(extra_data)

    submission.updated_by = actor
    submission.save()

    if responses is not None:
        submission.responses.all().delete()
        for idx, resp in enumerate(responses):
            EvaluationResponse.objects.create(
                submission=submission,
                field_key=resp.get("field_key", ""),
                field_label=resp.get("field_label", ""),
                field_type=resp.get("field_type", ""),
                value_text=resp.get("value_text", ""),
                value_number=resp.get("value_number"),
                value_json=resp.get("value_json", {}),
                sort_order=resp.get("sort_order", idx),
            )

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_UPDATED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "status": submission.status},
    )
    return submission


@transaction.atomic
def submit_evaluation(*, submission: EvaluationSubmission, actor=None) -> EvaluationSubmission:
    if submission.status not in ["DRAFT", "RETURNED"]:
        raise ValidationError({"status": "Cannot submit evaluation unless it is in DRAFT or RETURNED status."})

    old_status = submission.status
    submission.status = "SUBMITTED"
    submission.submitted_at = timezone.now()
    submission.updated_by = actor
    submission.save()

    if submission.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=submission.resident,
            supervisor=submission.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
            notes__contains=f"evaluation_submission_id: {submission.id}",
        ).first()

        if not queue_item:
            SupervisorReviewQueueItem.objects.create(
                resident=submission.resident,
                supervisor=submission.supervisor,
                training_record=submission.training_record,
                queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
                status=SupervisorReviewQueueItem.STATUS_PENDING,
                notes=f"Evaluation submission review. evaluation_submission_id: {submission.id}",
                created_by=actor,
                updated_by=actor,
            )
        else:
            queue_item.status = SupervisorReviewQueueItem.STATUS_PENDING
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_SUBMITTED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "old_status": old_status, "new_status": "SUBMITTED"},
    )
    return submission


@transaction.atomic
def start_evaluation_review(*, submission: EvaluationSubmission, actor=None) -> EvaluationSubmission:
    if submission.status != "SUBMITTED":
        raise ValidationError({"status": "Cannot start review unless evaluation status is SUBMITTED."})

    is_admin = actor and actor.role == "ADMIN"
    if submission.supervisor and actor and actor.role == "SUPERVISOR":
        if submission.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can review this evaluation."})

    old_status = submission.status
    submission.status = "UNDER_REVIEW"
    submission.updated_by = actor
    submission.save()

    if submission.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=submission.resident,
            supervisor=submission.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
            notes__contains=f"evaluation_submission_id: {submission.id}",
            status=SupervisorReviewQueueItem.STATUS_PENDING,
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_IN_PROGRESS
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_REVIEW_STARTED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "old_status": old_status, "new_status": "UNDER_REVIEW"},
    )
    return submission


@transaction.atomic
def approve_evaluation(
    *,
    submission: EvaluationSubmission,
    supervisor_comments: str = "",
    score: float | None = None,
    max_score: float | None = None,
    actor=None,
) -> EvaluationSubmission:
    if submission.status not in ["SUBMITTED", "UNDER_REVIEW"]:
        raise ValidationError({"status": "Evaluation must be SUBMITTED or UNDER_REVIEW to approve."})

    is_admin = actor and actor.role == "ADMIN"
    if submission.supervisor and actor and actor.role == "SUPERVISOR":
        if submission.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can approve this evaluation."})

    old_status = submission.status
    submission.status = "APPROVED"
    submission.approved_at = timezone.now()
    submission.reviewed_at = timezone.now()
    if supervisor_comments:
        submission.supervisor_comments = supervisor_comments
    if score is not None:
        submission.score = score
    if max_score is not None:
        submission.max_score = max_score
    submission.updated_by = actor
    submission.save()

    if submission.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=submission.resident,
            supervisor=submission.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
            notes__contains=f"evaluation_submission_id: {submission.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DONE
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_APPROVED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "old_status": old_status, "new_status": "APPROVED"},
    )
    return submission


@transaction.atomic
def return_evaluation(*, submission: EvaluationSubmission, supervisor_comments: str, actor=None) -> EvaluationSubmission:
    if submission.status not in ["SUBMITTED", "UNDER_REVIEW"]:
        raise ValidationError({"status": "Evaluation must be SUBMITTED or UNDER_REVIEW to return."})

    if not supervisor_comments.strip():
        raise ValidationError({"supervisor_comments": "Supervisor comments are required when returning an evaluation."})

    is_admin = actor and actor.role == "ADMIN"
    if submission.supervisor and actor and actor.role == "SUPERVISOR":
        if submission.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can return this evaluation."})

    old_status = submission.status
    submission.status = "RETURNED"
    submission.reviewed_at = timezone.now()
    submission.supervisor_comments = supervisor_comments
    submission.updated_by = actor
    submission.save()

    if submission.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=submission.resident,
            supervisor=submission.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
            notes__contains=f"evaluation_submission_id: {submission.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DISMISSED
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_RETURNED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "old_status": old_status, "new_status": "RETURNED"},
    )
    return submission


@transaction.atomic
def reject_evaluation(*, submission: EvaluationSubmission, supervisor_comments: str = "", actor=None) -> EvaluationSubmission:
    if submission.status not in ["SUBMITTED", "UNDER_REVIEW"]:
        raise ValidationError({"status": "Evaluation must be SUBMITTED or UNDER_REVIEW to reject."})

    is_admin = actor and actor.role == "ADMIN"
    if submission.supervisor and actor and actor.role == "SUPERVISOR":
        if submission.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can reject this evaluation."})

    old_status = submission.status
    submission.status = "REJECTED"
    submission.reviewed_at = timezone.now()
    if supervisor_comments:
        submission.supervisor_comments = supervisor_comments
    submission.updated_by = actor
    submission.save()

    if submission.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=submission.resident,
            supervisor=submission.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
            notes__contains=f"evaluation_submission_id: {submission.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DONE
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_REJECTED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "old_status": old_status, "new_status": "REJECTED"},
    )
    return submission


@transaction.atomic
def cancel_evaluation(*, submission: EvaluationSubmission, actor=None) -> EvaluationSubmission:
    if submission.status not in ["DRAFT", "RETURNED"]:
        raise ValidationError({"status": "Only draft or returned evaluations can be cancelled."})

    old_status = submission.status
    submission.status = "CANCELLED"
    submission.updated_by = actor
    submission.save()

    if submission.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=submission.resident,
            supervisor=submission.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
            notes__contains=f"evaluation_submission_id: {submission.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DISMISSED
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="EVALUATION_CANCELLED",
        target=submission,
        metadata={"resident_id": submission.resident_id, "submission_id": submission.id, "old_status": old_status, "new_status": "CANCELLED"},
    )
    return submission


@transaction.atomic
def create_logbook_entry(
    *,
    resident: ResidentProfile,
    category: LogbookCategory,
    entry_date: date,
    title: str,
    description: str = "",
    case_identifier: str = "",
    patient_age: str = "",
    patient_gender: str = "",
    supervisor: SupervisorProfile | None = None,
    academic_period: AcademicPeriod | None = None,
    resident_reflection: str = "",
    extra_data: dict | None = None,
    procedure_data: dict | None = None,
    actor=None,
) -> LogbookEntry:
    training_record = ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).first()
    if not training_record:
        raise ValidationError({"resident": "Resident does not have an active training record."})

    primary_assignment = ResidentSupervisorAssignment.objects.filter(
        resident=resident,
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
        status="ACTIVE",
    ).first()

    is_admin = actor and actor.role == "ADMIN"
    if not primary_assignment and not is_admin:
        raise ValidationError({"resident": "Resident does not have an active primary supervisor."})

    resolved_supervisor = supervisor
    if resolved_supervisor:
        is_assigned = ResidentSupervisorAssignment.objects.filter(
            resident=resident,
            supervisor=resolved_supervisor,
            status="ACTIVE",
        ).exists()
        if not is_assigned and not is_admin:
            raise ValidationError({"supervisor": "Supervisor is not assigned to this resident."})
    else:
        if primary_assignment:
            resolved_supervisor = primary_assignment.supervisor

    entry = LogbookEntry.objects.create(
        resident=resident,
        training_record=training_record,
        category=category,
        supervisor=resolved_supervisor,
        academic_period=academic_period,
        entry_date=entry_date,
        title=title,
        description=description,
        case_identifier=case_identifier,
        patient_age=patient_age,
        patient_gender=patient_gender,
        status="DRAFT",
        resident_reflection=resident_reflection,
        extra_data=extra_data or {},
        created_by=actor,
        updated_by=actor,
    )

    if procedure_data:
        ProcedureRecord.objects.create(
            logbook_entry=entry,
            procedure_name=procedure_data.get("procedure_name", title),
            procedure_code=procedure_data.get("procedure_code", ""),
            role_performed=procedure_data.get("role_performed", "OBSERVED"),
            complexity=procedure_data.get("complexity", "LOW"),
            outcome=procedure_data.get("outcome", ""),
            complications=procedure_data.get("complications", ""),
        )

    ActivityLog.log(
        actor=actor,
        action="create",
        verb="LOGBOOK_ENTRY_CREATED",
        target=entry,
        metadata={"resident_id": resident.id, "entry_id": entry.id, "old_status": None, "new_status": "DRAFT"},
    )
    return entry


@transaction.atomic
def update_logbook_draft(
    *,
    entry: LogbookEntry,
    title: str | None = None,
    description: str | None = None,
    entry_date: date | None = None,
    case_identifier: str | None = None,
    patient_age: str | None = None,
    patient_gender: str | None = None,
    resident_reflection: str | None = None,
    supervisor: SupervisorProfile | None = None,
    academic_period: AcademicPeriod | None = None,
    extra_data: dict | None = None,
    procedure_data: dict | None = None,
    actor=None,
) -> LogbookEntry:
    if entry.status not in ["DRAFT", "RETURNED"]:
        raise ValidationError({"status": "Cannot update logbook entry unless it is in DRAFT or RETURNED status."})

    if title is not None:
        entry.title = title
    if description is not None:
        entry.description = description
    if entry_date is not None:
        entry.entry_date = entry_date
    if case_identifier is not None:
        entry.case_identifier = case_identifier
    if patient_age is not None:
        entry.patient_age = patient_age
    if patient_gender is not None:
        entry.patient_gender = patient_gender
    if resident_reflection is not None:
        entry.resident_reflection = resident_reflection
    if supervisor is not None:
        entry.supervisor = supervisor
    if academic_period is not None:
        entry.academic_period = academic_period
    if extra_data is not None:
        entry.extra_data.update(extra_data)

    entry.updated_by = actor
    entry.save()

    if procedure_data is not None:
        proc_record = getattr(entry, "procedure_record", None)
        if proc_record:
            for key, val in procedure_data.items():
                setattr(proc_record, key, val)
            proc_record.save()
        else:
            ProcedureRecord.objects.create(
                logbook_entry=entry,
                procedure_name=procedure_data.get("procedure_name", entry.title),
                procedure_code=procedure_data.get("procedure_code", ""),
                role_performed=procedure_data.get("role_performed", "OBSERVED"),
                complexity=procedure_data.get("complexity", "LOW"),
                outcome=procedure_data.get("outcome", ""),
                complications=procedure_data.get("complications", ""),
            )

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="LOGBOOK_ENTRY_UPDATED",
        target=entry,
        metadata={"resident_id": entry.resident_id, "entry_id": entry.id, "status": entry.status},
    )
    return entry


@transaction.atomic
def submit_logbook_entry(*, entry: LogbookEntry, actor=None) -> LogbookEntry:
    if entry.status not in ["DRAFT", "RETURNED"]:
        raise ValidationError({"status": "Cannot submit logbook entry unless it is in DRAFT or RETURNED status."})

    old_status = entry.status
    entry.status = "SUBMITTED"
    entry.submitted_at = timezone.now()
    entry.updated_by = actor
    entry.save()

    if entry.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=entry.resident,
            supervisor=entry.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
            notes__contains=f"logbook_entry_id: {entry.id}",
        ).first()

        if not queue_item:
            SupervisorReviewQueueItem.objects.create(
                resident=entry.resident,
                supervisor=entry.supervisor,
                training_record=entry.training_record,
                queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
                status=SupervisorReviewQueueItem.STATUS_PENDING,
                notes=f"Logbook entry review. logbook_entry_id: {entry.id}",
                created_by=actor,
                updated_by=actor,
            )
        else:
            queue_item.status = SupervisorReviewQueueItem.STATUS_PENDING
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="LOGBOOK_ENTRY_SUBMITTED",
        target=entry,
        metadata={"resident_id": entry.resident_id, "entry_id": entry.id, "old_status": old_status, "new_status": "SUBMITTED"},
    )
    return entry


@transaction.atomic
def verify_logbook_entry(*, entry: LogbookEntry, supervisor_comments: str = "", actor=None) -> LogbookEntry:
    if entry.status not in ["SUBMITTED"]:
        raise ValidationError({"status": "Logbook entry must be SUBMITTED to verify."})

    is_admin = actor and actor.role == "ADMIN"
    if entry.supervisor and actor and actor.role == "SUPERVISOR":
        if entry.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can verify this logbook entry."})

    old_status = entry.status
    entry.status = "VERIFIED"
    entry.verified_at = timezone.now()
    if supervisor_comments:
        entry.supervisor_comments = supervisor_comments
    entry.updated_by = actor
    entry.save()

    if hasattr(entry, "procedure_record"):
        ActivityLog.log(
            actor=actor,
            action="update",
            verb="PROCEDURE_RECORD_VERIFIED",
            target=entry.procedure_record,
            metadata={"resident_id": entry.resident_id, "logbook_entry_id": entry.id},
        )

    if entry.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=entry.resident,
            supervisor=entry.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
            notes__contains=f"logbook_entry_id: {entry.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DONE
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="LOGBOOK_ENTRY_VERIFIED",
        target=entry,
        metadata={"resident_id": entry.resident_id, "entry_id": entry.id, "old_status": old_status, "new_status": "VERIFIED"},
    )
    return entry


@transaction.atomic
def return_logbook_entry(*, entry: LogbookEntry, supervisor_comments: str, actor=None) -> LogbookEntry:
    if entry.status not in ["SUBMITTED"]:
        raise ValidationError({"status": "Logbook entry must be SUBMITTED to return."})

    if not supervisor_comments.strip():
        raise ValidationError({"supervisor_comments": "Supervisor comments are required when returning a logbook entry."})

    is_admin = actor and actor.role == "ADMIN"
    if entry.supervisor and actor and actor.role == "SUPERVISOR":
        if entry.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can return this logbook entry."})

    old_status = entry.status
    entry.status = "RETURNED"
    entry.supervisor_comments = supervisor_comments
    entry.updated_by = actor
    entry.save()

    if entry.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=entry.resident,
            supervisor=entry.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
            notes__contains=f"logbook_entry_id: {entry.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DISMISSED
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="LOGBOOK_ENTRY_RETURNED",
        target=entry,
        metadata={"resident_id": entry.resident_id, "entry_id": entry.id, "old_status": old_status, "new_status": "RETURNED"},
    )
    return entry


@transaction.atomic
def reject_logbook_entry(*, entry: LogbookEntry, supervisor_comments: str = "", actor=None) -> LogbookEntry:
    if entry.status not in ["SUBMITTED"]:
        raise ValidationError({"status": "Logbook entry must be SUBMITTED to reject."})

    is_admin = actor and actor.role == "ADMIN"
    if entry.supervisor and actor and actor.role == "SUPERVISOR":
        if entry.supervisor.user_id != actor.id:
            raise ValidationError({"supervisor": "Only the assigned supervisor or an admin can reject this logbook entry."})

    old_status = entry.status
    entry.status = "REJECTED"
    if supervisor_comments:
        entry.supervisor_comments = supervisor_comments
    entry.updated_by = actor
    entry.save()

    if entry.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=entry.resident,
            supervisor=entry.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
            notes__contains=f"logbook_entry_id: {entry.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DONE
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="LOGBOOK_ENTRY_REJECTED",
        target=entry,
        metadata={"resident_id": entry.resident_id, "entry_id": entry.id, "old_status": old_status, "new_status": "REJECTED"},
    )
    return entry


@transaction.atomic
def cancel_logbook_entry(*, entry: LogbookEntry, actor=None) -> LogbookEntry:
    if entry.status not in ["DRAFT", "RETURNED"]:
        raise ValidationError({"status": "Only draft or returned logbook entries can be cancelled."})

    old_status = entry.status
    entry.status = "CANCELLED"
    entry.updated_by = actor
    entry.save()

    if entry.supervisor:
        queue_item = SupervisorReviewQueueItem.objects.filter(
            resident=entry.resident,
            supervisor=entry.supervisor,
            queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
            notes__contains=f"logbook_entry_id: {entry.id}",
        ).first()
        if queue_item:
            queue_item.status = SupervisorReviewQueueItem.STATUS_DISMISSED
            queue_item.updated_by = actor
            queue_item.save()

    ActivityLog.log(
        actor=actor,
        action="update",
        verb="LOGBOOK_ENTRY_CANCELLED",
        target=entry,
        metadata={"resident_id": entry.resident_id, "entry_id": entry.id, "old_status": old_status, "new_status": "CANCELLED"},
    )
    return entry


def get_resident_academic_progress(*, resident: ResidentProfile) -> dict[str, Any]:
    record = ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).first()
    supervision = get_resident_supervision_summary(resident=resident)
    primary_supervisor = supervision["active_primary"]

    evals = EvaluationSubmission.objects.filter(resident=resident)
    evals_by_status = dict(evals.values_list("status").annotate(count=Count("status")))

    entries = LogbookEntry.objects.filter(resident=resident)
    logbooks_by_status = dict(entries.values_list("status").annotate(count=Count("status")))

    procedures_count = ProcedureRecord.objects.filter(logbook_entry__resident=resident).count()

    pending_returned_evals = evals.filter(status="RETURNED").count()
    pending_returned_logbooks = entries.filter(status="RETURNED").count()

    approved_evals = evals.filter(status="APPROVED").count()
    verified_logbooks = entries.filter(status="VERIFIED").count()

    categories = LogbookCategory.objects.filter(is_active=True)
    category_progress = []
    for cat in categories:
        cat_entries = entries.filter(category=cat, status="VERIFIED").count()
        category_progress.append({
            "category_id": cat.id,
            "category_name": cat.name,
            "category_type": cat.category_type,
            "minimum_required": cat.minimum_required,
            "verified_count": cat_entries,
            "is_met": (cat.minimum_required is None) or (cat_entries >= cat.minimum_required),
        })

    review_queue_pending = SupervisorReviewQueueItem.objects.filter(
        resident=resident,
        status=SupervisorReviewQueueItem.STATUS_PENDING,
    ).count()

    return {
        "training_record_status": record.status if record else None,
        "training_record_id": record.id if record else None,
        "primary_supervisor": _serialize_supervision_assignment(primary_supervisor),
        "evaluation_counts": evals_by_status,
        "logbook_counts": logbooks_by_status,
        "procedures_count": procedures_count,
        "pending_returned_evaluations": pending_returned_evals,
        "pending_returned_logbooks": pending_returned_logbooks,
        "approved_evaluations": approved_evals,
        "verified_logbooks": verified_logbooks,
        "category_progress": category_progress,
        "review_queue_pending_count": review_queue_pending,
    }


def get_supervisor_academic_workload(*, supervisor: SupervisorProfile) -> dict[str, Any]:
    supervision = get_supervisor_resident_summary(supervisor=supervisor)
    primary_residents = supervision["active_primary_residents"]
    co_supervised = supervision["active_co_supervised_residents"]
    assigned_residents = primary_residents + co_supervised
    resident_ids = [assignment.resident_id for assignment in assigned_residents]

    pending_evals = EvaluationSubmission.objects.filter(
        supervisor=supervisor,
        status__in=["SUBMITTED", "UNDER_REVIEW"],
    ).count()

    pending_logbooks = LogbookEntry.objects.filter(
        supervisor=supervisor,
        status="SUBMITTED",
    ).count()

    today = date.today()
    overdue_reviews = SupervisorReviewQueueItem.objects.filter(
        supervisor=supervisor,
        status=SupervisorReviewQueueItem.STATUS_PENDING,
        due_date__lt=today,
    ).count()

    evals = EvaluationSubmission.objects.filter(supervisor=supervisor)
    evals_by_status = dict(evals.values_list("status").annotate(count=Count("status")))

    entries = LogbookEntry.objects.filter(supervisor=supervisor)
    logbooks_by_status = dict(entries.values_list("status").annotate(count=Count("status")))

    return {
        "assigned_residents_count": len(resident_ids),
        "pending_evaluations_count": pending_evals,
        "pending_logbooks_count": pending_logbooks,
        "overdue_reviews_count": overdue_reviews,
        "evaluation_counts": evals_by_status,
        "logbook_counts": logbooks_by_status,
    }


def get_admin_academic_workflow_overview() -> dict[str, Any]:
    total_active_residents = ResidentProfile.objects.filter(user__is_active=True).count()
    residents_with_training_record = ResidentTrainingRecord.objects.filter(is_active=True).values_list("resident_id", flat=True).distinct().count()
    residents_without_training_record = total_active_residents - residents_with_training_record

    pending_evals = EvaluationSubmission.objects.filter(status__in=["SUBMITTED", "UNDER_REVIEW"]).count()
    pending_logbooks = LogbookEntry.objects.filter(status="SUBMITTED").count()

    today = date.today()
    overdue_reviews = SupervisorReviewQueueItem.objects.filter(
        status=SupervisorReviewQueueItem.STATUS_PENDING,
        due_date__lt=today,
    ).count()

    residents = ResidentProfile.objects.filter(user__is_active=True)
    missing_logbook_minimums = 0
    categories = LogbookCategory.objects.filter(is_active=True, minimum_required__gt=0)
    for res in residents:
        for cat in categories:
            cat_entries = LogbookEntry.objects.filter(resident=res, category=cat, status="VERIFIED").count()
            if cat.minimum_required and cat_entries < cat.minimum_required:
                missing_logbook_minimums += 1
                break

    dq = get_academic_data_quality()
    dq_issues_count = sum(section["count"] for section in dq["sections"])

    return {
        "total_active_residents": total_active_residents,
        "residents_with_training_records": residents_with_training_record,
        "residents_without_training_records": residents_without_training_record,
        "pending_evaluations": pending_evals,
        "pending_logbook_verifications": pending_logbooks,
        "overdue_review_items": overdue_reviews,
        "residents_missing_logbook_minimums": missing_logbook_minimums,
        "data_quality_issues_count": dq_issues_count,
    }


@transaction.atomic
def seed_pilot_academic_workflows(*, actor=None) -> dict[str, int]:
    result_academics = seed_pilot_academics(actor=actor)
    
    templates_data = [
        {
            "code": "EVAL-ROT-MED",
            "name": "Rotation Evaluation Template",
            "form_type": EvaluationFormTemplate.TYPE_ROTATION_EVALUATION,
            "description": "Standard evaluation at the end of a rotation.",
            "schema": {
                "fields": [
                    {"key": "clinical_skills", "label": "Clinical Skills", "type": "number", "min": 1, "max": 5},
                    {"key": "professionalism", "label": "Professionalism", "type": "number", "min": 1, "max": 5},
                    {"key": "overall_performance", "label": "Overall Performance", "type": "text"}
                ]
            }
        },
        {
            "code": "EVAL-SUP-REV",
            "name": "Supervisor Periodic Review",
            "form_type": EvaluationFormTemplate.TYPE_SUPERVISOR_REVIEW,
            "description": "Supervisor periodic performance review template.",
            "schema": {
                "fields": [
                    {"key": "academic_progress", "label": "Academic Progress", "type": "number", "min": 1, "max": 10},
                    {"key": "comments", "label": "Supervisor Comments", "type": "text"}
                ]
            }
        }
    ]
    
    templates_created = 0
    for td in templates_data:
        _, created = EvaluationFormTemplate.objects.get_or_create(
            code=td["code"],
            defaults={
                "name": td["name"],
                "form_type": td["form_type"],
                "description": td["description"],
                "schema": td["schema"],
                "is_active": True,
                "created_by": actor,
                "updated_by": actor,
            }
        )
        if created:
            templates_created += 1

    categories_data = [
        {
            "code": "LOG-CAT-PROC-GEN",
            "name": "General Procedures",
            "category_type": LogbookCategory.TYPE_PROCEDURE,
            "minimum_required": 5,
            "description": "Standard clinical procedures."
        },
        {
            "code": "LOG-CAT-CASE-MED",
            "name": "Internal Medicine Cases",
            "category_type": LogbookCategory.TYPE_CASE_LOG,
            "minimum_required": 10,
            "description": "Standard internal medicine cases."
        },
        {
            "code": "LOG-CAT-SKILL-GEN",
            "name": "Core Clinical Skills",
            "category_type": LogbookCategory.TYPE_SKILL,
            "minimum_required": 3,
            "description": "Core clinical skills assessments."
        }
    ]
    
    categories_created = 0
    for cd in categories_data:
        _, created = LogbookCategory.objects.get_or_create(
            code=cd["code"],
            defaults={
                "name": cd["name"],
                "category_type": cd["category_type"],
                "minimum_required": cd["minimum_required"],
                "description": cd["description"],
                "is_active": True,
                "created_by": actor,
                "updated_by": actor,
            }
        )
        if created:
            categories_created += 1

    residents = ResidentProfile.objects.all()
    supervisors = SupervisorProfile.objects.all()
    
    submissions_created = 0
    logbook_entries_created = 0
    review_items_created = 0
    
    if residents.exists() and supervisors.exists():
        resident = residents.first()
        supervisor = supervisors.first()
        
        training_record = ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).first()
        if not training_record:
            training_record = ResidentTrainingRecord.objects.create(
                resident=resident,
                program=resident.program_ref,
                academic_session=resident.academic_session_ref,
                training_site=resident.hospital,
                department=resident.department_ref,
                start_date=date(2026, 7, 1),
                expected_end_date=date(2027, 6, 30),
                training_year=1,
                status=ResidentTrainingRecord.STATUS_ACTIVE,
                is_active=True,
                created_by=actor,
                updated_by=actor,
            )
            
        assignment = ResidentSupervisorAssignment.objects.filter(resident=resident, supervisor=supervisor, status="ACTIVE").first()
        if not assignment:
            assignment = ResidentSupervisorAssignment.objects.create(
                resident=resident,
                supervisor=supervisor,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                status="ACTIVE",
                start_date=date(2026, 7, 1),
                created_by=actor,
                updated_by=actor,
            )

        period = AcademicPeriod.objects.first()
        template_rot = EvaluationFormTemplate.objects.get(code="EVAL-ROT-MED")
        cat_proc = LogbookCategory.objects.get(code="LOG-CAT-PROC-GEN")
        
        if not EvaluationSubmission.objects.filter(resident=resident, template=template_rot).exists():
            eval_draft = EvaluationSubmission.objects.create(
                resident=resident,
                training_record=training_record,
                template=template_rot,
                supervisor=supervisor,
                academic_period=period,
                status="DRAFT",
                resident_comments="I think I did well in this rotation.",
                extra_data={},
                created_by=actor,
                updated_by=actor,
            )
            EvaluationResponse.objects.create(
                submission=eval_draft,
                field_key="clinical_skills",
                field_label="Clinical Skills",
                field_type="number",
                value_number=4.00,
            )
            submissions_created += 1
            
            eval_sub = EvaluationSubmission.objects.create(
                resident=resident,
                training_record=training_record,
                template=template_rot,
                supervisor=supervisor,
                academic_period=period,
                status="SUBMITTED",
                submitted_at=timezone.now(),
                resident_comments="Submitted for evaluation.",
                extra_data={},
                created_by=actor,
                updated_by=actor,
            )
            EvaluationResponse.objects.create(
                submission=eval_sub,
                field_key="clinical_skills",
                field_label="Clinical Skills",
                field_type="number",
                value_number=4.50,
            )
            submissions_created += 1
            
            SupervisorReviewQueueItem.objects.create(
                resident=resident,
                supervisor=supervisor,
                training_record=training_record,
                queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW,
                status=SupervisorReviewQueueItem.STATUS_PENDING,
                notes=f"Evaluation submission review. evaluation_submission_id: {eval_sub.id}",
                created_by=actor,
                updated_by=actor,
            )
            review_items_created += 1
            
            eval_app = EvaluationSubmission.objects.create(
                resident=resident,
                training_record=training_record,
                template=template_rot,
                supervisor=supervisor,
                academic_period=period,
                status="APPROVED",
                submitted_at=timezone.now(),
                reviewed_at=timezone.now(),
                approved_at=timezone.now(),
                score=4.80,
                max_score=5.00,
                resident_comments="I did my best.",
                supervisor_comments="Excellent performance on all fronts.",
                extra_data={},
                created_by=actor,
                updated_by=actor,
            )
            EvaluationResponse.objects.create(
                submission=eval_app,
                field_key="clinical_skills",
                field_label="Clinical Skills",
                field_type="number",
                value_number=4.80,
            )
            submissions_created += 1

        if not LogbookEntry.objects.filter(resident=resident, category=cat_proc).exists():
            log_draft = LogbookEntry.objects.create(
                resident=resident,
                training_record=training_record,
                category=cat_proc,
                supervisor=supervisor,
                academic_period=period,
                entry_date=date(2026, 7, 10),
                title="Suturing a laceration",
                description="Performed simple interrupted suturing on a forearm laceration.",
                status="DRAFT",
                resident_reflection="Need to work on spacing consistency.",
                created_by=actor,
                updated_by=actor,
            )
            ProcedureRecord.objects.create(
                logbook_entry=log_draft,
                procedure_name="Suturing",
                procedure_code="CPT-12001",
                role_performed="PERFORMED_UNDER_SUPERVISION",
                complexity="LOW",
                outcome="SUCCESSFUL",
            )
            logbook_entries_created += 1
            
            log_sub = LogbookEntry.objects.create(
                resident=resident,
                training_record=training_record,
                category=cat_proc,
                supervisor=supervisor,
                academic_period=period,
                entry_date=date(2026, 7, 12),
                title="Intubation in ER",
                description="Rapid sequence intubation in emergency department.",
                status="SUBMITTED",
                submitted_at=timezone.now(),
                resident_reflection="Good view of vocal cords.",
                created_by=actor,
                updated_by=actor,
            )
            ProcedureRecord.objects.create(
                logbook_entry=log_sub,
                procedure_name="Intubation",
                procedure_code="CPT-31500",
                role_performed="PERFORMED_UNDER_SUPERVISION",
                complexity="MODERATE",
                outcome="SUCCESSFUL",
            )
            logbook_entries_created += 1
            
            SupervisorReviewQueueItem.objects.create(
                resident=resident,
                supervisor=supervisor,
                training_record=training_record,
                queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW,
                status=SupervisorReviewQueueItem.STATUS_PENDING,
                notes=f"Logbook entry review. logbook_entry_id: {log_sub.id}",
                created_by=actor,
                updated_by=actor,
            )
            review_items_created += 1
            
            log_ver = LogbookEntry.objects.create(
                resident=resident,
                training_record=training_record,
                category=cat_proc,
                supervisor=supervisor,
                academic_period=period,
                entry_date=date(2026, 7, 14),
                title="Central Line Placement",
                description="Placed ultrasound-guided internal jugular central venous catheter.",
                status="VERIFIED",
                submitted_at=timezone.now(),
                verified_at=timezone.now(),
                resident_reflection="Smooth procedure, no complications.",
                supervisor_comments="Well executed with aseptic technique.",
                created_by=actor,
                updated_by=actor,
            )
            ProcedureRecord.objects.create(
                logbook_entry=log_ver,
                procedure_name="Central Line",
                procedure_code="CPT-36556",
                role_performed="PERFORMED_INDEPENDENTLY",
                complexity="HIGH",
                outcome="SUCCESSFUL",
            )
            logbook_entries_created += 1

    counts = {
        "periods": result_academics.get("periods", 0),
        "evaluation_templates": templates_created,
        "logbook_categories": categories_created,
        "evaluation_submissions": submissions_created,
        "logbook_entries": logbook_entries_created,
        "review_queue_items": review_items_created,
    }
    ActivityLog.log(actor=actor, action="create", verb="PILOT_ACADEMIC_WORKFLOWS_SEEDED", metadata=counts)
    return counts

