from django.contrib import admin, messages
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import CaseCategory, CaseReview, CaseStatistics, ClinicalCase


@admin.register(CaseCategory)
class CaseCategoryAdmin(admin.ModelAdmin):
    """Admin interface for case categories"""

    list_display = ("name", "color_preview", "case_count", "is_active", "sort_order", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("sort_order", "name")

    fieldsets = (
        (None, {"fields": ("name", "description", "is_active")}),
        ("Display Settings", {"fields": ("color_code", "sort_order"), "classes": ("collapse",)}),
        ("Audit Information", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ("created_at", "updated_at")

    def color_preview(self, obj):
        """Display color preview with hex code"""
        return format_html(
            '<div style="display: inline-block; width: 20px; height: 20px; '
            "background-color: {}; border: 1px solid #ddd; margin-right: 5px; "
            'vertical-align: middle;"></div>{}',
            obj.color_code,
            obj.color_code,
        )

    color_preview.short_description = "Color"

    def case_count(self, obj):
        """Display count of cases in this category"""
        count = obj.cases.count()
        if count > 0:
            url = reverse("admin:cases_clinicalcase_changelist") + f"?category__id__exact={obj.id}"
            return format_html('<a href="{}">{} cases</a>', url, count)
        return "0 cases"

    case_count.short_description = "Cases"

    def get_queryset(self, request):
        """Optimize queries with annotations"""
        return super().get_queryset(request).annotate(case_count_annotation=Count("cases"))


@admin.register(ClinicalCase)
class ClinicalCaseAdmin(admin.ModelAdmin):
    """Admin interface for clinical cases with role-based access control"""

    list_display = (
        "case_title",
        "pg",
        "category",
        "patient_age",
        "patient_gender",
        "status_indicator",
        "supervisor",
        "date_encountered",
        "status",
    )
    list_filter = ("status", "category", "patient_gender", "date_encountered", "created_at")
    search_fields = (
        "case_title",
        "pg__username",
        "pg__first_name",
        "pg__last_name",
        "primary_diagnosis__name",
    )
    ordering = ("-date_encountered", "-created_at")
    date_hierarchy = "date_encountered"
    # Role-based field restrictions
    fieldsets = (
        (
            "Case Information",
            {"fields": ("case_title", "category", "date_encountered", "rotation")},
        ),
        ("Patient Details", {"fields": ("patient_age", "patient_gender", "chief_complaint")}),
        (
            "Clinical Details",
            {
                "fields": (
                    "primary_diagnosis",
                    "differential_diagnosis",
                    "physical_examination",
                    "management_plan",
                )
            },
        ),
        (
            "Learning & Assessment",
            {"fields": ("learning_objectives", "clinical_reasoning", "learning_points")},
        ),
        ("Documentation", {"fields": ("case_files", "case_images"), "classes": ("collapse",)}),
        (
            "Review Information",
            {"fields": ("supervisor", "status", "supervisor_feedback"), "classes": ("collapse",)},
        ),
        ("Audit Trail", {"fields": ("pg", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ("created_at", "updated_at")

    filter_horizontal = ("secondary_diagnoses", "procedures_performed")

    def get_queryset(self, request):
        """Filter queryset based on user role"""
        qs = (
            super()
            .get_queryset(request)
            .select_related("pg", "supervisor", "category", "primary_diagnosis", "rotation")
            .prefetch_related("secondary_diagnoses", "procedures_performed")
        )

        if hasattr(request.user, "role"):
            if request.user.role == "pg":
                # PGs can only see their own cases
                return qs.filter(pg=request.user)
            elif request.user.role == "supervisor":
                # Supervisors can see cases assigned to them and cases in their rotations
                return qs.filter(Q(supervisor=request.user) | Q(rotation__supervisor=request.user))
        # Admins can see all cases
        return qs

    def get_readonly_fields(self, request, obj=None):
        """Dynamic readonly fields based on user role and case status"""
        readonly = list(self.readonly_fields)

        if hasattr(request.user, "role"):
            if request.user.role == "pg":
                # PGs cannot edit supervisor-only fields
                readonly.extend(["supervisor", "supervisor_feedback", "status"])

                # If case is already reviewed, make it mostly readonly
                if obj and obj.status in ["reviewed", "approved"]:
                    readonly.extend(
                        [
                            "case_title",
                            "date",
                            "patient_initials",
                            "primary_diagnosis",
                            "procedures_performed",
                        ]
                    )

            elif request.user.role == "supervisor":
                # Supervisors cannot edit PG identity but can edit all clinical content
                readonly.extend(["pg"])

        return readonly

    def get_fieldsets(self, request, obj=None):
        """Dynamic fieldsets based on user role"""
        fieldsets = list(self.fieldsets)

        if hasattr(request.user, "role") and request.user.role == "pg":
            # Hide review information from PGs initially
            if not obj or obj.status == "draft":
                fieldsets = [fs for fs in fieldsets if fs[0] != "Review Information"]

        return fieldsets

    def status_indicator(self, obj):
        """Visual status indicator with colors"""
        status_colors = {
            "draft": "#6c757d",  # Gray
            "submitted": "#007bff",  # Blue
            "under_review": "#ffc107",  # Yellow
            "reviewed": "#28a745",  # Green
            "approved": "#20c997",  # Teal
            "needs_revision": "#dc3545",  # Red
        }

        color = status_colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="display: inline-block; width: 12px; height: 12px; '
            'background-color: {}; border-radius: 50%; margin-right: 5px;"></span>{}',
            color,
            obj.get_status_display(),
        )

    status_indicator.short_description = "Status"

    def save_model(self, request, obj, form, change):
        """Auto-assign PG and handle status changes"""
        if not change:  # Creating new case
            if hasattr(request.user, "role") and request.user.role == "pg":
                obj.pg = request.user

        # Auto-update timestamps for status changes
        if change and "status" in form.changed_data:
            if obj.status == "submitted":
                obj.submitted_at = timezone.now()
            elif obj.status in ["reviewed", "approved"]:
                obj.reviewed_at = timezone.now()

        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        """Check if user can edit this specific case"""
        if not super().has_change_permission(request, obj):
            return False

        if obj and hasattr(request.user, "role"):
            if request.user.role == "pg":
                # PGs can only edit their own cases and only if not finalized
                return obj.pg == request.user and obj.status not in ["approved"]
            elif request.user.role == "supervisor":
                # Supervisors can edit cases assigned to them
                return obj.supervisor == request.user or (
                    obj.rotation and obj.rotation.supervisor == request.user
                )

        return True

    def has_delete_permission(self, request, obj=None):
        """Restrict deletion based on case status and user role"""
        if not super().has_delete_permission(request, obj):
            return False

        if obj:
            # Only draft cases can be deleted
            if obj.status != "draft":
                return False

            if hasattr(request.user, "role") and request.user.role == "pg":
                return obj.pg == request.user

        return True


@admin.register(CaseReview)
class CaseReviewAdmin(admin.ModelAdmin):
    """Admin interface for case reviews"""

    list_display = ("case", "reviewer", "review_date", "overall_score", "status")
    list_filter = ("review_date", "overall_score", "status")
    search_fields = ("case__case_title", "reviewer__username", "overall_feedback")
    ordering = ("-review_date",)
    date_hierarchy = "review_date"

    fieldsets = (
        ("Review Information", {"fields": ("case", "reviewer", "review_date", "status")}),
        (
            "Assessment Scores",
            {
                "fields": (
                    "clinical_knowledge_score",
                    "clinical_reasoning_score",
                    "documentation_score",
                    "overall_score",
                )
            },
        ),
        (
            "Feedback",
            {
                "fields": (
                    "overall_feedback",
                    "clinical_reasoning_feedback",
                    "documentation_feedback",
                    "areas_for_improvement",
                )
            },
        ),
        ("Audit", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        """Filter reviews based on user role"""
        qs = super().get_queryset(request).select_related("case", "reviewer", "case__pg")

        if hasattr(request.user, "role"):
            if request.user.role == "pg":
                # PGs can only see reviews of their cases
                return qs.filter(case__pg=request.user)
            elif request.user.role == "supervisor":
                # Supervisors can see reviews they created or of cases they supervise
                return qs.filter(Q(reviewer=request.user) | Q(case__supervisor=request.user))

        return qs

    def recommendation_status(self, obj):
        """Display recommendation with color coding"""
        colors = {
            "approved": "#28a745",
            "revision_needed": "#ffc107",
            "rejected": "#dc3545",
        }
        color = colors.get(obj.recommendation, "#6c757d")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_recommendation_display(),
        )

    recommendation_status.short_description = "Recommendation"

    def save_model(self, request, obj, form, change):
        """Auto-assign reviewer and update case status"""
        if not change:
            obj.reviewer = request.user

        # Update related case status based on review
        if obj.recommendation == "approved":
            obj.case.status = "approved"
            obj.case.save()
        elif obj.recommendation == "revision_needed":
            obj.case.status = "needs_revision"
            obj.case.save()

        super().save_model(request, obj, form, change)


@admin.register(CaseStatistics)
class CaseStatisticsAdmin(admin.ModelAdmin):
    """Admin interface for case statistics - mostly read-only analytics"""

    list_display = (
        "pg",
        "total_cases",
        "approved_cases",
        "completion_rate",
        "average_supervisor_score",
        "last_updated",
    )
    list_filter = ("last_updated",)
    search_fields = ("pg__username", "pg__first_name", "pg__last_name")
    ordering = ("-average_supervisor_score", "-total_cases")

    fieldsets = (
        ("PG Information", {"fields": ("pg",)}),
        (
            "Case Statistics",
            {"fields": ("total_cases", "approved_cases", "pending_cases", "draft_cases")},
        ),
        (
            "Performance Metrics",
            {"fields": ("average_self_score", "average_supervisor_score", "completion_rate")},
        ),
        ("Timestamps", {"fields": ("last_updated",), "classes": ("collapse",)}),
    )

    readonly_fields = ("last_updated",)

    def get_queryset(self, request):
        """Filter statistics based on user role"""
        qs = super().get_queryset(request).select_related("pg")

        if hasattr(request.user, "role"):
            if request.user.role == "pg":
                # PGs can only see their own statistics
                return qs.filter(pg=request.user)
            elif request.user.role == "supervisor":
                # Supervisors can see statistics for PGs they supervise
                supervised_pgs = request.user.assigned_pgs.values_list("id", flat=True)
                return qs.filter(pg__in=supervised_pgs)

        return qs

    def has_add_permission(self, request):
        """Statistics are auto-generated, no manual creation"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Statistics should not be deleted manually"""
        return request.user.is_superuser


# Custom admin actions
def mark_cases_as_reviewed(modeladmin, request, queryset):
    """Bulk action to mark selected cases as reviewed"""
    if not hasattr(request.user, "role") or request.user.role not in ["supervisor", "admin"]:
        messages.error(request, "Only supervisors can mark cases as reviewed.")
        return

    updated = queryset.filter(status__in=["submitted", "under_review"]).update(
        status="reviewed", reviewed_at=timezone.now()
    )

    messages.success(request, f"{updated} cases marked as reviewed.")


mark_cases_as_reviewed.short_description = "Mark selected cases as reviewed"


def generate_case_statistics(modeladmin, request, queryset):
    """Bulk action to regenerate statistics for selected PGs"""

    for case_stat in queryset:
        case_stat.refresh_statistics()
        case_stat.save()

    messages.success(request, f"Statistics regenerated for {queryset.count()} PGs.")


generate_case_statistics.short_description = "Regenerate statistics"


# Register the bulk actions
ClinicalCaseAdmin.actions = [mark_cases_as_reviewed]
CaseStatisticsAdmin.actions = [generate_case_statistics]
