from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import SPECIALTY_CHOICES, USER_ROLES, YEAR_CHOICES, User


class CustomUserCreationForm(UserCreationForm):
    """
    Enhanced user creation form for SIMS with role-based fields.

    Created: 2025-05-29 16:01:19 UTC
    Author: SMIB2012
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email address"}
        ),
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
    )

    role = forms.ChoiceField(
        choices=USER_ROLES,
        widget=forms.Select(attrs={"class": "form-control", "onchange": "toggleRoleFields()"}),
    )

    specialty = forms.ChoiceField(
        choices=[("", "Select Specialty")] + list(SPECIALTY_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    year = forms.ChoiceField(
        choices=[("", "Select Year")] + list(YEAR_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role="supervisor", is_active=True),
        required=False,
        empty_label="Select Supervisor",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    registration_number = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Medical Registration Number"}
        ),
    )

    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "role",
            "specialty",
            "year",
            "supervisor",
            "registration_number",
            "phone_number",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "password1": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Password"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Confirm Password"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        # Filter supervisor choices by specialty if editing PG
        if self.instance and self.instance.pk and self.instance.specialty:
            self.fields["supervisor"].queryset = User.objects.filter(
                role="supervisor", specialty=self.instance.specialty, is_active=True
            )

        # Restrict role choices for non-admin users
        if self.request_user and not self.request_user.is_superuser:
            if self.request_user.role != "admin":
                # Remove admin role from choices
                role_choices = [choice for choice in USER_ROLES if choice[0] != "admin"]
                self.fields["role"].choices = role_choices

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        specialty = cleaned_data.get("specialty")
        year = cleaned_data.get("year")
        supervisor = cleaned_data.get("supervisor")

        # Role-specific validation
        if role == "pg":
            if not specialty:
                raise ValidationError({"specialty": "Specialty is required for PGs"})
            if not year:
                raise ValidationError({"year": "Training year is required for PGs"})
            if not supervisor:
                raise ValidationError({"supervisor": "Supervisor is required for PGs"})

        elif role == "supervisor":
            if not specialty:
                raise ValidationError({"specialty": "Specialty is required for Supervisors"})

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            # Set created_by if request_user available
            if self.request_user:
                user.created_by = self.request_user
                user.save(update_fields=["created_by"])

        return user


class CustomUserChangeForm(UserChangeForm):
    """Enhanced user edit form for SIMS"""

    class Meta:
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
            "registration_number",
            "phone_number",
            "is_active",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
            "specialty": forms.Select(attrs={"class": "form-control"}),
            "year": forms.Select(attrs={"class": "form-control"}),
            "supervisor": forms.Select(attrs={"class": "form-control"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

        # Remove password field from change form
        if "password" in self.fields:
            del self.fields["password"]

        # Filter supervisor choices
        self.fields["supervisor"].queryset = User.objects.filter(role="supervisor", is_active=True)


class ProfileEditForm(forms.ModelForm):
    """Form for users to edit their own profile"""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "registration_number", "phone_number")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
        }


class SupervisorAssignmentForm(forms.Form):
    """Form for bulk supervisor assignment"""

    pgs = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="pg", is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Select PGs",
    )

    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role="supervisor", is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Assign Supervisor",
    )

    def __init__(self, *args, **kwargs):
        specialty = kwargs.pop("specialty", None)
        super().__init__(*args, **kwargs)

        if specialty:
            # Filter by specialty
            self.fields["pgs"].queryset = self.fields["pgs"].queryset.filter(specialty=specialty)
            self.fields["supervisor"].queryset = self.fields["supervisor"].queryset.filter(
                specialty=specialty
            )


class UserSearchForm(forms.Form):
    """Advanced user search form"""

    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by name, username, or email"}
        ),
    )

    role = forms.ChoiceField(
        choices=[("", "All Roles")] + list(USER_ROLES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    specialty = forms.ChoiceField(
        choices=[("", "All Specialties")] + list(SPECIALTY_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    year = forms.ChoiceField(
        choices=[("", "All Years")] + list(YEAR_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role="supervisor", is_active=True),
        required=False,
        empty_label="All Supervisors",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    is_active = forms.ChoiceField(
        choices=[("", "All"), ("true", "Active"), ("false", "Inactive")],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class BulkUserUploadForm(forms.Form):
    """Form for bulk user upload via CSV/Excel"""

    file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".csv,.xlsx,.xls"}),
        help_text="Upload CSV or Excel file with user data",
    )

    update_existing = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Update existing users if username matches",
    )

    send_notifications = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Send email notifications to new users",
    )

    def clean_file(self):
        file = self.cleaned_data["file"]

        # Validate file type
        if not file.name.endswith((".csv", ".xlsx", ".xls")):
            raise ValidationError("File must be CSV or Excel format")

        # Validate file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            raise ValidationError("File size must be less than 5MB")

        return file


class CustomLoginForm(forms.Form):
    """Custom login form with additional features"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Remember me",
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is None:
                raise ValidationError("Invalid username or password")

            if not self.user_cache.is_active:
                raise ValidationError("This account is inactive")

            if self.user_cache.is_archived:
                raise ValidationError("This account has been archived")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class UserFilterForm(forms.Form):
    """Form for filtering user lists with advanced options"""

    SORT_CHOICES = [
        ("last_name", "Last Name"),
        ("first_name", "First Name"),
        ("username", "Username"),
        ("date_joined", "Date Joined"),
        ("last_login", "Last Login"),
        ("role", "Role"),
        ("specialty", "Specialty"),
    ]

    ORDER_CHOICES = [
        ("asc", "Ascending"),
        ("desc", "Descending"),
    ]

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial="last_name",
        widget=forms.Select(attrs={"class": "form-control form-control-sm"}),
    )

    order = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False,
        initial="asc",
        widget=forms.Select(attrs={"class": "form-control form-control-sm"}),
    )

    page_size = forms.ChoiceField(
        choices=[("10", "10"), ("25", "25"), ("50", "50"), ("100", "100")],
        required=False,
        initial="25",
        widget=forms.Select(attrs={"class": "form-control form-control-sm"}),
    )


class UserProfileForm(forms.ModelForm):
    """Form for users to edit their own profile"""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "registration_number"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email Address"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "registration_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Medical Registration Number"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class PGSearchForm(forms.Form):
    """Search form for PG lists"""

    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by name or username..."}
        ),
    )

    specialty = forms.ChoiceField(
        choices=[("", "All Specialties")] + list(SPECIALTY_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    year = forms.ChoiceField(
        choices=[("", "All Years")] + list(YEAR_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
