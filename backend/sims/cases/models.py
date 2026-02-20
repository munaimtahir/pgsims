from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

User = get_user_model()


def case_file_upload_path(instance, filename):
    """Generate upload path for case files"""
    return f'cases/pg_{instance.pg.id}/{instance.date.strftime("%Y/%m")}/{filename}'


def case_image_upload_path(instance, filename):
    """Generate upload path for case images"""
    return f'cases/pg_{instance.pg.id}/images/{instance.date.strftime("%Y/%m")}/{filename}'


class CaseCategory(models.Model):
    """
    Model representing categories for clinical cases.

    Created: 2025-05-29 17:45:00 UTC
    Author: SMIB2012
    """

    name = models.CharField(max_length=100, unique=True, help_text="Name of the case category")

    description = models.TextField(blank=True, help_text="Description of the case category")

    color_code = models.CharField(
        max_length=7,
        default="#007bff",
        help_text="Hex color code for visual identification",
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether this category is currently active"
    )

    sort_order = models.PositiveIntegerField(default=0, help_text="Sort order for display")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Case Category"
        verbose_name_plural = "Case Categories"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_case_count(self):
        """Get count of cases in this category"""
        return self.cases.filter(is_active=True).count()


class ClinicalCase(models.Model):
    """
    Model representing individual clinical cases for documentation and learning.

    Created: 2025-05-29 17:45:00 UTC
    Author: SMIB2012
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted for Review"),
        ("approved", "Approved"),
        ("needs_revision", "Needs Revision"),
        ("archived", "Archived"),
    ]

    COMPLEXITY_CHOICES = [
        ("simple", "Simple"),
        ("moderate", "Moderate"),
        ("complex", "Complex"),
        ("highly_complex", "Highly Complex"),
    ]

    PATIENT_GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("U", "Unknown/Not Specified"),
    ]

    # Core case information
    pg = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="clinical_cases",
        limit_choices_to={"role": "pg"},
        help_text="Postgraduate who created this case",
    )

    case_title = models.CharField(max_length=300, help_text="Descriptive title for the case")

    category = models.ForeignKey(
        CaseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="cases",
        help_text="Category of the clinical case",
    )

    date_encountered = models.DateField(help_text="Date when the case was encountered")

    rotation = models.ForeignKey(
        "rotations.Rotation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clinical_cases",
        help_text="Rotation during which this case occurred",
    )

    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_cases",
        limit_choices_to={"role__in": ["supervisor", "admin"]},
        help_text="Supervising consultant",
    )

    # Patient information (anonymized)
    patient_age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        help_text="Patient age in years",
    )

    patient_gender = models.CharField(
        max_length=1, choices=PATIENT_GENDER_CHOICES, help_text="Patient gender"
    )

    # Case complexity and type
    complexity = models.CharField(
        max_length=20,
        choices=COMPLEXITY_CHOICES,
        default="moderate",
        help_text="Complexity level of the case",
    )

    # Clinical details
    chief_complaint = models.TextField(help_text="Patient's chief complaint or presenting symptoms")

    history_of_present_illness = models.TextField(
        help_text="Detailed history of the present illness"
    )

    past_medical_history = models.TextField(blank=True, help_text="Relevant past medical history")

    family_history = models.TextField(blank=True, help_text="Relevant family history")

    social_history = models.TextField(
        blank=True, help_text="Social history including habits and occupation"
    )

    physical_examination = models.TextField(help_text="Physical examination findings")

    investigations = models.TextField(blank=True, help_text="Investigations ordered and results")

    # Diagnosis and management
    primary_diagnosis = models.ForeignKey(
        "logbook.Diagnosis",
        on_delete=models.SET_NULL,
        null=True,
        related_name="primary_cases",
        help_text="Primary diagnosis",
    )

    secondary_diagnoses = models.ManyToManyField(
        "logbook.Diagnosis",
        blank=True,
        related_name="secondary_cases",
        help_text="Secondary or differential diagnoses",
    )

    differential_diagnosis = models.TextField(
        blank=True, help_text="Differential diagnosis considerations"
    )

    management_plan = models.TextField(help_text="Management and treatment plan")

    procedures_performed = models.ManyToManyField(
        "logbook.Procedure",
        blank=True,
        related_name="clinical_cases",
        help_text="Procedures performed during this case",
    )

    # Educational aspects
    learning_objectives = models.TextField(
        blank=True, help_text="Learning objectives for this case"
    )

    clinical_reasoning = models.TextField(help_text="Clinical reasoning and thought process")

    learning_points = models.TextField(help_text="Key learning points from this case")

    challenges_faced = models.TextField(
        blank=True, help_text="Challenges encountered and how they were addressed"
    )

    literature_review = models.TextField(
        blank=True, help_text="Relevant literature review and evidence"
    )

    # Follow-up and outcomes
    outcome = models.TextField(blank=True, help_text="Patient outcome and follow-up")

    follow_up_plan = models.TextField(blank=True, help_text="Follow-up plan and actions required")

    # Assessment and feedback
    supervisor_feedback = models.TextField(
        blank=True, help_text="Supervisor's feedback on this case"
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

    # File attachments
    case_files = models.FileField(
        upload_to=case_file_upload_path,
        blank=True,
        null=True,
        help_text="Additional case files (reports, documents)",
    )

    case_images = models.ImageField(
        upload_to=case_image_upload_path,
        blank=True,
        null=True,
        help_text="Case images (X-rays, scans, photos)",
    )

    # Status and workflow
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        help_text="Current status of the case",
    )

    is_active = models.BooleanField(default=True, help_text="Whether this case is active")

    is_featured = models.BooleanField(
        default=False, help_text="Mark as featured case for educational purposes"
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_cases",
        help_text="User who created this case",
    )

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_cases",
        help_text="User who reviewed/approved this case",
    )

    reviewed_at = models.DateTimeField(
        null=True, blank=True, help_text="Date and time when case was reviewed"
    )

    class Meta:
        verbose_name = "Clinical Case"
        verbose_name_plural = "Clinical Cases"
        ordering = ["-date_encountered", "-created_at"]
        indexes = [
            models.Index(fields=["pg", "date_encountered"]),
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["complexity"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["created_at"]),
        ]
        # Note: Date validation is handled in the clean() method
        # Database CHECK constraints with dynamic values (e.g., timezone.now().date()) are evaluated at migration time,
        # not at runtime. This means such constraints will not behave as expected for future data changes.
        # Therefore, only static values should be used in database constraints; dynamic date validation is done in clean().
        constraints = [
            models.CheckConstraint(
                check=models.Q(patient_age__gte=0) & models.Q(patient_age__lte=150),
                name="case_valid_age",
            ),
        ]

    def __str__(self):
        return f"{self.case_title} - {self.pg.get_full_name()}"

    def clean(self):
        """Validate case data"""
        errors = {}

        # Validate date is not in the future
        if self.date_encountered and self.date_encountered > timezone.now().date():
            errors["date_encountered"] = "Case date cannot be in the future"

        # Validate date is not too old (more than 2 years)
        if self.date_encountered and self.date_encountered < (
            timezone.now().date() - timedelta(days=730)
        ):
            errors["date_encountered"] = "Case date cannot be more than 2 years old"

        # Validate supervisor assignment for PG's rotation
        # Guard: only validate if both FKs are set (avoids RelatedObjectDoesNotExist before save)
        if self.supervisor_id and self.pg_id and self.rotation_id:
            if (
                self.pg.supervisor
                and self.supervisor != self.pg.supervisor
                and not self.supervisor.role == "admin"
            ):
                errors["supervisor"] = "Supervisor should be the PG's assigned supervisor"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Override save to handle validation and auto-assignments"""
        self.full_clean()

        # Auto-assign supervisor if not set
        if not self.supervisor and hasattr(self, "pg") and self.pg_id:
            pg = self.pg
            if pg and pg.supervisor:
                self.supervisor = pg.supervisor

        # Set created_by on first save
        if not self.pk and not self.created_by:
            # This will need to be set in the view/admin
            pass

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get absolute URL for this case"""
        return reverse("cases:case_detail", kwargs={"pk": self.pk})

    def can_be_edited(self):
        """Check if case can be edited"""
        return self.status in ["draft", "needs_revision"]

    def can_be_deleted(self):
        """Check if case can be deleted"""
        return self.status == "draft"

    def can_be_submitted(self):
        """Check if case can be submitted for review"""
        return self.status == "draft"

    def can_be_reviewed(self):
        """Check if case can be reviewed"""
        return self.status in ["submitted", "under_review"]

    def is_complete(self):
        """Check if case has all required fields filled"""
        required_fields = [
            self.case_title,
            self.chief_complaint,
            self.history_of_present_illness,
            self.physical_examination,
            self.management_plan,
            self.clinical_reasoning,
            self.learning_points,
        ]
        return all(field for field in required_fields)

    def can_edit(self, user):
        """Check if user can edit this case"""
        # Admin can edit any case
        if user.is_admin():
            return True
        # PG can edit their own draft cases
        if user == self.pg and self.status in ["draft", "needs_revision"]:
            return True
        # Supervisor can edit cases assigned to them
        if user == self.supervisor:
            return True
        return False

    def is_overdue(self):
        """Check if case submission is overdue"""
        if self.status != "draft":
            return False

        # Consider overdue if older than 30 days
        return (timezone.now().date() - self.date_encountered).days > 30

    def get_complexity_badge_class(self):
        """Get CSS class for complexity badge"""
        complexity_classes = {
            "simple": "badge-success",
            "moderate": "badge-info",
            "complex": "badge-warning",
            "highly_complex": "badge-danger",
        }
        return complexity_classes.get(self.complexity, "badge-secondary")

    def get_status_badge_class(self):
        """Get CSS class for status badge"""
        status_classes = {
            "draft": "badge-secondary",
            "submitted": "badge-warning",
            "approved": "badge-success",
            "needs_revision": "badge-danger",
            "archived": "badge-dark",
        }
        return status_classes.get(self.status, "badge-secondary")

    def get_procedure_count(self):
        """Get count of procedures performed"""
        return self.procedures_performed.count()

    def get_diagnosis_count(self):
        """Get total count of diagnoses"""
        return self.secondary_diagnoses.count() + (1 if self.primary_diagnosis else 0)


class CaseReview(models.Model):
    """
    Model representing reviews and feedback for clinical cases.

    Created: 2025-05-29 17:45:00 UTC
    Author: SMIB2012
    """

    STATUS_CHOICES = [
        ("approved", "Approved"),
        ("needs_revision", "Needs Revision"),
        ("rejected", "Rejected"),
    ]

    case = models.ForeignKey(
        ClinicalCase,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Case being reviewed",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="case_reviews",
        limit_choices_to={"role__in": ["supervisor", "admin"]},
        help_text="User conducting the review",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, help_text="Review outcome")

    review_date = models.DateField(
        default=date.today, help_text="Date when the review was conducted"
    )

    # Detailed feedback
    overall_feedback = models.TextField(help_text="Overall feedback on the case presentation")

    clinical_reasoning_feedback = models.TextField(
        blank=True, help_text="Feedback on clinical reasoning"
    )

    documentation_feedback = models.TextField(
        blank=True, help_text="Feedback on case documentation"
    )

    learning_points_feedback = models.TextField(
        blank=True, help_text="Feedback on learning points identified"
    )

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

    # Assessment scores
    clinical_knowledge_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Clinical knowledge score (1-10)",
    )

    clinical_reasoning_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Clinical reasoning score (1-10)",
    )

    documentation_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Documentation quality score (1-10)",
    )

    overall_score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Overall performance score (1-10)",
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Case Review"
        verbose_name_plural = "Case Reviews"
        ordering = ["-created_at"]
        unique_together = [["case", "reviewer", "review_date"]]

    def __str__(self):
        return f"Review of {self.case.case_title} by {self.reviewer.get_full_name()}"

    def clean(self):
        """Validate review data"""
        errors = {}

        # Ensure reviewer is not the case author
        if (
            hasattr(self, "case")
            and self.case_id
            and hasattr(self, "reviewer")
            and self.reviewer_id
        ):
            if self.case.pg == self.reviewer:
                errors["reviewer"] = "Case author cannot review their own case"

        # Validate review date
        if self.review_date and self.review_date > timezone.now().date():
            errors["review_date"] = "Review date cannot be in the future"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Override save to update case status"""
        self.full_clean()
        super().save(*args, **kwargs)

        # Update case status based on review
        if self.case:
            self.case.status = self.status
            self.case.reviewed_by = self.reviewer
            self.case.reviewed_at = timezone.now()
            if self.overall_score:
                self.case.supervisor_assessment_score = self.overall_score
            self.case.save()


class CaseStatistics(models.Model):
    """
    Model for tracking statistics and analytics for clinical cases.

    Created: 2025-05-29 17:45:00 UTC
    Author: SMIB2012
    """

    pg = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="case_statistics",
        limit_choices_to={"role": "pg"},
        help_text="Postgraduate for these statistics",
    )

    # Case counts
    total_cases = models.PositiveIntegerField(
        default=0, help_text="Total number of cases submitted"
    )

    approved_cases = models.PositiveIntegerField(default=0, help_text="Number of approved cases")

    pending_cases = models.PositiveIntegerField(
        default=0, help_text="Number of cases pending review"
    )

    draft_cases = models.PositiveIntegerField(default=0, help_text="Number of draft cases")

    # Case complexity distribution
    simple_cases = models.PositiveIntegerField(
        default=0, help_text="Number of simple complexity cases"
    )

    moderate_cases = models.PositiveIntegerField(
        default=0, help_text="Number of moderate complexity cases"
    )

    complex_cases = models.PositiveIntegerField(default=0, help_text="Number of complex cases")

    highly_complex_cases = models.PositiveIntegerField(
        default=0, help_text="Number of highly complex cases"
    )

    # Performance metrics
    average_self_score = models.FloatField(default=0.0, help_text="Average self-assessment score")

    average_supervisor_score = models.FloatField(
        default=0.0, help_text="Average supervisor assessment score"
    )

    completion_rate = models.FloatField(
        default=0.0, help_text="Percentage of cases completed vs required"
    )

    # Time metrics
    average_submission_time = models.FloatField(
        default=0.0, help_text="Average days from encounter to submission"
    )

    overdue_cases = models.PositiveIntegerField(
        default=0, help_text="Number of overdue case submissions"
    )

    # Update tracking
    last_updated = models.DateTimeField(
        auto_now=True, help_text="Last time statistics were updated"
    )

    class Meta:
        verbose_name = "Case Statistics"
        verbose_name_plural = "Case Statistics"

    def __str__(self):
        return f"Case Statistics for {self.pg.get_full_name()}"

    def update_statistics(self):
        """Update all statistics for this PG"""
        cases = ClinicalCase.objects.filter(pg=self.pg, is_active=True)

        # Update case counts
        self.total_cases = cases.count()
        self.approved_cases = cases.filter(status="approved").count()
        self.pending_cases = cases.filter(status="submitted").count()
        self.draft_cases = cases.filter(status="draft").count()

        # Update complexity distribution
        self.simple_cases = cases.filter(complexity="simple").count()
        self.moderate_cases = cases.filter(complexity="moderate").count()
        self.complex_cases = cases.filter(complexity="complex").count()
        self.highly_complex_cases = cases.filter(complexity="highly_complex").count()

        # Update performance metrics
        self_scores = cases.filter(self_assessment_score__isnull=False).values_list(
            "self_assessment_score", flat=True
        )

        if self_scores:
            self.average_self_score = sum(self_scores) / len(self_scores)

        supervisor_scores = cases.filter(supervisor_assessment_score__isnull=False).values_list(
            "supervisor_assessment_score", flat=True
        )

        if supervisor_scores:
            self.average_supervisor_score = sum(supervisor_scores) / len(supervisor_scores)

        # Update completion rate (assuming minimum requirement)
        required_cases = 50  # This could be configurable
        self.completion_rate = (self.approved_cases / required_cases) * 100 if required_cases else 0

        # Update time metrics
        submitted_cases = cases.exclude(status="draft")
        if submitted_cases.exists():
            submission_times = []
            for case in submitted_cases:
                if case.created_at and case.date_encountered:
                    days_diff = (case.created_at.date() - case.date_encountered).days
                    submission_times.append(days_diff)

            if submission_times:
                self.average_submission_time = sum(submission_times) / len(submission_times)

        # Count overdue cases
        self.overdue_cases = sum(1 for case in cases.filter(status="draft") if case.is_overdue())

        self.save()

    def get_performance_trend(self):
        """Get performance trend indicator"""
        if self.average_supervisor_score >= self.average_self_score:
            return "improving"
        elif self.average_supervisor_score < self.average_self_score - 2:
            return "needs_attention"
        else:
            return "stable"

    def get_completion_status(self):
        """Get completion status indicator"""
        if self.completion_rate >= 90:
            return "excellent"
        elif self.completion_rate >= 70:
            return "good"
        elif self.completion_rate >= 50:
            return "satisfactory"
        else:
            return "poor"
