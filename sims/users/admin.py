from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import User


class UserResource(resources.ModelResource):
    """Resource for bulk import/export of users via CSV/Excel"""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "specialty",
            "year",
            "supervisor__username",
            "is_active",
            "date_joined",
        )
        export_order = fields
        import_id_fields = ("username",)

    def before_import_row(self, row, **kwargs):
        """Custom logic before importing each row"""
        # Convert supervisor username to supervisor object if provided
        supervisor_username = row.get("supervisor__username")
        if supervisor_username:
            try:
                supervisor = User.objects.get(username=supervisor_username, role="supervisor")
                row["supervisor"] = supervisor.id
            except User.DoesNotExist:
                row["supervisor"] = None
        return row


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for admin"""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "specialty",
            "year",
            "supervisor",
        )


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form for admin"""

    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    """Enhanced user admin with bulk import/export and role-based management"""

    resource_class = UserResource
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "specialty",
        "year",
        "supervisor",
        "is_active",
        "date_joined",
    )
    list_filter = ("role", "specialty", "year", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("SIMS Role & Assignment"),
            {
                "fields": ("role", "specialty", "year", "supervisor"),
                "description": "Role-based access control for SIMS system",
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined"), "classes": ("collapse",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
        (
            _("SIMS Role & Assignment"),
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "role", "specialty", "year", "supervisor"),
            },
        ),
    )

    def get_queryset(self, request):
        """Filter queryset based on user role"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.role == "admin":
            return qs
        elif request.user.role == "supervisor":
            # Supervisors can only view their assigned PGs
            return qs.filter(supervisor=request.user)
        else:
            # PGs can only view their own profile
            return qs.filter(id=request.user.id)

    def get_form(self, request, obj=None, **kwargs):
        """Customize form based on user permissions"""
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            # Non-superusers cannot modify superuser status
            if "is_superuser" in form.base_fields:
                form.base_fields["is_superuser"].disabled = True

            # Only admins can assign admin role
            if request.user.role != "admin" and "role" in form.base_fields:
                choices = [
                    choice for choice in form.base_fields["role"].choices if choice[0] != "admin"
                ]
                form.base_fields["role"].choices = choices

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter supervisor choices to only show supervisors"""
        if db_field.name == "supervisor":
            kwargs["queryset"] = User.objects.filter(role="supervisor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        """Control who can add users"""
        return request.user.is_superuser or request.user.role == "admin"

    def has_change_permission(self, request, obj=None):
        """Control who can change users"""
        if request.user.is_superuser or request.user.role == "admin":
            return True
        if request.user.role == "supervisor" and obj:
            return obj.supervisor == request.user
        if obj:
            return obj == request.user
        return False

    def has_delete_permission(self, request, obj=None):
        """Control who can delete users"""
        return request.user.is_superuser or request.user.role == "admin"

    def save_model(self, request, obj, form, change):
        """Custom save logic"""
        if not change:  # New user
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


# Customize admin site headers
admin.site.site_header = "SIMS - Postgraduate Medical Training System"
admin.site.site_title = "SIMS Admin"
admin.site.index_title = "Welcome to SIMS Administration"
