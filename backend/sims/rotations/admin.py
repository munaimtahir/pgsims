from django.contrib import admin
from sims.rotations.models import Hospital, HospitalDepartment


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
