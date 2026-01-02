from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Role choices for the SIMS system
USER_ROLES = (
    ("admin", "Admin"),
    ("supervisor", "Supervisor"),
    ("pg", "Postgraduate"),
)

# Medical specialty choices (expand as needed)
SPECIALTY_CHOICES = (
    ("medicine", "Internal Medicine"),
    ("surgery", "Surgery"),
    ("pediatrics", "Pediatrics"),
    ("gynecology", "Gynecology & Obstetrics"),
    ("orthopedics", "Orthopedics"),
    ("cardiology", "Cardiology"),
    ("neurology", "Neurology"),
    ("psychiatry", "Psychiatry"),
    ("dermatology", "Dermatology"),
    ("radiology", "Radiology"),
    ("anesthesia", "Anesthesia"),
    ("pathology", "Pathology"),
    ("microbiology", "Microbiology"),
    ("pharmacology", "Pharmacology"),
    ("community_medicine", "Community Medicine"),
    ("forensic_medicine", "Forensic Medicine"),
    ("other", "Other"),
)

# Year choices for PG training
YEAR_CHOICES = (
    ("1", "Year 1"),
    ("2", "Year 2"),
    ("3", "Year 3"),
    ("4", "Year 4"),  # For some specialties
)


class User(AbstractUser):
    """
    Custom User model for SIMS with role-based access control.

    Extends Django's AbstractUser to include medical training specific fields:
    - Role-based permissions (Admin/Supervisor/PG)
    - Medical specialty and training year
    - Supervisor-PG relationships
    - Audit trail fields

    Created: 2025-05-29 15:57:19 UTC
    Author: SMIB2012
    """

    # Core SIMS fields
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        help_text="User role determines access permissions in SIMS",
    )

    specialty = models.CharField(
        max_length=100,
        choices=SPECIALTY_CHOICES,
        blank=True,
        null=True,
        help_text="Medical specialty (required for PGs and Supervisors)",
    )

    year = models.CharField(
        max_length=10,
        choices=YEAR_CHOICES,
        blank=True,
        null=True,
        help_text="Training year (required for PGs)",
    )

    supervisor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_pgs",
        limit_choices_to={"role": "supervisor"},
        help_text="Assigned supervisor (required for PGs)",
    )

    # Profile fields
    registration_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Medical council registration number",
    )

    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="Contact phone number"
    )

    # Audit fields
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_created",
        help_text="Admin who created this user account",
    )

    modified_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_modified",
        help_text="Last admin to modify this user account",
    )

    last_login_ip = models.GenericIPAddressField(
        null=True, blank=True, help_text="IP address of last login"
    )

    # Status fields
    is_archived = models.BooleanField(
        default=False, help_text="Mark as archived instead of deleting"
    )

    archived_date = models.DateTimeField(
        null=True, blank=True, help_text="Date when user was archived"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "SIMS User"
        verbose_name_plural = "SIMS Users"
        ordering = ["role", "last_name", "first_name"]
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["specialty"]),
            models.Index(fields=["supervisor"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        """String representation showing name and role"""
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"

    def clean(self):
        """Validate model fields and business rules"""
        super().clean()

        # PGs must have specialty, year, and supervisor
        if self.role == "pg":
            if not self.specialty:
                raise ValidationError({"specialty": "Specialty is required for PGs"})
            if not self.year:
                raise ValidationError({"year": "Training year is required for PGs"})
            if not self.supervisor:
                raise ValidationError({"supervisor": "Supervisor is required for PGs"})

        # Supervisors must have specialty
        if self.role == "supervisor" and not self.specialty:
            raise ValidationError({"specialty": "Specialty is required for Supervisors"})

        # Admins don't need specialty/year/supervisor
        if self.role == "admin":
            if self.supervisor:
                raise ValidationError({"supervisor": "Admins cannot have supervisors"})

        # Prevent self-supervision
        if self.supervisor == self:
            raise ValidationError({"supervisor": "Users cannot supervise themselves"})

        # Ensure supervisor is actually a supervisor
        if self.supervisor and self.supervisor.role != "supervisor":
            raise ValidationError({"supervisor": "Assigned supervisor must have supervisor role"})

    def save(self, *args, **kwargs):
        """Override save to handle archiving and validation"""
        # Run validation
        self.full_clean()

        # Set archived date if being archived
        if self.is_archived and not self.archived_date:
            self.archived_date = timezone.now()

        # Clear archived date if un-archiving
        if not self.is_archived and self.archived_date:
            self.archived_date = None

        super().save(*args, **kwargs)

    # Role checking methods
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == "admin"

    def is_supervisor(self):
        """Check if user is a supervisor"""
        return self.role == "supervisor"

    def is_pg(self):
        """Check if user is a postgraduate"""
        return self.role == "pg"

    # Relationship methods
    def get_assigned_pgs(self):
        """Get all PGs assigned to this supervisor"""
        if self.is_supervisor():
            return self.assigned_pgs.filter(is_active=True, is_archived=False)
        return User.objects.none()

    def get_supervisor_name(self):
        """Get supervisor's full name or username"""
        if self.supervisor:
            return self.supervisor.get_full_name() or self.supervisor.username
        return "No Supervisor Assigned"

    # Dashboard URLs
    def get_dashboard_url(self):
        """Get appropriate dashboard URL based on role"""
        if self.is_admin():
            return reverse("admin:index")
        elif self.is_supervisor():
            return reverse("users:supervisor_dashboard")
        elif self.is_pg():
            return reverse("users:pg_dashboard")
        return reverse("users:profile")

    def get_absolute_url(self):
        """Get URL for user detail/profile"""
        return reverse("users:profile", kwargs={"pk": self.pk})

    # Display methods
    def get_display_name(self):
        """Get display name for UI"""
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    def get_role_badge_class(self):
        """Get CSS class for role badge"""
        role_classes = {
            "admin": "badge-danger",
            "supervisor": "badge-warning",
            "pg": "badge-info",
        }
        return role_classes.get(self.role, "badge-secondary")

    # Statistics methods (for analytics)
    def get_documents_pending_count(self):
        """Get count of documents pending review (for supervisors)"""
        if not self.is_supervisor():
            return 0

        count = 0
        try:
            # Import here to avoid circular imports
            from django.apps import apps

            # Check if apps exist before importing
            if apps.is_installed("sims.certificates"):
                from sims.certificates.models import Certificate

                for pg in self.get_assigned_pgs():
                    count += Certificate.objects.filter(pg=pg, status="pending").count()

            if apps.is_installed("sims.rotations"):
                from sims.rotations.models import Rotation

                for pg in self.get_assigned_pgs():
                    count += Rotation.objects.filter(pg=pg, status="pending").count()

            if apps.is_installed("sims.logbook"):
                from sims.logbook.models import LogbookEntry

                for pg in self.get_assigned_pgs():
                    count += LogbookEntry.objects.filter(pg=pg, status="pending").count()

            if apps.is_installed("sims.cases"):
                from sims.cases.models import ClinicalCase

                for pg in self.get_assigned_pgs():
                    count += ClinicalCase.objects.filter(pg=pg, status="pending").count()

        except ImportError:
            # Handle case where related models don't exist yet
            pass

        return count

    def get_documents_submitted_count(self):
        """Get count of documents submitted by this PG"""
        if not self.is_pg():
            return 0

        count = 0
        try:
            # Import here to avoid circular imports
            from django.apps import apps

            # Check if apps exist before importing
            if apps.is_installed("sims.certificates"):
                from sims.certificates.models import Certificate

                count += Certificate.objects.filter(pg=self).count()

            if apps.is_installed("sims.rotations"):
                from sims.rotations.models import Rotation

                count += Rotation.objects.filter(pg=self).count()

            if apps.is_installed("sims.logbook"):
                from sims.logbook.models import LogbookEntry

                count += LogbookEntry.objects.filter(pg=self).count()

            if apps.is_installed("sims.cases"):
                from sims.cases.models import ClinicalCase

                count += ClinicalCase.objects.filter(pg=self).count()

        except ImportError:
            # Handle case where related models don't exist yet
            pass

        return count
