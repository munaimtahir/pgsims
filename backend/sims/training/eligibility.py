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
from typing import TYPE_CHECKING

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
        ResidentMilestoneEligibility,
        ResidentResearchProject,
        ResidentThesis,
    )

    unmet: list[str] = []

    # ---------------------------------------------------------------
    # 1. Research requirements
    # ---------------------------------------------------------------
    try:
        req_research = milestone.research_requirement
    except Exception:
        req_research = None

    if req_research:
        try:
            project = rtr.research_project
        except ResidentResearchProject.DoesNotExist:
            project = None

        if req_research.requires_synopsis_approved:
            approved = (
                project is not None
                and project.status
                in (
                    ResidentResearchProject.STATUS_APPROVED_SUPERVISOR,
                    ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
                    ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
                )
            )
            if not approved:
                unmet.append("Synopsis not yet approved by supervisor")

        if req_research.requires_synopsis_submitted_to_university:
            submitted = project is not None and project.status in (
                ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY,
                ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY,
            )
            if not submitted:
                unmet.append("Synopsis not yet submitted to university")

        if req_research.requires_thesis_submitted:
            try:
                thesis = rtr.thesis
                thesis_ok = thesis.status == ResidentThesis.STATUS_SUBMITTED
            except ResidentThesis.DoesNotExist:
                thesis_ok = False
            if not thesis_ok:
                unmet.append("Thesis not yet submitted")

    # ---------------------------------------------------------------
    # 2. Workshop requirements
    # ---------------------------------------------------------------
    for w_req in milestone.workshop_requirements.select_related("workshop").all():
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
    for lb_req in milestone.logbook_requirements.all():
        key = lb_req.procedure_key or lb_req.category or f"logbook_req_{lb_req.pk}"
        # TODO: wire to logbook engine when available
        unmet.append(
            f"Logbook requirement '{key}': min {lb_req.min_entries} entries (logbook engine pending)"
        )

    # ---------------------------------------------------------------
    # 4. Derive status from unmet count
    # ---------------------------------------------------------------
    total_requirements = 0
    if req_research:
        if req_research.requires_synopsis_approved:
            total_requirements += 1
        if req_research.requires_synopsis_submitted_to_university:
            total_requirements += 1
        if req_research.requires_thesis_submitted:
            total_requirements += 1
    total_requirements += milestone.workshop_requirements.count()
    total_requirements += milestone.logbook_requirements.count()

    if total_requirements == 0:
        # No requirements defined — milestone has no blocking criteria yet
        status = ResidentMilestoneEligibility.STATUS_ELIGIBLE
    elif len(unmet) == 0:
        status = ResidentMilestoneEligibility.STATUS_ELIGIBLE
    elif len(unmet) < total_requirements:
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
