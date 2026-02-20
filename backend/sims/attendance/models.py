"""
Attendance and Eligibility models for tracking PG attendance and exam eligibility.

Created for SIMS production-ready release.
"""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Session(models.Model):
    """
    Model representing an attendance session (lecture, clinical rotation, etc.).
    """

    SESSION_TYPE_CHOICES = [
        ("lecture", "Lecture"),
        ("clinical", "Clinical Rotation"),
        ("tutorial", "Tutorial"),
        ("seminar", "Seminar"),
        ("workshop", "Workshop"),
        ("practical", "Practical Session"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    title = models.CharField(max_length=200, help_text="Title of the session")
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default="lecture",
        help_text="Type of session",
    )
    date = models.DateField(help_text="Date of the session")
    start_time = models.TimeField(help_text="Start time of the session")
    end_time = models.TimeField(help_text="End time of the session")

    # Link to module or rotation (optional)
    rotation = models.ForeignKey(
        "rotations.Rotation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions",
        help_text="Associated rotation (if applicable)",
    )

    module_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Module or course name (if not rotation-based)",
    )

    location = models.CharField(max_length=200, blank=True, help_text="Location of the session")

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taught_sessions",
        help_text="Instructor or facilitator",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
        help_text="Current status of the session",
    )

    notes = models.TextField(blank=True, help_text="Additional notes about the session")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance Session"
        verbose_name_plural = "Attendance Sessions"
        ordering = ["-date", "-start_time"]
        indexes = [
            models.Index(fields=["date", "status"]),
            models.Index(fields=["rotation"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.date}"


class AttendanceRecord(models.Model):
    """
    Model representing an individual's attendance record for a session.
    """

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused Absence"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        help_text="User (PG) this record belongs to",
    )

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="attendance_records",
        help_text="Session this record is for",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="present",
        help_text="Attendance status",
    )

    check_in_time = models.DateTimeField(null=True, blank=True, help_text="Time user checked in")

    remarks = models.TextField(blank=True, help_text="Additional remarks or notes")

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_attendance",
        help_text="User who recorded this attendance",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        unique_together = ["user", "session"]
        ordering = ["-session__date", "user__last_name"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["session", "status"]),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.session.title} ({self.status})"


class EligibilitySummary(models.Model):
    """
    Model representing eligibility summary based on attendance.

    Business rule: eligible if attendance >= 75% (configurable via env).
    """

    PERIOD_CHOICES = [
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("semester", "Semester"),
        ("yearly", "Yearly"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eligibility_summaries",
        help_text="User (PG) this summary is for",
    )

    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        help_text="Time period for this summary",
    )

    start_date = models.DateField(help_text="Start date of the period")
    end_date = models.DateField(help_text="End date of the period")

    total_sessions = models.IntegerField(
        default=0, help_text="Total number of sessions in this period"
    )

    attended_sessions = models.IntegerField(
        default=0, help_text="Number of sessions attended (present or late)"
    )

    percentage_present = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Percentage of sessions attended",
    )

    is_eligible = models.BooleanField(
        default=False, help_text="Whether user meets eligibility threshold"
    )

    threshold_percentage = models.FloatField(
        default=75.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Threshold percentage for eligibility (default 75%)",
    )

    remarks = models.TextField(blank=True, help_text="Additional remarks")

    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Eligibility Summary"
        verbose_name_plural = "Eligibility Summaries"
        unique_together = ["user", "period", "start_date", "end_date"]
        ordering = ["-start_date", "user__last_name"]
        indexes = [
            models.Index(fields=["user", "period"]),
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["is_eligible"]),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.period} ({self.start_date} to {self.end_date})"

    def calculate_eligibility(self):
        """Calculate and update eligibility based on attendance percentage."""
        if self.total_sessions > 0:
            self.percentage_present = round((self.attended_sessions / self.total_sessions) * 100, 2)
        else:
            self.percentage_present = 0.0

        self.is_eligible = self.percentage_present >= self.threshold_percentage
        self.save()
