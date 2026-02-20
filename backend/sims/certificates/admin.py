from django.contrib import admin, messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Certificate, CertificateReview, CertificateType


class CertificateResource(resources.ModelResource):
    """Resource for bulk import/export of certificates via CSV/Excel"""

    class Meta:
        model = Certificate
        fields = (
            "id",
            "pg__username",
            "certificate_type__name",
            "title",
            "issuing_organization",
            "issue_date",
            "expiry_date",
            "status",
            "created_at",
        )
        export_order = fields
        import_id_fields = ("id",)

    def before_import_row(self, row, **kwargs):
        """Custom logic before importing each row"""
        # Convert usernames to user objects
        pg_username = row.get("pg__username")
        if pg_username:
            try:
                from sims.users.models import User

                pg = User.objects.get(username=pg_username, role="pg")
                row["pg"] = pg.id
            except User.DoesNotExist:
                row["pg"] = None

        # Convert certificate type names to IDs
        cert_type_name = row.get("certificate_type__name")
        if cert_type_name:
            cert_type, created = CertificateType.objects.get_or_create(name=cert_type_name)
            row["certificate_type"] = cert_type.id

        return row


class CertificateReviewInline(admin.TabularInline):
    """Inline admin for certificate reviews"""

    model = CertificateReview
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("reviewer", "status", "comments", "review_date")

    def get_queryset(self, request):
        """Filter reviews based on user role"""
        qs = super().get_queryset(request)
        if request.user.role == "supervisor":
            # Supervisors only see reviews for their PGs
            return qs.filter(certificate__pg__supervisor=request.user)
        return qs


@admin.register(CertificateType)
class CertificateTypeAdmin(admin.ModelAdmin):
    """Admin interface for certificate types"""

    list_display = (
        "name",
        "category",
        "is_required",
        "validity_period_months",
        "certificate_count",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "is_required", "is_active", "created_at")
    search_fields = ("name", "description", "category")
    ordering = ("category", "name")

    fieldsets = (
        (None, {"fields": ("name", "category", "is_active")}),
        (
            "Requirements",
            {
                "fields": ("is_required", "validity_period_months", "prerequisites"),
                "classes": ("collapse",),
            },
        ),
        (
            "Details",
            {
                "fields": ("description", "requirements", "verification_guidelines"),
                "classes": ("collapse",),
            },
        ),
        ("Points & Credits", {"fields": ("cme_points", "cpd_credits"), "classes": ("collapse",)}),
    )

    def certificate_count(self, obj):
        """Display count of certificates of this type"""
        count = obj.certificates.count()
        if count > 0:
            url = reverse("admin:certificates_certificate_changelist")
            return format_html(
                '<a href="{}?certificate_type__id__exact={}">{} certificates</a>',
                url,
                obj.id,
                count,
            )
        return "0 certificates"

    certificate_count.short_description = "Certificates"


@admin.register(Certificate)
class CertificateAdmin(ImportExportModelAdmin):
    """Enhanced certificate admin with role-based access and bulk operations"""

    resource_class = CertificateResource
    list_display = (
        "title",
        "get_pg_name",
        "certificate_type",
        "issuing_organization",
        "issue_date",
        "expiry_date",
        "status_badge",
        "review_status",
        "created_at",
    )
    list_filter = (
        "status",
        "certificate_type",
        "issue_date",
        "expiry_date",
        "created_at",
        "issuing_organization",
    )
    search_fields = (
        "title",
        "pg__username",
        "pg__first_name",
        "pg__last_name",
        "issuing_organization",
        "certificate_number",
    )
    date_hierarchy = "issue_date"
    ordering = ("-created_at", "pg__last_name")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("pg", "certificate_type", "title", "certificate_number")},
        ),
        (
            "Issuing Details",
            {
                "fields": ("issuing_organization", "issue_date", "expiry_date", "status"),
                "description": "Information about who issued the certificate and when",
            },
        ),
        (
            "Certificate Content",
            {
                "fields": ("description", "skills_acquired", "cme_points_earned"),
                "classes": ("collapse",),
            },
        ),
        (
            "Documentation",
            {"fields": ("certificate_file", "additional_documents"), "classes": ("collapse",)},
        ),
        (
            "Verification",
            {
                "fields": ("verification_url", "verification_code", "is_verified"),
                "classes": ("collapse",),
            },
        ),
        (
            "Audit Information",
            {
                "fields": ("created_by", "verified_by", "verified_at"),
                "classes": ("collapse",),
                "description": "System tracking information",
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "created_by", "verified_by", "verified_at")
    inlines = [CertificateReviewInline]

    # Custom actions
    actions = ["approve_certificates", "reject_certificates", "mark_verified", "mark_expired"]

    def get_queryset(self, request):
        """Filter certificates based on user role"""
        qs = (
            super()
            .get_queryset(request)
            .select_related("pg", "certificate_type", "created_by")
            .prefetch_related("reviews")
        )

        if request.user.is_superuser or request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors see certificates for their assigned PGs
            return qs.filter(pg__supervisor=request.user)
        elif request.user.role == "pg":
            # PGs see only their own certificates
            return qs.filter(pg=request.user)

        return qs.none()

    def get_pg_name(self, obj):
        """Display PG name with link to profile"""
        if obj.pg:
            url = reverse("admin:users_user_change", args=[obj.pg.id])
            return format_html(
                '<a href="{}" title="View PG Profile">{}</a>',
                url,
                obj.pg.get_full_name() or obj.pg.username,
            )
        return "No PG Assigned"

    get_pg_name.short_description = "Postgraduate"
    get_pg_name.admin_order_field = "pg__last_name"

    def status_badge(self, obj):
        """Display status with colored badge"""
        status_colors = {
            "pending": "#ffc107",  # Yellow
            "approved": "#28a745",  # Green
            "rejected": "#dc3545",  # Red
            "expired": "#6c757d",  # Gray
            "under_review": "#007bff",  # Blue
        }
        color = status_colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"

    def review_status(self, obj):
        """Display review status"""
        reviews = obj.reviews.all()
        if not reviews.exists():
            return "No reviews"

        latest_review = reviews.first()
        return format_html(
            '<span title="Latest review by {}">{}</span>',
            latest_review.reviewer.get_full_name() if latest_review.reviewer else "Unknown",
            latest_review.get_status_display(),
        )

    review_status.short_description = "Review Status"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key choices based on user role and context"""
        if db_field.name == "pg":
            from sims.users.models import User

            if request.user.role == "supervisor":
                # Supervisors can only manage certificates for their PGs
                kwargs["queryset"] = User.objects.filter(
                    role="pg", supervisor=request.user, is_active=True
                )
            else:
                kwargs["queryset"] = User.objects.filter(role="pg", is_active=True)

        elif db_field.name == "certificate_type":
            kwargs["queryset"] = CertificateType.objects.filter(is_active=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Custom save logic with audit trail"""
        if not change:  # New certificate
            obj.created_by = request.user

        # Auto-verify if user has permission
        if obj.status == "pending" and (request.user.is_superuser or request.user.role == "admin"):
            obj.status = "approved"
            obj.verified_by = request.user
            obj.verified_at = timezone.now()

        super().save_model(request, obj, form, change)

        # Send notification to PG and supervisor
        if not change:
            self.send_certificate_notification(obj, "uploaded")
        elif obj.status in ["approved", "rejected"]:
            self.send_certificate_notification(obj, obj.status)

    def send_certificate_notification(self, certificate, action):
        """Send notification about certificate changes"""
        try:
            from sims.notifications.models import Notification
        except ImportError:
            Notification = None

        if Notification is not None:
            # Notify PG
            if certificate.pg:
                if action == "uploaded":
                    title = "Certificate Uploaded"
                    message = f"Your certificate '{certificate.title}' has been uploaded and is pending review."
                elif action == "approved":
                    title = "Certificate Approved"
                    message = f"Your certificate '{certificate.title}' has been approved."
                elif action == "rejected":
                    title = "Certificate Rejected"
                    message = f"Your certificate '{certificate.title}' requires revision."

                Notification.objects.create(
                    user=certificate.pg,
                    title=title,
                    message=message,
                    type="certificate",
                    related_object_id=certificate.id,
                )

            # Notify supervisor for uploaded certificates
            if action == "uploaded" and certificate.pg and certificate.pg.supervisor:
                Notification.objects.create(
                    user=certificate.pg.supervisor,
                    title="New Certificate for Review",
                    message=f"{certificate.pg.get_full_name()} has uploaded a new certificate: {certificate.title}",
                    type="certificate",
                    related_object_id=certificate.id,
                )

    # Custom Actions
    def approve_certificates(self, request, queryset):
        """Bulk approve selected certificates"""
        if not (request.user.is_superuser or request.user.role in ["admin", "supervisor"]):
            messages.error(request, "You don't have permission to approve certificates.")
            return

        count = 0
        for certificate in queryset.filter(status="pending"):
            certificate.status = "approved"
            certificate.verified_by = request.user
            certificate.verified_at = timezone.now()
            certificate.save()
            self.send_certificate_notification(certificate, "approved")
            count += 1

        messages.success(request, f"Successfully approved {count} certificates.")

    approve_certificates.short_description = "Approve selected certificates"

    def reject_certificates(self, request, queryset):
        """Bulk reject selected certificates"""
        if not (request.user.is_superuser or request.user.role in ["admin", "supervisor"]):
            messages.error(request, "You don't have permission to reject certificates.")
            return

        count = queryset.filter(status="pending").update(status="rejected")

        # Send notifications
        for certificate in queryset.filter(status="rejected"):
            self.send_certificate_notification(certificate, "rejected")

        messages.success(request, f"Successfully rejected {count} certificates.")

    reject_certificates.short_description = "Reject selected certificates"

    def mark_verified(self, request, queryset):
        """Mark selected certificates as verified"""
        if not (request.user.is_superuser or request.user.role == "admin"):
            messages.error(request, "You don't have permission to verify certificates.")
            return

        count = 0
        for certificate in queryset.exclude(is_verified=True):
            certificate.is_verified = True
            certificate.verified_by = request.user
            certificate.verified_at = timezone.now()
            certificate.save()
            count += 1

        messages.success(request, f"Successfully verified {count} certificates.")

    mark_verified.short_description = "Mark as verified"

    def mark_expired(self, request, queryset):
        """Mark certificates as expired"""
        count = queryset.filter(
            expiry_date__lt=timezone.now().date(), status__in=["approved", "pending"]
        ).update(status="expired")

        messages.success(request, f"Successfully marked {count} certificates as expired.")

    mark_expired.short_description = "Mark expired certificates"

    def get_readonly_fields(self, request, obj=None):
        """Set readonly fields based on user role"""
        readonly_fields = list(self.readonly_fields)

        if request.user.role == "supervisor":
            # Supervisors can't edit certain fields
            readonly_fields.extend(["pg", "certificate_type"])
        elif request.user.role == "pg":
            # PGs have very limited editing
            readonly_fields.extend(["status", "is_verified", "verified_by", "verified_at"])

        return readonly_fields


@admin.register(CertificateReview)
class CertificateReviewAdmin(admin.ModelAdmin):
    """Admin interface for certificate reviews"""

    list_display = ("certificate_display", "reviewer", "status", "review_date", "created_at")
    list_filter = ("status", "review_date", "created_at", "certificate__certificate_type")
    search_fields = (
        "certificate__title",
        "certificate__pg__username",
        "certificate__pg__first_name",
        "certificate__pg__last_name",
        "reviewer__username",
        "comments",
    )
    ordering = ("-created_at",)

    fieldsets = (
        ("Review Details", {"fields": ("certificate", "reviewer", "status", "review_date")}),
        ("Feedback", {"fields": ("comments", "recommendations", "required_changes")}),
        (
            "Audit Information",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        """Filter reviews based on user role"""
        qs = (
            super()
            .get_queryset(request)
            .select_related("certificate__pg", "certificate__certificate_type", "reviewer")
        )

        if request.user.is_superuser or request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors see reviews for their PGs or reviews they created
            return qs.filter(Q(certificate__pg__supervisor=request.user) | Q(reviewer=request.user))
        elif request.user.role == "pg":
            # PGs see only reviews of their own certificates
            return qs.filter(certificate__pg=request.user)

        return qs.none()

    def certificate_display(self, obj):
        """Display certificate details with link"""
        if obj.certificate:
            url = reverse("admin:certificates_certificate_change", args=[obj.certificate.id])
            return format_html(
                '<a href="{}" title="View Certificate">{}</a>', url, obj.certificate.title
            )
        return "No Certificate"

    certificate_display.short_description = "Certificate"
    certificate_display.admin_order_field = "certificate__title"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key choices"""
        if db_field.name == "certificate":
            if request.user.role == "supervisor":
                kwargs["queryset"] = Certificate.objects.filter(pg__supervisor=request.user)
            elif request.user.role == "pg":
                kwargs["queryset"] = Certificate.objects.filter(pg=request.user)

        elif db_field.name == "reviewer":
            from sims.users.models import User

            kwargs["queryset"] = User.objects.filter(
                role__in=["supervisor", "admin"], is_active=True
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Set reviewer to current user if not set"""
        if not obj.reviewer:
            obj.reviewer = request.user

        super().save_model(request, obj, form, change)

        # Update certificate status based on review
        if obj.status == "approved" and obj.certificate.status == "pending":
            obj.certificate.status = "approved"
            obj.certificate.verified_by = request.user
            obj.certificate.verified_at = timezone.now()
            obj.certificate.save()
        elif obj.status == "rejected":
            obj.certificate.status = "rejected"
            obj.certificate.save()


# Custom admin actions for certificate management
def check_expiring_certificates(modeladmin, request, queryset):
    """Check for certificates expiring soon"""
    from datetime import timedelta

    expiring_soon = Certificate.objects.filter(
        expiry_date__lte=timezone.now().date() + timedelta(days=30),
        expiry_date__gt=timezone.now().date(),
        status="approved",
    ).count()

    messages.info(request, f"Found {expiring_soon} certificates expiring within 30 days")


check_expiring_certificates.short_description = "Check expiring certificates"

# Add the action to Certificate admin
CertificateAdmin.actions.append(check_expiring_certificates)


# Add custom CSS for better admin interface
class CertificateAdminConfig:
    """Custom admin configuration for certificates"""

    class Media:
        css = {"all": ("admin/css/certificate_admin.css",)}
        js = ("admin/js/certificate_admin.js",)


# Apply custom styling
for admin_class in [CertificateAdmin, CertificateReviewAdmin, CertificateTypeAdmin]:
    admin_class.Media = CertificateAdminConfig.Media


# Additional reporting functionality for Certificate admin
class CertificateReportAdmin:
    """Additional admin for certificate reporting"""

    def has_module_permission(self, request):
        """Only show this admin to admins"""
        return request.user.is_superuser or request.user.role == "admin"

    def get_urls(self):
        """Add custom URLs for reports"""
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "reports/expiring/",
                self.admin_site.admin_view(self.expiring_certificates_report),
                name="certificates_expiring_report",
            ),
            path(
                "reports/compliance/",
                self.admin_site.admin_view(self.compliance_report),
                name="certificates_compliance_report",
            ),
        ]
        return custom_urls + urls

    def expiring_certificates_report(self, request):
        """Generate expiring certificates report"""
        from datetime import timedelta

        from django.template.response import TemplateResponse

        expiring_certificates = Certificate.objects.filter(
            expiry_date__lte=timezone.now().date() + timedelta(days=90),
            expiry_date__gt=timezone.now().date(),
            status="approved",
        ).select_related("pg", "certificate_type")

        context = {
            "title": "Expiring Certificates Report",
            "certificates": expiring_certificates,
            "opts": Certificate._meta,
        }

        return TemplateResponse(request, "admin/certificates/expiring_report.html", context)

    def compliance_report(self, request):
        """Generate compliance report"""
        from django.template.response import TemplateResponse

        # Get required certificate types
        required_types = CertificateType.objects.filter(is_required=True)

        # Get PGs and their certificate compliance
        from sims.users.models import User

        pgs = User.objects.filter(role="pg", is_active=True)

        compliance_data = []
        for pg in pgs:
            pg_certificates = Certificate.objects.filter(pg=pg, status="approved").values_list(
                "certificate_type", flat=True
            )

            missing_required = required_types.exclude(id__in=pg_certificates).values_list(
                "name", flat=True
            )

            compliance_data.append(
                {
                    "pg": pg,
                    "total_certificates": len(pg_certificates),
                    "missing_required": list(missing_required),
                    "compliance_rate": (
                        (
                            (required_types.count() - len(missing_required))
                            / required_types.count()
                            * 100
                        )
                        if required_types.count() > 0
                        else 100
                    ),
                }
            )

        context = {
            "title": "Certificate Compliance Report",
            "compliance_data": compliance_data,
            "required_types": required_types,
            "opts": Certificate._meta,
        }

        return TemplateResponse(request, "admin/certificates/compliance_report.html", context)


# Don't register the report admin as a separate model
# It's just for adding custom views to the main Certificate admin
