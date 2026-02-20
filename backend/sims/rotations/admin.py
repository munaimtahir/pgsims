from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Department, Hospital, Rotation, RotationEvaluation


class RotationResource(resources.ModelResource):
    """Resource for bulk import/export of rotations via CSV/Excel"""

    class Meta:
        model = Rotation
        fields = (
            "id",
            "pg__username",
            "department__name",
            "hospital__name",
            "start_date",
            "end_date",
            "supervisor__username",
            "status",
            "objectives",
            "created_at",
        )
        export_order = fields
        import_id_fields = ("id",)

    def before_import_row(self, row, **kwargs):
        """Custom logic before importing each row"""
        # Convert usernames to user objects
        pg_username = row.get("pg__username")
        supervisor_username = row.get("supervisor__username")

        if pg_username:
            try:
                from sims.users.models import User

                pg = User.objects.get(username=pg_username, role="pg")
                row["pg"] = pg.id
            except User.DoesNotExist:
                row["pg"] = None

        if supervisor_username:
            try:
                from sims.users.models import User

                supervisor = User.objects.get(username=supervisor_username, role="supervisor")
                row["supervisor"] = supervisor.id
            except User.DoesNotExist:
                row["supervisor"] = None

        # Convert department and hospital names to IDs
        dept_name = row.get("department__name")
        hospital_name = row.get("hospital__name")

        if dept_name:
            dept, created = Department.objects.get_or_create(name=dept_name)
            row["department"] = dept.id

        if hospital_name:
            hospital, created = Hospital.objects.get_or_create(name=hospital_name)
            row["hospital"] = hospital.id

        return row


class RotationEvaluationInline(admin.TabularInline):
    """Inline admin for rotation evaluations"""

    model = RotationEvaluation
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("evaluator", "evaluation_type", "score", "comments", "status")

    def get_queryset(self, request):
        """Filter evaluations based on user role"""
        qs = super().get_queryset(request)
        if request.user.role == "supervisor":
            # Supervisors only see evaluations for their PGs
            return qs.filter(rotation__pg__supervisor=request.user)
        return qs


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    """Admin interface for hospitals"""

    list_display = ("name", "address", "phone", "email", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "address", "phone", "email")
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "code", "is_active")}),
        (
            "Contact Information",
            {"fields": ("address", "phone", "email", "website"), "classes": ("collapse",)},
        ),
        (
            "Additional Information",
            {"fields": ("description", "facilities"), "classes": ("collapse",)},
        ),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for departments"""

    list_display = ("name", "hospital", "head_of_department", "is_active", "rotation_count")
    list_filter = ("hospital", "is_active", "created_at")
    search_fields = ("name", "hospital__name", "head_of_department")
    ordering = ("hospital", "name")

    fieldsets = (
        (None, {"fields": ("name", "hospital", "is_active")}),
        (
            "Department Details",
            {
                "fields": ("head_of_department", "contact_email", "contact_phone"),
                "classes": ("collapse",),
            },
        ),
        (
            "Training Information",
            {
                "fields": ("description", "training_objectives", "required_skills"),
                "classes": ("collapse",),
            },
        ),
    )

    def rotation_count(self, obj):
        """Display count of rotations in this department"""
        count = obj.rotations.count()
        if count > 0:
            url = reverse("admin:rotations_rotation_changelist")
            return format_html(
                '<a href="{}?department__id__exact={}">{} rotations</a>', url, obj.id, count
            )
        return "0 rotations"

    rotation_count.short_description = "Rotations"


@admin.register(Rotation)
class RotationAdmin(ImportExportModelAdmin):
    """Enhanced rotation admin with role-based access and bulk operations"""

    resource_class = RotationResource
    list_display = (
        "get_pg_name",
        "department",
        "hospital",
        "start_date",
        "end_date",
        "duration_display",
        "status_badge",
        "supervisor",
        "evaluation_count",
        "created_at",
    )
    list_filter = (
        "status",
        "department",
        "hospital",
        "start_date",
        "end_date",
        "created_at",
        "supervisor",
    )
    search_fields = (
        "pg__username",
        "pg__first_name",
        "pg__last_name",
        "department__name",
        "hospital__name",
        "supervisor__username",
    )
    date_hierarchy = "start_date"
    ordering = ("-start_date", "pg__last_name")

    fieldsets = (
        ("Basic Information", {"fields": ("pg", "department", "hospital", "supervisor")}),
        (
            "Rotation Period",
            {
                "fields": ("start_date", "end_date", "status"),
                "description": "Define the rotation schedule and current status",
            },
        ),
        (
            "Training Details",
            {
                "fields": ("objectives", "learning_outcomes", "requirements"),
                "classes": ("collapse",),
            },
        ),
        (
            "Completion & Feedback",
            {"fields": ("completion_certificate", "feedback", "notes"), "classes": ("collapse",)},
        ),
        (
            "Audit Information",
            {
                "fields": ("created_by", "approved_by", "approved_at"),
                "classes": ("collapse",),
                "description": "System tracking information",
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "created_by", "approved_by", "approved_at")
    inlines = [RotationEvaluationInline]

    # Custom actions
    actions = ["approve_rotations", "reject_rotations", "mark_completed", "export_rotation_reports"]

    def get_queryset(self, request):
        """Filter rotations based on user role"""
        qs = (
            super()
            .get_queryset(request)
            .select_related("pg", "department", "hospital", "supervisor", "created_by")
            .prefetch_related("evaluations")
        )

        if request.user.is_superuser or request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors see rotations for their assigned PGs
            return qs.filter(Q(supervisor=request.user) | Q(pg__supervisor=request.user))
        elif request.user.role == "pg":
            # PGs see only their own rotations
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

    def duration_display(self, obj):
        """Display rotation duration in a readable format"""
        if obj.start_date and obj.end_date:
            duration = obj.get_duration_months()
            if duration:
                return f"{duration:.1f} months"
        return "Not set"

    duration_display.short_description = "Duration"

    def status_badge(self, obj):
        """Display status with colored badge"""
        status_colors = {
            "planned": "#6c757d",  # Gray
            "ongoing": "#007bff",  # Blue
            "completed": "#28a745",  # Green
            "cancelled": "#dc3545",  # Red
            "pending": "#ffc107",  # Yellow
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

    def evaluation_count(self, obj):
        """Display count of evaluations with link"""
        count = obj.evaluations.count()
        if count > 0:
            url = reverse("admin:rotations_rotationevaluation_changelist")
            return format_html(
                '<a href="{}?rotation__id__exact={}" title="View Evaluations">{} evaluations</a>',
                url,
                obj.id,
                count,
            )
        return "No evaluations"

    evaluation_count.short_description = "Evaluations"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key choices based on user role and context"""
        if db_field.name == "pg":
            from sims.users.models import User

            if request.user.role == "supervisor":
                # Supervisors can only assign rotations to their PGs
                kwargs["queryset"] = User.objects.filter(
                    role="pg", supervisor=request.user, is_active=True
                )
            else:
                kwargs["queryset"] = User.objects.filter(role="pg", is_active=True)

        elif db_field.name == "supervisor":
            from sims.users.models import User

            kwargs["queryset"] = User.objects.filter(role="supervisor", is_active=True)

        elif db_field.name == "department":
            kwargs["queryset"] = Department.objects.filter(is_active=True)

        elif db_field.name == "hospital":
            kwargs["queryset"] = Hospital.objects.filter(is_active=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Custom save logic with audit trail"""
        if not change:  # New rotation
            obj.created_by = request.user

        # Auto-approve if user has permission
        if obj.status == "pending" and (request.user.is_superuser or request.user.role == "admin"):
            obj.status = "approved"
            obj.approved_by = request.user
            obj.approved_at = timezone.now()

        super().save_model(request, obj, form, change)

        # Send notification to PG and supervisor
        if not change:
            self.send_rotation_notification(obj, "created")

    def send_rotation_notification(self, rotation, action):
        """Send notification about rotation changes"""
        try:
            from sims.notifications.models import Notification
        except (ImportError, ModuleNotFoundError):
            Notification = None

        if Notification:
            # Notify PG
            if rotation.pg:
                Notification.objects.create(
                    user=rotation.pg,
                    title=f"Rotation {action.title()}",
                    message=f"Your rotation in {rotation.department} has been {action}.",
                    type="rotation",
                    related_object_id=rotation.id,
                )

            # Notify supervisor
            if rotation.supervisor and rotation.supervisor != rotation.pg:
                Notification.objects.create(
                    user=rotation.supervisor,
                    title="New Rotation Assignment",
                    message=f"You have been assigned to supervise {rotation.pg.get_full_name()} "
                    f"in {rotation.department}.",
                    type="rotation",
                    related_object_id=rotation.id,
                )

    # Custom Actions
    def approve_rotations(self, request, queryset):
        """Bulk approve selected rotations"""
        if not (request.user.is_superuser or request.user.role == "admin"):
            messages.error(request, "You don't have permission to approve rotations.")
            return

        count = 0
        for rotation in queryset.filter(status="pending"):
            rotation.status = "approved"
            rotation.approved_by = request.user
            rotation.approved_at = timezone.now()
            rotation.save()
            count += 1

        messages.success(request, f"Successfully approved {count} rotations.")

    approve_rotations.short_description = "Approve selected rotations"

    def reject_rotations(self, request, queryset):
        """Bulk reject selected rotations"""
        if not (request.user.is_superuser or request.user.role == "admin"):
            messages.error(request, "You don't have permission to reject rotations.")
            return

        count = queryset.filter(status="pending").update(status="cancelled")
        messages.success(request, f"Successfully rejected {count} rotations.")

    reject_rotations.short_description = "Reject selected rotations"

    def mark_completed(self, request, queryset):
        """Mark selected rotations as completed"""
        count = 0
        for rotation in queryset.filter(status="ongoing"):
            if rotation.end_date and rotation.end_date <= timezone.now().date():
                rotation.status = "completed"
                rotation.save()
                count += 1

        messages.success(request, f"Successfully marked {count} rotations as completed.")

    mark_completed.short_description = "Mark as completed (if end date passed)"

    def export_rotation_reports(self, request, queryset):
        """Export detailed rotation reports"""
        # This would generate a detailed report with evaluations
        # For now, redirect to a custom export view
        selected = queryset.values_list("id", flat=True)
        ids = ",".join(str(id) for id in selected)
        return HttpResponseRedirect(f"/rotations/export/?ids={ids}")

    export_rotation_reports.short_description = "Export detailed reports"


@admin.register(RotationEvaluation)
class RotationEvaluationAdmin(admin.ModelAdmin):
    """Admin interface for rotation evaluations"""

    list_display = (
        "rotation_display",
        "evaluator",
        "evaluation_type",
        "score_display",
        "status",
        "created_at",
    )
    list_filter = (
        "evaluation_type",
        "status",
        "score",
        "created_at",
        "rotation__department",
        "rotation__hospital",
    )
    search_fields = (
        "rotation__pg__username",
        "rotation__pg__first_name",
        "rotation__pg__last_name",
        "evaluator__username",
        "comments",
    )
    ordering = ("-created_at",)

    fieldsets = (
        ("Evaluation Details", {"fields": ("rotation", "evaluator", "evaluation_type")}),
        ("Assessment", {"fields": ("score", "status", "comments", "recommendations")}),
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
        """Filter evaluations based on user role"""
        qs = (
            super()
            .get_queryset(request)
            .select_related(
                "rotation__pg", "rotation__department", "rotation__hospital", "evaluator"
            )
        )

        if request.user.is_superuser or request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors see evaluations for their PGs or evaluations they created
            return qs.filter(
                Q(rotation__supervisor=request.user)
                | Q(rotation__pg__supervisor=request.user)
                | Q(evaluator=request.user)
            )
        elif request.user.role == "pg":
            # PGs see only their own evaluations
            return qs.filter(rotation__pg=request.user)

        return qs.none()

    def rotation_display(self, obj):
        """Display rotation details with link"""
        if obj.rotation:
            url = reverse("admin:rotations_rotation_change", args=[obj.rotation.id])
            return format_html(
                '<a href="{}" title="View Rotation">{} - {}</a>',
                url,
                obj.rotation.pg.get_full_name() if obj.rotation.pg else "No PG",
                obj.rotation.department.name if obj.rotation.department else "No Dept",
            )
        return "No Rotation"

    rotation_display.short_description = "Rotation"
    rotation_display.admin_order_field = "rotation__pg__last_name"

    def score_display(self, obj):
        """Display score with color coding"""
        if obj.score is not None:
            if obj.score >= 80:
                color = "#28a745"  # Green
            elif obj.score >= 60:
                color = "#ffc107"  # Yellow
            else:
                color = "#dc3545"  # Red

            return format_html(
                '<span style="color: {}; font-weight: bold;">{}/100</span>', color, obj.score
            )
        return "Not scored"

    score_display.short_description = "Score"
    score_display.admin_order_field = "score"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key choices"""
        if db_field.name == "rotation":
            if request.user.role == "supervisor":
                kwargs["queryset"] = Rotation.objects.filter(
                    Q(supervisor=request.user) | Q(pg__supervisor=request.user)
                )
            elif request.user.role == "pg":
                kwargs["queryset"] = Rotation.objects.filter(pg=request.user)
        elif db_field.name == "evaluator":
            from sims.users.models import User

            kwargs["queryset"] = User.objects.filter(
                role__in=["supervisor", "admin"], is_active=True
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Add custom CSS for better admin interface
class RotationAdminConfig:
    """Custom admin configuration for rotations"""

    class Media:
        css = {"all": ("admin/css/rotation_admin.css",)}
        js = ("admin/js/rotation_admin.js",)


# Apply custom styling
for admin_class in [RotationAdmin, RotationEvaluationAdmin, DepartmentAdmin, HospitalAdmin]:
    admin_class.Media = RotationAdminConfig.Media
