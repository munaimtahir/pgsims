from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

# Role choices for the SIMS system
USER_ROLES = (
    ("ADMIN", "Admin"),
    ("RESIDENT", "Resident"),
    ("SUPERVISOR", "Supervisor"),
    ("SUPPORT_STAFF", "Support Staff"),
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
    ("5", "Year 5"),  # For 5-year specialties
)


class User(AbstractUser):
    """
    Custom User model for SIMS with role-based access control.

    Extends Django's AbstractUser to include medical training specific fields:
    - Role-based permissions (ADMIN/SUPERVISOR/RESIDENT/SUPPORT_STAFF)
    - Medical specialty and training year
    - Supervisor-PG relationships
    - Audit trail fields
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
        limit_choices_to={"role": "SUPERVISOR"},
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

    is_complete_profile = models.BooleanField(
        default=False,
        help_text="Computed data quality flag for resident/admin correction workflows.",
    )

    is_profile_complete = models.BooleanField(
        default=False,
        help_text="Computed flag indicating if required onboarding profile fields are filled.",
    )

    must_change_password = models.BooleanField(
        default=False,
        help_text="Flag indicating the user must change password on next login.",
    )

    has_placeholder_email = models.BooleanField(
        default=False,
        help_text="True when email appears to be a placeholder value.",
    )

    data_issues = models.JSONField(
        default=list,
        blank=True,
        help_text="Computed list of data quality issue codes for this user.",
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
        return self.role == "ADMIN"

    def is_supervisor(self):
        """Check if user is a supervisor"""
        return self.role == "SUPERVISOR"

    def is_resident(self):
        """Check if user is resident role."""
        return self.role == "RESIDENT"

    def is_support_staff(self):
        """Check if user is support staff role."""
        return self.role == "SUPPORT_STAFF"

    # Compatibility methods
    def is_pg(self):
        return self.role == "RESIDENT"

    def is_faculty(self):
        return self.role == "SUPERVISOR"

    def is_utrmc_user(self):
        return self.role == "ADMIN"

    def is_utrmc_admin(self):
        return self.role == "ADMIN"

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
        if self.role == "ADMIN":
            return "/dashboard/utrmc"
        elif self.role == "SUPERVISOR":
            return "/dashboard/supervisor"
        elif self.role == "RESIDENT":
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
            "ADMIN": "badge-danger",
            "SUPERVISOR": "badge-warning",
            "RESIDENT": "badge-info",
            "SUPPORT_STAFF": "badge-secondary",
        }
        return role_classes.get(self.role, "badge-secondary")

    def get_documents_pending_count(self):
        """
        Get count of pending documents requiring action by this user/supervisor.
        """
        try:
            if self.role == "SUPERVISOR":
                assigned_pgs = self.get_assigned_pgs()
                if not assigned_pgs.exists():
                    return 0
                
                total = 0
                
                # Pending logbook entry reviews
                try:
                    from sims.training.models import LogbookEntry
                    total += LogbookEntry.objects.filter(
                        resident_training_record__resident_user__in=assigned_pgs,
                        status="SUBMITTED"
                    ).count()
                except Exception:
                    pass

                # Pending rotation completion verifications or assignments
                try:
                    from sims.training.models import RotationAssignment
                    total += RotationAssignment.objects.filter(
                        resident_training__resident_user__in=assigned_pgs,
                        status="SUBMITTED"
                    ).count()
                except Exception:
                    pass

                # Pending leave requests
                try:
                    from sims.training.models import LeaveRequest
                    total += LeaveRequest.objects.filter(
                        resident_training__resident_user__in=assigned_pgs,
                        status="SUBMITTED"
                    ).count()
                except Exception:
                    pass

                # Pending synopses/theses
                try:
                    from sims.training.models import ResidentSubmission
                    total += ResidentSubmission.objects.filter(
                        resident_training_record__resident_user__in=assigned_pgs,
                        status="SUBMITTED"
                    ).count()
                except Exception:
                    pass
                
                return total
            
            elif self.role == "RESIDENT":
                total = 0
                try:
                    from sims.training.models import LogbookEntry
                    total += LogbookEntry.objects.filter(
                        resident_training_record__resident_user=self,
                        status="SUBMITTED"
                    ).count()
                except Exception:
                    pass
                return total
        except Exception:
            return 0
        return 0

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


class AdminProfile(models.Model):
    """Profile metadata for admin users."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="admin_profile",
    )
    designation = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    admin_scope = models.TextField(blank=True, help_text="Scope of administrative authority")
    profile_status = models.CharField(
        max_length=20,
        choices=[("INCOMPLETE", "Incomplete"), ("COMPLETE", "Complete")],
        default="INCOMPLETE",
    )
    profile_schema_version = models.PositiveIntegerField(default=1)
    completed_schema_version = models.PositiveIntegerField(default=0)
    profile_completed_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"

    def __str__(self):
        return f"AdminProfile<{self.user_id}>"

    def clean(self):
        super().clean()
        if self.user_id and self.user.role != "ADMIN":
            raise ValidationError({"user": "Admin profile requires ADMIN role."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ResidentProfile(models.Model):
    """Training metadata for residents/postgraduates."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="resident_profile",
    )
    registration_no = models.CharField(max_length=50, blank=True, null=True)
    cnic = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    hospital = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_profiles",
    )
    department_ref = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_profiles",
    )
    program_ref = models.ForeignKey(
        "training.TrainingProgram",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_profiles",
    )
    academic_session_ref = models.ForeignKey(
        "academics.AcademicSession",
        to_field="code",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_profiles",
        db_column="academic_session_ref",
    )
    specialty_ref = models.ForeignKey(
        "academics.Specialty",
        to_field="code",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_profiles",
        db_column="specialty_ref",
    )
    profile_status = models.CharField(
        max_length=20,
        choices=[("INCOMPLETE", "Incomplete"), ("COMPLETE", "Complete")],
        default="INCOMPLETE",
    )
    profile_schema_version = models.PositiveIntegerField(default=1)
    completed_schema_version = models.PositiveIntegerField(default=0)
    profile_completed_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    is_archived = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Resident Profile"
        verbose_name_plural = "Resident Profiles"

    def __str__(self):
        return f"ResidentProfile<{self.user_id}>"

    def clean(self):
        super().clean()
        if self.user_id and self.user.role != "RESIDENT":
            raise ValidationError({"user": "Resident profile requires RESIDENT role."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class SupervisorProfile(models.Model):
    """Profile metadata for supervisors."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="supervisor_profile",
    )
    pmdc_no = models.CharField(max_length=50, blank=True, null=True)
    official_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    hospital = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisor_profiles",
    )
    department_ref = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisor_profiles",
    )
    designation_ref = models.ForeignKey(
        "academics.Designation",
        to_field="code",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisor_profiles",
        db_column="designation_ref",
    )
    program_ref = models.ForeignKey(
        "training.TrainingProgram",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisor_profiles",
    )
    specialty_ref = models.ForeignKey(
        "academics.Specialty",
        to_field="code",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisor_profiles",
        db_column="specialty_ref",
    )
    profile_status = models.CharField(
        max_length=20,
        choices=[("INCOMPLETE", "Incomplete"), ("COMPLETE", "Complete")],
        default="INCOMPLETE",
    )
    profile_schema_version = models.PositiveIntegerField(default=1)
    completed_schema_version = models.PositiveIntegerField(default=0)
    profile_completed_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    is_archived = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Supervisor Profile"
        verbose_name_plural = "Supervisor Profiles"

    def __str__(self):
        return f"SupervisorProfile<{self.user_id}>"

    def clean(self):
        super().clean()
        if self.user_id and self.user.role != "SUPERVISOR":
            raise ValidationError({"user": "Supervisor profile requires SUPERVISOR role."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class SupportStaffProfile(models.Model):
    """Profile metadata for support staff."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="support_staff_profile",
    )
    designation = models.CharField(max_length=100, blank=True, null=True)
    department_ref = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="support_staff_profiles",
    )
    hospital = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="support_staff_profiles",
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    scope_notes = models.TextField(blank=True)
    profile_status = models.CharField(
        max_length=20,
        choices=[("INCOMPLETE", "Incomplete"), ("COMPLETE", "Complete")],
        default="INCOMPLETE",
    )
    profile_schema_version = models.PositiveIntegerField(default=1)
    completed_schema_version = models.PositiveIntegerField(default=0)
    profile_completed_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    is_archived = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Support Staff Profile"
        verbose_name_plural = "Support Staff Profiles"

    def __str__(self):
        return f"SupportStaffProfile<{self.user_id}>"

    def clean(self):
        super().clean()
        if self.user_id and self.user.role != "SUPPORT_STAFF":
            raise ValidationError({"user": "Support staff profile requires SUPPORT_STAFF role."})

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
        verbose_name = "User Department Membership"
        verbose_name_plural = "User Department Memberships"
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
            self.MEMBER_FACULTY: {"SUPERVISOR"},
            self.MEMBER_SUPERVISOR: {"SUPERVISOR"},
            self.MEMBER_RESIDENT: {"RESIDENT"},
        }
        if self.user_id and self.user.role not in role_map.get(self.member_type, set()):
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
        verbose_name = "User Hospital-Department Assignment"
        verbose_name_plural = "User Hospital-Department Assignments"
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


class DataCorrectionAudit(models.Model):
    """Field-level audit trail for manual and bulk correction actions."""

    actor = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="data_corrections_made",
    )
    entity_type = models.CharField(max_length=50)
    entity_id = models.CharField(max_length=64)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["entity_type", "entity_id", "created_at"],
                name="users_datac_entity__308bcb_idx",
            ),
            models.Index(fields=["actor", "created_at"], name="users_datac_actor_i_b92e94_idx"),
            models.Index(fields=["field_name", "created_at"], name="users_datac_field_n_611183_idx"),
        ]

    def __str__(self):
        return f"{self.entity_type}:{self.entity_id}:{self.field_name}"


class SafeForeignKeyDescriptor:
    def __init__(self, original_descriptor, target_model):
        self.orig = original_descriptor
        self.target_model = target_model

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.orig.__get__(instance, owner)

    def __set__(self, instance, value):
        if isinstance(value, str):
            if not value.strip():
                value = None
            else:
                obj, _ = self.target_model.objects.get_or_create(
                    code=value,
                    defaults={"name": value, "active": True}
                )
                value = obj
        elif isinstance(value, int):
            try:
                value = self.target_model.objects.get(id=value)
            except self.target_model.DoesNotExist:
                value = None
        self.orig.__set__(instance, value)


# Wrap descriptors to allow string assignments cleanly
from sims.academics.models import Designation, Specialty, AcademicSession

ResidentProfile.academic_session_ref = SafeForeignKeyDescriptor(
    ResidentProfile.academic_session_ref, AcademicSession
)
ResidentProfile.specialty_ref = SafeForeignKeyDescriptor(
    ResidentProfile.specialty_ref, Specialty
)
SupervisorProfile.designation_ref = SafeForeignKeyDescriptor(
    SupervisorProfile.designation_ref, Designation
)
SupervisorProfile.specialty_ref = SafeForeignKeyDescriptor(
    SupervisorProfile.specialty_ref, Specialty
)

