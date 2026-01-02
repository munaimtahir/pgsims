from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

from sims.domain.validators import (
    sanitize_free_text,
    validate_chronology,
    validate_same_supervisor,
)

User = get_user_model()


class Hospital(models.Model):
    """
    Model representing hospitals where rotations take place.

    Created: 2025-05-29 16:28:44 UTC
    Author: SMIB2012
    """

    name = models.CharField(max_length=200, help_text="Official name of the hospital")

    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text="Hospital code or abbreviation",
    )

    address = models.TextField(blank=True, help_text="Complete hospital address")

    phone = models.CharField(max_length=20, blank=True, help_text="Hospital contact phone number")

    email = models.EmailField(blank=True, help_text="Hospital contact email")

    website = models.URLField(blank=True, help_text="Hospital website URL")

    description = models.TextField(
        blank=True, help_text="Description of hospital and its specialties"
    )

    facilities = models.TextField(blank=True, help_text="Available facilities and equipment")

    is_active = models.BooleanField(
        default=True, help_text="Whether this hospital is currently accepting rotations"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    def get_active_rotations_count(self):
        """Get count of currently active rotations at this hospital"""
        return self.rotations.filter(
            status="ongoing",
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).count()

    def get_departments_count(self):
        """Get count of departments in this hospital"""
        return self.departments.filter(is_active=True).count()


class Department(models.Model):
    """
    Model representing departments within hospitals.

    Created: 2025-05-29 16:28:44 UTC
    Author: SMIB2012
    """

    name = models.CharField(max_length=200, help_text="Name of the department")

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="departments",
        help_text="Hospital this department belongs to",
    )

    head_of_department = models.CharField(
        max_length=200, blank=True, help_text="Name of the department head"
    )

    contact_email = models.EmailField(blank=True, help_text="Department contact email")

    contact_phone = models.CharField(
        max_length=20, blank=True, help_text="Department contact phone"
    )

    description = models.TextField(
        blank=True, help_text="Description of the department and its services"
    )

    training_objectives = models.TextField(
        blank=True, help_text="Learning objectives for rotations in this department"
    )

    required_skills = models.TextField(
        blank=True, help_text="Skills that should be acquired during rotation"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this department is currently accepting rotations",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["hospital__name", "name"]
        unique_together = ["hospital", "name"]
        indexes = [
            models.Index(fields=["hospital", "name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"

    def get_current_rotations_count(self):
        """Get count of current rotations in this department"""
        return self.rotations.filter(
            status="ongoing",
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date(),
        ).count()

    def get_total_rotations_count(self):
        """Get total count of rotations in this department"""
        return self.rotations.count()


class Rotation(models.Model):
    """
    Model representing a rotation assignment for a postgraduate.

    A rotation is a scheduled training period in a specific department
    under the supervision of an assigned supervisor.

    Created: 2025-05-29 16:28:44 UTC
    Author: SMIB2012
    """

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("pending", "Pending Approval"),
    ]

    # Core rotation information
    pg = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rotations",
        limit_choices_to={"role": "pg"},
        help_text="Postgraduate assigned to this rotation",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="rotations",
        help_text="Department where rotation takes place",
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="rotations",
        help_text="Hospital where rotation takes place",
    )

    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_rotations",
        limit_choices_to={"role": "supervisor"},
        help_text="Supervisor assigned to oversee this rotation",
    )

    # Rotation schedule
    start_date = models.DateField(help_text="Start date of the rotation")

    end_date = models.DateField(help_text="End date of the rotation")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
        help_text="Current status of the rotation",
    )

    # Training content
    objectives = models.TextField(
        blank=True, help_text="Specific learning objectives for this rotation"
    )

    learning_outcomes = models.TextField(
        blank=True, help_text="Expected learning outcomes and competencies"
    )

    requirements = models.TextField(
        blank=True, help_text="Requirements and prerequisites for this rotation"
    )

    # Completion information
    completion_certificate = models.FileField(
        upload_to="rotations/certificates/",
        blank=True,
        null=True,
        help_text="Completion certificate for the rotation",
    )

    feedback = models.TextField(
        blank=True, help_text="Overall feedback and comments on the rotation"
    )

    notes = models.TextField(blank=True, help_text="Additional notes and observations")

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rotations_created",
        help_text="User who created this rotation assignment",
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rotations_approved",
        help_text="User who approved this rotation",
    )

    approved_at = models.DateTimeField(
        null=True, blank=True, help_text="Date and time when rotation was approved"
    )

    class Meta:
        verbose_name = "Rotation"
        verbose_name_plural = "Rotations"
        ordering = ["-start_date", "pg__last_name"]
        indexes = [
            models.Index(fields=["pg", "status"]),
            models.Index(fields=["supervisor", "status"]),
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["department"]),
            models.Index(fields=["hospital"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F("start_date")),
                name="rotation_end_after_start",
            ),
        ]

    def __str__(self):
        pg_name = self.pg.get_full_name() if self.pg else "No PG"
        dept_name = self.department.name if self.department else "No Department"
        return f"{pg_name} - {dept_name} ({self.start_date} to {self.end_date})"

    def clean(self):
        """Validate rotation data"""
        errors = {}

        # Rotations are typically planned in advance, so future dates are valid
        # We only validate chronology (end >= start)
        try:
            validate_chronology(self.start_date, self.end_date, "start_date", "end_date")
        except ValidationError as exc:
            errors.update(exc.message_dict)

        # Check for overlapping rotations for the same PG
        if self.pg and self.start_date and self.end_date:
            overlapping = Rotation.objects.filter(
                pg=self.pg, status__in=["planned", "ongoing"]
            ).exclude(pk=self.pk)

            for rotation in overlapping:
                if self.start_date <= rotation.end_date and self.end_date >= rotation.start_date:
                    errors["start_date"] = (
                        f"This rotation overlaps with existing rotation: {rotation}"
                    )
                    break

        # Validate department belongs to hospital
        if self.department and self.hospital:
            if self.department.hospital != self.hospital:
                errors["department"] = "Department must belong to the selected hospital"

        # Validate supervisor specialty matches rotation department (if applicable)
        if self.supervisor and self.pg:
            if (
                hasattr(self.supervisor, "specialty")
                and hasattr(self.pg, "specialty")
                and self.supervisor.specialty != self.pg.specialty
            ):
                # This is a warning, not an error
                pass

        try:
            validate_same_supervisor(self.pg, self.supervisor)
        except ValidationError as exc:
            errors.update(exc.message_dict)

        if self.notes:
            try:
                self.notes = sanitize_free_text(self.notes)
            except ValidationError as exc:
                errors.update({"notes": exc.messages})

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Override save to update status based on dates"""
        # Auto-update status based on dates
        today = timezone.now().date()

        if self.status == "planned" and self.start_date <= today <= self.end_date:
            self.status = "ongoing"
        elif self.status == "ongoing" and today > self.end_date:
            self.status = "completed"

        # Set hospital from department if not set
        if self.department and not self.hospital:
            self.hospital = self.department.hospital

        super().save(*args, **kwargs)

    def get_duration_days(self):
        """Calculate rotation duration in days"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return None

    def get_duration_months(self):
        """Calculate rotation duration in months"""
        if self.start_date and self.end_date:
            rd = relativedelta(self.end_date, self.start_date)
            return rd.months + (rd.days / 30.0)
        return None

    def get_completion_percentage(self):
        """Calculate how much of the rotation is completed"""
        if not self.start_date or not self.end_date:
            return 0

        today = timezone.now().date()

        if today < self.start_date:
            return 0
        elif today > self.end_date:
            return 100
        else:
            total_days = (self.end_date - self.start_date).days
            completed_days = (today - self.start_date).days
            return int((completed_days / total_days) * 100) if total_days > 0 else 0

    def get_remaining_days(self):
        """Get number of days remaining in rotation"""
        if not self.end_date:
            return None

        today = timezone.now().date()
        if today <= self.end_date:
            return (self.end_date - today).days
        return 0

    def is_current(self):
        """Check if rotation is currently active"""
        if not self.start_date or not self.end_date:
            return False

        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.status == "ongoing"

    def is_upcoming(self):
        """Check if rotation is upcoming"""
        if not self.start_date:
            return False

        today = timezone.now().date()
        return self.start_date > today and self.status == "planned"

    def is_overdue(self):
        """Check if rotation is overdue for completion"""
        if not self.end_date:
            return False

        today = timezone.now().date()
        return today > self.end_date and self.status != "completed"

    def get_absolute_url(self):
        """Get URL for rotation detail page"""
        return reverse("rotations:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        """Get URL for rotation edit page"""
        return reverse("rotations:edit", kwargs={"pk": self.pk})

    def get_evaluation_count(self):
        """Get count of evaluations for this rotation"""
        return self.evaluations.count()

    def get_average_evaluation_score(self):
        """Get average evaluation score for this rotation"""
        evaluations = self.evaluations.filter(score__isnull=False)
        if evaluations.exists():
            return evaluations.aggregate(models.Avg("score"))["score__avg"]
        return None

    def can_be_evaluated(self):
        """Check if rotation can be evaluated"""
        return self.status in ["ongoing", "completed"]

    def can_be_edited(self):
        """Check if rotation can be edited"""
        return self.status in ["planned", "pending"]

    def can_be_cancelled(self):
        """Check if rotation can be cancelled"""
        return self.status in ["planned", "pending"]


class RotationEvaluation(models.Model):
    """
    Model for evaluating rotation performance and feedback.

    Created: 2025-05-29 16:28:44 UTC
    Author: SMIB2012
    """

    EVALUATION_TYPES = [
        ("mid_rotation", "Mid-Rotation Evaluation"),
        ("final", "Final Evaluation"),
        ("peer", "Peer Evaluation"),
        ("self", "Self Evaluation"),
        ("supervisor", "Supervisor Evaluation"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("reviewed", "Reviewed"),
        ("approved", "Approved"),
    ]

    rotation = models.ForeignKey(
        Rotation,
        on_delete=models.CASCADE,
        related_name="evaluations",
        help_text="Rotation being evaluated",
    )

    evaluator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="evaluations_given",
        help_text="Person conducting the evaluation",
    )

    evaluation_type = models.CharField(
        max_length=20, choices=EVALUATION_TYPES, help_text="Type of evaluation"
    )

    score = models.IntegerField(null=True, blank=True, help_text="Numerical score (0-100)")

    comments = models.TextField(blank=True, help_text="Detailed comments and feedback")

    recommendations = models.TextField(blank=True, help_text="Recommendations for improvement")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        help_text="Status of the evaluation",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rotation Evaluation"
        verbose_name_plural = "Rotation Evaluations"
        ordering = ["-created_at"]
        unique_together = ["rotation", "evaluator", "evaluation_type"]
        indexes = [
            models.Index(fields=["rotation", "evaluation_type"]),
            models.Index(fields=["evaluator"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__gte=0) & models.Q(score__lte=100),
                name="evaluation_score_range",
            ),
        ]

    def __str__(self):
        return f"{self.get_evaluation_type_display()} - {self.rotation}"

    def clean(self):
        """Validate evaluation data"""
        # Guard: only validate if both FKs are set (avoids RelatedObjectDoesNotExist before save)
        if not (self.evaluator_id and self.rotation_id):
            return

        # Ensure evaluator has permission to evaluate this rotation
        if self.evaluator and self.rotation:
            if (
                self.evaluator.role == "supervisor"
                and self.evaluator != self.rotation.supervisor
                and self.evaluator != self.rotation.pg.supervisor
            ):
                raise ValidationError("Supervisor can only evaluate rotations they supervise")

            if (
                self.evaluator.role == "pg"
                and self.evaluator != self.rotation.pg
                and self.evaluation_type not in ["peer", "self"]
            ):
                raise ValidationError("PG can only do self or peer evaluations")

    def get_score_grade(self):
        """Get letter grade based on score"""
        if self.score is None:
            return "Not Graded"

        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"

    def get_score_color(self):
        """Get color code for score display"""
        if self.score is None:
            return "#6c757d"

        if self.score >= 80:
            return "#28a745"  # Green
        elif self.score >= 60:
            return "#ffc107"  # Yellow
        else:
            return "#dc3545"  # Red

    def is_passing(self):
        """Check if evaluation score is passing"""
        return self.score is not None and self.score >= 60

    def can_be_edited(self):
        """Check if evaluation can be edited"""
        return self.status in ["draft", "submitted"]

    def get_absolute_url(self):
        """Get URL for evaluation detail page"""
        return reverse("rotations:evaluation_detail", kwargs={"pk": self.pk})
