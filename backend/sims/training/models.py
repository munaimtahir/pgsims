"""
Training & Rotations canonical models for PGSIMS.

Replaces the legacy sims.rotations.Rotation with a full state-machine workflow.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

User = get_user_model()


# ---------------------------------------------------------------------------
# Training Programs
# ---------------------------------------------------------------------------

class TrainingProgram(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    duration_months = models.PositiveIntegerField(help_text="Total program duration in months")
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        verbose_name = "Training Program"
        verbose_name_plural = "Training Programs"

    def __str__(self):
        return f"{self.name} ({self.code})"


class ProgramRotationTemplate(models.Model):
    program = models.ForeignKey(
        TrainingProgram, on_delete=models.CASCADE, related_name="rotation_templates"
    )
    name = models.CharField(max_length=200)
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.CASCADE,
        related_name="rotation_templates",
    )
    duration_weeks = models.PositiveIntegerField(help_text="Expected duration in weeks")
    required = models.BooleanField(default=True)
    sequence_order = models.PositiveIntegerField(default=0)
    allowed_hospitals = models.ManyToManyField(
        "rotations.Hospital", blank=True, related_name="rotation_templates"
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["program", "sequence_order", "name"]
        verbose_name = "Rotation Template"
        verbose_name_plural = "Rotation Templates"

    def __str__(self):
        return f"{self.program.code} – {self.name}"


# ---------------------------------------------------------------------------
# Resident Enrollment
# ---------------------------------------------------------------------------

class ResidentTrainingRecord(models.Model):
    LEVEL_CHOICES = [
        ("y1", "Year 1"), ("y2", "Year 2"), ("y3", "Year 3"),
        ("y4", "Year 4"), ("y5", "Year 5"),
    ]

    resident_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="training_records",
        limit_choices_to={"role__in": ["pg", "resident"]},
    )
    program = models.ForeignKey(
        TrainingProgram, on_delete=models.CASCADE, related_name="resident_records"
    )
    start_date = models.DateField()
    expected_end_date = models.DateField(null=True, blank=True)
    current_level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, blank=True
    )
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="training_records_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Resident Training Record"
        verbose_name_plural = "Resident Training Records"
        constraints = [
            models.UniqueConstraint(
                fields=["resident_user", "program"],
                condition=models.Q(active=True),
                name="unique_active_training_per_resident",
            )
        ]

    def clean(self):
        if self.expected_end_date and self.start_date and self.expected_end_date <= self.start_date:
            raise ValidationError({"expected_end_date": "End date must be after start date."})

    def __str__(self):
        name = self.resident_user.get_full_name() or self.resident_user.username
        return f"{name} – {self.program.code}"


# ---------------------------------------------------------------------------
# Rotation Assignment (replaces legacy Rotation)
# ---------------------------------------------------------------------------

class RotationAssignment(models.Model):
    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_APPROVED = "APPROVED"
    STATUS_ACTIVE = "ACTIVE"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_RETURNED = "RETURNED"
    STATUS_REJECTED = "REJECTED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_RETURNED, "Returned"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    resident_training = models.ForeignKey(
        ResidentTrainingRecord,
        on_delete=models.CASCADE,
        related_name="rotation_assignments",
    )
    hospital_department = models.ForeignKey(
        "rotations.HospitalDepartment",
        on_delete=models.CASCADE,
        related_name="rotation_assignments",
    )
    template = models.ForeignKey(
        ProgramRotationTemplate,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="rotation_assignments",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    notes = models.TextField(blank=True)
    return_reason = models.TextField(blank=True)
    reject_reason = models.TextField(blank=True)

    # Audit trail
    requested_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="rotation_assignments_requested",
    )
    approved_by_hod = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="rotation_assignments_hod_approved",
    )
    approved_by_utrmc = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="rotation_assignments_utrmc_approved",
    )

    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Rotation Assignment"
        verbose_name_plural = "Rotation Assignments"
        indexes = [
            models.Index(fields=["resident_training", "status"]),
            models.Index(fields=["status"]),
            models.Index(fields=["start_date", "end_date"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F("start_date")),
                name="rotation_assignment_end_after_start",
            ),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError({"end_date": "End date must be after start date."})
        # Overlap check: no two active/scheduled rotations for the same resident
        if self.resident_training_id and self.start_date and self.end_date:
            overlap_statuses = {
                self.STATUS_SUBMITTED, self.STATUS_APPROVED, self.STATUS_ACTIVE
            }
            qs = RotationAssignment.objects.filter(
                resident_training=self.resident_training_id,
                status__in=overlap_statuses,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    "Overlapping rotation already exists for this resident in the selected date range."
                )

    def __str__(self):
        return (
            f"{self.resident_training} | "
            f"{self.hospital_department} | "
            f"{self.start_date}→{self.end_date} [{self.status}]"
        )


# ---------------------------------------------------------------------------
# Leave Requests
# ---------------------------------------------------------------------------

class LeaveRequest(models.Model):
    TYPE_ANNUAL = "annual"
    TYPE_SICK = "sick"
    TYPE_CASUAL = "casual"
    TYPE_STUDY = "study"
    TYPE_MATERNITY = "maternity"
    TYPE_OTHER = "other"

    LEAVE_TYPE_CHOICES = [
        (TYPE_ANNUAL, "Annual Leave"),
        (TYPE_SICK, "Sick Leave"),
        (TYPE_CASUAL, "Casual Leave"),
        (TYPE_STUDY, "Study Leave"),
        (TYPE_MATERNITY, "Maternity Leave"),
        (TYPE_OTHER, "Other"),
    ]

    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    resident_training = models.ForeignKey(
        ResidentTrainingRecord,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="leaves_approved",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    reject_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="leave_end_after_start",
            ),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date must be on or after start date."})

    def __str__(self):
        return (
            f"{self.resident_training} | {self.get_leave_type_display()} "
            f"{self.start_date}→{self.end_date} [{self.status}]"
        )


# ---------------------------------------------------------------------------
# Deputation / Off-service Postings
# ---------------------------------------------------------------------------

class DeputationPosting(models.Model):
    TYPE_DEPUTATION = "deputation"
    TYPE_OFF_SERVICE = "off_service"

    POSTING_TYPE_CHOICES = [
        (TYPE_DEPUTATION, "Deputation"),
        (TYPE_OFF_SERVICE, "Off-service"),
    ]

    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"
    STATUS_COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_COMPLETED, "Completed"),
    ]

    resident_training = models.ForeignKey(
        ResidentTrainingRecord,
        on_delete=models.CASCADE,
        related_name="deputation_postings",
    )
    posting_type = models.CharField(max_length=20, choices=POSTING_TYPE_CHOICES)
    institution_name = models.CharField(max_length=300)
    city = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SUBMITTED)
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="postings_approved",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    reject_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Deputation/Off-service Posting"
        verbose_name_plural = "Deputation/Off-service Postings"
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="posting_end_after_start",
            ),
        ]

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date must be on or after start date."})

    def __str__(self):
        return (
            f"{self.resident_training} | {self.get_posting_type_display()} "
            f"@ {self.institution_name} [{self.status}]"
        )
