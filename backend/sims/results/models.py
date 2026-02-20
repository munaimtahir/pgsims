"""
Models for Results and Exams in SIMS.

This module defines:
- Exam: Examination/assessment records
- Score: Individual student scores for exams
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Exam(models.Model):
    """Exam/Assessment model."""

    EXAM_TYPE_CHOICES = [
        ("theory", "Theory"),
        ("practical", "Practical"),
        ("viva", "Viva Voce"),
        ("internal", "Internal Assessment"),
        ("midterm", "Midterm"),
        ("final", "Final Exam"),
        ("quiz", "Quiz"),
        ("assignment", "Assignment"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=200, help_text="Exam title")
    exam_type = models.CharField(
        max_length=20,
        choices=EXAM_TYPE_CHOICES,
        default="theory",
        help_text="Type of exam",
    )

    # Link to rotation or module
    rotation = models.ForeignKey(
        "rotations.Rotation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exams",
        help_text="Associated rotation (if applicable)",
    )

    module_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Module or course name (if not rotation-based)",
    )

    # Exam details
    date = models.DateField(help_text="Exam date")
    start_time = models.TimeField(null=True, blank=True, help_text="Start time")
    duration_minutes = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Duration in minutes",
    )

    max_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=100.0,
        validators=[MinValueValidator(0.0)],
        help_text="Maximum marks for this exam",
    )

    passing_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=40.0,
        validators=[MinValueValidator(0.0)],
        help_text="Passing marks threshold",
    )

    # Eligibility check
    requires_eligibility = models.BooleanField(
        default=False,
        help_text="Check attendance eligibility before allowing exam?",
    )

    # Status and metadata
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
        help_text="Current exam status",
    )

    conducted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conducted_exams",
        help_text="Exam conductor/invigilator",
    )

    instructions = models.TextField(blank=True, help_text="Exam instructions")
    remarks = models.TextField(blank=True, help_text="Additional remarks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ["-date", "title"]
        indexes = [
            models.Index(fields=["date", "status"]),
            models.Index(fields=["exam_type"]),
            models.Index(fields=["rotation"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.exam_type}) - {self.date}"

    def is_passing(self, marks):
        """Check if given marks are passing."""
        return marks >= self.passing_marks

    def calculate_percentage(self, marks):
        """Calculate percentage for given marks."""
        if self.max_marks > 0:
            return round((marks / self.max_marks) * 100, 2)
        return 0.0


class Score(models.Model):
    """Individual student score for an exam."""

    GRADE_CHOICES = [
        ("A+", "A+ (90-100)"),
        ("A", "A (80-89)"),
        ("B+", "B+ (70-79)"),
        ("B", "B (60-69)"),
        ("C+", "C+ (50-59)"),
        ("C", "C (40-49)"),
        ("F", "F (Below 40)"),
    ]

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="scores",
        help_text="Associated exam",
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_scores",
        limit_choices_to={"role": "pg"},
        help_text="Student",
    )

    marks_obtained = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Marks obtained by student",
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Percentage scored",
    )

    grade = models.CharField(
        max_length=5,
        choices=GRADE_CHOICES,
        blank=True,
        help_text="Letter grade",
    )

    is_passing = models.BooleanField(
        default=False,
        help_text="Did student pass?",
    )

    is_eligible = models.BooleanField(
        default=True,
        help_text="Was student eligible to appear in exam?",
    )

    ineligibility_reason = models.CharField(
        max_length=200,
        blank=True,
        help_text="Reason for ineligibility (if applicable)",
    )

    remarks = models.TextField(blank=True, help_text="Additional remarks")

    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entered_scores",
        help_text="User who entered this score",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        unique_together = ["exam", "student"]
        ordering = ["-exam__date", "student__last_name"]
        indexes = [
            models.Index(fields=["exam", "student"]),
            models.Index(fields=["is_passing"]),
            models.Index(fields=["grade"]),
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam.title} ({self.marks_obtained}/{self.exam.max_marks})"

    def save(self, *args, **kwargs):
        """Auto-calculate percentage, grade, and passing status on save."""
        # Calculate percentage
        self.percentage = self.exam.calculate_percentage(self.marks_obtained)

        # Determine passing status
        self.is_passing = self.exam.is_passing(self.marks_obtained)

        # Auto-assign grade based on percentage
        if self.percentage >= 90:
            self.grade = "A+"
        elif self.percentage >= 80:
            self.grade = "A"
        elif self.percentage >= 70:
            self.grade = "B+"
        elif self.percentage >= 60:
            self.grade = "B"
        elif self.percentage >= 50:
            self.grade = "C+"
        elif self.percentage >= 40:
            self.grade = "C"
        else:
            self.grade = "F"

        super().save(*args, **kwargs)

    def check_eligibility(self):
        """
        Check if student is eligible based on attendance.
        Returns tuple (is_eligible, reason).
        """
        if not self.exam.requires_eligibility:
            return True, ""

        # Check attendance eligibility from attendance app
        from sims.attendance.models import EligibilitySummary
        from django.conf import settings

        threshold = getattr(settings, "ATTENDANCE_THRESHOLD", 75.0)

        # Find the most recent eligibility summary for this student
        eligibility = (
            EligibilitySummary.objects.filter(
                user=self.student,
                end_date__lte=self.exam.date,
            )
            .order_by("-end_date")
            .first()
        )

        if eligibility and eligibility.is_eligible:
            return True, ""
        elif eligibility:
            return False, f"Attendance below {threshold}% ({eligibility.percentage_present}%)"
        else:
            # No eligibility record found, assume eligible
            return True, ""
