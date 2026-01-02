from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

from sims.domain.validators import sanitize_free_text, validate_not_future

# Attempt to import USER_ROLES, fall back if necessary during migrations or specific contexts
try:
    from sims.users.models import USER_ROLES

    PG_ROLE_STRING = next(role[0] for role in USER_ROLES if role[1] == "Postgraduate")
    SUPERVISOR_ROLE_STRING = next(role[0] for role in USER_ROLES if role[1] == "Supervisor")
    ADMIN_ROLE_STRING = next(role[0] for role in USER_ROLES if role[1] == "Admin")
except (
    ImportError,
    StopIteration,
):  # Handle cases like initial migrations or if roles aren't found
    PG_ROLE_STRING = "pg"
    SUPERVISOR_ROLE_STRING = "supervisor"
    ADMIN_ROLE_STRING = "admin"

User = get_user_model()


class Procedure(models.Model):
    """
    Model representing medical procedures that can be performed and logged.

    Created: 2025-05-29 17:19:21 UTC
    Author: SMIB2012
    """

    CATEGORY_CHOICES = [
        ("basic", "Basic Procedures"),
        ("intermediate", "Intermediate Procedures"),
        ("advanced", "Advanced Procedures"),
        ("diagnostic", "Diagnostic Procedures"),
        ("therapeutic", "Therapeutic Procedures"),
        ("surgical", "Surgical Procedures"),
        ("emergency", "Emergency Procedures"),
    ]

    name = models.CharField(max_length=200, unique=True, help_text="Name of the procedure")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="basic",
        help_text="Category of the procedure",
    )

    description = models.TextField(blank=True, help_text="Detailed description of the procedure")

    difficulty_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1,
        help_text="Difficulty level from 1 (basic) to 5 (expert)",
    )

    duration_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Typical duration in minutes"
    )

    cme_points = models.PositiveIntegerField(
        default=0, help_text="CME points typically awarded for this procedure"
    )

    learning_objectives = models.TextField(
        blank=True, help_text="Learning objectives for this procedure"
    )

    prerequisites = models.TextField(
        blank=True, help_text="Prerequisites or requirements before performing"
    )

    required_skills = models.ManyToManyField(
        "Skill",
        blank=True,
        related_name="required_for_procedures",
        help_text="Skills required to perform this procedure",
    )

    assessment_criteria = models.TextField(
        blank=True, help_text="Criteria for assessing competency in this procedure"
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether this procedure is currently active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Procedure"
        verbose_name_plural = "Procedures"
        ordering = ["category", "difficulty_level", "name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["difficulty_level"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def get_usage_count(self):
        """Get count of logbook entries using this procedure"""
        return self.logbook_entries.count()

    def get_average_score(self):
        """Get average assessment score for this procedure"""
        entries = self.logbook_entries.filter(supervisor_assessment_score__isnull=False)
        if entries.exists():
            return entries.aggregate(avg_score=models.Avg("supervisor_assessment_score"))[
                "avg_score"
            ]
        return None

    def get_difficulty_display_color(self):
        """Get color code for difficulty level display"""
        colors = {
            1: "#28a745",  # Green - Easy
            2: "#6c757d",  # Gray - Basic
            3: "#ffc107",  # Yellow - Intermediate
            4: "#fd7e14",  # Orange - Advanced
            5: "#dc3545",  # Red - Expert
        }
        return colors.get(self.difficulty_level, "#6c757d")


class Diagnosis(models.Model):
    """
    Model representing medical diagnoses that can be assigned to cases.

    Created: 2025-05-29 17:19:21 UTC
    Author: SMIB2012
    """

    CATEGORY_CHOICES = [
        ("cardiovascular", "Cardiovascular"),
        ("respiratory", "Respiratory"),
        ("gastrointestinal", "Gastrointestinal"),
        ("neurological", "Neurological"),
        ("endocrine", "Endocrine"),
        ("infectious", "Infectious Disease"),
        ("hematology", "Hematology"),
        ("oncology", "Oncology"),
        ("psychiatry", "Psychiatry"),
        ("dermatology", "Dermatology"),
        ("musculoskeletal", "Musculoskeletal"),
        ("genitourinary", "Genitourinary"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200, help_text="Name of the diagnosis")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
        help_text="Medical category of the diagnosis",
    )

    icd_code = models.CharField(max_length=20, blank=True, help_text="ICD-10 or ICD-11 code")

    description = models.TextField(blank=True, help_text="Detailed description of the diagnosis")

    typical_presentation = models.TextField(blank=True, help_text="Typical clinical presentation")

    common_procedures = models.ManyToManyField(
        Procedure,
        blank=True,
        related_name="common_diagnoses",
        help_text="Procedures commonly associated with this diagnosis",
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether this diagnosis is currently active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Diagnosis"
        verbose_name_plural = "Diagnoses"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["icd_code"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_diagnosis_per_category"
            ),
        ]

    def __str__(self):
        icd_display = f" ({self.icd_code})" if self.icd_code else ""
        return f"{self.name}{icd_display}"

    def get_usage_count(self):
        """Get total count of logbook entries with this diagnosis"""
        return self.primary_entries.count() + self.secondary_entries.count()

    def get_primary_usage_count(self):
        """Get count as primary diagnosis"""
        return self.primary_entries.count()

    def get_secondary_usage_count(self):
        """Get count as secondary diagnosis"""
        return self.secondary_entries.count()


class Skill(models.Model):
    """
    Model representing clinical skills that can be demonstrated and assessed.

    Created: 2025-05-29 17:19:21 UTC
    Author: SMIB2012
    """

    CATEGORY_CHOICES = [
        ("clinical", "Clinical Skills"),
        ("technical", "Technical Skills"),
        ("communication", "Communication Skills"),
        ("professional", "Professional Skills"),
        ("academic", "Academic Skills"),
        ("leadership", "Leadership Skills"),
        ("research", "Research Skills"),
    ]

    LEVEL_CHOICES = [
        ("basic", "Basic Level"),
        ("intermediate", "Intermediate Level"),
        ("advanced", "Advanced Level"),
        ("expert", "Expert Level"),
    ]

    name = models.CharField(max_length=200, help_text="Name of the skill")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="clinical",
        help_text="Category of the skill",
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="basic",
        help_text="Expected competency level",
    )

    description = models.TextField(blank=True, help_text="Detailed description of the skill")

    competency_requirements = models.TextField(
        blank=True, help_text="Requirements to demonstrate competency"
    )

    assessment_methods = models.TextField(blank=True, help_text="Methods for assessing this skill")

    is_active = models.BooleanField(
        default=True, help_text="Whether this skill is currently active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ["category", "level", "name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["level"]),
            models.Index(fields=["is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name", "category"], name="unique_skill_per_category"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    def get_usage_count(self):
        """Get count of logbook entries demonstrating this skill"""
        return self.logbook_entries.count()

    def get_level_order(self):
        """Get numeric order for level"""
        level_order = {
            "basic": 1,
            "intermediate": 2,
            "advanced": 3,
            "expert": 4,
        }
        return level_order.get(self.level, 1)


class LogbookTemplate(models.Model):
    """
    Model representing templates for different types of logbook entries.

    Created: 2025-05-29 17:19:21 UTC
    Author: SMIB2012
    """

    TEMPLATE_TYPE_CHOICES = [
        ("medical", "Medical Case"),
        ("surgical", "Surgical Case"),
        ("emergency", "Emergency Case"),
        ("outpatient", "Outpatient Case"),
        ("procedure", "Procedure Focused"),
        ("research", "Research Activity"),
        ("teaching", "Teaching Activity"),
        ("quality", "Quality Improvement"),
    ]

    name = models.CharField(max_length=200, unique=True, help_text="Name of the template")

    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPE_CHOICES,
        default="medical",
        help_text="Type of logbook entry this template is for",
    )

    description = models.TextField(blank=True, help_text="Description of when to use this template")

    template_structure = models.JSONField(
        default=dict, help_text="JSON structure defining the template layout"
    )

    required_fields = models.JSONField(
        default=list, help_text="List of required fields for this template"
    )

    completion_guidelines = models.TextField(
        blank=True, help_text="Guidelines for completing entries using this template"
    )

    example_entries = models.TextField(blank=True, help_text="Example entries using this template")

    is_default = models.BooleanField(default=False, help_text="Whether this is a default template")

    is_active = models.BooleanField(
        default=True, help_text="Whether this template is currently active"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_templates",
        help_text="User who created this template",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Logbook Template"
        verbose_name_plural = "Logbook Templates"
        ordering = ["template_type", "name"]
        indexes = [
            models.Index(fields=["template_type"]),
            models.Index(fields=["is_default"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

    def get_usage_count(self):
        """Get count of entries using this template"""
        return self.logbook_entries.count()

    def get_required_fields_list(self):
        """Get required fields as a formatted list"""
        if isinstance(self.required_fields, list):
            return self.required_fields
        return []

    def get_template_sections(self):
        """Get template sections from structure"""
        if isinstance(self.template_structure, dict):
            return self.template_structure.get("sections", [])
        return []


# --- REVISED LogbookEntry MODEL ---
class LogbookEntry(models.Model):
    """
    Model representing individual logbook entries documenting clinical experiences.
    (Original creation details retained and new feature requirements integrated)
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending Supervisor Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("returned", "Returned for Edits"),
        ("archived", "Archived"),
    ]

    PATIENT_GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("U", "Unknown/Not Specified"),
    ]

    pg = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="logbook_entries",
        limit_choices_to={"role": PG_ROLE_STRING},
        help_text="Postgraduate who created this entry",
    )
    case_title = models.CharField(
        max_length=300, blank=False, help_text="Title of case or diagnosis"
    )
    date = models.DateField(help_text="Date of case")
    location_of_activity = models.CharField(
        max_length=255,
        help_text="Location of clinical activity",
        blank=False,
        default="",
    )
    patient_history_summary = models.TextField(
        help_text="Brief history (narrative text)", blank=False, default=""
    )
    management_action = models.TextField(
        help_text="Management action (narrative text)", blank=False, default=""
    )
    topic_subtopic = models.CharField(
        max_length=255,
        help_text="Topic/Subtopic (free text for now)",
        blank=False,
        default="",
    )
    rotation = models.ForeignKey(
        "rotations.Rotation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logbook_entries",
        help_text="Rotation during which this case occurred",
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_entries",
        limit_choices_to={"role__in": [SUPERVISOR_ROLE_STRING, ADMIN_ROLE_STRING]},
        help_text="Assigned supervising consultant",
    )
    template = models.ForeignKey(
        LogbookTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logbook_entries",
        help_text="Template used for this entry",
    )
    patient_age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        help_text="Patient age in years",
        null=True,
        blank=True,
    )
    patient_gender = models.CharField(
        max_length=1,
        choices=PATIENT_GENDER_CHOICES,
        help_text="Patient gender",
        null=True,
        blank=True,
    )
    patient_chief_complaint = models.TextField(
        help_text="Patient's chief complaint or presenting symptoms", blank=True
    )
    primary_diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_entries",
        help_text="Primary diagnosis",
    )
    secondary_diagnoses = models.ManyToManyField(
        Diagnosis,
        blank=True,
        related_name="secondary_entries",
        help_text="Secondary or differential diagnoses",
    )
    procedures = models.ManyToManyField(
        Procedure,
        blank=True,
        related_name="logbook_entries",
        help_text="Procedures performed or observed",
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="logbook_entries",
        help_text="Skills demonstrated during this case",
    )
    investigations_ordered = models.TextField(
        blank=True, help_text="Investigations ordered and results"
    )
    clinical_reasoning = models.TextField(
        blank=True, help_text="Clinical reasoning and thought process"
    )
    learning_points = models.TextField(blank=True, help_text="Key learning points from this case")
    challenges_faced = models.TextField(
        blank=True, help_text="Challenges encountered and how they were addressed"
    )
    follow_up_required = models.TextField(
        blank=True, help_text="Follow-up actions or learning required"
    )
    supervisor_feedback = models.TextField(
        blank=True, help_text="Supervisor's comment or reason for rejection/return."
    )
    self_assessment_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Self-assessment score (1-10)",
    )
    supervisor_assessment_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Supervisor's assessment score (1-10)",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        help_text="Current status of the entry",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the entry was first created"
    )
    submitted_to_supervisor_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when entry was formally submitted to supervisor",
    )
    supervisor_action_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp when supervisor last took action"
    )
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of the last modification")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_logbook_entries",
        help_text="User who created this entry (should be the PG)",
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_logbook_entries",
        limit_choices_to={"role__in": [SUPERVISOR_ROLE_STRING, ADMIN_ROLE_STRING]},
        help_text="Supervisor who approved this entry",
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when entry was approved by supervisor",
    )

    class Meta:
        verbose_name = "Logbook Entry"
        verbose_name_plural = "Logbook Entries"
        ordering = ["-date", "-updated_at"]
        indexes = [
            models.Index(fields=["pg", "date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["date"]),
            models.Index(fields=["rotation"]),
            models.Index(fields=["supervisor"]),
            models.Index(fields=["primary_diagnosis"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["submitted_to_supervisor_at"]),
            models.Index(fields=["supervisor_action_at"]),
        ]
        constraints = []

    def __str__(self):
        title = self.case_title
        pg_name = self.pg.get_full_name() if self.pg else "No PG"
        return f"{title} - {pg_name}"

    def clean(self):
        super().clean()
        errors = {}
        try:
            validate_not_future(self.date, "date")
        except ValidationError as exc:
            errors.update(exc.message_dict)

        if self.patient_age is not None and (self.patient_age < 0 or self.patient_age > 150):
            errors.setdefault("patient_age", []).append("Patient age must be between 0 and 150.")

        # Sanitise free text inputs to prevent script injection.
        text_fields = [
            "patient_history_summary",
            "management_action",
            "topic_subtopic",
            "investigations_ordered",
            "clinical_reasoning",
            "learning_points",
            "challenges_faced",
            "follow_up_required",
        ]
        for field in text_fields:
            value = getattr(self, field, "")
            if not value:
                continue
            try:
                setattr(self, field, sanitize_free_text(value))
            except ValidationError as exc:
                errors.setdefault(field, []).extend(exc.messages)

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        is_new_entry = self._state.adding
        old_status = None

        if not is_new_entry and self.pk:
            try:
                old_instance = type(self).objects.get(pk=self.pk)
                old_status = old_instance.status
            except type(self).DoesNotExist:
                pass

        if (
            not self.supervisor
            and self.pg
            and hasattr(self.pg, "supervisor")
            and self.pg.supervisor
        ):
            self.supervisor = self.pg.supervisor

        if is_new_entry and self.pg and not self.created_by:
            self.created_by = self.pg

        intended_status = self.status
        self._handle_status_change(old_status, intended_status)

        super().save(*args, **kwargs)

    def _handle_status_change(self, old_status, new_status_intended):
        now = timezone.now()
        final_status_to_set = new_status_intended

        if new_status_intended == "pending":
            if self.supervisor:
                if old_status == "draft" or old_status is None or old_status == "returned":
                    self.submitted_to_supervisor_at = now
                    self.supervisor_action_at = None
                    self._notify_supervisor_of_submission()
                    final_status_to_set = "pending"
            else:
                final_status_to_set = "draft"
                if old_status == "pending":
                    self.submitted_to_supervisor_at = None

        elif old_status == "pending":
            if new_status_intended == "approved":
                self.supervisor_action_at = now
                self.verified_at = now
                if self.supervisor:
                    self.verified_by = self.supervisor
                final_status_to_set = "approved"
            elif new_status_intended == "rejected":
                self.supervisor_action_at = now
                self.verified_at = None
                self.verified_by = None
                final_status_to_set = "rejected"
            elif new_status_intended == "returned":
                self.supervisor_action_at = now
                self.verified_at = None
                self.verified_by = None
                final_status_to_set = "returned"

        elif new_status_intended == "draft":
            if old_status != "draft":
                self.submitted_to_supervisor_at = None
                self.supervisor_action_at = None
                self.verified_at = None
                self.verified_by = None
            final_status_to_set = "draft"

        elif new_status_intended == "archived":
            final_status_to_set = "archived"

        self.status = final_status_to_set

    def _notify_supervisor_of_submission(self):
        try:
            from sims.notifications.models import Notification

            if self.supervisor and Notification:
                Notification.objects.create(
                    user=self.supervisor,
                    title=f"Logbook Entry Submitted: '{self.case_title}'",
                    message=f"{self.pg.get_full_name()} has submitted a logbook entry for your review.",
                    type="logbook_submission",
                    related_object_id=self.id,
                )
        except ImportError:
            pass
        except Exception:
            pass

    def get_duration_since_creation(self):
        return timezone.now() - self.created_at

    def get_review_duration(self):
        if self.supervisor_action_at and self.submitted_to_supervisor_at:
            return self.supervisor_action_at - self.submitted_to_supervisor_at
        return None

    def is_overdue(self, days=7):
        if self.status == "draft":
            return (timezone.now().date() - self.date).days > days
        return False

    def can_be_edited(self):
        return self.status in ["draft", "returned"]

    def can_be_deleted(self):
        return self.status in ["draft"]

    def get_status_color(self):
        status_colors = {
            "draft": "#6c757d",
            "pending": "#ffc107",
            "approved": "#28a745",
            "rejected": "#dc3545",
            "returned": "#fd7e14",
            "archived": "#adb5bd",
        }
        return status_colors.get(self.status, "#6c757d")

    def get_procedures_display(self):
        procedures = self.procedures.all()
        if not procedures.exists():
            return "No procedures recorded"
        if procedures.count() <= 3:
            return ", ".join([p.name for p in procedures])
        return f"{', '.join([p.name for p in procedures[:3]])} (+{procedures.count() - 3} more)"

    def get_skills_display(self):
        skills = self.skills.all()
        if not skills.exists():
            return "No skills recorded"
        if skills.count() <= 3:
            return ", ".join([s.name for s in skills])
        return f"{', '.join([s.name for s in skills[:3]])} (+{skills.count() - 3} more)"

    def get_complexity_score(self):
        procedure_complexity = sum(p.difficulty_level for p in self.procedures.all())
        diagnosis_complexity = 1 if self.primary_diagnosis else 0
        diagnosis_complexity += self.secondary_diagnoses.count()
        return procedure_complexity + diagnosis_complexity

    def get_cme_points(self):
        return sum(p.cme_points for p in self.procedures.all())

    def get_absolute_url(self):
        return reverse("logbook:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        if self.status in ["draft", "returned"]:
            # This should ideally be decided in the template based on request.user
            # For now, assume if it's editable by PG, this URL is used.
            return reverse("logbook:pg_logbook_entry_edit", kwargs={"pk": self.pk})
        # Fallback to a generic edit URL if one exists, or None
        try:
            return reverse("logbook:edit", kwargs={"pk": self.pk})
        except:  # noqa
            return None


# --- END OF REVISED LogbookEntry MODEL ---


class LogbookReview(models.Model):
    """
    Model for detailed reviews and feedback on logbook entries.

    Created: 2025-05-29 17:19:21 UTC
    Author: SMIB2012
    """

    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        (
            "needs_revision",
            "Needs Revision",
        ),  # This is internal to review, maps to 'returned' for entry
        ("rejected", "Rejected"),
    ]

    logbook_entry = models.ForeignKey(
        LogbookEntry,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Logbook entry being reviewed",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="logbook_reviews_given",
        limit_choices_to={"role__in": [SUPERVISOR_ROLE_STRING, ADMIN_ROLE_STRING]},  # Updated
        help_text="Person conducting the review",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Review status",
    )

    review_date = models.DateField(
        default=timezone.now, help_text="Date when the review was conducted"
    )

    feedback = models.TextField(help_text="Overall feedback on the entry")

    strengths_identified = models.TextField(
        blank=True, help_text="Strengths demonstrated in this case"
    )

    areas_for_improvement = models.TextField(blank=True, help_text="Areas requiring improvement")

    recommendations = models.TextField(
        blank=True, help_text="Specific recommendations for future learning"
    )

    follow_up_required = models.BooleanField(
        default=False, help_text="Whether follow-up discussion is required"
    )

    clinical_knowledge_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Clinical knowledge score (1-10)",
    )

    clinical_skills_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Clinical skills score (1-10)",
    )

    professionalism_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Professionalism score (1-10)",
    )

    overall_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Overall performance score (1-10)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Logbook Review"
        verbose_name_plural = "Logbook Reviews"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["logbook_entry", "status"]),
            models.Index(fields=["reviewer"]),
            models.Index(fields=["review_date"]),
            models.Index(fields=["status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["logbook_entry", "reviewer"],
                name="unique_review_per_reviewer_entry",
            ),
        ]

    def __str__(self):
        return f"Review of {self.logbook_entry.case_title or 'Entry'} by {self.reviewer.get_full_name() if self.reviewer else 'N/A'}"

    def clean(self):
        super().clean()

        # Only validate if all required fields are present
        if (
            hasattr(self, "reviewer")
            and self.reviewer
            and hasattr(self, "logbook_entry")
            and self.logbook_entry
            and self.reviewer.role == SUPERVISOR_ROLE_STRING
        ):  # Use constant
            # Ensure the reviewer is the assigned supervisor of the entry's PG
            # This check assumes LogbookEntry.supervisor is correctly populated from PG.supervisor
            if self.logbook_entry.supervisor != self.reviewer:
                # Also check direct assignment on PG if entry.supervisor might be different (e.g. admin override)
                if self.logbook_entry.pg and self.logbook_entry.pg.supervisor != self.reviewer:
                    raise ValidationError(
                        "Supervisors can only review entries of PGs they directly supervise or entries explicitly assigned to them."
                    )

        if self.overall_score:
            if not all(
                [
                    self.clinical_knowledge_score,
                    self.clinical_skills_score,
                    self.professionalism_score,
                ]
            ):
                raise ValidationError(
                    "All component scores must be provided when giving an overall score."
                )

    def save(self, *args, **kwargs):
        # The LogbookEntry status is updated by SupervisorLogbookReviewActionView, not here.
        # This save method is for the LogbookReview instance itself.
        super().save(*args, **kwargs)

    def get_average_score(self):
        scores = [
            self.clinical_knowledge_score,
            self.clinical_skills_score,
            self.professionalism_score,
        ]
        valid_scores = [s for s in scores if s is not None]

        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return None

    def get_status_color(self):
        status_colors = {
            "pending": "#ffc107",
            "approved": "#28a745",
            "needs_revision": "#fd7e14",
            "rejected": "#dc3545",
        }
        return status_colors.get(self.status, "#6c757d")

    def is_complete(self):
        return self.feedback and self.status != "pending" and self.overall_score is not None


class LogbookStatistics(models.Model):
    pg = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="logbook_stats",
        limit_choices_to={"role": PG_ROLE_STRING},
        help_text="Postgraduate these statistics belong to",
    )

    # Reverting to original field names to avoid rename prompts
    total_entries = models.PositiveIntegerField(default=0)
    draft_entries = models.PositiveIntegerField(default=0)
    submitted_entries = models.PositiveIntegerField(default=0)  # Original name
    approved_entries = models.PositiveIntegerField(default=0)
    revision_entries = models.PositiveIntegerField(
        default=0
    )  # Original name, will map 'returned' status here
    # rejected_entries field removed for now to simplify migration

    total_procedures = models.PositiveIntegerField(default=0)
    unique_procedures = models.PositiveIntegerField(default=0)

    total_skills = models.PositiveIntegerField(default=0)
    unique_skills = models.PositiveIntegerField(default=0)

    average_self_score = models.FloatField(null=True, blank=True)
    average_supervisor_score = models.FloatField(
        null=True, blank=True
    )  # Score from LogbookEntry.supervisor_assessment_score
    average_review_score = models.FloatField(
        null=True, blank=True
    )  # Score from LogbookReview.overall_score

    total_cme_points = models.PositiveIntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)

    average_review_time = models.FloatField(null=True, blank=True)
    last_entry_date = models.DateField(null=True, blank=True)
    most_active_month = models.CharField(max_length=7, blank=True)

    entries_needing_revision_rate = models.FloatField(
        default=0.0
    )  # Reverted to original name to avoid prompt
    on_time_submission_rate = models.FloatField(default=0.0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Logbook Statistics"
        verbose_name_plural = "Logbook Statistics"

    def __str__(self):
        return f"Logbook Stats for {self.pg.get_full_name() if self.pg else 'N/A'}"

    def update_statistics(self):
        entries = LogbookEntry.objects.filter(pg=self.pg)

        self.total_entries = entries.count()
        self.draft_entries = entries.filter(status="draft").count()
        self.submitted_entries = entries.filter(
            status="pending"
        ).count()  # Map 'pending' to 'submitted_entries'
        self.approved_entries = entries.filter(status="approved").count()
        self.revision_entries = entries.filter(
            status="returned"
        ).count()  # Map 'returned' to 'revision_entries'
        # Not tracking rejected_entries directly in stats model for now

        procedure_entries = entries.filter(procedures__isnull=False).distinct()
        self.total_procedures = sum(e.procedures.count() for e in procedure_entries)
        self.unique_procedures = procedure_entries.values("procedures").distinct().count()

        skill_entries = entries.filter(skills__isnull=False).distinct()
        self.total_skills = sum(e.skills.count() for e in skill_entries)
        self.unique_skills = skill_entries.values("skills").distinct().count()

        approved_entries_qs = entries.filter(status="approved")
        self.total_cme_points = sum(e.get_cme_points() for e in approved_entries_qs)

        non_archived_non_draft_entries_count = entries.exclude(
            status__in=["draft", "archived"]
        ).count()
        if non_archived_non_draft_entries_count > 0:
            self.completion_rate = (
                self.approved_entries / non_archived_non_draft_entries_count
            ) * 100
        else:
            self.completion_rate = 0.0

        self.last_entry_date = entries.order_by("-date").first().date if entries.exists() else None

        actioned_entries = entries.filter(
            submitted_to_supervisor_at__isnull=False,
            supervisor_action_at__isnull=False,
            status__in=["approved", "rejected", "returned"],
        )
        review_times_seconds = [
            (e.supervisor_action_at - e.submitted_to_supervisor_at).total_seconds()
            for e in actioned_entries
            if e.supervisor_action_at and e.submitted_to_supervisor_at
        ]
        if review_times_seconds:
            self.average_review_time = (sum(review_times_seconds) / len(review_times_seconds)) / (
                60 * 60 * 24
            )  # Corrected field name
        else:
            self.average_review_time = None  # Corrected field name

        actionable_by_supervisor_count = entries.filter(
            status__in=["approved", "rejected", "returned"]
        ).count()
        if actionable_by_supervisor_count > 0:
            self.entries_needing_revision_rate = (
                self.revision_entries / actionable_by_supervisor_count
            ) * 100
        else:
            self.entries_needing_revision_rate = 0.0

        # Scores (example, adapt as needed)
        self.average_self_score = entries.aggregate(avg=models.Avg("self_assessment_score"))["avg"]
        self.average_supervisor_score = entries.aggregate(
            avg=models.Avg("supervisor_assessment_score")
        )["avg"]
        # For average_review_score, you'd query LogbookReview related to these entries

        self.save()

    @classmethod
    def update_all_statistics(cls):
        for pg_user in User.objects.filter(role=PG_ROLE_STRING, is_active=True):
            stats, created = cls.objects.get_or_create(pg=pg_user)
            stats.update_statistics()

    def get_performance_trend(self):
        if self.average_supervisor_score and self.average_self_score:
            if self.average_supervisor_score > self.average_self_score + 0.5:
                return "Improving"
            elif self.average_supervisor_score < self.average_self_score - 0.5:
                return "Needs Attention"
            else:
                return "Stable"
        return "N/A"

    def get_completion_status(self):
        if self.completion_rate >= 90:
            return "Excellent"
        elif self.completion_rate >= 70:
            return "Good"
        elif self.completion_rate >= 50:
            return "Fair"
        elif self.total_entries > 0:
            return "Poor"
        return "N/A"
