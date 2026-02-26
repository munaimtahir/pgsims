"""Rotation policy services (single source of truth)."""

from dataclasses import dataclass
from typing import Optional

from django.utils import timezone


@dataclass(frozen=True)
class RotationOverrideDecision:
    requires_utrmc_approval: bool
    reason: Optional[str] = None


def evaluate_rotation_override_policy(pg, hospital, department) -> RotationOverrideDecision:
    """Read-only policy evaluation for a proposed/current rotation destination."""
    if not (pg and hospital and department):
        return RotationOverrideDecision(False)

    home_hospital = getattr(pg, "home_hospital", None)
    home_department = getattr(pg, "home_department", None)
    if not home_hospital or hospital == home_hospital:
        return RotationOverrideDecision(False)

    from sims.rotations.models import HospitalDepartment

    available_at_home = HospitalDepartment.objects.filter(
        hospital=home_hospital,
        department=department,
        is_active=True,
    ).exists()

    if home_department and department == home_department:
        return RotationOverrideDecision(
            True,
            "Home department outside home hospital requires UTRMC approval.",
        )
    if available_at_home:
        return RotationOverrideDecision(
            True,
            "Destination department is available in home hospital.",
        )
    return RotationOverrideDecision(False)


def validate_rotation_override_requirements(
    pg,
    hospital,
    department,
    override_reason,
    approved_by_role,
):
    """
    Enforce inter-hospital override requirements.

    Raises ValueError when approval metadata is insufficient.
    Returns policy decision object.
    """
    decision = evaluate_rotation_override_policy(pg, hospital, department)
    if not decision.requires_utrmc_approval:
        return decision

    if not str(override_reason or "").strip():
        raise ValueError("override_reason is required for this inter-hospital rotation")
    if approved_by_role != "utrmc_admin":
        raise ValueError("utrmc_admin approval is required for this inter-hospital rotation")
    return decision


def approve_rotation_override(*, rotation, approver):
    """Persist UTRMC approval on a rotation using the shared validator."""
    role = getattr(approver, "role", None)
    validate_rotation_override_requirements(
        rotation.pg,
        rotation.hospital,
        rotation.department,
        rotation.override_reason,
        role,
    )
    rotation.utrmc_approved_by = approver
    rotation.utrmc_approved_at = timezone.now()
    rotation.save(update_fields=["utrmc_approved_by", "utrmc_approved_at", "updated_at"])
    return evaluate_rotation_override_policy(rotation.pg, rotation.hospital, rotation.department)
