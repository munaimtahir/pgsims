from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
import uuid
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
    ("5", "Year 5"),  # For 5-year specialties
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
    cnic = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text="Computerized National Identity Card number",
    )

    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="Contact phone number"
    )
    force_password_change = models.BooleanField(
        default=False,
        help_text="Force the user to change their password on next login.",
    )
    is_complete_profile = models.BooleanField(
        default=False,
        help_text="Computed data quality flag for resident/admin correction workflows.",
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

    def get_documents_pending_count(self):
        """
        Get count of pending documents requiring action by this user/supervisor.
        """
        try:
            if self.role in {"supervisor", "faculty"}:
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
            
            elif self.role in {"pg", "resident"}:
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

    PROFILE_PENDING = "pending"
    PROFILE_COMPLETE = "complete"
    PROFILE_STATUS_CHOICES = (
        (PROFILE_PENDING, "Pending"),
        (PROFILE_COMPLETE, "Complete"),
    )

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="resident_profile",
        limit_choices_to={"role__in": ["pg", "resident"]},
    )
    import_batch = models.ForeignKey(
        "users.OnboardingImportBatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_profiles",
    )
    pgr_id = models.CharField(max_length=60, blank=True)
    program_name = models.CharField(max_length=200, blank=True)
    training_year = models.CharField(max_length=20, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    raw_import_data = models.JSONField(null=True, blank=True)
    # Legacy residents predate onboarding; only imported/explicitly incomplete profiles opt in.
    profile_completed = models.BooleanField(default=True)
    profile_completed_at = models.DateTimeField(null=True, blank=True)
    first_login_completed_at = models.DateTimeField(null=True, blank=True)
    login_generated = models.BooleanField(default=False)
    login_issued = models.BooleanField(default=False)
    login_issued_at = models.DateTimeField(null=True, blank=True)
    login_issued_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resident_logins_issued",
    )
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


class OnboardingImportBatch(models.Model):
    """Audit record for resident onboarding imports."""

    STATUS_UPLOADED = "uploaded"
    STATUS_MAPPED = "mapped"
    STATUS_READY = "ready"
    STATUS_IMPORTED = "imported"
    STATUS_LOGINS_GENERATED = "logins_generated"
    STATUS_ISSUED = "issued"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = (
        (STATUS_UPLOADED, "Uploaded"),
        (STATUS_MAPPED, "Mapped"),
        (STATUS_READY, "Ready"),
        (STATUS_IMPORTED, "Imported"),
        (STATUS_LOGINS_GENERATED, "Logins Generated"),
        (STATUS_ISSUED, "Issued"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    )

    file_name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="onboarding_batches",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_rows = models.PositiveIntegerField(default=0)
    ready_rows = models.PositiveIntegerField(default=0)
    error_rows = models.PositiveIntegerField(default=0)
    duplicate_rows = models.PositiveIntegerField(default=0)
    imported_rows = models.PositiveIntegerField(default=0)
    logins_generated = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_UPLOADED)
    mapping_json = models.JSONField(default=dict, blank=True)
    headers_json = models.JSONField(default=list, blank=True)
    sample_rows_json = models.JSONField(default=list, blank=True)
    raw_rows_json = models.JSONField(default=list, blank=True)
    preview_rows_json = models.JSONField(default=list, blank=True)
    error_rows_json = models.JSONField(default=list, blank=True)
    imported_resident_ids_json = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"OnboardingImportBatch<{self.id}:{self.file_name}>"


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
    has_default_dates = models.BooleanField(
        default=False,
        help_text="Computed flag set when this link uses default/synthetic dates.",
    )
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


class WorkspaceIdentity(models.Model):
    STATUS_NOT_SENT = "not_sent"
    STATUS_SENT = "sent"
    STATUS_RECEIVED = "received"
    STATUS_NEEDS_REVIEW = "needs_review"
    STATUS_MAPPING_REQUIRED = "mapping_required"
    STATUS_READY_FOR_PROVISIONING = "ready_for_provisioning"
    STATUS_APPROVAL_PENDING = "approval_pending"
    STATUS_PROVISIONING = "provisioning"
    STATUS_WORKSPACE_READY = "workspace_ready"
    STATUS_SKIPPED_EXISTING = "skipped_existing"
    STATUS_DUPLICATE_CONFLICT = "duplicate_conflict"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"
    STATUS_REVOKED = "revoked"

    STATUS_CHOICES = [
        (STATUS_NOT_SENT, "Not Sent"),
        (STATUS_SENT, "Sent"),
        (STATUS_RECEIVED, "Received"),
        (STATUS_NEEDS_REVIEW, "Needs Review"),
        (STATUS_MAPPING_REQUIRED, "Mapping Required"),
        (STATUS_READY_FOR_PROVISIONING, "Ready For Provisioning"),
        (STATUS_APPROVAL_PENDING, "Approval Pending"),
        (STATUS_PROVISIONING, "Provisioning"),
        (STATUS_WORKSPACE_READY, "Workspace Ready"),
        (STATUS_SKIPPED_EXISTING, "Skipped Existing"),
        (STATUS_DUPLICATE_CONFLICT, "Duplicate Conflict"),
        (STATUS_FAILED, "Failed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_REVOKED, "Revoked"),
    ]

    ONBOARDING_STATUS_DRAFT = "DRAFT"
    ONBOARDING_STATUS_VERIFIED = "VERIFIED_BY_DEPARTMENT"
    ONBOARDING_STATUS_APPROVED = "APPROVED_FOR_WORKSPACE_ONBOARDING"

    ONBOARDING_CHOICES = [
        (ONBOARDING_STATUS_DRAFT, "Draft"),
        (ONBOARDING_STATUS_VERIFIED, "Verified by Department"),
        (ONBOARDING_STATUS_APPROVED, "Approved for Workspace Onboarding"),
    ]

    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="workspace_identity")
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # PGSIMS side approval
    onboarding_status = models.CharField(max_length=50, choices=ONBOARDING_CHOICES, default=ONBOARDING_STATUS_DRAFT)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="workspace_approvals")

    # Workspace status returned from AdminOps
    workspace_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_NOT_SENT)
    workspace_primary_email = models.EmailField(blank=True)
    workspace_org_unit_path = models.CharField(max_length=500, blank=True)
    workspace_groups = models.JSONField(default=list, blank=True)

    workspace_last_sync_at = models.DateTimeField(null=True, blank=True)
    workspace_ready_at = models.DateTimeField(null=True, blank=True)
    workspace_failure_reason = models.TextField(blank=True)
    adminops_reference = models.CharField(max_length=200, blank=True)

    last_bridge_attempt_at = models.DateTimeField(null=True, blank=True)
    last_bridge_error = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def get_external_id(self):
        if self.user.is_resident() or self.user.is_pg():
            return f"pgsims-resident-{self.public_id}"
        return f"pgsims-supervisor-{self.public_id}"

    class Meta:
        verbose_name = "Workspace Identity"
        verbose_name_plural = "Workspace Identities"
        indexes = [
            models.Index(fields=["onboarding_status"]),
            models.Index(fields=["workspace_status"]),
        ]

    def __str__(self):
        return f"WorkspaceIdentity<{self.user_id}:{self.onboarding_status}:{self.workspace_status}>"


class WorkspaceBridgeLog(models.Model):
    identity = models.ForeignKey(WorkspaceIdentity, on_delete=models.CASCADE, related_name="bridge_logs")
    person_type = models.CharField(max_length=50)
    external_id = models.CharField(max_length=200)
    request_id = models.CharField(max_length=200)
    endpoint = models.CharField(max_length=500)
    payload_hash = models.CharField(max_length=64, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)
    response_body_sanitized = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey("users.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="bridge_logs_created")

    class Meta:
        verbose_name = "Workspace Bridge Log"
        verbose_name_plural = "Workspace Bridge Logs"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"BridgeLog<{self.external_id}:{self.status}>"
