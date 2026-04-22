"""
Eligibility computation engine for residency milestones.

Deterministic, pure-function-based computation of whether a resident
is ready for a given milestone (IMM / FINAL).

Trigger points:
  - On save of ResidentResearchProject or ResidentThesis
  - On save of ResidentWorkshopCompletion
  - Via nightly management command: recompute_eligibility
"""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from django.db import models

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from sims.training.models import ResidentTrainingRecord, ProgramMilestone


def compute_milestone_eligibility(
    rtr: "ResidentTrainingRecord",
    milestone: "ProgramMilestone",
) -> dict:
    """
    Pure function: compute eligibility status for a resident + milestone.

    Returns a dict with keys:
        status: "NOT_READY" | "PARTIALLY_READY" | "ELIGIBLE"
        reasons: list[str]  – unmet requirements in deterministic order
    """
    from sims.training.models import (
        LogbookEntry,
        LogbookThresholdConfig,
        ProgramMilestoneResearchRequirement,
        ProgramRotationRequirement,
        ResidentMilestoneEligibility,
        ResidentResearchProject,
        ResidentSubmission,
        ResidentThesis,
        RotationAssignment,
        RotationCompletion,
    )

    unmet: list[str] = []
    requirement_checks = 0
    resident = rtr.resident_user
    # Deterministic day reference for time-window checks.
    from django.utils import timezone
    today = timezone.now().date()

    # ---------------------------------------------------------------
    # 1. Research requirements
    # ---------------------------------------------------------------
    try:
        req_research = milestone.research_requirement
    except ProgramMilestoneResearchRequirement.DoesNotExist:
        req_research = None

    synopsis_certificate_issued = ResidentSubmission.objects.filter(
        resident_training_record=rtr,
        submission_type=ResidentSubmission.TYPE_SYNOPSIS,
        status=ResidentSubmission.STATUS_CERTIFICATE_ISSUED,
    ).exists()
    thesis_certificate_issued = ResidentSubmission.objects.filter(
        resident_training_record=rtr,
        submission_type=ResidentSubmission.TYPE_THESIS,
        status=ResidentSubmission.STATUS_CERTIFICATE_ISSUED,
    ).exists()

    if req_research:
        try:
            project = rtr.research_project
        except ResidentResearchProject.DoesNotExist:
            project = None

        if req_research.requires_synopsis_approved:
            requirement_checks += 1
            approved = (
                project is not None
                and project.status
                in (
                    ResidentResearchProject.STATUS_APPROVED_SUPERVISOR,
                    ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
                    ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
                )
            )
            approved = approved or synopsis_certificate_issued
            if not approved:
                unmet.append("Synopsis submission not yet verified")

        if req_research.requires_synopsis_submitted_to_university:
            requirement_checks += 1
            submitted = project is not None and project.status in (
                ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
                ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
            )
            submitted = submitted or synopsis_certificate_issued
            if not submitted:
                unmet.append("Synopsis not yet submitted to university")

        if req_research.requires_thesis_submitted:
            requirement_checks += 1
            try:
                thesis = rtr.thesis
                thesis_ok = thesis.status == ResidentThesis.STATUS_SUBMITTED
            except ResidentThesis.DoesNotExist:
                thesis_ok = False
            thesis_ok = thesis_ok or thesis_certificate_issued
            if not thesis_ok:
                unmet.append("Thesis submission not yet verified")

    # ---------------------------------------------------------------
    # 2. Workshop requirements
    # ---------------------------------------------------------------
    for w_req in milestone.workshop_requirements.select_related("workshop").all():
        requirement_checks += 1
        completed_count = rtr.workshop_completions.filter(
            workshop=w_req.workshop
        ).count()
        if completed_count < w_req.required_count:
            shortfall = w_req.required_count - completed_count
            unmet.append(
                f"Workshop '{w_req.workshop.name}': "
                f"{completed_count}/{w_req.required_count} completed "
                f"(need {shortfall} more)"
            )

    # ---------------------------------------------------------------
    # 3. Logbook requirements (placeholder — check if requirement defined)
    # ---------------------------------------------------------------
    approved_logbook_qs = LogbookEntry.objects.filter(
        resident_training_record=rtr,
        status=LogbookEntry.STATUS_APPROVED,
    )
    for lb_req in milestone.logbook_requirements.all():
        requirement_checks += 1
        key = (lb_req.procedure_key or lb_req.category or f"logbook_req_{lb_req.pk}").strip()
        scoped_qs = approved_logbook_qs
        if key:
            scoped_qs = scoped_qs.filter(
                models.Q(disease_area__icontains=key)
                | models.Q(diagnosis__icontains=key)
                | models.Q(clinical_presentation__icontains=key)
                | models.Q(management_plan__icontains=key)
            )
        approved_count = scoped_qs.count()
        if approved_count < lb_req.min_entries:
            unmet.append(
                f"Logbook requirement '{key}': {approved_count}/{lb_req.min_entries} approved entries"
            )

    # ---------------------------------------------------------------
    # 4. Logbook threshold configs (rotation + period based)
    # ---------------------------------------------------------------
    threshold_configs = LogbookThresholdConfig.objects.filter(is_active=True).filter(
        models.Q(program__isnull=True) | models.Q(program=rtr.program)
    ).filter(
        models.Q(department__isnull=True) | models.Q(department=resident.home_department)
    )
    for cfg in threshold_configs:
        requirement_checks += 1
        if cfg.mode == LogbookThresholdConfig.MODE_PER_PERIOD:
            days = cfg.period_days or 30
            window_start = today - timedelta(days=days - 1)
            count = approved_logbook_qs.filter(
                approved_at__date__gte=window_start,
                approved_at__date__lte=today,
            ).count()
            if count < cfg.min_approved_entries:
                unmet.append(
                    f"Logbook threshold '{cfg.name}' not met: {count}/{cfg.min_approved_entries}"
                )
            continue

        rotations = RotationAssignment.objects.filter(
            resident_training=rtr,
            status__in=[
                RotationAssignment.STATUS_ACTIVE,
                RotationAssignment.STATUS_APPROVED,
                RotationAssignment.STATUS_COMPLETED,
            ],
        )
        if not rotations.exists():
            unmet.append(f"Logbook threshold '{cfg.name}' not met: no eligible rotation found")
            continue

        unmet_per_rotation = 0
        for rotation in rotations:
            count = approved_logbook_qs.filter(rotation_assignment=rotation).count()
            if count < cfg.min_approved_entries:
                unmet_per_rotation += 1
        if unmet_per_rotation:
            unmet.append(
                f"Logbook threshold '{cfg.name}' not met for {unmet_per_rotation} rotation(s)"
            )

    # ---------------------------------------------------------------
    # 5. Rotation verification hook for FINAL readiness
    # ---------------------------------------------------------------
    if milestone.code == "FINAL":
        mandatory_rotations = ProgramRotationRequirement.objects.filter(
            program=rtr.program,
            is_mandatory=True,
        ).count()
        if mandatory_rotations > 0:
            requirement_checks += 1
            verified_rotations = RotationCompletion.objects.filter(
                rotation__resident_training=rtr,
                status=RotationCompletion.STATUS_VERIFIED,
            ).count()
            if verified_rotations < mandatory_rotations:
                unmet.append(
                    f"Verified rotations: {verified_rotations}/{mandatory_rotations} mandatory completed"
                )

    # ---------------------------------------------------------------
    # 6. Derive status from unmet count
    # ---------------------------------------------------------------
    if requirement_checks == 0:
        # No requirements defined — milestone has no blocking criteria yet
        status = ResidentMilestoneEligibility.STATUS_ELIGIBLE
    elif len(unmet) == 0:
        status = ResidentMilestoneEligibility.STATUS_ELIGIBLE
    elif len(unmet) < requirement_checks:
        status = ResidentMilestoneEligibility.STATUS_PARTIALLY_READY
    else:
        status = ResidentMilestoneEligibility.STATUS_NOT_READY

    return {"status": status, "reasons": unmet}


def recompute_for_record(rtr: "ResidentTrainingRecord") -> list[dict]:
    """
    Recompute eligibility for all active milestones of the resident's program.
    Creates or updates ResidentMilestoneEligibility rows.
    Returns list of result dicts.
    """
    from sims.training.models import ProgramMilestone, ResidentMilestoneEligibility

    results = []
    milestones = ProgramMilestone.objects.filter(
        program=rtr.program, is_active=True
    ).prefetch_related(
        "research_requirement",
        "workshop_requirements__workshop",
        "logbook_requirements",
    )

    for milestone in milestones:
        result = compute_milestone_eligibility(rtr, milestone)
        obj, created = ResidentMilestoneEligibility.objects.update_or_create(
            resident_training_record=rtr,
            milestone=milestone,
            defaults={
                "status": result["status"],
                "reasons_json": result["reasons"],
            },
        )
        results.append(
            {
                "milestone_code": milestone.code,
                "status": obj.status,
                "reasons": obj.reasons_json,
            }
        )
        logger.debug(
            "Eligibility recomputed: rtr=%d milestone=%s status=%s",
            rtr.pk,
            milestone.code,
            obj.status,
        )

    return results
