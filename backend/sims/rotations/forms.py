from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment, Rotation, RotationEvaluation
from sims.rotations.services import validate_rotation_override_requirements

User = get_user_model()


def _hosted_departments_qs():
    return Department.objects.filter(active=True).order_by("name")


def _hospitals_qs():
    return Hospital.objects.filter(is_active=True).order_by("name")


def _validate_department_hosted(hospital, department):
    if not (hospital and department):
        return
    if not HospitalDepartment.objects.filter(
        hospital=hospital, department=department, is_active=True
    ).exists():
        raise ValidationError("Selected department is not hosted by the selected hospital")


class RotationCreateForm(forms.ModelForm):
    class Meta:
        model = Rotation
        fields = [
            "pg",
            "department",
            "hospital",
            "supervisor",
            "start_date",
            "end_date",
            "objectives",
            "learning_outcomes",
            "requirements",
            "status",
            "override_reason",
            "utrmc_approved_by",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "objectives": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "learning_outcomes": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "requirements": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "override_reason": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = _hosted_departments_qs()
        self.fields["hospital"].queryset = _hospitals_qs()
        self.fields["pg"].queryset = User.objects.filter(role="pg", is_active=True).order_by(
            "last_name", "first_name"
        )
        self.fields["supervisor"].queryset = User.objects.filter(
            role="supervisor", is_active=True
        ).order_by("last_name", "first_name")
        self.fields["utrmc_approved_by"].queryset = User.objects.filter(
            role="utrmc_admin", is_active=True
        ).order_by("last_name", "first_name")

        if self.user and self.user.role == "supervisor":
            self.fields["pg"].queryset = self.fields["pg"].queryset.filter(supervisor=self.user)
            self.fields["supervisor"].initial = self.user
            self.fields["supervisor"].queryset = User.objects.filter(pk=self.user.pk)

        today = timezone.now().date()
        self.fields["start_date"].initial = today
        self.fields["end_date"].initial = today + relativedelta(months=6) - timedelta(days=1)

    def clean(self):
        cleaned = super().clean()
        pg = cleaned.get("pg")
        department = cleaned.get("department")
        hospital = cleaned.get("hospital")
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        supervisor = cleaned.get("supervisor")

        if start_date and end_date and end_date <= start_date:
            raise ValidationError("End date must be after start date")

        _validate_department_hosted(hospital, department)

        if self.user and self.user.role == "supervisor":
            if pg and pg.supervisor_id != self.user.id:
                raise ValidationError("You can only create rotations for PGs assigned to you")
            if supervisor and supervisor != self.user:
                raise ValidationError("Supervisor users can only assign themselves")
            cleaned["supervisor"] = self.user

        approved_role = getattr(cleaned.get("utrmc_approved_by"), "role", None)
        try:
            validate_rotation_override_requirements(
                pg,
                hospital,
                department,
                cleaned.get("override_reason"),
                approved_role,
            )
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc

        return cleaned


class RotationUpdateForm(RotationCreateForm):
    pass


class RotationEvaluationForm(forms.ModelForm):
    class Meta:
        model = RotationEvaluation
        fields = ["evaluation_type", "score", "comments", "recommendations", "status"]


class RotationSearchForm(forms.Form):
    search = forms.CharField(required=False)
    status = forms.ChoiceField(required=False, choices=[("", "All")] + Rotation.STATUS_CHOICES)
    department = forms.ModelChoiceField(required=False, queryset=_hosted_departments_qs())
    hospital = forms.ModelChoiceField(required=False, queryset=_hospitals_qs())
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))


class RotationFilterForm(forms.Form):
    SORT_CHOICES = [
        ("-start_date", "Start Date (Newest First)"),
        ("start_date", "Start Date (Oldest First)"),
        ("pg__last_name", "PG Name (A-Z)"),
        ("department__name", "Department (A-Z)"),
        ("status", "Status"),
    ]

    pg = forms.ModelChoiceField(required=False, queryset=User.objects.filter(role="pg", is_active=True))
    supervisor = forms.ModelChoiceField(
        required=False, queryset=User.objects.filter(role="supervisor", is_active=True)
    )
    year = forms.ChoiceField(required=False)
    sort_by = forms.ChoiceField(required=False, choices=SORT_CHOICES, initial="-start_date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = timezone.now().year
        self.fields["year"].choices = [("", "All Years")] + [
            (str(y), str(y)) for y in range(current_year - 5, current_year + 2)
        ]


class BulkRotationAssignmentForm(forms.Form):
    pgs = forms.ModelMultipleChoiceField(queryset=User.objects.filter(role="pg", is_active=True))
    department = forms.ModelChoiceField(queryset=_hosted_departments_qs())
    hospital = forms.ModelChoiceField(queryset=_hospitals_qs())
    supervisor = forms.ModelChoiceField(queryset=User.objects.filter(role="supervisor", is_active=True))
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    objectives = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    override_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))
    utrmc_approved_by = forms.ModelChoiceField(
        required=False, queryset=User.objects.filter(role="utrmc_admin", is_active=True)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.role == "supervisor":
            self.fields["pgs"].queryset = self.fields["pgs"].queryset.filter(supervisor=self.user)
            self.fields["supervisor"].initial = self.user
            self.fields["supervisor"].queryset = User.objects.filter(pk=self.user.pk)

    def clean(self):
        cleaned = super().clean()
        _validate_department_hosted(cleaned.get("hospital"), cleaned.get("department"))
        approved_role = getattr(cleaned.get("utrmc_approved_by"), "role", None)
        for pg in cleaned.get("pgs") or []:
            try:
                validate_rotation_override_requirements(
                    pg,
                    cleaned.get("hospital"),
                    cleaned.get("department"),
                    cleaned.get("override_reason"),
                    approved_role,
                )
            except ValueError as exc:
                raise ValidationError(str(exc)) from exc
        return cleaned


class QuickRotationForm(forms.Form):
    pg = forms.ModelChoiceField(queryset=User.objects.filter(role="pg", is_active=True))
    hospital = forms.ModelChoiceField(queryset=_hospitals_qs())
    department = forms.ModelChoiceField(queryset=_hosted_departments_qs())
    duration_months = forms.ChoiceField(choices=[(3, "3 months"), (6, "6 months"), (12, "12 months")], initial=6)
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    override_reason = forms.CharField(required=False)
    utrmc_approved_by = forms.ModelChoiceField(
        required=False, queryset=User.objects.filter(role="utrmc_admin", is_active=True)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.role == "supervisor":
            self.fields["pg"].queryset = self.fields["pg"].queryset.filter(supervisor=self.user)

    def clean(self):
        cleaned = super().clean()
        _validate_department_hosted(cleaned.get("hospital"), cleaned.get("department"))
        approved_role = getattr(cleaned.get("utrmc_approved_by"), "role", None)
        try:
            validate_rotation_override_requirements(
                cleaned.get("pg"),
                cleaned.get("hospital"),
                cleaned.get("department"),
                cleaned.get("override_reason"),
                approved_role,
            )
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        return cleaned
