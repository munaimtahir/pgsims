from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Department, Hospital, Rotation, RotationEvaluation

User = get_user_model()


class RotationCreateForm(forms.ModelForm):
    """
    Form for creating new rotations with role-based field filtering.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

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
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "objectives": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Enter specific learning objectives for this rotation...",
                }
            ),
            "learning_outcomes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Expected learning outcomes and competencies...",
                }
            ),
            "requirements": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Prerequisites and requirements...",
                }
            ),
            "pg": forms.Select(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-control"}),
            "hospital": forms.Select(attrs={"class": "form-control"}),
            "supervisor": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter querysets based on user role
        if self.user:
            self._setup_field_querysets()
            self._setup_field_requirements()

        # Set default dates
        self._set_default_dates()

        # Add CSS classes
        for field_name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"

    def _setup_field_querysets(self):
        """Setup field querysets based on user role"""
        if self.user.role == "admin":
            # Admins see all active users and facilities
            self.fields["pg"].queryset = User.objects.filter(role="pg", is_active=True).order_by(
                "last_name", "first_name"
            )

            self.fields["supervisor"].queryset = User.objects.filter(
                role="supervisor", is_active=True
            ).order_by("last_name", "first_name")

        elif self.user.role == "supervisor":
            # Supervisors see only their assigned PGs
            self.fields["pg"].queryset = User.objects.filter(
                role="pg", supervisor=self.user, is_active=True
            ).order_by("last_name", "first_name")

            # Set supervisor to current user and make it readonly
            self.fields["supervisor"].initial = self.user
            self.fields["supervisor"].queryset = User.objects.filter(id=self.user.id)
            self.fields["supervisor"].widget.attrs["readonly"] = True

        # Filter departments and hospitals to active only
        self.fields["department"].queryset = (
            Department.objects.filter(is_active=True)
            .select_related("hospital")
            .order_by("hospital__name", "name")
        )

        self.fields["hospital"].queryset = Hospital.objects.filter(is_active=True).order_by("name")

        # Limit status choices for non-admins
        if self.user.role != "admin":
            status_choices = [
                ("planned", "Planned"),
                ("pending", "Pending Approval"),
            ]
            self.fields["status"].choices = status_choices

    def _setup_field_requirements(self):
        """Setup field requirements and help text"""
        self.fields["pg"].help_text = "Select the postgraduate for this rotation"
        self.fields["department"].help_text = "Select the department for the rotation"
        self.fields["hospital"].help_text = "Select the hospital where rotation will take place"
        self.fields["supervisor"].help_text = "Supervisor who will oversee this rotation"
        self.fields["start_date"].help_text = "When the rotation should begin"
        self.fields["end_date"].help_text = "When the rotation should end"

        # Make fields required
        required_fields = ["pg", "department", "hospital", "start_date", "end_date"]
        for field_name in required_fields:
            self.fields[field_name].required = True

    def _set_default_dates(self):
        """Set sensible default dates"""
        today = timezone.now().date()

        # Default start date: next Monday
        days_ahead = 7 - today.weekday()  # Monday is 0
        if days_ahead <= 0:
            days_ahead += 7
        default_start = today + timedelta(days=days_ahead)

        # Default end date: 6 months from start
        default_end = default_start + relativedelta(months=6) - timedelta(days=1)

        self.fields["start_date"].initial = default_start
        self.fields["end_date"].initial = default_end

    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        pg = cleaned_data.get("pg")
        department = cleaned_data.get("department")
        hospital = cleaned_data.get("hospital")

        # Validate dates
        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("End date must be after start date")

            # Check minimum duration (at least 1 week)
            if (end_date - start_date).days < 7:
                raise ValidationError("Rotation must be at least 1 week long")

            # Check maximum duration (no more than 12 months)
            if (end_date - start_date).days > 365:
                raise ValidationError("Rotation cannot be longer than 12 months")

            # Warn if start date is in the past
            if start_date < timezone.now().date():
                raise ValidationError("Start date cannot be in the past")

        # Validate PG availability
        if pg and start_date and end_date:
            overlapping_rotations = Rotation.objects.filter(
                pg=pg, status__in=["planned", "ongoing", "pending"]
            ).exclude(pk=self.instance.pk if self.instance else None)

            for rotation in overlapping_rotations:
                if start_date <= rotation.end_date and end_date >= rotation.start_date:
                    raise ValidationError(
                        f"This PG already has a rotation scheduled from "
                        f"{rotation.start_date} to {rotation.end_date}"
                    )

        # Validate department belongs to hospital
        if department and hospital:
            if department.hospital != hospital:
                raise ValidationError(
                    "Selected department does not belong to the selected hospital"
                )

        # Validate supervisor permissions
        if self.user and self.user.role == "supervisor":
            supervisor = cleaned_data.get("supervisor")
            if supervisor and supervisor != self.user:
                raise ValidationError("You can only assign rotations to yourself")

            # Check if PG is assigned to this supervisor
            if pg and pg.supervisor != self.user:
                raise ValidationError("You can only create rotations for PGs assigned to you")

        return cleaned_data


class RotationUpdateForm(RotationCreateForm):
    """
    Form for updating existing rotations with additional restrictions.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict editing based on rotation status
        if self.instance and self.instance.pk:
            self._apply_status_restrictions()

    def _apply_status_restrictions(self):
        """Apply editing restrictions based on rotation status"""
        rotation = self.instance

        # Ongoing rotations: limited editing
        if rotation.status == "ongoing":
            readonly_fields = ["pg", "start_date", "department", "hospital"]
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
                    self.fields[field_name].help_text += " (Cannot be changed for ongoing rotation)"

        # Completed rotations: very limited editing
        elif rotation.status == "completed":
            readonly_fields = [
                "pg",
                "start_date",
                "end_date",
                "department",
                "hospital",
                "supervisor",
            ]
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
                    self.fields[
                        field_name
                    ].help_text += " (Cannot be changed for completed rotation)"

            # Only allow editing of feedback and notes for completed rotations
            editable_fields = ["feedback", "notes", "objectives", "learning_outcomes"]
            for field_name in list(self.fields.keys()):
                if field_name not in editable_fields:
                    del self.fields[field_name]


class RotationEvaluationForm(forms.ModelForm):
    """
    Form for creating and updating rotation evaluations.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

    class Meta:
        model = RotationEvaluation
        fields = ["evaluation_type", "score", "comments", "recommendations", "status"]
        widgets = {
            "evaluation_type": forms.Select(attrs={"class": "form-control"}),
            "score": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 100, "step": 1}
            ),
            "comments": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-control",
                    "placeholder": "Provide detailed feedback on performance...",
                }
            ),
            "recommendations": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Recommendations for improvement or continued development...",
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.rotation = kwargs.pop("rotation", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user and self.rotation:
            self._setup_evaluation_type_choices()
            self._setup_field_requirements()

        # Set initial status
        if not self.instance.pk:
            self.fields["status"].initial = "draft"

    def _setup_evaluation_type_choices(self):
        """Filter evaluation type choices based on user role"""
        user_role = self.user.role

        if user_role == "supervisor":
            # Supervisors can do supervisor and mid-rotation evaluations
            allowed_types = ["supervisor", "mid_rotation", "final"]
        elif user_role == "pg":
            # PGs can do self evaluations
            allowed_types = ["self"]
        elif user_role == "admin":
            # Admins can do any type
            allowed_types = [choice[0] for choice in RotationEvaluation.EVALUATION_TYPES]
        else:
            allowed_types = []

        # Filter choices
        filtered_choices = [
            choice for choice in RotationEvaluation.EVALUATION_TYPES if choice[0] in allowed_types
        ]
        self.fields["evaluation_type"].choices = filtered_choices

        # Check for existing evaluations to prevent duplicates
        if self.rotation:
            existing_evaluations = RotationEvaluation.objects.filter(
                rotation=self.rotation, evaluator=self.user
            ).values_list("evaluation_type", flat=True)

            # Remove already completed evaluation types
            filtered_choices = [
                choice for choice in filtered_choices if choice[0] not in existing_evaluations
            ]

            self.fields["evaluation_type"].choices = filtered_choices

    def _setup_field_requirements(self):
        """Setup field requirements and help text"""
        self.fields["evaluation_type"].help_text = "Type of evaluation being conducted"
        self.fields["score"].help_text = "Numerical score from 0-100 (60+ is passing)"
        self.fields["comments"].help_text = (
            "Detailed feedback on performance, achievements, and areas for improvement"
        )
        self.fields["recommendations"].help_text = "Specific recommendations for future development"

        # Make certain fields required
        self.fields["evaluation_type"].required = True
        self.fields["comments"].required = True

    def clean_score(self):
        """Validate score is within acceptable range"""
        score = self.cleaned_data.get("score")

        if score is not None:
            if score < 0 or score > 100:
                raise ValidationError("Score must be between 0 and 100")

        return score

    def clean(self):
        """Additional validation"""
        cleaned_data = super().clean()
        evaluation_type = cleaned_data.get("evaluation_type")
        score = cleaned_data.get("score")
        comments = cleaned_data.get("comments")

        # Require score for final evaluations
        if evaluation_type == "final" and score is None:
            raise ValidationError("Score is required for final evaluations")

        # Require substantial comments for low scores
        if score is not None and score < 60:
            if not comments or len(comments.strip()) < 50:
                raise ValidationError("Detailed comments are required for scores below 60")

        return cleaned_data


class RotationSearchForm(forms.Form):
    """
    Form for searching and filtering rotations.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by PG name, department, or hospital...",
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        choices=[("", "All Statuses")] + Rotation.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    department = forms.ModelChoiceField(
        required=False,
        queryset=Department.objects.filter(is_active=True),
        empty_label="All Departments",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    hospital = forms.ModelChoiceField(
        required=False,
        queryset=Hospital.objects.filter(is_active=True),
        empty_label="All Hospitals",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )


class RotationFilterForm(forms.Form):
    """
    Advanced filtering form for rotation reports.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

    SORT_CHOICES = [
        ("-start_date", "Start Date (Newest First)"),
        ("start_date", "Start Date (Oldest First)"),
        ("-end_date", "End Date (Newest First)"),
        ("end_date", "End Date (Oldest First)"),
        ("pg__last_name", "PG Name (A-Z)"),
        ("-pg__last_name", "PG Name (Z-A)"),
        ("department__name", "Department (A-Z)"),
        ("status", "Status"),
    ]

    pg = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(role="pg", is_active=True),
        empty_label="All PGs",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    supervisor = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(role="supervisor", is_active=True),
        empty_label="All Supervisors",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    year = forms.ChoiceField(required=False, widget=forms.Select(attrs={"class": "form-control"}))

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial="-start_date",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate year choices
        current_year = timezone.now().year
        year_choices = [("", "All Years")]
        for year in range(current_year - 5, current_year + 2):
            year_choices.append((str(year), str(year)))

        self.fields["year"].choices = year_choices


class BulkRotationAssignmentForm(forms.Form):
    """
    Form for bulk assignment of rotations to multiple PGs.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

    pgs = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="pg", is_active=True),
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the PGs to assign this rotation to",
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Department for the rotation",
    )

    hospital = forms.ModelChoiceField(
        queryset=Hospital.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Hospital where rotation will take place",
    )

    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role="supervisor", is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="Supervisor for all rotations",
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="Start date for all rotations",
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        help_text="End date for all rotations",
    )

    objectives = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        required=False,
        help_text="Common objectives for all rotations",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Configure form based on user role
        if self.user:
            if self.user.role == "supervisor":
                # Supervisors can only assign rotations to their own PGs
                self.fields["pgs"].queryset = User.objects.filter(
                    role="pg", supervisor=self.user, is_active=True
                ).order_by("last_name", "first_name")

                # Set supervisor to current user and make it readonly
                self.fields["supervisor"].initial = self.user
                self.fields["supervisor"].queryset = User.objects.filter(id=self.user.id)
                self.fields["supervisor"].widget.attrs.update({"readonly": True, "disabled": True})

            elif self.user.role == "admin":
                # Admins see all active PGs and supervisors
                self.fields["pgs"].queryset = User.objects.filter(
                    role="pg", is_active=True
                ).order_by("last_name", "first_name")

    def clean(self):
        """Validate bulk assignment data"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        pgs = cleaned_data.get("pgs")
        department = cleaned_data.get("department")
        hospital = cleaned_data.get("hospital")
        cleaned_data.get("supervisor")

        # For supervisors, ensure they are set as the supervisor regardless of form input
        if self.user and self.user.role == "supervisor":
            cleaned_data["supervisor"] = self.user

        # Validate dates
        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError("End date must be after start date")

            if start_date < timezone.now().date():
                raise ValidationError("Start date cannot be in the past")

        # Validate department belongs to hospital
        if department and hospital:
            if department.hospital != hospital:
                raise ValidationError(
                    "Selected department does not belong to the selected hospital"
                )

        # Check for conflicts with existing rotations
        if pgs and start_date and end_date:
            conflicts = []
            for pg in pgs:
                overlapping = Rotation.objects.filter(
                    pg=pg, status__in=["planned", "ongoing", "pending"]
                ).filter(start_date__lte=end_date, end_date__gte=start_date)

                if overlapping.exists():
                    conflicts.append(f"{pg.get_full_name()} has conflicting rotations")

            if conflicts:
                raise ValidationError("Conflicts found: " + "; ".join(conflicts))

        return cleaned_data


class QuickRotationForm(forms.Form):
    """
    Simplified form for quick rotation creation.

    Created: 2025-05-29 16:33:10 UTC
    Author: SMIB2012
    """

    pg = forms.ModelChoiceField(
        queryset=User.objects.filter(role="pg", is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    duration_months = forms.ChoiceField(
        choices=[
            (3, "3 months"),
            (6, "6 months"),
            (12, "12 months"),
        ],
        initial=6,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.role == "supervisor":
            self.fields["pg"].queryset = User.objects.filter(
                role="pg", supervisor=self.user, is_active=True
            )
