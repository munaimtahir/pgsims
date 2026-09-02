import os
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

User = get_user_model()


def certificate_upload_path(instance, filename):
    """Generate upload path for certificate files"""
    # Upload to certificates/pg_username/year/filename
    year = timezone.now().year
    return f"certificates/{instance.pg.username}/{year}/{filename}"


def additional_documents_upload_path(instance, filename):
    """Generate upload path for additional certificate documents"""
    year = timezone.now().year
    return f"certificates/{instance.pg.username}/{year}/additional/{filename}"


class CertificateType(models.Model):
    """
    Model representing different types of certificates.

    Created: 2025-05-29 16:56:20 UTC
    Author: SMIB2012
    """

    CATEGORY_CHOICES = [
        ("academic", "Academic Qualification"),
        ("professional", "Professional Certification"),
        ("cme", "Continuing Medical Education"),
        ("cpd", "Continuing Professional Development"),
        ("specialty", "Specialty Training"),
        ("safety", "Safety & Compliance"),
        ("skills", "Skills & Competency"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200, unique=True, help_text="Name of the certificate type")

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
        help_text="Category this certificate type belongs to",
    )

    description = models.TextField(
        blank=True, help_text="Detailed description of this certificate type"
    )

    is_required = models.BooleanField(
        default=False, help_text="Whether this certificate is required for all PGs"
    )

    validity_period_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="How many months this certificate is valid for (leave blank if no expiry)",
    )

    cme_points = models.PositiveIntegerField(
        default=0, help_text="CME points typically awarded for this certificate type"
    )

    cpd_credits = models.PositiveIntegerField(
        default=0, help_text="CPD credits typically awarded for this certificate type"
    )

    prerequisites = models.TextField(
        blank=True,
        help_text="Prerequisites or requirements for obtaining this certificate",
    )

    requirements = models.TextField(
        blank=True, help_text="Specific requirements for this certificate type"
    )

    verification_guidelines = models.TextField(
        blank=True, help_text="Guidelines for verifying certificates of this type"
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether this certificate type is currently active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Certificate Type"
        verbose_name_plural = "Certificate Types"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["is_required"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def get_active_certificates_count(self):
        """Get count of active certificates of this type"""
        return self.certificates.filter(status="approved").count()

    def get_pending_certificates_count(self):
        """Get count of pending certificates of this type"""
        return self.certificates.filter(status="pending").count()


class Certificate(models.Model):
    """
    Model representing a certificate earned by a postgraduate.

    Created: 2025-05-29 16:56:20 UTC
    Author: SMIB2012
    """

    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("expired", "Expired"),
        ("under_review", "Under Review"),
    ]

    # Core certificate information
    pg = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certificates",
        limit_choices_to={"role": "pg"},
        help_text="Postgraduate who earned this certificate",
    )

    certificate_type = models.ForeignKey(
        CertificateType,
        on_delete=models.CASCADE,
        related_name="certificates",
        help_text="Type of certificate",
    )

    title = models.CharField(max_length=300, help_text="Full title of the certificate")

    certificate_number = models.CharField(
        max_length=100, blank=True, help_text="Official certificate number or ID"
    )

    # Issuing information
    issuing_organization = models.CharField(
        max_length=300, help_text="Organization that issued the certificate"
    )

    issue_date = models.DateField(help_text="Date when the certificate was issued")

    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the certificate expires (if applicable)",
    )

    # Content and details
    description = models.TextField(
        blank=True, help_text="Description of the certificate content and training"
    )

    skills_acquired = models.TextField(
        blank=True,
        help_text="Skills and competencies acquired through this certificate",
    )

    cme_points_earned = models.PositiveIntegerField(
        default=0, help_text="CME points earned for this certificate"
    )

    cpd_credits_earned = models.PositiveIntegerField(
        default=0, help_text="CPD credits earned for this certificate"
    )

    # Documentation
    certificate_file = models.FileField(
        upload_to=certificate_upload_path,
        help_text="Upload the certificate document (PDF, JPG, PNG)",
    )

    additional_documents = models.FileField(
        upload_to=additional_documents_upload_path,
        blank=True,
        null=True,
        help_text="Additional supporting documents",
    )

    # Verification
    verification_url = models.URLField(
        blank=True, help_text="URL for online verification of this certificate"
    )

    verification_code = models.CharField(
        max_length=100, blank=True, help_text="Verification code for this certificate"
    )

    is_verified = models.BooleanField(
        default=False, help_text="Whether this certificate has been verified"
    )

    # Status and approval
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Current status of the certificate",
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
        related_name="certificates_created",
        help_text="User who uploaded this certificate",
    )

    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="certificates_verified",
        help_text="User who verified this certificate",
    )

    verified_at = models.DateTimeField(
        null=True, blank=True, help_text="Date and time when certificate was verified"
    )

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        ordering = ["-created_at", "pg__last_name"]
        indexes = [
            models.Index(fields=["pg", "status"]),
            models.Index(fields=["certificate_type", "status"]),
            models.Index(fields=["issue_date"]),
            models.Index(fields=["expiry_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_verified"]),
            models.Index(fields=["issuing_organization"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(expiry_date__isnull=True)
                | models.Q(expiry_date__gt=models.F("issue_date")),
                name="certificate_expiry_after_issue",
            ),
        ]

    def __str__(self):
        pg_name = self.pg.get_full_name() if self.pg else "No PG"
        return f"{self.title} - {pg_name}"

    def clean(self):
        """Validate certificate data"""
        errors = {}

        # Validate dates
        if self.issue_date and self.expiry_date:
            if self.expiry_date <= self.issue_date:
                errors["expiry_date"] = "Expiry date must be after issue date"

        # Validate issue date is not in the future
        if self.issue_date and self.issue_date > timezone.now().date():
            errors["issue_date"] = "Issue date cannot be in the future"

        # Validate file type
        if self.certificate_file:
            allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
            file_extension = os.path.splitext(self.certificate_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                errors["certificate_file"] = (
                    f"File type {file_extension} not allowed. Use: {', '.join(allowed_extensions)}"
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Override save to handle automatic status updates"""
        # Auto-expire certificates
        if (
            self.expiry_date
            and self.expiry_date <= timezone.now().date()
            and self.status == "approved"
        ):
            self.status = "expired"

        # Set automatic expiry date based on certificate type
        if (
            not self.expiry_date
            and self.certificate_type
            and self.certificate_type.validity_period_months
        ):
            self.expiry_date = self.issue_date + timedelta(
                days=self.certificate_type.validity_period_months * 30
            )

        # Set default CME/CPD points from certificate type
        if not self.cme_points_earned and self.certificate_type:
            self.cme_points_earned = self.certificate_type.cme_points

        if not self.cpd_credits_earned and self.certificate_type:
            self.cpd_credits_earned = self.certificate_type.cpd_credits

        super().save(*args, **kwargs)

    def is_expired(self):
        """Check if certificate is expired"""
        if not self.expiry_date:
            return False
        return self.expiry_date <= timezone.now().date()

    def is_expiring_soon(self, days=30):
        """Check if certificate is expiring within specified days"""
        if not self.expiry_date:
            return False
        warning_date = timezone.now().date() + timedelta(days=days)
        return self.expiry_date <= warning_date

    def get_days_until_expiry(self):
        """Get number of days until expiry"""
        if not self.expiry_date:
            return None

        today = timezone.now().date()
        if self.expiry_date <= today:
            return 0

        return (self.expiry_date - today).days

    def get_validity_status(self):
        """Get validity status as string"""
        if not self.expiry_date:
            return "No Expiry"

        days_left = self.get_days_until_expiry()

        if days_left == 0:
            return "Expired"
        elif days_left <= 30:
            return f"Expires in {days_left} days"
        else:
            return "Valid"

    def get_status_color(self):
        """Get color code for status display"""
        status_colors = {
            "pending": "#ffc107",  # Yellow
            "approved": "#28a745",  # Green
            "rejected": "#dc3545",  # Red
            "expired": "#6c757d",  # Gray
            "under_review": "#007bff",  # Blue
        }
        return status_colors.get(self.status, "#6c757d")

    def can_be_edited(self):
        """Check if certificate can be edited"""
        return self.status in ["pending", "rejected"]

    def can_be_deleted(self):
        """Check if certificate can be deleted"""
        return self.status in ["pending", "rejected"]

    def get_absolute_url(self):
        """Get URL for certificate detail page"""
        return reverse("certificates:detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        """Get URL for certificate edit page"""
        return reverse("certificates:edit", kwargs={"pk": self.pk})

    def get_file_size_display(self):
        """Get human-readable file size"""
        if not self.certificate_file:
            return "No file"

        size = self.certificate_file.size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_reviews_count(self):
        """Get count of reviews for this certificate"""
        return self.reviews.count()

    def get_latest_review(self):
        """Get the most recent review"""
        return self.reviews.first()


class CertificateReview(models.Model):
    """
    Model for reviewing and providing feedback on certificates.

    Created: 2025-05-29 16:56:20 UTC
    Author: SMIB2012
    """

    STATUS_CHOICES = [
        ("pending", "Pending Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("needs_clarification", "Needs Clarification"),
    ]

    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Certificate being reviewed",
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certificate_reviews_given",
        help_text="Person conducting the review",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Review status",
    )

    comments = models.TextField(blank=True, help_text="Detailed review comments")

    recommendations = models.TextField(
        blank=True, help_text="Recommendations for improvement or next steps"
    )

    required_changes = models.TextField(
        blank=True, help_text="Specific changes required before approval"
    )

    review_date = models.DateField(
        default=timezone.now, help_text="Date when the review was conducted"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certificate Review"
        verbose_name_plural = "Certificate Reviews"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["certificate", "status"]),
            models.Index(fields=["reviewer"]),
            models.Index(fields=["review_date"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Review of {self.certificate.title} by {self.reviewer.get_full_name()}"

    def clean(self):
        """Validate review data"""
        # Guard: only validate if both FKs are set (avoids RelatedObjectDoesNotExist before save)
        if not (self.reviewer_id and self.certificate_id):
            return

        # Ensure reviewer has permission to review this certificate
        if self.reviewer and self.certificate:
            if (
                self.reviewer.role == "supervisor"
                and self.reviewer != self.certificate.pg.supervisor
            ):
                raise ValidationError(
                    "Supervisor can only review certificates of their assigned PGs"
                )

            if self.reviewer.role == "pg":
                raise ValidationError("PGs cannot review certificates")

    def save(self, *args, **kwargs):
        """Override save to update certificate status"""
        super().save(*args, **kwargs)

        # Update certificate status based on review
        if self.status == "approved":
            self.certificate.status = "approved"
            self.certificate.verified_by = self.reviewer
            self.certificate.verified_at = timezone.now()
            self.certificate.save()
        elif self.status == "rejected":
            self.certificate.status = "rejected"
            self.certificate.save()
        elif self.status == "needs_clarification":
            self.certificate.status = "under_review"
            self.certificate.save()

    def get_status_color(self):
        """Get color code for status display"""
        status_colors = {
            "pending": "#ffc107",  # Yellow
            "approved": "#28a745",  # Green
            "rejected": "#dc3545",  # Red
            "needs_clarification": "#007bff",  # Blue
        }
        return status_colors.get(self.status, "#6c757d")

    def is_final(self):
        """Check if this is a final review (approved/rejected)"""
        return self.status in ["approved", "rejected"]

    def get_absolute_url(self):
        """Get URL for review detail page"""
        return reverse("certificates:review_detail", kwargs={"pk": self.pk})


# Signal handlers would be defined in signals.py
# These handle automatic notifications, status updates, etc.


class CertificateStatistics(models.Model):
    """
    Model for storing certificate statistics and analytics.
    This could be used for dashboard metrics and reporting.

    Created: 2025-05-29 16:56:20 UTC
    Author: SMIB2012
    """

    pg = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="certificate_stats",
        limit_choices_to={"role": "pg"},
    )

    total_certificates = models.PositiveIntegerField(default=0)
    approved_certificates = models.PositiveIntegerField(default=0)
    pending_certificates = models.PositiveIntegerField(default=0)
    expired_certificates = models.PositiveIntegerField(default=0)

    total_cme_points = models.PositiveIntegerField(default=0)
    total_cpd_credits = models.PositiveIntegerField(default=0)

    last_certificate_date = models.DateField(null=True, blank=True)
    compliance_rate = models.FloatField(default=0.0)  # Percentage

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certificate Statistics"
        verbose_name_plural = "Certificate Statistics"

    def __str__(self):
        return f"Certificate Stats for {self.pg.get_full_name()}"

    def update_statistics(self):
        """Update statistics based on current certificates"""
        certificates = self.pg.certificates.all()

        self.total_certificates = certificates.count()
        self.approved_certificates = certificates.filter(status="approved").count()
        self.pending_certificates = certificates.filter(status="pending").count()
        self.expired_certificates = certificates.filter(status="expired").count()

        # Calculate CME points and CPD credits
        approved_certs = certificates.filter(status="approved")
        self.total_cme_points = sum(cert.cme_points_earned for cert in approved_certs)
        self.total_cpd_credits = sum(cert.cpd_credits_earned for cert in approved_certs)

        # Get last certificate date
        latest_cert = certificates.filter(status="approved").order_by("-issue_date").first()
        self.last_certificate_date = latest_cert.issue_date if latest_cert else None

        # Calculate compliance rate
        required_types = CertificateType.objects.filter(is_required=True).count()
        if required_types > 0:
            pg_required_certs = (
                certificates.filter(certificate_type__is_required=True, status="approved")
                .values("certificate_type")
                .distinct()
                .count()
            )
            self.compliance_rate = (pg_required_certs / required_types) * 100
        else:
            self.compliance_rate = 100.0

        self.save()

    @classmethod
    def update_all_statistics(cls):
        """Update statistics for all PGs"""
        from sims.users.models import User

        for pg in User.objects.filter(role="pg", is_active=True):
            stats, created = cls.objects.get_or_create(pg=pg)
            stats.update_statistics()
