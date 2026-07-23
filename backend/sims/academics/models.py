"""
Models for Brick 6 masters and Brick 8 academic workflow foundation.
"""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords


class Institution(models.Model):
    """Institution / Awarding Body model."""

    name = models.CharField(max_length=200, unique=True, help_text="Institution name")
    code = models.CharField(max_length=20, unique=True, help_text="Institution code")
    description = models.TextField(blank=True, help_text="Institution description")
    active = models.BooleanField(default=True, help_text="Is institution active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class Department(models.Model):
    """Academic department model."""

    name = models.CharField(max_length=200, unique=True, help_text="Department name")
    code = models.CharField(max_length=20, unique=True, help_text="Department code")
    description = models.TextField(blank=True, help_text="Department description")
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
        limit_choices_to={"role__in": ["ADMIN", "SUPERVISOR"]},
        help_text="Department head",
    )
    active = models.BooleanField(default=True, help_text="Is department active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department / Specialty"
        verbose_name_plural = "Departments / Specialties"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class Specialty(models.Model):
    """Specialty model."""

    name = models.CharField(max_length=200, unique=True, help_text="Specialty name")
    code = models.CharField(max_length=20, unique=True, help_text="Specialty code")
    description = models.TextField(blank=True, help_text="Specialty description")
    active = models.BooleanField(default=True, help_text="Is specialty active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Specialties"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class Designation(models.Model):
    """Designation model."""

    name = models.CharField(max_length=200, unique=True, help_text="Designation name")
    code = models.CharField(max_length=20, unique=True, help_text="Designation code")
    description = models.TextField(blank=True, help_text="Designation description")
    active = models.BooleanField(default=True, help_text="Is designation active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class AcademicSession(models.Model):
    """Academic Session / Induction model."""

    name = models.CharField(max_length=200, unique=True, help_text="Session name")
    code = models.CharField(max_length=20, unique=True, help_text="Session code")
    description = models.TextField(blank=True, help_text="Session description")
    active = models.BooleanField(default=True, help_text="Is session active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class ResidentTrainingRecord(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_PAUSED = "PAUSED"
    STATUS_WITHDRAWN = "WITHDRAWN"
    STATUS_TRANSFERRED = "TRANSFERRED"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_WITHDRAWN, "Withdrawn"),
        (STATUS_TRANSFERRED, "Transferred"),
    ]

    resident = models.ForeignKey(
        "users.ResidentProfile",
        on_delete=models.PROTECT,
        related_name="academic_training_records",
    )
    program = models.ForeignKey(
        "training.TrainingProgram",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_training_records",
    )
    academic_session = models.ForeignKey(
        "academics.AcademicSession",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="training_records",
    )
    training_site = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_training_records",
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_training_records",
    )
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    training_year = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-is_active", "-start_date", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["resident"],
                condition=models.Q(is_active=True),
                name="uniq_active_academic_training_record_per_resident",
            )
        ]

    def __str__(self):
        return f"{self.resident.user.get_full_name() or self.resident.user.username} training record"


class AcademicPeriod(models.Model):
    TYPE_YEAR = "YEAR"
    TYPE_TERM = "TERM"
    TYPE_QUARTER = "QUARTER"
    TYPE_MONTH = "MONTH"
    TYPE_CUSTOM = "CUSTOM"

    PERIOD_TYPE_CHOICES = [
        (TYPE_YEAR, "Training Year"),
        (TYPE_TERM, "Term"),
        (TYPE_QUARTER, "Quarter"),
        (TYPE_MONTH, "Month"),
        (TYPE_CUSTOM, "Custom"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    academic_session = models.ForeignKey(
        "academics.AcademicSession",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_periods",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    period_type = models.CharField(max_length=32, choices=PERIOD_TYPE_CHOICES, default=TYPE_CUSTOM)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["sort_order", "start_date", "name"]

    def __str__(self):
        return self.name


class RotationTemplate(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    program = models.ForeignKey(
        "training.TrainingProgram",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_rotation_templates",
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="academic_rotation_templates",
    )
    training_year = models.PositiveIntegerField(null=True, blank=True)
    duration_weeks = models.PositiveIntegerField(null=True, blank=True)
    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class EvaluationFormTemplate(models.Model):
    TYPE_SUPERVISOR_REVIEW = "SUPERVISOR_REVIEW"
    TYPE_ROTATION_EVALUATION = "ROTATION_EVALUATION"
    TYPE_CASE_BASED_DISCUSSION = "CASE_BASED_DISCUSSION"
    TYPE_MINI_CEX = "MINI_CEX"
    TYPE_DOPS = "DOPS"
    TYPE_PROGRESS_REVIEW = "PROGRESS_REVIEW"

    FORM_TYPE_CHOICES = [
        (TYPE_SUPERVISOR_REVIEW, "Supervisor Review"),
        (TYPE_ROTATION_EVALUATION, "Rotation Evaluation"),
        (TYPE_CASE_BASED_DISCUSSION, "Case-Based Discussion"),
        (TYPE_MINI_CEX, "Mini-CEX"),
        (TYPE_DOPS, "DOPS"),
        (TYPE_PROGRESS_REVIEW, "Progress Review"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    program = models.ForeignKey(
        "training.TrainingProgram",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="evaluation_form_templates",
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="evaluation_form_templates",
    )
    form_type = models.CharField(max_length=64, choices=FORM_TYPE_CHOICES)
    schema = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LogbookCategory(models.Model):
    TYPE_CASE_LOG = "CASE_LOG"
    TYPE_PROCEDURE = "PROCEDURE"
    TYPE_SKILL = "SKILL"
    TYPE_RESEARCH = "RESEARCH"
    TYPE_TEACHING = "TEACHING"
    TYPE_OTHER = "OTHER"

    CATEGORY_TYPE_CHOICES = [
        (TYPE_CASE_LOG, "Case Log"),
        (TYPE_PROCEDURE, "Procedure"),
        (TYPE_SKILL, "Skill"),
        (TYPE_RESEARCH, "Research"),
        (TYPE_TEACHING, "Teaching"),
        (TYPE_OTHER, "Other"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=64, unique=True)
    program = models.ForeignKey(
        "training.TrainingProgram",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="logbook_categories",
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="logbook_categories",
    )
    category_type = models.CharField(max_length=64, choices=CATEGORY_TYPE_CHOICES, default=TYPE_CASE_LOG)
    minimum_required = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SupervisorReviewQueueItem(models.Model):
    TYPE_PROFILE_REVIEW = "PROFILE_REVIEW"
    TYPE_TRAINING_RECORD_REVIEW = "TRAINING_RECORD_REVIEW"
    TYPE_PROGRESS_REVIEW = "PROGRESS_REVIEW"
    TYPE_FUTURE_EVALUATION = "FUTURE_EVALUATION"
    TYPE_EVALUATION_REVIEW = "EVALUATION_REVIEW"
    TYPE_LOGBOOK_REVIEW = "LOGBOOK_REVIEW"

    QUEUE_TYPE_CHOICES = [
        (TYPE_PROFILE_REVIEW, "Profile Review"),
        (TYPE_TRAINING_RECORD_REVIEW, "Training Record Review"),
        (TYPE_PROGRESS_REVIEW, "Progress Review"),
        (TYPE_FUTURE_EVALUATION, "Future Evaluation"),
        (TYPE_EVALUATION_REVIEW, "Evaluation Review"),
        (TYPE_LOGBOOK_REVIEW, "Logbook Review"),
    ]

    STATUS_PENDING = "PENDING"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_DONE = "DONE"
    STATUS_DISMISSED = "DISMISSED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
        (STATUS_DISMISSED, "Dismissed"),
    ]

    resident = models.ForeignKey(
        "users.ResidentProfile",
        on_delete=models.PROTECT,
        related_name="review_queue_items",
    )
    supervisor = models.ForeignKey(
        "users.SupervisorProfile",
        on_delete=models.PROTECT,
        related_name="review_queue_items",
    )
    training_record = models.ForeignKey(
        "academics.ResidentTrainingRecord",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="review_queue_items",
    )
    queue_type = models.CharField(max_length=64, choices=QUEUE_TYPE_CHOICES)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["status", "due_date", "-created_at"]

    def __str__(self):
        return f"{self.resident.user.get_full_name() or self.resident.user.username} / {self.queue_type}"


class EvaluationSubmission(models.Model):
    resident = models.ForeignKey(
        "users.ResidentProfile",
        on_delete=models.PROTECT,
        related_name="evaluation_submissions",
    )
    training_record = models.ForeignKey(
        "academics.ResidentTrainingRecord",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="evaluation_submissions",
    )
    template = models.ForeignKey(
        "academics.EvaluationFormTemplate",
        on_delete=models.PROTECT,
        related_name="submissions",
    )
    supervisor = models.ForeignKey(
        "users.SupervisorProfile",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="evaluation_reviews",
    )
    academic_period = models.ForeignKey(
        "academics.AcademicPeriod",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=32,
        choices=[
            ("DRAFT", "Draft"),
            ("SUBMITTED", "Submitted"),
            ("UNDER_REVIEW", "Under Review"),
            ("RETURNED", "Returned for Revision"),
            ("APPROVED", "Approved"),
            ("REJECTED", "Rejected"),
            ("CANCELLED", "Cancelled"),
        ],
        default="DRAFT",
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    resident_comments = models.TextField(blank=True)
    supervisor_comments = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Evaluation {self.id} - {self.resident.user.username} ({self.status})"


class EvaluationResponse(models.Model):
    submission = models.ForeignKey(
        EvaluationSubmission,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    field_key = models.CharField(max_length=128)
    field_label = models.CharField(max_length=255, blank=True)
    field_type = models.CharField(max_length=64, blank=True)
    value_text = models.TextField(blank=True)
    value_number = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_json = models.JSONField(default=dict, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]


class LogbookEntry(models.Model):
    resident = models.ForeignKey(
        "users.ResidentProfile",
        on_delete=models.PROTECT,
        related_name="logbook_entries",
    )
    training_record = models.ForeignKey(
        "academics.ResidentTrainingRecord",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="logbook_entries",
    )
    category = models.ForeignKey(
        "academics.LogbookCategory",
        on_delete=models.PROTECT,
        related_name="entries",
    )
    supervisor = models.ForeignKey(
        "users.SupervisorProfile",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="logbook_reviews",
    )
    academic_period = models.ForeignKey(
        "academics.AcademicPeriod",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    entry_date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    case_identifier = models.CharField(max_length=128, blank=True)
    patient_age = models.CharField(max_length=64, blank=True)
    patient_gender = models.CharField(max_length=64, blank=True)
    status = models.CharField(
        max_length=32,
        choices=[
            ("DRAFT", "Draft"),
            ("SUBMITTED", "Submitted"),
            ("VERIFIED", "Verified"),
            ("RETURNED", "Returned for Revision"),
            ("REJECTED", "Rejected"),
            ("CANCELLED", "Cancelled"),
        ],
        default="DRAFT",
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    resident_reflection = models.TextField(blank=True)
    supervisor_comments = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-entry_date", "-created_at"]

    def __str__(self):
        return f"LogbookEntry {self.id} - {self.title} ({self.status})"


class ProcedureRecord(models.Model):
    logbook_entry = models.OneToOneField(
        LogbookEntry,
        on_delete=models.CASCADE,
        related_name="procedure_record",
    )
    procedure_name = models.CharField(max_length=255)
    procedure_code = models.CharField(max_length=64, blank=True)
    role_performed = models.CharField(
        max_length=64,
        choices=[
            ("OBSERVED", "Observed"),
            ("ASSISTED", "Assisted"),
            ("PERFORMED_UNDER_SUPERVISION", "Performed Under Supervision"),
            ("PERFORMED_INDEPENDENTLY", "Performed Independently"),
        ],
    )
    complexity = models.CharField(
        max_length=64,
        choices=[
            ("LOW", "Low"),
            ("MODERATE", "Moderate"),
            ("HIGH", "High"),
        ],
        blank=True,
    )
    outcome = models.CharField(max_length=255, blank=True)
    complications = models.TextField(blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"ProcedureRecord {self.id} - {self.procedure_name}"

