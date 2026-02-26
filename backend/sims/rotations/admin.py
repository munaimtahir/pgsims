from django.contrib import admin
from django.core.exceptions import ValidationError

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment, Rotation, RotationEvaluation
from sims.rotations.services import validate_rotation_override_requirements


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")
    list_filter = ("is_active",)


@admin.register(HospitalDepartment)
class HospitalDepartmentAdmin(admin.ModelAdmin):
    list_display = ("hospital", "department", "is_active")
    list_filter = ("hospital", "department", "is_active")
    search_fields = ("hospital__name", "department__name", "department__code")


@admin.register(Rotation)
class RotationAdmin(admin.ModelAdmin):
    list_display = ("pg", "department", "hospital", "start_date", "end_date", "status")
    list_filter = ("status", "hospital", "department")
    search_fields = (
        "pg__username",
        "pg__first_name",
        "pg__last_name",
        "department__name",
        "department__code",
        "hospital__name",
    )
    autocomplete_fields = ("pg", "supervisor", "department", "hospital")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            kwargs["queryset"] = Department.objects.filter(active=True).order_by("name")
        if db_field.name == "hospital":
            kwargs["queryset"] = Hospital.objects.filter(is_active=True).order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        approved_role = getattr(getattr(obj, "utrmc_approved_by", None), "role", None)
        try:
            validate_rotation_override_requirements(
                obj.pg,
                obj.hospital,
                obj.department,
                obj.override_reason,
                approved_role,
            )
        except ValueError as exc:
            raise ValidationError(str(exc))
        super().save_model(request, obj, form, change)


@admin.register(RotationEvaluation)
class RotationEvaluationAdmin(admin.ModelAdmin):
    list_display = ("rotation", "evaluator", "evaluation_type", "score", "status", "created_at")
    list_filter = ("evaluation_type", "status")
    search_fields = ("rotation__pg__username", "evaluator__username", "comments")
