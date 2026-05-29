from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "head", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]

