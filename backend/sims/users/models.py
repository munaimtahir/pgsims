from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Role choices for the SIMS system
USER_ROLES = (
    ("admin", "Admin"),
    ("supervisor", "Supervisor"),
    ("pg", "Postgraduate"),
    ("resident", "Resident"),
    ("faculty", "Faculty"),
    ("utrmc_user", "UTRMC User"),
    ("utrmc_admin", "UTRMC Admin"),
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
    ("urology", "Urology"),
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
        limit_choices_to={"role__in": ["supervisor", "faculty"]},
        help_text="Assigned supervisor (required for PGs)",
    )

    home_hospital = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_pgs",
        help_text="Primary home hospital for PG users until graduation",
    )

    home_department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_pgs",
        help_text="Primary home department for PG users until graduation",
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
        """Validate model fields — only prevent self-supervision."""
        super().clean()
        if self.supervisor and self.pk and self.supervisor_id == self.pk:
            raise ValidationError({"supervisor": "Users cannot supervise themselves"})

    def save(self, *args, **kwargs):
        """Override save to handle archiving."""
        if self.is_archived and not self.archived_date:
            self.archived_date = timezone.now()
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
        """Check if user is a resident/postgraduate."""
        return self.role in {"pg", "resident"}

    def is_resident(self):
        """Check if user is explicitly resident role."""
        return self.role == "resident"

    def is_faculty(self):
        """Check if user is faculty role."""
        return self.role == "faculty"

    def is_utrmc_user(self):
        """Check if user is UTRMC read-only oversight user."""
        return self.role == "utrmc_user"

    def is_utrmc_admin(self):
        """Check if user is UTRMC admin user."""
        return self.role == "utrmc_admin"

    # Relationship methods
    def get_assigned_pgs(self):
        """Get all PGs assigned to this supervisor"""
        if self.is_supervisor():
            return self.assigned_pgs.filter(is_active=True, is_archived=False)
        if self.is_faculty():
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
        if self.role in {"admin", "utrmc_admin", "utrmc_user"}:
            return "/dashboard/utrmc"
        elif self.role in {"supervisor", "faculty"}:
            return "/dashboard/supervisor"
        elif self.role in {"pg", "resident"}:
            return "/dashboard/resident"
        return "/dashboard"

    def get_absolute_url(self):
        return "/dashboard"

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
            "resident": "badge-info",
            "faculty": "badge-primary",
            "utrmc_user": "badge-secondary",
            "utrmc_admin": "badge-dark",
        }
        return role_classes.get(self.role, "badge-secondary")

class StaffProfile(models.Model):
    """Profile metadata for faculty and supervisors."""

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="staff_profile",
        limit_choices_to={"role__in": ["supervisor", "faculty"]},
    )
    designation = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]
        indexes = [models.Index(fields=["active"])]

    def __str__(self):
        return f"StaffProfile<{self.user_id}>"

    def clean(self):
        super().clean()
        if self.user_id and self.user.role not in {"supervisor", "faculty"}:
            raise ValidationError({"user": "Staff profile requires supervisor/faculty role."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ResidentProfile(models.Model):
    """Training metadata for residents/postgraduates."""

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="resident_profile",
        limit_choices_to={"role__in": ["pg", "resident"]},
    )
    pgr_id = models.CharField(max_length=60, blank=True)
    training_start = models.DateField()
    training_end = models.DateField(null=True, blank=True)
    training_level = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]
        indexes = [models.Index(fields=["active"]), models.Index(fields=["training_start"])]

    def __str__(self):
        return f"ResidentProfile<{self.user_id}>"

    def clean(self):
        super().clean()
        if self.user_id and self.user.role not in {"pg", "resident"}:
            raise ValidationError({"user": "Resident profile requires pg/resident role."})
        if self.training_end and self.training_end < self.training_start:
            raise ValidationError({"training_end": "Training end must be on/after training_start."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class DepartmentMembership(models.Model):
    """Membership mapping between users and departments."""

    MEMBER_FACULTY = "faculty"
    MEMBER_SUPERVISOR = "supervisor"
    MEMBER_RESIDENT = "resident"
    MEMBER_TYPE_CHOICES = (
        (MEMBER_FACULTY, "Faculty"),
        (MEMBER_SUPERVISOR, "Supervisor"),
        (MEMBER_RESIDENT, "Resident"),
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="department_memberships"
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES)
    is_primary = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="department_memberships_created",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="department_memberships_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["department__name", "user__last_name", "user__first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(is_primary=True, active=True),
                name="uniq_active_primary_dept_member_user",
            ),
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True)
                | models.Q(end_date__gte=models.F("start_date")),
                name="dept_member_dates_valid",
            ),
        ]
        indexes = [
            models.Index(fields=["department", "member_type", "active"]),
            models.Index(fields=["user", "active"]),
        ]

    def __str__(self):
        return f"{self.department} / {self.user} / {self.member_type}"

    def clean(self):
        super().clean()
        role_map = {
            self.MEMBER_FACULTY: {"faculty"},
            self.MEMBER_SUPERVISOR: {"supervisor"},
            self.MEMBER_RESIDENT: {"pg", "resident"},
        }
        if self.user_id and self.user.role not in role_map[self.member_type]:
            raise ValidationError({"member_type": "member_type must match user role."})
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "end_date must be on/after start_date."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class HospitalAssignment(models.Model):
    """Maps users to hospital/department matrix sites."""

    ASSIGNMENT_PRIMARY_TRAINING = "primary_training"
    ASSIGNMENT_POSTING = "posting"
    ASSIGNMENT_FACULTY_SITE = "faculty_site"
    ASSIGNMENT_TYPE_CHOICES = (
        (ASSIGNMENT_PRIMARY_TRAINING, "Primary Training"),
        (ASSIGNMENT_POSTING, "Posting"),
        (ASSIGNMENT_FACULTY_SITE, "Faculty Site"),
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="hospital_assignments"
    )
    hospital_department = models.ForeignKey(
        "rotations.HospitalDepartment",
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    assignment_type = models.CharField(max_length=30, choices=ASSIGNMENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hospital_assignments_created",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hospital_assignments_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["hospital_department__hospital__name", "user__last_name"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True)
                | models.Q(end_date__gte=models.F("start_date")),
                name="hospital_assignment_dates_valid",
            )
        ]
        indexes = [
            models.Index(fields=["user", "active"]),
            models.Index(fields=["hospital_department", "active"]),
        ]

    def __str__(self):
        return f"{self.user} @ {self.hospital_department}"

    def clean(self):
        super().clean()
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "end_date must be on/after start_date."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class SupervisorResidentLink(models.Model):
    """Tracks dated supervisor/faculty to resident links."""

    supervisor_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="supervisor_links",
    )
    resident_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="resident_links",
    )
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervision_links",
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervision_links_created",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervision_links_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-active", "resident_user__last_name"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True)
                | models.Q(end_date__gte=models.F("start_date")),
                name="supervision_link_dates_valid",
            ),
            models.UniqueConstraint(
                fields=["supervisor_user", "resident_user", "department"],
                condition=models.Q(active=True),
                name="uniq_active_supervision_link",
            ),
        ]
        indexes = [
            models.Index(fields=["supervisor_user", "active"]),
            models.Index(fields=["resident_user", "active"]),
            models.Index(fields=["department", "active"]),
        ]

    def __str__(self):
        return f"{self.supervisor_user} -> {self.resident_user}"

    def clean(self):
        super().clean()
        if self.supervisor_user_id and self.supervisor_user.role not in {"supervisor", "faculty"}:
            raise ValidationError(
                {"supervisor_user": "Supervisor must have supervisor/faculty role."}
            )
        if self.resident_user_id and self.resident_user.role not in {"pg", "resident"}:
            raise ValidationError({"resident_user": "Resident must have pg/resident role."})
        if (
            self.supervisor_user_id
            and self.resident_user_id
            and self.supervisor_user_id == self.resident_user_id
        ):
            raise ValidationError(
                {"resident_user": "Supervisor and resident must be different users."}
            )
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "end_date must be on/after start_date."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class HODAssignment(models.Model):
    """Tracks dated HOD assignment per department."""

    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.CASCADE,
        related_name="hod_assignments",
    )
    hod_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="hod_assignments",
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hod_assignments_created",
    )
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hod_assignments_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["department__name", "-start_date"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__isnull=True)
                | models.Q(end_date__gte=models.F("start_date")),
                name="hod_assignment_dates_valid",
            ),
            models.UniqueConstraint(
                fields=["department"],
                condition=models.Q(active=True),
                name="uniq_active_hod_assignment_per_department",
            ),
        ]
        indexes = [
            models.Index(fields=["department", "active"]),
            models.Index(fields=["hod_user", "active"]),
        ]

    def __str__(self):
        return f"HOD<{self.department}>: {self.hod_user}"

    def clean(self):
        super().clean()
        if self.hod_user_id and self.hod_user.role not in {"faculty", "supervisor"}:
            raise ValidationError({"hod_user": "HOD must have faculty/supervisor role."})
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "end_date must be on/after start_date."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

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

            if apps.is_installed("sims.training"):
                from sims.training.models import RotationAssignment

                count += RotationAssignment.objects.filter(
                    resident_training__resident_user=self
                ).count()

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
