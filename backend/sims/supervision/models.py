from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from sims.users.models import ResidentProfile, SupervisorProfile


class ResidentSupervisorAssignment(models.Model):
    """Tracks assignments of supervisors to residents (primary and co-supervisors)."""

    ASSIGNMENT_PRIMARY = "PRIMARY"
    ASSIGNMENT_CO_SUPERVISOR = "CO_SUPERVISOR"
    ASSIGNMENT_TYPE_CHOICES = [
        (ASSIGNMENT_PRIMARY, "Primary Supervisor"),
        (ASSIGNMENT_CO_SUPERVISOR, "Co-Supervisor"),
    ]

    STATUS_ACTIVE = "ACTIVE"
    STATUS_ENDED = "ENDED"
    STATUS_SUSPENDED = "SUSPENDED"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_ENDED, "Ended"),
        (STATUS_SUSPENDED, "Suspended"),
    ]

    resident = models.ForeignKey(
        ResidentProfile,
        on_delete=models.PROTECT,
        related_name="supervisor_assignments",
        help_text="The resident being supervised",
    )
    supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.PROTECT,
        related_name="resident_assignments",
        help_text="The assigned supervisor",
    )
    assignment_type = models.CharField(
        max_length=32,
        choices=ASSIGNMENT_TYPE_CHOICES,
        default=ASSIGNMENT_PRIMARY,
        help_text="Type of supervision assignment",
    )
    start_date = models.DateField(help_text="Start date of the supervision assignment")
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="End date of the supervision assignment (required if status is ENDED)",
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        help_text="Status of the supervision assignment",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Convenience flag to query active assignments",
    )
    notes = models.TextField(
        blank=True,
        help_text="General comments or notes",
    )
    reason_for_change = models.TextField(
        blank=True,
        help_text="Reason for modifying, ending, or changing the assignment",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ["-start_date", "-created_at"]
        constraints = [
            # Only one active primary supervisor per resident at a time
            models.UniqueConstraint(
                fields=["resident"],
                condition=models.Q(is_active=True, assignment_type="PRIMARY"),
                name="unique_active_primary_supervisor",
            ),
            # Do not allow duplicate active assignments for the same resident and supervisor
            models.UniqueConstraint(
                fields=["resident", "supervisor", "assignment_type"],
                condition=models.Q(is_active=True),
                name="unique_active_resident_supervisor_type",
            ),
        ]

    def __str__(self):
        return f"{self.resident.user.get_full_name()} -> {self.supervisor.user.get_full_name()} ({self.assignment_type})"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Enforce end_date validation if status is ended
        if self.status == self.STATUS_ENDED and not self.end_date:
            raise ValidationError({"end_date": "End date is required when status is ENDED."})
        if self.status == self.STATUS_ACTIVE and self.end_date:
            raise ValidationError({"end_date": "Active assignment cannot have an end date."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
