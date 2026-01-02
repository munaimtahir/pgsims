from django.contrib import admin, messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Diagnosis,
    LogbookEntry,
    LogbookReview,
    LogbookStatistics,
    LogbookTemplate,
    Procedure,
    Skill,
)


class LogbookEntryResource(resources.ModelResource):
    """Resource for bulk import/export of logbook entries via CSV/Excel"""

    class Meta:
        model = LogbookEntry
        fields = (
            "id",
            "pg__username",
            "date",
            "rotation__department__name",
            "patient_age",
            "patient_gender",
            "primary_diagnosis__name",
            "procedures_performed",
            "skills_demonstrated",
            "learning_points",
            "supervisor__username",
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

        supervisor_username = row.get("supervisor__username")
        if supervisor_username:
            try:
                from sims.users.models import User

                supervisor = User.objects.get(username=supervisor_username, role="supervisor")
                row["supervisor"] = supervisor.id
            except User.DoesNotExist:
                row["supervisor"] = None

        # Convert diagnosis names to IDs
        diagnosis_name = row.get("primary_diagnosis__name")
        if diagnosis_name:
            diagnosis, created = Diagnosis.objects.get_or_create(name=diagnosis_name)
            row["primary_diagnosis"] = diagnosis.id

        return row


class ProcedureInline(admin.TabularInline):
    """Inline admin for procedures in logbook entries"""

    model = LogbookEntry.procedures.through
    extra = 1
    verbose_name = "Procedure"
    verbose_name_plural = "Procedures"


class SkillInline(admin.TabularInline):
    """Inline admin for skills in logbook entries"""

    model = LogbookEntry.skills.through
    extra = 1
    verbose_name = "Skill"
    verbose_name_plural = "Skills"


class LogbookReviewInline(admin.TabularInline):
    """Inline admin for logbook reviews"""

    model = LogbookReview
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("reviewer", "status", "feedback", "review_date")

    def get_queryset(self, request):
        """Filter reviews based on user role"""
        qs = super().get_queryset(request)
        if request.user.role == "supervisor":
            # Supervisors only see reviews for their PGs
            return qs.filter(logbook_entry__pg__supervisor=request.user)
        return qs


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    """Admin interface for procedures"""

    list_display = (
        "name",
        "category",
        "difficulty_level",
        "cme_points",
        "usage_count",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "difficulty_level", "is_active", "created_at")
    search_fields = ("name", "description", "category")
    ordering = ("category", "name")

    fieldsets = (
        (None, {"fields": ("name", "category", "is_active")}),
        (
            "Details",
            {
                "fields": ("description", "difficulty_level", "duration_minutes"),
                "classes": ("collapse",),
            },
        ),
        (
            "Learning & Assessment",
            {
                "fields": ("cme_points", "learning_objectives", "assessment_criteria"),
                "classes": ("collapse",),
            },
        ),
        (
            "Prerequisites",
            {"fields": ("required_skills", "prerequisites"), "classes": ("collapse",)},
        ),
    )

    def usage_count(self, obj):
        """Display count of logbook entries using this procedure"""
        count = obj.logbook_entries.count()
        if count > 0:
            url = reverse("admin:logbook_logbookentry_changelist")
            return format_html(
                '<a href="{}?procedures__id__exact={}">{} entries</a>', url, obj.id, count
            )
        return "0 entries"

    usage_count.short_description = "Usage"


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    """Admin interface for diagnoses"""

    list_display = ("name", "category", "icd_code", "usage_count", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "icd_code", "description", "category")
    ordering = ("category", "name")

    fieldsets = (
        (None, {"fields": ("name", "category", "icd_code", "is_active")}),
        (
            "Details",
            {
                "fields": ("description", "typical_presentation", "common_procedures"),
                "classes": ("collapse",),
            },
        ),
    )

    def usage_count(self, obj):
        """Display count of logbook entries with this diagnosis"""
        count = obj.primary_entries.count() + obj.secondary_entries.count()
        if count > 0:
            return format_html(
                '<span title="Primary: {}, Secondary: {}">{} entries</span>',
                obj.primary_entries.count(),
                obj.secondary_entries.count(),
                count,
            )
        return "0 entries"

    usage_count.short_description = "Usage"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin interface for skills"""

    list_display = ("name", "category", "level", "usage_count", "is_active", "created_at")
    list_filter = ("category", "level", "is_active", "created_at")
    search_fields = ("name", "description", "category")
    ordering = ("category", "level", "name")

    fieldsets = (
        (None, {"fields": ("name", "category", "level", "is_active")}),
        (
            "Details",
            {
                "fields": ("description", "competency_requirements", "assessment_methods"),
                "classes": ("collapse",),
            },
        ),
    )

    def usage_count(self, obj):
        """Display count of logbook entries demonstrating this skill"""
        count = obj.logbook_entries.count()
        if count > 0:
            url = reverse("admin:logbook_logbookentry_changelist")
            return format_html(
                '<a href="{}?skills__id__exact={}">{} entries</a>', url, obj.id, count
            )
        return "0 entries"

    usage_count.short_description = "Usage"


@admin.register(LogbookTemplate)
class LogbookTemplateAdmin(admin.ModelAdmin):
    """Admin interface for logbook templates"""

    list_display = (
        "name",
        "template_type",
        "is_default",
        "usage_count",
        "is_active",
        "created_by",
        "created_at",
    )
    list_filter = ("template_type", "is_default", "is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("template_type", "name")

    fieldsets = (
        (None, {"fields": ("name", "template_type", "is_default", "is_active")}),
        (
            "Template Structure",
            {
                "fields": ("description", "template_structure", "required_fields"),
                "classes": ("collapse",),
            },
        ),
        (
            "Guidelines",
            {"fields": ("completion_guidelines", "example_entries"), "classes": ("collapse",)},
        ),
        ("Audit Information", {"fields": ("created_by",), "classes": ("collapse",)}),
    )

    readonly_fields = ("created_at", "updated_at", "created_by")

    def usage_count(self, obj):
        """Display count of entries using this template"""
        count = obj.logbook_entries.count()
        return f"{count} entries"

    usage_count.short_description = "Usage"


@admin.register(LogbookEntry)
class LogbookEntryAdmin(ImportExportModelAdmin):
    """Enhanced logbook entry admin with role-based access and bulk operations"""

    resource_class = LogbookEntryResource
    list_display = (
        "get_entry_title",
        "get_pg_name",
        "date",
        "get_rotation",
        "primary_diagnosis",
        "procedure_count",
        "status_badge",
        "review_status",
        "created_at",
    )
    list_filter = (
        "status",
        "date",
        "patient_gender",
        "created_at",
        "rotation__department",
        "supervisor",
    )
    search_fields = (
        "pg__username",
        "pg__first_name",
        "pg__last_name",
        "case_title",
        "patient_chief_complaint",
        "learning_points",
        "primary_diagnosis__name",
    )
    date_hierarchy = "date"
    ordering = ("-date", "-created_at")

    fieldsets = (
        (
            "Entry Information",
            {
                "fields": ("pg", "date", "rotation", "supervisor", "case_title"),
                "description": "Basic information about the logbook entry",
            },
        ),
        (
            "Patient Information",
            {
                "fields": (
                    "patient_age",
                    "patient_gender",
                    "patient_chief_complaint",
                    "patient_history_summary",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Clinical Details",
            {
                "fields": (
                    "primary_diagnosis",
                    "secondary_diagnoses",
                    "procedures",
                    "skills",
                    "investigations_ordered",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Learning & Reflection",
            {
                "fields": (
                    "clinical_reasoning",
                    "learning_points",
                    "challenges_faced",
                    "supervisor_feedback",
                    "follow_up_required",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Assessment & Status",
            {
                "fields": (
                    "self_assessment_score",
                    "supervisor_assessment_score",
                    "status",
                    "template",
                ),
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
    filter_horizontal = ("secondary_diagnoses", "procedures", "skills")
    inlines = [LogbookReviewInline]

    # Custom actions
    actions = ["approve_entries", "request_revision", "mark_verified", "bulk_assign_supervisor"]

    def get_queryset(self, request):
        """Filter entries based on user role"""
        qs = (
            super()
            .get_queryset(request)
            .select_related(
                "pg", "rotation__department", "primary_diagnosis", "supervisor", "created_by"
            )
            .prefetch_related("procedures", "skills", "reviews")
        )

        if request.user.is_superuser or request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors see entries for their assigned PGs
            return qs.filter(pg__supervisor=request.user)
        elif request.user.role == "pg":
            # PGs see only their own entries
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

    def get_entry_title(self, obj):
        """Display entry title or summary"""
        title = obj.case_title or f"Entry for {obj.date}"
        if len(title) > 50:
            title = title[:47] + "..."

        url = reverse("admin:logbook_logbookentry_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, title)

    get_entry_title.short_description = "Entry"
    get_entry_title.admin_order_field = "case_title"

    def get_rotation(self, obj):
        """Display rotation information"""
        if obj.rotation:
            return f"{obj.rotation.department.name}"
        return "No Rotation"

    get_rotation.short_description = "Rotation"
    get_rotation.admin_order_field = "rotation__department__name"

    def procedure_count(self, obj):
        """Display count of procedures performed"""
        count = obj.procedures.count()
        if count > 0:
            procedures = ", ".join([p.name for p in obj.procedures.all()[:3]])
            if count > 3:
                procedures += f" (+{count - 3} more)"
            return format_html('<span title="{}">{} procedures</span>', procedures, count)
        return "0 procedures"

    procedure_count.short_description = "Procedures"

    def status_badge(self, obj):
        """Display status with colored badge"""
        status_colors = {
            "draft": "#6c757d",  # Gray
            "submitted": "#ffc107",  # Yellow
            "approved": "#28a745",  # Green
            "needs_revision": "#fd7e14",  # Orange
            "archived": "#6c757d",  # Gray
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
                # Supervisors can only manage entries for their PGs
                kwargs["queryset"] = User.objects.filter(
                    role="pg", supervisor=request.user, is_active=True
                )
            else:
                kwargs["queryset"] = User.objects.filter(role="pg", is_active=True)

        elif db_field.name == "supervisor":
            from sims.users.models import User

            kwargs["queryset"] = User.objects.filter(role="supervisor", is_active=True)

        elif db_field.name == "rotation":
            from sims.rotations.models import Rotation

            if request.user.role == "supervisor":
                kwargs["queryset"] = Rotation.objects.filter(pg__supervisor=request.user)
            else:
                kwargs["queryset"] = Rotation.objects.all()

        elif db_field.name == "primary_diagnosis":
            kwargs["queryset"] = Diagnosis.objects.filter(is_active=True)

        elif db_field.name == "template":
            kwargs["queryset"] = LogbookTemplate.objects.filter(is_active=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """Filter many-to-many choices"""
        if db_field.name == "procedures":
            kwargs["queryset"] = Procedure.objects.filter(is_active=True)
        elif db_field.name == "skills":
            kwargs["queryset"] = Skill.objects.filter(is_active=True)
        elif db_field.name == "secondary_diagnoses":
            kwargs["queryset"] = Diagnosis.objects.filter(is_active=True)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Custom save logic with audit trail"""
        if not change:  # New entry
            obj.created_by = request.user

            # Set PG to current user if they are a PG
            if request.user.role == "pg":
                obj.pg = request.user

        # Auto-approve if user has permission
        if obj.status == "submitted" and (
            request.user.is_superuser or request.user.role == "admin"
        ):
            obj.status = "approved"
            obj.verified_by = request.user
            obj.verified_at = timezone.now()

        super().save_model(request, obj, form, change)

        # Send notification to supervisor for new entries
        if not change and obj.pg and obj.pg.supervisor:
            self.send_entry_notification(obj, "submitted")

    def send_entry_notification(self, entry, action):
        """Send notification about entry changes"""
        try:
            from sims.notifications.models import Notification
        except ImportError:
            # Notifications app not available
            return

        # Notify supervisor for new submissions
        if action == "submitted" and entry.pg and getattr(entry.pg, "supervisor", None):
            Notification.objects.create(
                user=entry.pg.supervisor,
                title="New Logbook Entry for Review",
                message=f"{entry.pg.get_full_name()} has submitted a new logbook entry: {entry.case_title or 'Untitled'}",
                type="logbook",
                related_object_id=entry.id,
            )

        # Notify PG for status changes
        elif action in ["approved", "needs_revision"] and entry.pg:
            if action == "approved":
                title = "Logbook Entry Approved"
                message = (
                    f"Your logbook entry '{entry.case_title or 'Untitled'}' has been approved."
                )
            else:
                title = "Logbook Entry Needs Revision"
                message = (
                    f"Your logbook entry '{entry.case_title or 'Untitled'}' requires revision."
                )

            Notification.objects.create(
                user=entry.pg,
                title=title,
                message=message,
                type="logbook",
                related_object_id=entry.id,
            )

    # Custom Actions
    def approve_entries(self, request, queryset):
        """Bulk approve selected entries"""
        if not (request.user.is_superuser or request.user.role in ["admin", "supervisor"]):
            messages.error(request, "You don't have permission to approve entries.")
            return

        count = 0
        for entry in queryset.filter(status="submitted"):
            # Check permission for supervisors
            if request.user.role == "supervisor" and entry.pg.supervisor != request.user:
                continue

            entry.status = "approved"
            entry.verified_by = request.user
            entry.verified_at = timezone.now()
            entry.save()
            self.send_entry_notification(entry, "approved")
            count += 1

        messages.success(request, f"Successfully approved {count} entries.")

    approve_entries.short_description = "Approve selected entries"

    def request_revision(self, request, queryset):
        """Request revision for selected entries"""
        if not (request.user.is_superuser or request.user.role in ["admin", "supervisor"]):
            messages.error(request, "You don't have permission to request revisions.")
            return

        count = 0
        for entry in queryset.filter(status="submitted"):
            # Check permission for supervisors
            if request.user.role == "supervisor" and entry.pg.supervisor != request.user:
                continue

            entry.status = "needs_revision"
            entry.save()
            self.send_entry_notification(entry, "needs_revision")
            count += 1

        messages.success(request, f"Requested revision for {count} entries.")

    request_revision.short_description = "Request revision for selected entries"

    def mark_verified(self, request, queryset):
        """Mark entries as verified"""
        if not (request.user.is_superuser or request.user.role == "admin"):
            messages.error(request, "You don't have permission to verify entries.")
            return

        count = 0
        for entry in queryset.exclude(verified_by__isnull=False):
            entry.verified_by = request.user
            entry.verified_at = timezone.now()
            entry.save()
            count += 1

        messages.success(request, f"Successfully verified {count} entries.")

    mark_verified.short_description = "Mark as verified"

    def bulk_assign_supervisor(self, request, queryset):
        """Bulk assign supervisor to entries"""
        if not (request.user.is_superuser or request.user.role == "admin"):
            messages.error(request, "You don't have permission to assign supervisors.")
            return

        # This would typically open a form to select supervisor
        # For now, just show count of eligible entries
        count = queryset.filter(supervisor__isnull=True).count()
        messages.info(request, f"Found {count} entries without assigned supervisors.")

    bulk_assign_supervisor.short_description = "Assign supervisor to selected entries"

    def get_readonly_fields(self, request, obj=None):
        """Set readonly fields based on user role"""
        readonly_fields = list(self.readonly_fields)

        if request.user.role == "supervisor":
            # Supervisors can't edit PG or certain core fields
            readonly_fields.extend(["pg", "date"])
        elif request.user.role == "pg":
            # PGs have limited editing after submission
            if obj and obj.status != "draft":
                readonly_fields.extend(["supervisor", "status"])

        return readonly_fields


@admin.register(LogbookReview)
class LogbookReviewAdmin(admin.ModelAdmin):
    """Admin interface for logbook reviews"""

    list_display = ("logbook_entry_display", "reviewer", "status", "review_date", "created_at")
    list_filter = ("status", "review_date", "created_at", "logbook_entry__rotation__department")
    search_fields = (
        "logbook_entry__case_title",
        "logbook_entry__pg__username",
        "logbook_entry__pg__first_name",
        "logbook_entry__pg__last_name",
        "reviewer__username",
        "feedback",
    )
    ordering = ("-created_at",)

    fieldsets = (
        ("Review Details", {"fields": ("logbook_entry", "reviewer", "status", "review_date")}),
        (
            "Feedback",
            {
                "fields": (
                    "feedback",
                    "strengths_identified",
                    "areas_for_improvement",
                    "recommendations",
                    "follow_up_required",
                )
            },
        ),
        (
            "Assessment",
            {
                "fields": (
                    "clinical_knowledge_score",
                    "clinical_skills_score",
                    "professionalism_score",
                    "overall_score",
                ),
                "classes": ("collapse",),
            },
        ),
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
            .select_related("logbook_entry__pg", "logbook_entry__rotation__department", "reviewer")
        )

        if request.user.is_superuser or request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors see reviews for their PGs or reviews they created
            return qs.filter(
                Q(logbook_entry__pg__supervisor=request.user) | Q(reviewer=request.user)
            )
        elif request.user.role == "pg":
            # PGs see only reviews of their own entries
            return qs.filter(logbook_entry__pg=request.user)

        return qs.none()

    def logbook_entry_display(self, obj):
        """Display logbook entry details with link"""
        if obj.logbook_entry:
            url = reverse("admin:logbook_logbookentry_change", args=[obj.logbook_entry.id])
            title = obj.logbook_entry.case_title or f"Entry {obj.logbook_entry.date}"
            return format_html('<a href="{}" title="View Entry">{}</a>', url, title)
        return "No Entry"

    logbook_entry_display.short_description = "Logbook Entry"
    logbook_entry_display.admin_order_field = "logbook_entry__case_title"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key choices"""
        if db_field.name == "logbook_entry":
            if request.user.role == "supervisor":
                kwargs["queryset"] = LogbookEntry.objects.filter(pg__supervisor=request.user)
            elif request.user.role == "pg":
                kwargs["queryset"] = LogbookEntry.objects.filter(pg=request.user)

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

        # Update entry status based on review
        if obj.status == "approved" and obj.logbook_entry.status == "submitted":
            obj.logbook_entry.status = "approved"
            obj.logbook_entry.verified_by = request.user
            obj.logbook_entry.verified_at = timezone.now()
            obj.logbook_entry.save()
        elif obj.status == "needs_revision":
            obj.logbook_entry.status = "needs_revision"
            obj.logbook_entry.save()


# Custom admin views for reporting
@admin.register(LogbookStatistics)
class LogbookStatisticsAdmin(admin.ModelAdmin):
    """Admin interface for logbook statistics"""

    list_display = (
        "pg",
        "total_entries",
        "approved_entries",
        "average_review_score",
        "last_entry_date",
        "completion_rate",
        "updated_at",
    )
    list_filter = ("last_entry_date", "updated_at")
    search_fields = ("pg__username", "pg__first_name", "pg__last_name")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        """Statistics are auto-generated, not manually added"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of statistics"""
        return request.user.is_superuser


# Custom admin actions for logbook management
def check_overdue_entries(modeladmin, request, queryset):
    """Check for overdue logbook entries"""
    from datetime import timedelta

    overdue_threshold = timezone.now().date() - timedelta(days=7)
    overdue_count = LogbookEntry.objects.filter(date__lt=overdue_threshold, status="draft").count()

    messages.info(request, f"Found {overdue_count} draft entries older than 7 days")


check_overdue_entries.short_description = "Check for overdue entries"

# Add the action to LogbookEntry admin
LogbookEntryAdmin.actions.append(check_overdue_entries)


# Add custom CSS and JS for better admin interface
class LogbookAdminConfig:
    """Custom admin configuration for logbook"""

    class Media:
        css = {"all": ("admin/css/logbook_admin.css",)}
        js = ("admin/js/logbook_admin.js",)


# Apply custom styling
for admin_class in [
    LogbookEntryAdmin,
    LogbookReviewAdmin,
    ProcedureAdmin,
    DiagnosisAdmin,
    SkillAdmin,
]:
    admin_class.Media = LogbookAdminConfig.Media


# Register additional admin views for reporting
class LogbookReportAdmin:
    """Additional admin for logbook reporting"""

    def has_module_permission(self, request):
        """Only show this admin to admins and supervisors"""
        return request.user.is_superuser or request.user.role in ["admin", "supervisor"]

    def get_urls(self):
        """Add custom URLs for reports"""
        from django.urls import path

        urls = []
        custom_urls = [
            path("reports/completion/", self.completion_report, name="logbook_completion_report"),
            path("reports/procedures/", self.procedures_report, name="logbook_procedures_report"),
            path(
                "reports/learning-analytics/",
                self.learning_analytics_report,
                name="logbook_learning_analytics",
            ),
        ]
        return custom_urls + urls

    def completion_report(self, request):
        """Generate completion report"""
        from django.template.response import TemplateResponse

        # Get completion statistics
        from sims.users.models import User

        pgs = User.objects.filter(role="pg", is_active=True)

        completion_data = []
        for pg in pgs:
            entries = LogbookEntry.objects.filter(pg=pg)
            completion_data.append(
                {
                    "pg": pg,
                    "total_entries": entries.count(),
                    "approved_entries": entries.filter(status="approved").count(),
                    "pending_entries": entries.filter(status="submitted").count(),
                    "draft_entries": entries.filter(status="draft").count(),
                    "last_entry": entries.order_by("-date").first(),
                }
            )

        context = {
            "title": "Logbook Completion Report",
            "completion_data": completion_data,
            "opts": LogbookEntry._meta,
        }

        return TemplateResponse(request, "admin/logbook/completion_report.html", context)

    def procedures_report(self, request):
        """Generate procedures report"""
        from django.db.models import Count
        from django.template.response import TemplateResponse

        # Get procedure usage statistics
        procedure_stats = Procedure.objects.annotate(usage_count=Count("logbook_entries")).order_by(
            "-usage_count"
        )

        context = {
            "title": "Procedures Report",
            "procedure_stats": procedure_stats,
            "opts": LogbookEntry._meta,
        }

        return TemplateResponse(request, "admin/logbook/procedures_report.html", context)

    def learning_analytics_report(self, request):
        """Generate learning analytics report"""
        from django.db.models import Avg, Count
        from django.template.response import TemplateResponse

        # Get learning analytics
        analytics = {
            "average_scores": LogbookEntry.objects.aggregate(
                avg_self=Avg("self_assessment_score"),
                avg_supervisor=Avg("supervisor_assessment_score"),
            ),
            "entries_by_month": LogbookEntry.objects.extra(
                {"month": "EXTRACT(month FROM date)", "year": "EXTRACT(year FROM date)"}
            )
            .values("year", "month")
            .annotate(count=Count("id"))
            .order_by("year", "month"),
            "top_diagnoses": Diagnosis.objects.annotate(usage=Count("primary_entries")).order_by(
                "-usage"
            )[:10],
        }

        context = {
            "title": "Learning Analytics Report",
            "analytics": analytics,
            "opts": LogbookEntry._meta,
        }

        return TemplateResponse(request, "admin/logbook/learning_analytics_report.html", context)


# Don't register the report admin as a separate model
# It's just for adding custom views to the main admin
