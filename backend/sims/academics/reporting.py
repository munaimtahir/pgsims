from datetime import date
from django.db.models import Count
from django.utils import timezone
from sims.academics.models import (
    ResidentTrainingRecord,
    SupervisorReviewQueueItem,
    EvaluationSubmission,
    LogbookEntry,
    AcademicPeriod,
    AcademicSession,
    Department,
    LogbookCategory,
)
from sims.training.models import TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.academics.services import get_academic_data_quality


def get_admin_monitoring_dashboard() -> dict:
    total_residents = ResidentProfile.objects.filter(is_archived=False).count()
    active_residents = ResidentProfile.objects.filter(is_archived=False, user__is_active=True).count()
    
    residents_with_record = ResidentTrainingRecord.objects.filter(is_active=True).values_list("resident_id", flat=True).distinct()
    residents_with_record_count = len(residents_with_record)
    residents_without_record_count = total_residents - residents_with_record_count
    
    residents_with_primary_supervisor = ResidentSupervisorAssignment.objects.filter(
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
        status="ACTIVE"
    ).values_list("resident_id", flat=True).distinct()
    residents_with_primary_supervisor_count = len(residents_with_primary_supervisor)
    residents_without_primary_supervisor_count = total_residents - residents_with_primary_supervisor_count
    
    eval_stats = dict(
        EvaluationSubmission.objects.values_list("status").annotate(count=Count("id"))
    )
    log_stats = dict(
        LogbookEntry.objects.values_list("status").annotate(count=Count("id"))
    )
    
    pending_reviews = SupervisorReviewQueueItem.objects.filter(status=SupervisorReviewQueueItem.STATUS_PENDING).count()
    overdue_reviews = SupervisorReviewQueueItem.objects.filter(
        status=SupervisorReviewQueueItem.STATUS_PENDING,
        due_date__lt=date.today()
    ).count()
    
    returned_evals = EvaluationSubmission.objects.filter(status="RETURNED").count()
    returned_logbooks = LogbookEntry.objects.filter(status="RETURNED").count()
    returned_items = returned_evals + returned_logbooks
    
    rejected_items = EvaluationSubmission.objects.filter(status="REJECTED").count() + LogbookEntry.objects.filter(status="REJECTED").count()
    
    verified_logbooks = LogbookEntry.objects.filter(status="VERIFIED").count()
    approved_evaluations = EvaluationSubmission.objects.filter(status="APPROVED").count()
    
    dept_breakdown = []
    for dept in Department.objects.filter(active=True):
        dept_residents = ResidentProfile.objects.filter(department_ref=dept, is_archived=False).values_list("id", flat=True)
        active_records = ResidentTrainingRecord.objects.filter(resident_id__in=dept_residents, is_active=True).count()
        dept_breakdown.append({
            "id": dept.id,
            "name": dept.name,
            "active_residents": len(dept_residents),
            "active_records": active_records,
        })
        
    prog_breakdown = []
    for prog in TrainingProgram.objects.filter(active=True):
        prog_residents = ResidentProfile.objects.filter(program_ref=prog, is_archived=False).values_list("id", flat=True)
        active_records = ResidentTrainingRecord.objects.filter(resident_id__in=prog_residents, is_active=True).count()
        prog_breakdown.append({
            "id": prog.id,
            "name": prog.name,
            "active_residents": len(prog_residents),
            "active_records": active_records,
        })

    dq = get_academic_data_quality()
    dq_issue_count = sum(section["count"] for section in dq.get("sections", []))
    
    return {
        "total_residents": total_residents,
        "active_residents": active_residents,
        "residents_with_training_record": residents_with_record_count,
        "residents_without_training_record": residents_without_record_count,
        "residents_with_primary_supervisor": residents_with_primary_supervisor_count,
        "residents_without_primary_supervisor": residents_without_primary_supervisor_count,
        "eval_stats": eval_stats,
        "log_stats": log_stats,
        "pending_supervisor_reviews": pending_reviews,
        "overdue_supervisor_reviews": overdue_reviews,
        "returned_items": returned_items,
        "rejected_items": rejected_items,
        "verified_logbooks": verified_logbooks,
        "approved_evaluations": approved_evaluations,
        "department_breakdown": dept_breakdown,
        "program_breakdown": prog_breakdown,
        "data_quality_issue_count": dq_issue_count,
    }


def get_supervisor_monitoring_dashboard(supervisor: SupervisorProfile) -> dict:
    assigned_residents_ids = ResidentSupervisorAssignment.objects.filter(
        supervisor=supervisor,
        status="ACTIVE"
    ).values_list("resident_id", flat=True)
    
    pending_evals = EvaluationSubmission.objects.filter(
        resident_id__in=assigned_residents_ids,
        supervisor=supervisor,
        status="SUBMITTED"
    ).count()
    
    pending_logbooks = LogbookEntry.objects.filter(
        resident_id__in=assigned_residents_ids,
        supervisor=supervisor,
        status="SUBMITTED"
    ).count()
    
    overdue_reviews = SupervisorReviewQueueItem.objects.filter(
        supervisor=supervisor,
        status=SupervisorReviewQueueItem.STATUS_PENDING,
        due_date__lt=date.today()
    ).count()
    
    returned_items = EvaluationSubmission.objects.filter(
        resident_id__in=assigned_residents_ids,
        supervisor=supervisor,
        status="RETURNED"
    ).count() + LogbookEntry.objects.filter(
        resident_id__in=assigned_residents_ids,
        supervisor=supervisor,
        status="RETURNED"
    ).count()
    
    recently_approved = EvaluationSubmission.objects.filter(
        supervisor=supervisor,
        status="APPROVED"
    ).select_related("resident__user").order_by("-approved_at")[:5]
    
    recently_verified = LogbookEntry.objects.filter(
        supervisor=supervisor,
        status="VERIFIED"
    ).select_related("resident__user").order_by("-verified_at")[:5]
    
    residents_below_req = []
    for res_id in assigned_residents_ids:
        resident = ResidentProfile.objects.select_related("user").get(id=res_id)
        below = False
        for cat in LogbookCategory.objects.filter(is_active=True):
            if cat.minimum_required and cat.minimum_required > 0:
                count = LogbookEntry.objects.filter(
                    resident=resident,
                    category=cat,
                    status="VERIFIED"
                ).count()
                if count < cat.minimum_required:
                    below = True
                    break
        if below:
            residents_below_req.append({
                "id": resident.id,
                "name": resident.user.get_full_name() or resident.user.username,
                "username": resident.user.username,
            })
            
    residents_list = []
    for res_id in assigned_residents_ids:
        resident = ResidentProfile.objects.select_related("user", "program_ref").get(id=res_id)
        tr = ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).first()
        residents_list.append({
            "resident_id": resident.id,
            "name": resident.user.get_full_name() or resident.user.username,
            "username": resident.user.username,
            "program_name": resident.program_ref.name if resident.program_ref else None,
            "training_year": tr.training_year if tr else None,
            "training_status": tr.status if tr else "NO_RECORD",
            "training_record_id": tr.id if tr else None,
        })
        
    queue_items = []
    for item in SupervisorReviewQueueItem.objects.filter(
        supervisor=supervisor,
        status=SupervisorReviewQueueItem.STATUS_PENDING
    ).select_related("resident__user"):
        queue_items.append({
            "id": item.id,
            "resident_name": item.resident.user.get_full_name() or item.resident.user.username,
            "queue_type": item.queue_type,
            "due_date": item.due_date.isoformat() if item.due_date else None,
            "notes": item.notes,
        })
        
    return {
        "assigned_residents_count": len(assigned_residents_ids),
        "pending_evaluation_reviews_count": pending_evals,
        "pending_logbook_reviews_count": pending_logbooks,
        "overdue_reviews_count": overdue_reviews,
        "returned_items_count": returned_items,
        "recently_approved_evaluations": [
            {"id": e.id, "resident_name": e.resident.user.get_full_name(), "approved_at": e.approved_at.isoformat() if e.approved_at else None}
            for e in recently_approved
        ],
        "recently_verified_logbooks": [
            {"id": l.id, "resident_name": l.resident.user.get_full_name(), "verified_at": l.verified_at.isoformat() if l.verified_at else None}
            for l in recently_verified
        ],
        "residents_below_req": residents_below_req,
        "assigned_residents": residents_list,
        "review_queue": queue_items,
    }


def get_resident_monitoring_my_progress(resident: ResidentProfile) -> dict:
    tr = ResidentTrainingRecord.objects.filter(resident=resident, is_active=True).first()
    
    primary_assignment = ResidentSupervisorAssignment.objects.filter(
        resident=resident,
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
        status="ACTIVE"
    ).select_related("supervisor__user").first()
    
    co_assignments = ResidentSupervisorAssignment.objects.filter(
        resident=resident,
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
        status="ACTIVE"
    ).select_related("supervisor__user")
    
    evals_total = EvaluationSubmission.objects.filter(resident=resident).count()
    evals_approved = EvaluationSubmission.objects.filter(resident=resident, status="APPROVED").count()
    evals_pending = EvaluationSubmission.objects.filter(resident=resident, status="SUBMITTED").count()
    evals_returned = EvaluationSubmission.objects.filter(resident=resident, status="RETURNED").count()
    
    logbooks_total = LogbookEntry.objects.filter(resident=resident).count()
    logbooks_verified = LogbookEntry.objects.filter(resident=resident, status="VERIFIED").count()
    logbooks_pending = LogbookEntry.objects.filter(resident=resident, status="SUBMITTED").count()
    logbooks_returned = LogbookEntry.objects.filter(resident=resident, status="RETURNED").count()
    
    logbooks_summary = []
    for cat in LogbookCategory.objects.filter(is_active=True):
        v_count = LogbookEntry.objects.filter(resident=resident, category=cat, status="VERIFIED").count()
        logbooks_summary.append({
            "category_id": cat.id,
            "category_name": cat.name,
            "category_type": cat.category_type,
            "verified_count": v_count,
            "minimum_required": cat.minimum_required,
        })
        
    return {
        "training_record_id": tr.id if tr else None,
        "program_name": tr.program.name if tr and tr.program else (resident.program_ref.name if resident.program_ref else None),
        "department_name": tr.department.name if tr and tr.department else (resident.department_ref.name if resident.department_ref else None),
        "training_year": tr.training_year if tr else None,
        "training_record_status": tr.status if tr else "NO_RECORD",
        "start_date": tr.start_date.isoformat() if tr and tr.start_date else None,
        "expected_end_date": tr.expected_end_date.isoformat() if tr and tr.expected_end_date else None,
        "primary_supervisor": {
            "name": primary_assignment.supervisor.user.get_full_name() or primary_assignment.supervisor.user.username,
            "email": primary_assignment.supervisor.user.email,
        } if primary_assignment else None,
        "co_supervisors": [
            {
                "id": co.supervisor.id,
                "name": co.supervisor.user.get_full_name() or co.supervisor.user.username,
            }
            for co in co_assignments
        ],
        "evaluations_total": evals_total,
        "evaluations_approved": evals_approved,
        "evaluations_pending": evals_pending,
        "evaluations_returned": evals_returned,
        "logbooks_total": logbooks_total,
        "logbooks_verified": logbooks_verified,
        "logbooks_pending": logbooks_pending,
        "logbooks_returned": logbooks_returned,
        "logbooks_summary": logbooks_summary,
    }


def get_resident_progress_report(resident_id: int) -> dict:
    resident = ResidentProfile.objects.select_related("user", "program_ref", "department_ref", "hospital").get(pk=resident_id)
    progress = get_resident_monitoring_my_progress(resident)
    return {
        "resident": {
            "id": resident.id,
            "name": resident.user.get_full_name() or resident.user.username,
            "username": resident.user.username,
            "email": resident.user.email,
            "hospital_name": resident.hospital.name if resident.hospital else None,
            "program_name": resident.program_ref.name if resident.program_ref else None,
            "department_name": resident.department_ref.name if resident.department_ref else None,
        },
        "progress": progress
    }


def get_supervisor_workload_report(supervisor_id: int) -> dict:
    supervisor = SupervisorProfile.objects.select_related("user", "department_ref", "hospital").get(pk=supervisor_id)
    workload = get_supervisor_monitoring_dashboard(supervisor)
    return {
        "supervisor": {
            "id": supervisor.id,
            "name": supervisor.user.get_full_name() or supervisor.user.username,
            "username": supervisor.user.username,
            "email": supervisor.user.email,
            "department_name": supervisor.department_ref.name if supervisor.department_ref else None,
            "hospital_name": supervisor.hospital.name if supervisor.hospital else None,
        },
        "workload": workload
    }


def get_evaluation_report(filters: dict) -> list:
    qs = EvaluationSubmission.objects.all().select_related(
        "resident__user",
        "supervisor__user",
        "template",
        "training_record__department",
        "training_record__program",
        "training_record__academic_session"
    )
    if filters.get("resident_id"):
        qs = qs.filter(resident_id=filters["resident_id"])
    if filters.get("supervisor_id"):
        qs = qs.filter(supervisor_id=filters["supervisor_id"])
    if filters.get("department_id"):
        qs = qs.filter(training_record__department_id=filters["department_id"])
    if filters.get("program_id"):
        qs = qs.filter(training_record__program_id=filters["program_id"])
    if filters.get("academic_session_id"):
        qs = qs.filter(training_record__academic_session_id=filters["academic_session_id"])
    if filters.get("status"):
        qs = qs.filter(status=filters["status"])
    if filters.get("template_id"):
        qs = qs.filter(template_id=filters["template_id"])
    if filters.get("date_from"):
        qs = qs.filter(submitted_at__date__gte=filters["date_from"])
    if filters.get("date_to"):
        qs = qs.filter(submitted_at__date__lte=filters["date_to"])

    rows = []
    for item in qs:
        pending_age = None
        if item.submitted_at and not item.approved_at:
            pending_age = (timezone.now() - item.submitted_at).days
            
        rows.append({
            "id": item.id,
            "resident_name": item.resident.user.get_full_name(),
            "supervisor_name": item.supervisor.user.get_full_name() if item.supervisor else None,
            "template_name": item.template.name,
            "department_name": item.training_record.department.name if item.training_record and item.training_record.department else None,
            "program_name": item.training_record.program.name if item.training_record and item.training_record.program else None,
            "session_name": item.training_record.academic_session.name if item.training_record and item.training_record.academic_session else None,
            "status": item.status,
            "score": str(item.score) if item.score is not None else None,
            "max_score": str(item.max_score) if item.max_score is not None else None,
            "submitted_at": item.submitted_at.isoformat() if item.submitted_at else None,
            "reviewed_at": item.reviewed_at.isoformat() if item.reviewed_at else None,
            "approved_at": item.approved_at.isoformat() if item.approved_at else None,
            "pending_age": pending_age,
        })
    return rows


def get_logbook_report(filters: dict) -> list:
    qs = LogbookEntry.objects.all().select_related(
        "resident__user",
        "supervisor__user",
        "category",
        "training_record__department",
        "training_record__program",
        "training_record__academic_session"
    ).prefetch_related("procedure_record")
    
    if filters.get("resident_id"):
        qs = qs.filter(resident_id=filters["resident_id"])
    if filters.get("supervisor_id"):
        qs = qs.filter(supervisor_id=filters["supervisor_id"])
    if filters.get("department_id"):
        qs = qs.filter(training_record__department_id=filters["department_id"])
    if filters.get("program_id"):
        qs = qs.filter(training_record__program_id=filters["program_id"])
    if filters.get("academic_session_id"):
        qs = qs.filter(training_record__academic_session_id=filters["academic_session_id"])
    if filters.get("category_id"):
        qs = qs.filter(category_id=filters["category_id"])
    if filters.get("status"):
        qs = qs.filter(status=filters["status"])
    if filters.get("date_from"):
        qs = qs.filter(entry_date__gte=filters["date_from"])
    if filters.get("date_to"):
        qs = qs.filter(entry_date__lte=filters["date_to"])

    rows = []
    for item in qs:
        pending_age = None
        if item.submitted_at and not item.verified_at:
            pending_age = (timezone.now() - item.submitted_at).days
            
        proc = item.procedure_record
        rows.append({
            "id": item.id,
            "resident_name": item.resident.user.get_full_name(),
            "supervisor_name": item.supervisor.user.get_full_name() if item.supervisor else None,
            "category_name": item.category.name,
            "category_type": item.category.category_type,
            "title": item.title,
            "entry_date": item.entry_date.isoformat() if item.entry_date else None,
            "status": item.status,
            "submitted_at": item.submitted_at.isoformat() if item.submitted_at else None,
            "verified_at": item.verified_at.isoformat() if item.verified_at else None,
            "pending_age": pending_age,
            "procedure_name": proc.procedure_name if proc else None,
            "procedure_code": proc.procedure_code if proc else None,
            "role_performed": proc.role_performed if proc else None,
            "complexity": proc.complexity if proc else None,
            "outcome": proc.outcome if proc else None,
        })
    return rows


def get_department_monitoring_summary() -> list:
    res = []
    for dept in Department.objects.filter(active=True):
        residents = ResidentProfile.objects.filter(department_ref=dept, is_archived=False).values_list("id", flat=True)
        active_records = ResidentTrainingRecord.objects.filter(resident_id__in=residents, is_active=True).count()
        supervisors = SupervisorProfile.objects.filter(department_ref=dept, is_archived=False).count()
        pending_evals = EvaluationSubmission.objects.filter(resident_id__in=residents, status="SUBMITTED").count()
        pending_logbooks = LogbookEntry.objects.filter(resident_id__in=residents, status="SUBMITTED").count()
        approved_evals = EvaluationSubmission.objects.filter(resident_id__in=residents, status="APPROVED").count()
        verified_logbooks = LogbookEntry.objects.filter(resident_id__in=residents, status="VERIFIED").count()
        res.append({
            "department_id": dept.id,
            "name": dept.name,
            "code": dept.code,
            "active_residents": len(residents),
            "supervisors": supervisors,
            "training_records": active_records,
            "pending_evaluations": pending_evals,
            "pending_logbooks": pending_logbooks,
            "approved_evaluations": approved_evals,
            "verified_logbooks": verified_logbooks,
        })
    return res


def get_program_monitoring_summary() -> list:
    res = []
    for prog in TrainingProgram.objects.filter(active=True):
        residents = ResidentProfile.objects.filter(program_ref=prog, is_archived=False).values_list("id", flat=True)
        active_records = ResidentTrainingRecord.objects.filter(resident_id__in=residents, is_active=True).count()
        pending_evals = EvaluationSubmission.objects.filter(resident_id__in=residents, status="SUBMITTED").count()
        pending_logbooks = LogbookEntry.objects.filter(resident_id__in=residents, status="SUBMITTED").count()
        approved_evals = EvaluationSubmission.objects.filter(resident_id__in=residents, status="APPROVED").count()
        verified_logbooks = LogbookEntry.objects.filter(resident_id__in=residents, status="VERIFIED").count()
        res.append({
            "program_id": prog.id,
            "name": prog.name,
            "code": prog.code,
            "active_residents": len(residents),
            "training_records": active_records,
            "pending_evaluations": pending_evals,
            "pending_logbooks": pending_logbooks,
            "approved_evaluations": approved_evals,
            "verified_logbooks": verified_logbooks,
        })
    return res


def get_session_monitoring_summary() -> list:
    res = []
    for session in AcademicSession.objects.filter(active=True):
        residents = ResidentProfile.objects.filter(academic_session_ref=session, is_archived=False).values_list("id", flat=True)
        active_records = ResidentTrainingRecord.objects.filter(resident_id__in=residents, is_active=True).count()
        pending_evals = EvaluationSubmission.objects.filter(resident_id__in=residents, status="SUBMITTED").count()
        pending_logbooks = LogbookEntry.objects.filter(resident_id__in=residents, status="SUBMITTED").count()
        res.append({
            "session_id": session.id,
            "name": session.name,
            "code": session.code,
            "active_residents": len(residents),
            "training_records": active_records,
            "pending_evaluations": pending_evals,
            "pending_logbooks": pending_logbooks,
        })
    return res
