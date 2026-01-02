"""
Models for Academic management in SIMS.

This module defines:
- Department: Academic departments
- Batch: Student batches/cohorts
- StudentProfile: Extended student information from admission to graduation
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


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
        limit_choices_to={"role__in": ["admin", "supervisor"]},
        help_text="Department head",
    )
    active = models.BooleanField(default=True, help_text="Is department active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Batch(models.Model):
    """Student batch/cohort model."""

    PROGRAM_CHOICES = [
        ("mbbs", "MBBS"),
        ("md", "MD"),
        ("ms", "MS"),
        ("dm", "DM"),
        ("mch", "MCh"),
        ("diploma", "Diploma"),
        ("fellowship", "Fellowship"),
    ]

    name = models.CharField(max_length=100, help_text="Batch name (e.g., 2024 Batch)")
    program = models.CharField(
        max_length=50,
        choices=PROGRAM_CHOICES,
        help_text="Academic program",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="batches",
        help_text="Department for this batch",
    )
    start_date = models.DateField(help_text="Batch start date")
    end_date = models.DateField(help_text="Expected batch end date")
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordinated_batches",
        limit_choices_to={"role__in": ["admin", "supervisor"]},
        help_text="Batch coordinator",
    )
    capacity = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1)],
        help_text="Maximum students in batch",
    )
    active = models.BooleanField(default=True, help_text="Is batch active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batches"
        ordering = ["-start_date", "name"]
        unique_together = ["name", "department", "start_date"]
        indexes = [
            models.Index(fields=["program"]),
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.department.code} ({self.program})"

    def current_strength(self):
        """Return current number of students in batch."""
        return self.student_profiles.filter(status__in=["enrolled", "active"]).count()

    def is_full(self):
        """Check if batch has reached capacity."""
        return self.current_strength() >= self.capacity


class StudentProfile(models.Model):
    """
    Extended student profile tracking admission to graduation.
    Linked to User model for authentication.
    """

    STATUS_CHOICES = [
        ("admitted", "Admitted"),
        ("enrolled", "Enrolled"),
        ("active", "Active"),
        ("on_leave", "On Leave"),
        ("suspended", "Suspended"),
        ("withdrawn", "Withdrawn"),
        ("graduated", "Graduated"),
        ("expelled", "Expelled"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        limit_choices_to={"role": "pg"},
        help_text="Linked user account",
    )

    # Academic Information
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name="student_profiles",
        help_text="Student's batch",
    )
    roll_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Student roll/registration number",
    )
    admission_date = models.DateField(help_text="Date of admission")
    expected_graduation_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected graduation date",
    )
    actual_graduation_date = models.DateField(
        null=True,
        blank=True,
        help_text="Actual graduation date",
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="admitted",
        help_text="Current enrollment status",
    )
    status_updated_at = models.DateTimeField(
        default=timezone.now,
        help_text="Last status change date",
    )

    # Academic Performance
    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Cumulative GPA",
    )

    # Additional Information
    previous_institution = models.CharField(
        max_length=200,
        blank=True,
        help_text="Previous institution",
    )
    previous_qualification = models.CharField(
        max_length=100,
        blank=True,
        help_text="Previous qualification",
    )

    # Emergency Contact
    emergency_contact_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Emergency contact person name",
    )
    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Emergency contact phone",
    )
    emergency_contact_relation = models.CharField(
        max_length=50,
        blank=True,
        help_text="Relationship to student",
    )

    # Remarks
    remarks = models.TextField(blank=True, help_text="Additional remarks")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
        ordering = ["roll_number"]
        indexes = [
            models.Index(fields=["roll_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["admission_date"]),
        ]

    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"

    def update_status(self, new_status):
        """Update student status with timestamp."""
        self.status = new_status
        self.status_updated_at = timezone.now()
        self.save()

    def is_active(self):
        """Check if student is currently active."""
        return self.status in ["enrolled", "active"]

    def duration_in_program(self):
        """Calculate duration in program (in days)."""
        end_date = self.actual_graduation_date or timezone.now().date()
        return (end_date - self.admission_date).days
