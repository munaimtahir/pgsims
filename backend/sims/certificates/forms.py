import os
from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Certificate, CertificateReview, CertificateType

User = get_user_model()


class CertificateCreateForm(forms.ModelForm):
    """
    Form for creating new certificates with role-based field filtering.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    class Meta:
        model = Certificate
        fields = [
            "pg",
            "certificate_type",
            "title",
            "certificate_number",
            "issuing_organization",
            "issue_date",
            "expiry_date",
            "description",
            "skills_acquired",
            "cme_points_earned",
            "cpd_credits_earned",
            "certificate_file",
            "additional_documents",
            "verification_url",
            "verification_code",
        ]
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "expiry_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Describe the certificate content, training received, and key learning outcomes...",
                }
            ),
            "skills_acquired": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "List specific skills and competencies acquired...",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the full certificate title...",
                }
            ),
            "certificate_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Official certificate number or ID (if available)",
                }
            ),
            "issuing_organization": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name of the issuing organization"}
            ),
            "verification_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "URL for online certificate verification (optional)",
                }
            ),
            "verification_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Verification code (if applicable)"}
            ),
            "cme_points_earned": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 1000}
            ),
            "cpd_credits_earned": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 1000}
            ),
            "pg": forms.Select(attrs={"class": "form-control"}),
            "certificate_type": forms.Select(attrs={"class": "form-control"}),
            "certificate_file": forms.FileInput(
                attrs={"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png"}
            ),
            "additional_documents": forms.FileInput(
                attrs={"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png,.doc,.docx"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter querysets based on user role
        if self.user:
            self._setup_field_querysets()
            self._setup_field_requirements()

        # Set default dates
        self._set_default_dates()

        # Add help text
        self._setup_help_text()

    def _setup_field_querysets(self):
        """Setup field querysets based on user role"""
        if self.user.role == "admin":
            # Admins see all active PGs
            self.fields["pg"].queryset = User.objects.filter(role="pg", is_active=True).order_by(
                "last_name", "first_name"
            )

        elif self.user.role == "supervisor":
            # Supervisors see only their assigned PGs
            self.fields["pg"].queryset = User.objects.filter(
                role="pg", supervisor=self.user, is_active=True
            ).order_by("last_name", "first_name")

        elif self.user.role == "pg":
            # PGs see only themselves
            self.fields["pg"].queryset = User.objects.filter(id=self.user.id)
            self.fields["pg"].initial = self.user
            self.fields["pg"].widget.attrs["readonly"] = True

        # Filter certificate types to active only
        self.fields["certificate_type"].queryset = CertificateType.objects.filter(
            is_active=True
        ).order_by("category", "name")

    def _setup_field_requirements(self):
        """Setup field requirements and validation"""
        # Required fields
        required_fields = [
            "title",
            "issuing_organization",
            "issue_date",
            "certificate_type",
            "certificate_file",
        ]

        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        # PG field is required for admins and supervisors
        if self.user and self.user.role in ["admin", "supervisor"]:
            self.fields["pg"].required = True

    def _set_default_dates(self):
        """Set sensible default dates"""
        today = timezone.now().date()

        # Default issue date to today
        self.fields["issue_date"].initial = today

        # Don't set default expiry date - let user choose based on certificate type

    def _setup_help_text(self):
        """Setup comprehensive help text for fields"""
        self.fields["title"].help_text = "Full official title of the certificate"
        self.fields["certificate_number"].help_text = (
            "Official certificate number, ID, or reference (if available)"
        )
        self.fields["issuing_organization"].help_text = (
            "Name of the organization that issued this certificate"
        )
        self.fields["issue_date"].help_text = "Date when the certificate was issued"
        self.fields["expiry_date"].help_text = (
            "Expiry date (leave blank if certificate doesn't expire)"
        )
        self.fields["description"].help_text = (
            "Detailed description of the training, course content, and learning outcomes"
        )
        self.fields["skills_acquired"].help_text = (
            "Specific skills and competencies gained from this certification"
        )
        self.fields["cme_points_earned"].help_text = "CME points earned (if applicable)"
        self.fields["cpd_credits_earned"].help_text = "CPD credits earned (if applicable)"
        self.fields["certificate_file"].help_text = (
            "Upload the certificate document (PDF, JPG, PNG format, max 10MB)"
        )
        self.fields["additional_documents"].help_text = (
            "Supporting documents like transcripts, course materials (optional)"
        )
        self.fields["verification_url"].help_text = (
            "Website URL where this certificate can be verified online"
        )
        self.fields["verification_code"].help_text = "Verification code for online validation"

    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        issue_date = cleaned_data.get("issue_date")
        expiry_date = cleaned_data.get("expiry_date")
        certificate_file = cleaned_data.get("certificate_file")
        certificate_type = cleaned_data.get("certificate_type")

        # Validate dates
        if issue_date and expiry_date:
            if expiry_date <= issue_date:
                raise ValidationError("Expiry date must be after issue date")

        # Validate issue date is not in the future
        if issue_date and issue_date > timezone.now().date():
            raise ValidationError("Issue date cannot be in the future")

        # Validate file size and type
        if certificate_file:
            # Check file size (10MB limit)
            if certificate_file.size > 10 * 1024 * 1024:
                raise ValidationError("Certificate file size cannot exceed 10MB")

            # Check file type
            allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
            file_extension = os.path.splitext(certificate_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f"File type {file_extension} not allowed. "
                    f"Please use: {', '.join(allowed_extensions)}"
                )

        # Auto-set expiry date based on certificate type if not provided
        if certificate_type and not expiry_date and certificate_type.validity_period_months:
            calculated_expiry = issue_date + timedelta(
                days=certificate_type.validity_period_months * 30
            )
            cleaned_data["expiry_date"] = calculated_expiry

        # Auto-set CME/CPD points from certificate type if not provided
        if certificate_type:
            if not cleaned_data.get("cme_points_earned"):
                cleaned_data["cme_points_earned"] = certificate_type.cme_points
            if not cleaned_data.get("cpd_credits_earned"):
                cleaned_data["cpd_credits_earned"] = certificate_type.cpd_credits

        return cleaned_data

    def clean_certificate_file(self):
        """Additional validation for certificate file"""
        certificate_file = self.cleaned_data.get("certificate_file")

        if certificate_file:
            # Additional security check - scan file content
            file_content = certificate_file.read(1024)  # Read first 1KB
            certificate_file.seek(0)  # Reset file pointer

            # Basic check for malicious content (very basic)
            suspicious_patterns = [b"<script", b"javascript:", b"<?php"]
            for pattern in suspicious_patterns:
                if pattern in file_content.lower():
                    raise ValidationError("Uploaded file contains suspicious content")

        return certificate_file


class CertificateUpdateForm(CertificateCreateForm):
    """
    Form for updating existing certificates with additional restrictions.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict editing based on certificate status
        if self.instance and self.instance.pk:
            self._apply_status_restrictions()

    def _apply_status_restrictions(self):
        """Apply editing restrictions based on certificate status"""
        certificate = self.instance

        # Approved certificates: limited editing
        if certificate.status == "approved":
            readonly_fields = ["pg", "certificate_type", "issue_date", "certificate_file"]
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
                    self.fields[
                        field_name
                    ].help_text += " (Cannot be changed for approved certificate)"

        # Rejected certificates: allow most editing except PG
        elif certificate.status == "rejected":
            if "pg" in self.fields:
                self.fields["pg"].disabled = True
                self.fields["pg"].help_text += " (Cannot be changed for existing certificate)"


class CertificateReviewForm(forms.ModelForm):
    """
    Form for creating and updating certificate reviews.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    class Meta:
        model = CertificateReview
        fields = ["status", "comments", "recommendations", "required_changes", "review_date"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "review_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "comments": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-control",
                    "placeholder": "Provide detailed feedback on the certificate...",
                }
            ),
            "recommendations": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Recommendations for the postgraduate...",
                }
            ),
            "required_changes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Specific changes needed before approval (if applicable)...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.certificate = kwargs.pop("certificate", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user and self.certificate:
            self._setup_field_requirements()

        # Set default review date
        if not self.instance.pk:
            self.fields["review_date"].initial = timezone.now().date()

        # Setup help text
        self._setup_help_text()

    def _setup_field_requirements(self):
        """Setup field requirements and validation"""
        self.fields["status"].required = True
        self.fields["comments"].required = True

        # Filter status choices based on current certificate status
        if self.certificate.status == "pending":
            status_choices = [
                ("pending", "Keep Pending"),
                ("approved", "Approve"),
                ("rejected", "Reject"),
                ("needs_clarification", "Needs Clarification"),
            ]
        elif self.certificate.status == "under_review":
            status_choices = [
                ("approved", "Approve"),
                ("rejected", "Reject"),
                ("needs_clarification", "Still Needs Clarification"),
            ]
        else:
            status_choices = CertificateReview.STATUS_CHOICES

        self.fields["status"].choices = status_choices

    def _setup_help_text(self):
        """Setup help text for fields"""
        self.fields["status"].help_text = "Review decision for this certificate"
        self.fields["comments"].help_text = (
            "Detailed feedback on the certificate quality, authenticity, and relevance"
        )
        self.fields["recommendations"].help_text = (
            "Recommendations for future professional development"
        )
        self.fields["required_changes"].help_text = (
            "If rejecting or requesting clarification, specify what needs to be changed"
        )
        self.fields["review_date"].help_text = "Date when this review was conducted"

    def clean(self):
        """Validate review data"""
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        comments = cleaned_data.get("comments")
        required_changes = cleaned_data.get("required_changes")

        # Require detailed comments for rejection
        if status == "rejected":
            if not comments or len(comments.strip()) < 20:
                raise ValidationError("Detailed comments are required when rejecting a certificate")

            if not required_changes:
                raise ValidationError("Please specify what changes are required for rejection")

        # Require comments for needs clarification
        if status == "needs_clarification":
            if not required_changes:
                raise ValidationError("Please specify what clarification is needed")

        # Ensure substantive comments for approval
        if status == "approved":
            if not comments or len(comments.strip()) < 10:
                raise ValidationError("Please provide comments explaining the approval")

        return cleaned_data


class CertificateSearchForm(forms.Form):
    """
    Form for searching and filtering certificates.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by title, PG name, organization, or certificate number...",
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        choices=[("", "All Statuses")] + Certificate.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    certificate_type = forms.ModelChoiceField(
        required=False,
        queryset=CertificateType.objects.filter(is_active=True),
        empty_label="All Certificate Types",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    verified = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All Certificates"),
            ("verified", "Verified Only"),
            ("unverified", "Unverified Only"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    expiry = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All Certificates"),
            ("expiring", "Expiring Soon"),
            ("expired", "Expired"),
            ("valid", "Currently Valid"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )


class CertificateFilterForm(forms.Form):
    """
    Advanced filtering form for certificate reports and analytics.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    SORT_CHOICES = [
        ("-created_at", "Upload Date (Newest First)"),
        ("created_at", "Upload Date (Oldest First)"),
        ("-issue_date", "Issue Date (Newest First)"),
        ("issue_date", "Issue Date (Oldest First)"),
        ("expiry_date", "Expiry Date (Earliest First)"),
        ("-expiry_date", "Expiry Date (Latest First)"),
        ("pg__last_name", "PG Name (A-Z)"),
        ("-pg__last_name", "PG Name (Z-A)"),
        ("certificate_type__name", "Certificate Type (A-Z)"),
        ("issuing_organization", "Organization (A-Z)"),
        ("status", "Status"),
    ]

    pg = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(role="pg", is_active=True),
        empty_label="All PGs",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    category = forms.ChoiceField(
        required=False,
        choices=[("", "All Categories")] + CertificateType.CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    issuing_organization = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Filter by issuing organization..."}
        ),
    )

    cme_points_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min CME points"}),
    )

    cme_points_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max CME points"}),
    )

    year = forms.ChoiceField(required=False, widget=forms.Select(attrs={"class": "form-control"}))

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial="-created_at",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate year choices
        current_year = timezone.now().year
        year_choices = [("", "All Years")]
        for year in range(current_year - 10, current_year + 1):
            year_choices.append((str(year), str(year)))

        self.fields["year"].choices = year_choices


class BulkCertificateApprovalForm(forms.Form):
    """
    Form for bulk approval/rejection of certificates.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    ACTION_CHOICES = [
        ("approve", "Approve Selected"),
        ("reject", "Reject Selected"),
        ("mark_verified", "Mark as Verified"),
    ]

    certificates = forms.ModelMultipleChoiceField(
        queryset=Certificate.objects.filter(status="pending"),
        widget=forms.CheckboxSelectMultiple,
        help_text="Select certificates to process",
    )

    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect,
        help_text="Action to perform on selected certificates",
    )

    bulk_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Optional comments to apply to all selected certificates...",
            }
        ),
        help_text="Comments will be added to all selected certificates",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter certificates based on user role
        if self.user:
            if self.user.role == "supervisor":
                self.fields["certificates"].queryset = Certificate.objects.filter(
                    pg__supervisor=self.user, status__in=["pending", "under_review"]
                )
            elif self.user.role == "admin":
                self.fields["certificates"].queryset = Certificate.objects.filter(
                    status__in=["pending", "under_review"]
                )

    def clean(self):
        """Validate bulk action data"""
        cleaned_data = super().clean()
        certificates = cleaned_data.get("certificates")
        action = cleaned_data.get("action")

        if not certificates:
            raise ValidationError("Please select at least one certificate")

        if action == "reject" and not cleaned_data.get("bulk_comments"):
            raise ValidationError("Comments are required when rejecting certificates")

        # Check permissions for each certificate
        if self.user and self.user.role == "supervisor":
            for cert in certificates:
                if cert.pg.supervisor != self.user:
                    raise ValidationError(
                        f"You don't have permission to process certificate: {cert.title}"
                    )

        return cleaned_data


class CertificateTypeForm(forms.ModelForm):
    """
    Form for creating and editing certificate types.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    class Meta:
        model = CertificateType
        fields = [
            "name",
            "category",
            "description",
            "is_required",
            "validity_period_months",
            "cme_points",
            "cpd_credits",
            "prerequisites",
            "requirements",
            "verification_guidelines",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "validity_period_months": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 120}
            ),
            "cme_points": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
            "cpd_credits": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 100}),
            "prerequisites": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "requirements": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "verification_guidelines": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "is_required": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup help text
        self.fields["name"].help_text = "Unique name for this certificate type"
        self.fields["category"].help_text = "Category this certificate type belongs to"
        self.fields["description"].help_text = "Detailed description of this certificate type"
        self.fields["is_required"].help_text = "Whether this certificate is required for all PGs"
        self.fields["validity_period_months"].help_text = (
            "How many months this certificate is valid (leave blank if no expiry)"
        )
        self.fields["cme_points"].help_text = "Default CME points for certificates of this type"
        self.fields["cpd_credits"].help_text = "Default CPD credits for certificates of this type"
        self.fields["prerequisites"].help_text = "Prerequisites for obtaining this certificate"
        self.fields["requirements"].help_text = "Specific requirements for this certificate type"
        self.fields["verification_guidelines"].help_text = (
            "Guidelines for verifying certificates of this type"
        )


class QuickCertificateUploadForm(forms.Form):
    """
    Simplified form for quick certificate upload.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    certificate_type = forms.ModelChoiceField(
        queryset=CertificateType.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    issuing_organization = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    certificate_file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png"})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Set defaults
        if not self.initial.get("issue_date"):
            self.fields["issue_date"].initial = timezone.now().date()

    def clean_certificate_file(self):
        """Validate uploaded file"""
        certificate_file = self.cleaned_data.get("certificate_file")

        if certificate_file:
            # Check file size (5MB limit for quick upload)
            if certificate_file.size > 5 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 5MB for quick upload")

            # Check file type
            allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png"]
            file_extension = os.path.splitext(certificate_file.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    f"File type {file_extension} not allowed. Use: {', '.join(allowed_extensions)}"
                )

        return certificate_file


class CertificateComplianceReportForm(forms.Form):
    """
    Form for generating certificate compliance reports.

    Created: 2025-05-29 17:01:14 UTC
    Author: SMIB2012
    """

    REPORT_TYPE_CHOICES = [
        ("individual", "Individual PG Compliance"),
        ("department", "Department Summary"),
        ("overall", "Overall System Compliance"),
        ("expiring", "Expiring Certificates"),
    ]

    report_type = forms.ChoiceField(
        choices=REPORT_TYPE_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    pg_filter = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(role="pg", is_active=True),
        empty_label="All PGs",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    include_expired = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Include expired certificates in the report",
    )

    include_pending = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Include pending certificates in the report",
    )

    export_format = forms.ChoiceField(
        choices=[
            ("html", "View in Browser"),
            ("csv", "Export as CSV"),
            ("pdf", "Export as PDF"),
        ],
        initial="html",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter PG choices based on user role
        if self.user and self.user.role == "supervisor":
            self.fields["pg_filter"].queryset = User.objects.filter(
                role="pg", supervisor=self.user, is_active=True
            )
