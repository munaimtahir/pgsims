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
    DEGREE_FCPS = "FCPS"
    DEGREE_MD = "MD"
    DEGREE_MS = "MS"
    DEGREE_DIPLOMA = "Diploma"
    DEGREE_OTHER = "Other"

    DEGREE_CHOICES = [
        (DEGREE_FCPS, "FCPS"),
        (DEGREE_MD, "MD"),
        (DEGREE_MS, "MS"),
        (DEGREE_DIPLOMA, "Diploma"),
        (DEGREE_OTHER, "Other"),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    duration_months = models.PositiveIntegerField(help_text="Total program duration in months")
    description = models.TextField(blank=True)
    degree_type = models.CharField(
        max_length=20, choices=DEGREE_CHOICES, default=DEGREE_OTHER,
        help_text="Academic degree type"
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="training_programs",
        help_text="Primary department for this program",
    )
    notes = models.TextField(blank=True, help_text="Additional notes or administrative remarks")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        verbose_name = "Training Program"
        verbose_name_plural = "Training Programs"

    @property
    def is_active(self):
        return self.active

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
    # Phase/year structure
    year_index = models.PositiveIntegerField(null=True, blank=True, help_text="Year in program (1-indexed)")
    phase_index = models.PositiveIntegerField(null=True, blank=True, help_text="Phase within year")
    block_index = models.PositiveIntegerField(null=True, blank=True, help_text="Block within phase")
    is_mandatory = models.BooleanField(default=True, help_text="Is this rotation mandatory for the program?")
    min_duration_weeks = models.PositiveIntegerField(
        null=True, blank=True, help_text="Minimum acceptable duration in weeks (if different from expected)"
    )
    requirements_json = models.JSONField(
        default=dict, blank=True, help_text="Additional requirements as structured JSON"
    )
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

    STATUS_ACTIVE = "ACTIVE"
    STATUS_PAUSED = "PAUSED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
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
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE,
        help_text="Current enrollment status"
    )
    locked_program = models.BooleanField(
        default=True, help_text="Prevent program change once training starts"
    )
    program_change_reason = models.TextField(
        blank=True, null=True, help_text="Reason if program was changed (requires admin override)"
    )
    restart_from_scratch_on_change = models.BooleanField(
        default=True, help_text="Reset training timeline on program change"
    )
    active = models.BooleanField(default=True)
    has_default_dates = models.BooleanField(
        default=False,
        help_text="Computed flag set when record uses default/synthetic dates.",
    )
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

    def current_month_index(self):
        """Compute how many months into the program the resident is (from start_date)."""
        from django.utils import timezone
        import math
        today = timezone.now().date()
        if not self.start_date or today < self.start_date:
            return 0
        delta = today - self.start_date
        return max(0, math.floor(delta.days / 30.44))

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


# ---------------------------------------------------------------------------
# Program Policy (1:1 with TrainingProgram)
# ---------------------------------------------------------------------------

class ProgramPolicy(models.Model):
    program = models.OneToOneField(
        TrainingProgram, on_delete=models.CASCADE, related_name="policy"
    )
    allow_program_change = models.BooleanField(
        default=False, help_text="Allow residents to change program after enrollment"
    )
    program_change_requires_restart = models.BooleanField(
        default=True, help_text="Restart training timeline on program change"
    )
    min_active_months_before_imm = models.PositiveIntegerField(
        null=True, blank=True, help_text="Minimum active months before iMM eligibility"
    )
    imm_allowed_from_month = models.PositiveIntegerField(
        null=True, blank=True, help_text="Month index from which iMM exam is allowed (e.g. halfway)"
    )
    final_allowed_from_month = models.PositiveIntegerField(
        null=True, blank=True, help_text="Month index from which Final exam is allowed"
    )
    exception_rules_text = models.TextField(
        blank=True, help_text="Free-text exceptional policy rules (non-executable)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Program Policy"
        verbose_name_plural = "Program Policies"

    def __str__(self):
        return f"Policy: {self.program.code}"


# ---------------------------------------------------------------------------
# Program Milestones (iMM / Final and definitions)
# ---------------------------------------------------------------------------

class ProgramMilestone(models.Model):
    CODE_IMM = "IMM"
    CODE_FINAL = "FINAL"

    CODE_CHOICES = [
        (CODE_IMM, "Intermediate Membership (iMM)"),
        (CODE_FINAL, "Final Examination"),
    ]

    program = models.ForeignKey(
        TrainingProgram, on_delete=models.CASCADE, related_name="milestones"
    )
    code = models.CharField(max_length=20, choices=CODE_CHOICES)
    name = models.CharField(max_length=200)
    recommended_month = models.PositiveIntegerField(
        null=True, blank=True, help_text="Recommended month in program to attempt this milestone"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Program Milestone"
        verbose_name_plural = "Program Milestones"
        unique_together = [("program", "code")]
        ordering = ["program", "code"]

    def __str__(self):
        return f"{self.program.code} – {self.get_code_display()}"


class ProgramMilestoneResearchRequirement(models.Model):
    milestone = models.OneToOneField(
        ProgramMilestone, on_delete=models.CASCADE, related_name="research_requirement"
    )
    requires_synopsis_approved = models.BooleanField(default=False)
    requires_synopsis_submitted_to_university = models.BooleanField(default=False)
    requires_thesis_submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Milestone Research Requirement"

    def __str__(self):
        return f"Research req: {self.milestone}"


class ProgramMilestoneWorkshopRequirement(models.Model):
    milestone = models.ForeignKey(
        ProgramMilestone, on_delete=models.CASCADE, related_name="workshop_requirements"
    )
    workshop = models.ForeignKey(
        "training.Workshop", on_delete=models.CASCADE, related_name="milestone_requirements"
    )
    required_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Milestone Workshop Requirement"
        unique_together = [("milestone", "workshop")]

    def __str__(self):
        return f"Workshop req: {self.milestone} — {self.workshop} x{self.required_count}"


class ProgramMilestoneLogbookRequirement(models.Model):
    """Placeholder for future logbook-based milestone requirements."""
    milestone = models.ForeignKey(
        ProgramMilestone, on_delete=models.CASCADE, related_name="logbook_requirements"
    )
    procedure_key = models.CharField(
        max_length=200, blank=True, help_text="Key identifying the logbook procedure/category"
    )
    category = models.CharField(max_length=200, blank=True)
    min_entries = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Milestone Logbook Requirement"

    def __str__(self):
        return f"Logbook req: {self.milestone} — {self.procedure_key or self.category} x{self.min_entries}"


# ---------------------------------------------------------------------------
# Workshop Models
# ---------------------------------------------------------------------------

class Workshop(models.Model):
    name = models.CharField(max_length=300)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class WorkshopBlock(models.Model):
    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="blocks"
    )
    name = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Workshop Block"
        verbose_name_plural = "Workshop Blocks"

    def __str__(self):
        return f"{self.workshop.code} – {self.name}"


class WorkshopRun(models.Model):
    STATUS_SCHEDULED = "SCHEDULED"
    STATUS_ONGOING = "ONGOING"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    block = models.ForeignKey(
        WorkshopBlock, on_delete=models.CASCADE, related_name="runs"
    )
    run_date = models.DateField()
    facilitator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="workshop_runs_facilitated"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Workshop Run"
        verbose_name_plural = "Workshop Runs"
        ordering = ["-run_date"]

    def __str__(self):
        return f"{self.block} – {self.run_date} [{self.status}]"


# ---------------------------------------------------------------------------
# Resident Research Project (state machine)
# ---------------------------------------------------------------------------

class ResidentResearchProject(models.Model):
    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED_SUPERVISOR = "SUBMITTED_TO_SUPERVISOR"
    STATUS_APPROVED_SUPERVISOR = "APPROVED_BY_SUPERVISOR"
    STATUS_SUBMITTED_UNIVERSITY = "SUBMITTED_TO_UNIVERSITY"
    STATUS_ACCEPTED_UNIVERSITY = "ACCEPTED_BY_UNIVERSITY"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED_SUPERVISOR, "Submitted to Supervisor"),
        (STATUS_APPROVED_SUPERVISOR, "Approved by Supervisor"),
        (STATUS_SUBMITTED_UNIVERSITY, "Submitted to University"),
        (STATUS_ACCEPTED_UNIVERSITY, "Accepted by University"),
    ]

    VALID_TRANSITIONS = {
        STATUS_DRAFT: [STATUS_SUBMITTED_SUPERVISOR],
        STATUS_SUBMITTED_SUPERVISOR: [STATUS_APPROVED_SUPERVISOR, STATUS_DRAFT],
        STATUS_APPROVED_SUPERVISOR: [STATUS_SUBMITTED_UNIVERSITY],
        STATUS_SUBMITTED_UNIVERSITY: [STATUS_ACCEPTED_UNIVERSITY],
        STATUS_ACCEPTED_UNIVERSITY: [],
    }

    resident_training_record = models.OneToOneField(
        ResidentTrainingRecord, on_delete=models.CASCADE, related_name="research_project"
    )
    title = models.CharField(max_length=500)
    topic_area = models.CharField(max_length=300, blank=True)
    supervisor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="supervised_research_projects",
        limit_choices_to={"role__in": ["supervisor", "faculty", "admin"]},
    )
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    synopsis_file = models.FileField(
        upload_to="research/synopsis/", null=True, blank=True
    )
    synopsis_approved_at = models.DateTimeField(null=True, blank=True)
    supervisor_feedback = models.TextField(blank=True, help_text="Supervisor comments on submission")
    university_submission_ref = models.CharField(max_length=200, blank=True, null=True)
    submitted_to_supervisor_at = models.DateTimeField(null=True, blank=True)
    submitted_to_university_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Research Project"
        verbose_name_plural = "Research Projects"

    def transition_to(self, new_status, actor=None):
        allowed = self.VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValidationError(
                f"Cannot transition from '{self.status}' to '{new_status}'."
            )
        from django.utils import timezone
        now = timezone.now()
        if new_status == self.STATUS_SUBMITTED_SUPERVISOR:
            self.submitted_to_supervisor_at = now
        elif new_status == self.STATUS_APPROVED_SUPERVISOR:
            self.synopsis_approved_at = now
        elif new_status == self.STATUS_SUBMITTED_UNIVERSITY:
            self.submitted_to_university_at = now
        elif new_status == self.STATUS_ACCEPTED_UNIVERSITY:
            self.accepted_at = now
        self.status = new_status
        self.save()

    def __str__(self):
        return f"{self.resident_training_record} – Research: {self.title[:50]}"


# ---------------------------------------------------------------------------
# Resident Thesis
# ---------------------------------------------------------------------------

class ResidentThesis(models.Model):
    STATUS_NOT_STARTED = "NOT_STARTED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_SUBMITTED = "SUBMITTED"

    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, "Not Started"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_SUBMITTED, "Submitted"),
    ]

    resident_training_record = models.OneToOneField(
        ResidentTrainingRecord, on_delete=models.CASCADE, related_name="thesis"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)
    thesis_file = models.FileField(upload_to="research/thesis/", null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    final_submission_ref = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Resident Thesis"
        verbose_name_plural = "Resident Theses"

    def __str__(self):
        return f"{self.resident_training_record} – Thesis [{self.status}]"


# ---------------------------------------------------------------------------
# Resident Workshop Completion (manual upload + system generated)
# ---------------------------------------------------------------------------

class ResidentWorkshopCompletion(models.Model):
    SOURCE_MANUAL = "MANUAL_UPLOAD"
    SOURCE_SYSTEM = "SYSTEM_GENERATED"

    SOURCE_CHOICES = [
        (SOURCE_MANUAL, "Manual Upload"),
        (SOURCE_SYSTEM, "System Generated"),
    ]

    resident_training_record = models.ForeignKey(
        ResidentTrainingRecord, on_delete=models.CASCADE, related_name="workshop_completions"
    )
    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="completions"
    )
    workshop_run = models.ForeignKey(
        WorkshopRun, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="completions"
    )
    completed_at = models.DateField()
    certificate_file = models.FileField(upload_to="workshops/certificates/", null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Workshop Completion"
        verbose_name_plural = "Workshop Completions"
        ordering = ["-completed_at"]
        indexes = [
            models.Index(fields=["resident_training_record", "workshop"]),
        ]

    def __str__(self):
        return (
            f"{self.resident_training_record} – {self.workshop.code} on {self.completed_at}"
        )


# ---------------------------------------------------------------------------
# Resident Milestone Eligibility (computed snapshot)
# ---------------------------------------------------------------------------

class ResidentMilestoneEligibility(models.Model):
    STATUS_NOT_READY = "NOT_READY"
    STATUS_PARTIALLY_READY = "PARTIALLY_READY"
    STATUS_ELIGIBLE = "ELIGIBLE"

    STATUS_CHOICES = [
        (STATUS_NOT_READY, "Not Ready"),
        (STATUS_PARTIALLY_READY, "Partially Ready"),
        (STATUS_ELIGIBLE, "Eligible"),
    ]

    resident_training_record = models.ForeignKey(
        ResidentTrainingRecord, on_delete=models.CASCADE, related_name="milestone_eligibilities"
    )
    milestone = models.ForeignKey(
        ProgramMilestone, on_delete=models.CASCADE, related_name="eligibilities"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_READY)
    reasons_json = models.JSONField(
        default=list, help_text="Ordered list of unmet requirement descriptions"
    )
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Milestone Eligibility"
        verbose_name_plural = "Milestone Eligibilities"
        unique_together = [("resident_training_record", "milestone")]
        ordering = ["resident_training_record", "milestone__code"]

    def __str__(self):
        return (
            f"{self.resident_training_record} – {self.milestone.get_code_display()} "
            f"[{self.status}]"
        )


# ---------------------------------------------------------------------------
# Logbook (feature-layer active runtime)
# ---------------------------------------------------------------------------


class LogbookThresholdConfig(models.Model):
    MODE_PER_ROTATION = "PER_ROTATION"
    MODE_PER_PERIOD = "PER_PERIOD"
    MODE_CHOICES = [
        (MODE_PER_ROTATION, "Per Rotation"),
        (MODE_PER_PERIOD, "Per Time Period"),
    ]

    name = models.CharField(max_length=150)
    mode = models.CharField(max_length=30, choices=MODE_CHOICES, default=MODE_PER_ROTATION)
    min_approved_entries = models.PositiveIntegerField(default=1)
    period_days = models.PositiveIntegerField(
        null=True, blank=True, help_text="Required when mode=PER_PERIOD"
    )
    program = models.ForeignKey(
        TrainingProgram,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="logbook_threshold_configs",
    )
    department = models.ForeignKey(
        "academics.Department",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="logbook_threshold_configs",
    )
    is_active = models.BooleanField(default=True)
    configured_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="logbook_thresholds_configured",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["name", "-updated_at"]
        indexes = [
            models.Index(fields=["mode", "is_active"]),
            models.Index(fields=["program", "is_active"]),
            models.Index(fields=["department", "is_active"]),
        ]

    def clean(self):
        if self.mode == self.MODE_PER_PERIOD and not self.period_days:
            raise ValidationError({"period_days": "period_days is required for PER_PERIOD mode."})
        if self.mode == self.MODE_PER_ROTATION and self.period_days:
            raise ValidationError({"period_days": "period_days must be empty for PER_ROTATION mode."})

    def __str__(self):
        return f"{self.name} ({self.mode})"


class LogbookEntry(models.Model):
    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_RETURNED = "RETURNED"
    STATUS_APPROVED = "APPROVED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_RETURNED, "Returned"),
        (STATUS_APPROVED, "Approved"),
    ]

    resident_training_record = models.ForeignKey(
        ResidentTrainingRecord,
        on_delete=models.CASCADE,
        related_name="logbook_entries",
    )
    rotation_assignment = models.ForeignKey(
        RotationAssignment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="logbook_entries",
        help_text="Optional link to active/completed rotation for per-rotation threshold checks.",
    )

    patient_id_number = models.CharField(max_length=120)
    patient_name = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    demographics = models.TextField(blank=True)

    disease_area = models.CharField(max_length=255, blank=True)
    diagnosis = models.TextField(blank=True)
    clinical_presentation = models.TextField(blank=True)
    management_plan = models.TextField(blank=True)
    resident_reflection = models.TextField(blank=True)

    patient_seen_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    submitted_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    supervisor_feedback = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="logbook_entries_reviewed",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="logbook_entries_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-patient_seen_at", "-created_at"]
        indexes = [
            models.Index(fields=["resident_training_record", "status"]),
            models.Index(fields=["rotation_assignment", "status"]),
            models.Index(fields=["patient_seen_at"]),
        ]

    def clean(self):
        if (
            self.rotation_assignment_id
            and self.rotation_assignment.resident_training_id != self.resident_training_record_id
        ):
            raise ValidationError(
                {"rotation_assignment": "rotation_assignment must belong to the same resident training record."}
            )

    def __str__(self):
        return f"LogbookEntry<{self.resident_training_record_id}:{self.status}>"


class LogbookReview(models.Model):
    ACTION_RETURNED = "RETURNED"
    ACTION_APPROVED = "APPROVED"
    ACTION_CHOICES = [
        (ACTION_RETURNED, "Returned"),
        (ACTION_APPROVED, "Approved"),
    ]

    entry = models.ForeignKey(
        LogbookEntry,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="logbook_reviews",
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["entry", "created_at"]),
            models.Index(fields=["action", "created_at"]),
        ]

    def __str__(self):
        return f"LogbookReview<{self.entry_id}:{self.action}>"


class LogbookThresholdSnapshot(models.Model):
    resident_training_record = models.ForeignKey(
        ResidentTrainingRecord,
        on_delete=models.CASCADE,
        related_name="logbook_threshold_snapshots",
    )
    threshold_config = models.ForeignKey(
        LogbookThresholdConfig,
        on_delete=models.CASCADE,
        related_name="snapshots",
    )
    rotation_assignment = models.ForeignKey(
        RotationAssignment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="threshold_snapshots",
    )
    window_start = models.DateField(null=True, blank=True)
    window_end = models.DateField(null=True, blank=True)
    approved_entries = models.PositiveIntegerField(default=0)
    required_entries = models.PositiveIntegerField(default=0)
    is_met = models.BooleanField(default=False)
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-computed_at"]
        indexes = [
            models.Index(fields=["resident_training_record", "computed_at"]),
            models.Index(fields=["threshold_config", "computed_at"]),
        ]

    def __str__(self):
        return (
            f"LogbookThresholdSnapshot<{self.resident_training_record_id}:"
            f"{self.threshold_config_id}:{self.approved_entries}/{self.required_entries}>"
        )


# ---------------------------------------------------------------------------
# Synopsis / Thesis submission completeness workflow
# ---------------------------------------------------------------------------


class SubmissionRequirementTemplate(models.Model):
    TYPE_SYNOPSIS = "SYNOPSIS"
    TYPE_THESIS = "THESIS"
    TYPE_CHOICES = [
        (TYPE_SYNOPSIS, "Synopsis"),
        (TYPE_THESIS, "Thesis"),
    ]

    submission_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    code = models.CharField(max_length=80)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_required = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    program = models.ForeignKey(
        TrainingProgram,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="submission_requirement_templates",
    )
    department = models.ForeignKey(
        "academics.Department",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="submission_requirement_templates",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="submission_requirements_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["submission_type", "sort_order", "title"]
        indexes = [
            models.Index(fields=["submission_type", "active"]),
            models.Index(fields=["program", "submission_type", "active"]),
            models.Index(fields=["department", "submission_type", "active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["submission_type", "program", "department", "code"],
                name="uniq_submission_requirement_template_scope",
            )
        ]

    def __str__(self):
        return f"{self.submission_type}:{self.code}"


class ResidentSubmission(models.Model):
    TYPE_SYNOPSIS = SubmissionRequirementTemplate.TYPE_SYNOPSIS
    TYPE_THESIS = SubmissionRequirementTemplate.TYPE_THESIS
    TYPE_CHOICES = SubmissionRequirementTemplate.TYPE_CHOICES

    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_UNDER_REVIEW = "UNDER_REVIEW"
    STATUS_RETURNED = "RETURNED"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_CERTIFICATE_ISSUED = "CERTIFICATE_ISSUED"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_UNDER_REVIEW, "Under Review"),
        (STATUS_RETURNED, "Returned"),
        (STATUS_VERIFIED, "Verified"),
        (STATUS_CERTIFICATE_ISSUED, "Certificate Issued"),
    ]

    resident_training_record = models.ForeignKey(
        ResidentTrainingRecord,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    submission_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    submitted_at = models.DateTimeField(null=True, blank=True)
    under_review_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    certificate_issued_at = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="resident_submissions_reviewed",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["resident_training_record", "submission_type"]),
            models.Index(fields=["submission_type", "status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["resident_training_record", "submission_type"],
                name="uniq_submission_per_resident_type",
            )
        ]

    def __str__(self):
        return f"ResidentSubmission<{self.resident_training_record_id}:{self.submission_type}:{self.status}>"


def _submission_document_upload_path(instance, filename):
    submission_type = getattr(instance.submission, "submission_type", "submission").lower()
    return f"submissions/{submission_type}/{instance.submission_id}/{filename}"


class SubmissionDocument(models.Model):
    submission = models.ForeignKey(
        ResidentSubmission,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    requirement = models.ForeignKey(
        SubmissionRequirementTemplate,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="documents",
    )
    file = models.FileField(upload_to=_submission_document_upload_path)
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="submission_documents_uploaded",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["submission", "uploaded_at"]),
            models.Index(fields=["requirement"]),
            models.Index(fields=["is_active"]),
        ]

    def clean(self):
        if self.requirement_id and self.requirement.submission_type != self.submission.submission_type:
            raise ValidationError(
                {"requirement": "Requirement type must match submission type."}
            )

    def save(self, *args, **kwargs):
        if not self.original_filename and getattr(self.file, "name", None):
            self.original_filename = self.file.name.split("/")[-1]
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"SubmissionDocument<{self.submission_id}:{self.original_filename}>"


class SubmissionReview(models.Model):
    ACTION_SUBMITTED = ResidentSubmission.STATUS_SUBMITTED
    ACTION_UNDER_REVIEW = ResidentSubmission.STATUS_UNDER_REVIEW
    ACTION_RETURNED = ResidentSubmission.STATUS_RETURNED
    ACTION_VERIFIED = ResidentSubmission.STATUS_VERIFIED
    ACTION_CERTIFICATE_ISSUED = ResidentSubmission.STATUS_CERTIFICATE_ISSUED
    ACTION_CHOICES = [
        (ACTION_SUBMITTED, "Submitted"),
        (ACTION_UNDER_REVIEW, "Under Review"),
        (ACTION_RETURNED, "Returned"),
        (ACTION_VERIFIED, "Verified"),
        (ACTION_CERTIFICATE_ISSUED, "Certificate Issued"),
    ]

    submission = models.ForeignKey(
        ResidentSubmission,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="submission_reviews",
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["submission", "created_at"]),
            models.Index(fields=["action", "created_at"]),
        ]

    def __str__(self):
        return f"SubmissionReview<{self.submission_id}:{self.action}>"


class SubmissionCertificate(models.Model):
    STATUS_ISSUED = "ISSUED"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_CHOICES = [
        (STATUS_ISSUED, "Issued"),
        (STATUS_VERIFIED, "Verified"),
    ]

    submission = models.OneToOneField(
        ResidentSubmission,
        on_delete=models.CASCADE,
        related_name="certificate",
    )
    certificate_number = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ISSUED)
    issued_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="submission_certificates_issued",
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="submission_certificates_verified",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["status", "issued_at"]),
            models.Index(fields=["certificate_number"]),
        ]

    def __str__(self):
        return f"SubmissionCertificate<{self.certificate_number}>"


# ---------------------------------------------------------------------------
# Rotation phase-1 structured requirements + completion verification
# ---------------------------------------------------------------------------


class ProgramRotationRequirement(models.Model):
    program = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        related_name="rotation_requirements",
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.CASCADE,
        related_name="program_rotation_requirements",
    )
    required_duration_weeks = models.PositiveIntegerField(default=4)
    sequence_order = models.PositiveIntegerField(default=0)
    is_mandatory = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["program", "sequence_order", "department__name"]
        indexes = [
            models.Index(fields=["program", "is_mandatory"]),
            models.Index(fields=["department"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["program", "department", "sequence_order"],
                name="uniq_program_rotation_requirement",
            )
        ]

    def __str__(self):
        return (
            f"{self.program.code}:{self.department.code or self.department.name}:"
            f"{self.required_duration_weeks}w"
        )


class RotationCompletion(models.Model):
    STATUS_CONFIRMED_BY_DEPARTMENT = "CONFIRMED_BY_DEPARTMENT"
    STATUS_PENDING_UTRMC_VERIFICATION = "PENDING_UTRMC_VERIFICATION"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_CHOICES = [
        (STATUS_CONFIRMED_BY_DEPARTMENT, "Confirmed by Department"),
        (STATUS_PENDING_UTRMC_VERIFICATION, "Pending UTRMC Verification"),
        (STATUS_VERIFIED, "Verified"),
    ]

    rotation = models.OneToOneField(
        RotationAssignment,
        on_delete=models.CASCADE,
        related_name="completion",
    )
    status = models.CharField(
        max_length=40,
        choices=STATUS_CHOICES,
        default=STATUS_CONFIRMED_BY_DEPARTMENT,
    )
    confirmed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rotation_completions_confirmed",
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    verification_submitted_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rotation_completions_verified",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-confirmed_at", "-verified_at"]
        indexes = [
            models.Index(fields=["status", "verified_at"]),
            models.Index(fields=["confirmed_at"]),
        ]

    def __str__(self):
        return f"RotationCompletion<{self.rotation_id}:{self.status}>"


class RotationCertificate(models.Model):
    STATUS_ISSUED = "ISSUED"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_CHOICES = [
        (STATUS_ISSUED, "Issued"),
        (STATUS_VERIFIED, "Verified"),
    ]

    completion = models.OneToOneField(
        RotationCompletion,
        on_delete=models.CASCADE,
        related_name="certificate",
    )
    certificate_number = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ISSUED)
    issued_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rotation_certificates_issued",
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rotation_certificates_verified",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["status", "issued_at"]),
            models.Index(fields=["certificate_number"]),
        ]

    def __str__(self):
        return f"RotationCertificate<{self.certificate_number}>"
