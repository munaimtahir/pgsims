from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Diagnosis, LogbookEntry, LogbookReview, LogbookTemplate, Procedure, Skill

User = get_user_model()


class LogbookEntryCreateForm(forms.ModelForm):
    """
    Form for creating new logbook entries with role-based field filtering.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    class Meta:
        model = LogbookEntry
        fields = [
            "pg",
            "date",
            "rotation",
            "supervisor",
            "case_title",
            "template",
            "patient_age",
            "patient_gender",
            "patient_chief_complaint",
            "patient_history_summary",
            "primary_diagnosis",
            "secondary_diagnoses",
            "procedures",
            "skills",
            "investigations_ordered",
            "clinical_reasoning",
            "learning_points",
            "challenges_faced",
            "follow_up_required",
            "self_assessment_score",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "case_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Brief, descriptive title for this case...",
                }
            ),
            "patient_age": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 150}),
            "patient_gender": forms.Select(attrs={"class": "form-control"}),
            "patient_chief_complaint": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Patient's presenting complaint and symptoms...",
                }
            ),
            "patient_history_summary": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Relevant past medical history, medications, allergies...",
                }
            ),
            "investigations_ordered": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Tests ordered, results obtained, imaging findings...",
                }
            ),
            "clinical_reasoning": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-control",
                    "placeholder": "Your clinical thought process, differential diagnosis, reasoning for management decisions...",
                }
            ),
            "learning_points": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Key learning points from this case, new knowledge gained, skills developed...",
                }
            ),
            "challenges_faced": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Challenges encountered and how you addressed them...",
                }
            ),
            "follow_up_required": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Follow-up actions needed, further learning required...",
                }
            ),
            "self_assessment_score": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 10}
            ),
            "pg": forms.Select(attrs={"class": "form-control"}),
            "rotation": forms.Select(attrs={"class": "form-control"}),
            "supervisor": forms.Select(attrs={"class": "form-control"}),
            "template": forms.Select(attrs={"class": "form-control"}),
            "primary_diagnosis": forms.Select(attrs={"class": "form-control"}),
            "secondary_diagnoses": forms.SelectMultiple(
                attrs={"class": "form-control", "size": "5"}
            ),
            "procedures": forms.SelectMultiple(attrs={"class": "form-control", "size": "6"}),
            "skills": forms.SelectMultiple(attrs={"class": "form-control", "size": "6"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter querysets based on user role
        if self.user:
            self._setup_field_querysets()
            self._setup_field_requirements()

        # Set default values
        self._set_default_values()

        # Add help text
        self._setup_help_text()

        # Add CSS classes for better styling
        self._add_css_classes()

    def _setup_field_querysets(self):
        """Setup field querysets based on user role"""
        if self.user.role == "admin":
            # Admins see all active PGs
            self.fields["pg"].queryset = User.objects.filter(role="pg", is_active=True).order_by(
                "last_name", "first_name"
            )

            # All active supervisors
            self.fields["supervisor"].queryset = User.objects.filter(
                role="supervisor", is_active=True
            ).order_by("last_name", "first_name")

            # All rotations
            from sims.rotations.models import Rotation

            self.fields["rotation"].queryset = Rotation.objects.select_related(
                "department", "hospital"
            ).order_by("department__name", "start_date")

        elif self.user.role == "supervisor":
            # Supervisors see only their assigned PGs
            self.fields["pg"].queryset = User.objects.filter(
                role="pg", supervisor=self.user, is_active=True
            ).order_by("last_name", "first_name")

            # Only themselves as supervisor
            self.fields["supervisor"].queryset = User.objects.filter(id=self.user.id)
            self.fields["supervisor"].initial = self.user

            # Rotations for their PGs
            from sims.rotations.models import Rotation

            self.fields["rotation"].queryset = (
                Rotation.objects.filter(pg__supervisor=self.user)
                .select_related("department", "hospital")
                .order_by("department__name")
            )

        elif self.user.role == "pg":
            # PGs see only themselves
            self.fields["pg"].queryset = User.objects.filter(id=self.user.id)
            self.fields["pg"].initial = self.user
            self.fields["pg"].widget.attrs["readonly"] = True

            # Their supervisor
            if self.user.supervisor:
                self.fields["supervisor"].queryset = User.objects.filter(id=self.user.supervisor.id)
                self.fields["supervisor"].initial = self.user.supervisor

            # Their rotations
            from sims.rotations.models import Rotation

            self.fields["rotation"].queryset = (
                Rotation.objects.filter(pg=self.user)
                .select_related("department", "hospital")
                .order_by("start_date")
            )

        # Filter other querysets to active only
        self.fields["template"].queryset = LogbookTemplate.objects.filter(is_active=True).order_by(
            "template_type", "name"
        )

        self.fields["primary_diagnosis"].queryset = Diagnosis.objects.filter(
            is_active=True
        ).order_by("category", "name")

        self.fields["secondary_diagnoses"].queryset = Diagnosis.objects.filter(
            is_active=True
        ).order_by("category", "name")

        self.fields["procedures"].queryset = Procedure.objects.filter(is_active=True).order_by(
            "category", "difficulty_level", "name"
        )

        self.fields["skills"].queryset = Skill.objects.filter(is_active=True).order_by(
            "category", "level", "name"
        )

    def _setup_field_requirements(self):
        """Setup field requirements based on user role"""
        # Core required fields
        required_fields = [
            "date",
            "patient_age",
            "patient_gender",
            "patient_chief_complaint",
            "primary_diagnosis",
            "clinical_reasoning",
            "learning_points",
        ]

        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

        # PG field is required for admins and supervisors
        if self.user and self.user.role in ["admin", "supervisor"]:
            self.fields["pg"].required = True

        # Case title is encouraged but not strictly required
        self.fields["case_title"].required = False

    def _set_default_values(self):
        """Set sensible default values"""
        today = timezone.now().date()

        # Default date to today
        self.fields["date"].initial = today

        # Default to a general medical template if available
        try:
            default_template = LogbookTemplate.objects.filter(
                is_default=True, template_type="medical", is_active=True
            ).first()
            if default_template:
                self.fields["template"].initial = default_template
        except LogbookTemplate.DoesNotExist:
            pass

    def _setup_help_text(self):
        """Setup comprehensive help text for fields"""
        self.fields["date"].help_text = "Date when this clinical encounter occurred"
        self.fields["case_title"].help_text = (
            "Brief, descriptive title (will be auto-generated if left blank)"
        )
        self.fields["template"].help_text = "Template to guide your entry structure (optional)"
        self.fields["patient_age"].help_text = "Patient age in years"
        self.fields["patient_gender"].help_text = "Patient gender"
        self.fields["patient_chief_complaint"].help_text = "Main reason for patient presentation"
        self.fields["patient_history_summary"].help_text = (
            "Relevant medical history, medications, social history"
        )
        self.fields["primary_diagnosis"].help_text = "Primary or working diagnosis"
        self.fields["secondary_diagnoses"].help_text = (
            "Secondary diagnoses or differential diagnoses"
        )
        self.fields["procedures"].help_text = "Procedures you performed or observed"
        self.fields["skills"].help_text = "Clinical skills you demonstrated"
        self.fields["investigations_ordered"].help_text = "Tests ordered and results"
        self.fields["clinical_reasoning"].help_text = "Your thought process and clinical reasoning"
        self.fields["learning_points"].help_text = "Key learning points and knowledge gained"
        self.fields["challenges_faced"].help_text = "Challenges encountered and how addressed"
        self.fields["follow_up_required"].help_text = "Further learning or follow-up needed"
        self.fields["self_assessment_score"].help_text = "Rate your performance (1-10)"
        self.fields["pg"].help_text = "Postgraduate who managed this case"
        self.fields["rotation"].help_text = "Rotation during which this case occurred"
        self.fields["supervisor"].help_text = "Supervising consultant"

    def _add_css_classes(self):
        """Add CSS classes for consistent styling"""
        for field_name, field in self.fields.items():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"

            # Add specific classes for different field types
            if isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs["class"] += " form-control-multiple"
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["class"] += " form-control-textarea"
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs["class"] += " form-control-date"

    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        date_field = cleaned_data.get("date")
        pg = cleaned_data.get("pg")
        supervisor = cleaned_data.get("supervisor")
        rotation = cleaned_data.get("rotation")
        primary_diagnosis = cleaned_data.get("primary_diagnosis")
        secondary_diagnoses = cleaned_data.get("secondary_diagnoses", [])
        patient_age = cleaned_data.get("patient_age")

        # Validate date is not in the future
        if date_field and date_field > timezone.now().date():
            raise ValidationError({"date": "Entry date cannot be in the future"})

        # Validate date is not too old (more than 1 year)
        if date_field and date_field < (timezone.now().date() - timedelta(days=365)):
            raise ValidationError(
                {
                    "date": "Entry date cannot be more than 1 year old. Contact admin if this is a valid historical entry."
                }
            )

        # Validate supervisor assignment
        if supervisor and pg:
            if pg.supervisor and supervisor != pg.supervisor and not supervisor.role == "admin":
                raise ValidationError(
                    {"supervisor": "Selected supervisor should be the PG's assigned supervisor"}
                )

        # Validate rotation assignment
        if rotation and pg:
            if rotation.pg and rotation.pg != pg:
                raise ValidationError(
                    {"rotation": "Selected rotation does not belong to the selected PG"}
                )

        # Validate that primary diagnosis is not in secondary diagnoses
        if primary_diagnosis and secondary_diagnoses:
            if primary_diagnosis in secondary_diagnoses:
                raise ValidationError(
                    {
                        "secondary_diagnoses": "Primary diagnosis cannot also be a secondary diagnosis"
                    }
                )

        # Validate patient age
        if patient_age is not None:
            if patient_age < 0 or patient_age > 150:
                raise ValidationError(
                    {"patient_age": "Please enter a valid patient age (0-150 years)"}
                )

        # Auto-generate case title if not provided
        if not cleaned_data.get("case_title"):
            if primary_diagnosis and patient_age is not None:
                gender_display = dict(LogbookEntry.PATIENT_GENDER_CHOICES).get(
                    cleaned_data.get("patient_gender"), "Patient"
                )
                cleaned_data["case_title"] = (
                    f"{patient_age}y {gender_display} - {primary_diagnosis.name}"
                )
            elif primary_diagnosis:
                cleaned_data["case_title"] = f"{primary_diagnosis.name} - {date_field}"
            else:
                cleaned_data["case_title"] = f"Clinical Case - {date_field}"

        return cleaned_data

    def clean_procedures(self):
        """Validate selected procedures"""
        procedures = self.cleaned_data.get("procedures")

        if procedures:
            # Check for reasonable number of procedures
            if procedures.count() > 10:
                raise ValidationError("Please select a maximum of 10 procedures for a single case")

            # Warn about high difficulty procedures
            high_difficulty = procedures.filter(difficulty_level__gte=4)
            if high_difficulty.count() > 2:
                # This is a warning, not an error
                pass

        return procedures

    def clean_skills(self):
        """Validate selected skills"""
        skills = self.cleaned_data.get("skills")

        if skills:
            # Check for reasonable number of skills
            if skills.count() > 15:
                raise ValidationError("Please select a maximum of 15 skills for a single case")

        return skills


class LogbookEntryUpdateForm(LogbookEntryCreateForm):
    """
    Form for updating existing logbook entries with additional restrictions.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply restrictions based on entry status
        if self.instance and self.instance.pk:
            self._apply_status_restrictions()

    def _apply_status_restrictions(self):
        """Apply editing restrictions based on entry status"""
        entry = self.instance

        # Approved entries: limited editing
        if entry.status == "approved":
            readonly_fields = ["pg", "date", "rotation", "primary_diagnosis", "procedures"]
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
                    self.fields[field_name].help_text += " (Cannot be changed for approved entry)"

        # Submitted entries: PGs can't edit, only supervisors/admins
        elif entry.status == "submitted":
            if self.user and self.user.role == "pg":
                # Disable most fields for PGs when entry is submitted
                editable_fields = ["learning_points", "follow_up_required", "challenges_faced"]
                for field_name, field in self.fields.items():
                    if field_name not in editable_fields:
                        field.disabled = True
                        field.help_text += " (Cannot be changed while under review)"


class LogbookReviewForm(forms.ModelForm):
    """
    Form for creating and updating logbook reviews.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    class Meta:
        model = LogbookReview
        fields = [
            "status",
            "review_date",
            "feedback",
            "strengths_identified",
            "areas_for_improvement",
            "recommendations",
            "follow_up_required",
            "clinical_knowledge_score",
            "clinical_skills_score",
            "professionalism_score",
            "overall_score",
        ]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "review_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "feedback": forms.Textarea(
                attrs={
                    "rows": 8,
                    "class": "form-control",
                    "placeholder": "Provide comprehensive feedback on this case presentation...",
                }
            ),
            "strengths_identified": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Highlight the strengths demonstrated in this case...",
                }
            ),
            "areas_for_improvement": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Areas where the trainee can improve...",
                }
            ),
            "recommendations": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Specific recommendations for future learning and development...",
                }
            ),
            "follow_up_required": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "clinical_knowledge_score": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 10}
            ),
            "clinical_skills_score": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 10}
            ),
            "professionalism_score": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 10}
            ),
            "overall_score": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 10}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.entry = kwargs.pop("entry", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Set up field labels
        self.fields["status"].label = "Review Decision"
        self.fields["feedback"].label = "Overall Feedback"
        self.fields["strengths_identified"].label = "Strengths Demonstrated"
        self.fields["areas_for_improvement"].label = "Areas for Improvement"
        self.fields["recommendations"].label = "Recommendations for Future Learning"
        self.fields["clinical_knowledge_score"].label = "Clinical Knowledge (1-10)"
        self.fields["clinical_skills_score"].label = "Clinical Skills (1-10)"
        self.fields["professionalism_score"].label = "Professionalism (1-10)"
        self.fields["overall_score"].label = "Overall Performance (1-10)"
        self.fields["review_date"].label = "Review Date"
        self.fields["follow_up_required"].label = "Follow-up Discussion Required"

        if self.user and self.entry:
            self._setup_field_requirements()

        # Set default review date
        if not self.instance.pk:
            self.fields["review_date"].initial = timezone.now().date()

        # Setup help text
        self._setup_help_text()

        # Customize status choices based on entry status
        self._setup_status_choices()

    def _setup_field_requirements(self):
        """Setup field requirements and validation"""
        self.fields["status"].required = True
        self.fields["feedback"].required = True
        self.fields["review_date"].required = True

        # Require scores for complete reviews
        if not self.instance.pk:  # New review
            self.fields["clinical_knowledge_score"].required = True
            self.fields["clinical_skills_score"].required = True
            self.fields["professionalism_score"].required = True
            self.fields["overall_score"].required = True

    def _setup_status_choices(self):
        """Setup status choices based on entry status"""
        if self.entry:
            if self.entry.status in ["pending", "submitted"]:
                status_choices = [
                    ("pending", "Keep Pending"),
                    ("approved", "Approve"),
                    ("needs_revision", "Needs Revision"),
                    ("rejected", "Reject"),
                ]
            else:
                status_choices = LogbookReview.STATUS_CHOICES

            self.fields["status"].choices = status_choices

    def _setup_help_text(self):
        """Setup help text for fields"""
        self.fields["status"].help_text = "Review decision for this logbook entry"
        self.fields["review_date"].help_text = "Date when this review was conducted"
        self.fields["feedback"].help_text = (
            "Comprehensive feedback on clinical performance and learning"
        )
        self.fields["strengths_identified"].help_text = (
            "Specific strengths demonstrated by the trainee"
        )
        self.fields["areas_for_improvement"].help_text = (
            "Areas requiring development or improvement"
        )
        self.fields["recommendations"].help_text = "Specific recommendations for future learning"
        self.fields["follow_up_required"].help_text = "Check if follow-up discussion is needed"
        self.fields["clinical_knowledge_score"].help_text = (
            "Clinical knowledge demonstration (1-10)"
        )
        self.fields["clinical_skills_score"].help_text = "Clinical skills performance (1-10)"
        self.fields["professionalism_score"].help_text = (
            "Professional behavior and communication (1-10)"
        )
        self.fields["overall_score"].help_text = "Overall performance assessment (1-10)"

    def clean(self):
        """Validate review data"""
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        feedback = cleaned_data.get("feedback")
        areas_for_improvement = cleaned_data.get("areas_for_improvement")
        clinical_knowledge_score = cleaned_data.get("clinical_knowledge_score")
        clinical_skills_score = cleaned_data.get("clinical_skills_score")
        professionalism_score = cleaned_data.get("professionalism_score")
        overall_score = cleaned_data.get("overall_score")

        # Require detailed feedback for all reviews
        if not feedback or len(feedback.strip()) < 20:
            raise ValidationError(
                {"feedback": "Please provide detailed feedback (minimum 20 characters)"}
            )

        # Require areas for improvement when not approved
        if status == "needs_revision":
            if not areas_for_improvement or len(areas_for_improvement.strip()) < 10:
                raise ValidationError(
                    {
                        "areas_for_improvement": "Please specify areas for improvement when requesting revision"
                    }
                )

        # Validate score consistency
        if all(
            [clinical_knowledge_score, clinical_skills_score, professionalism_score, overall_score]
        ):
            component_avg = (
                clinical_knowledge_score + clinical_skills_score + professionalism_score
            ) / 3

            # Overall score should be reasonably close to component average
            if abs(overall_score - component_avg) > 2:
                raise ValidationError(
                    {"overall_score": "Overall score should be consistent with component scores"}
                )

        # Check if all scores are provided when status is approved
        if status == "approved":
            if not all(
                [
                    clinical_knowledge_score,
                    clinical_skills_score,
                    professionalism_score,
                    overall_score,
                ]
            ):
                raise ValidationError("All assessment scores are required when approving an entry")

        return cleaned_data


class LogbookSearchForm(forms.Form):
    """
    Form for searching and filtering logbook entries.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by case title, PG name, diagnosis, or learning points...",
            }
        ),
    )

    status = forms.ChoiceField(
        required=False,
        choices=[("", "All Statuses")] + LogbookEntry.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    rotation = forms.ModelChoiceField(
        required=False,
        queryset=None,  # Set in __init__
        empty_label="All Rotations",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    diagnosis = forms.ModelChoiceField(
        required=False,
        queryset=Diagnosis.objects.filter(is_active=True),
        empty_label="All Diagnoses",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    procedure = forms.ModelChoiceField(
        required=False,
        queryset=Procedure.objects.filter(is_active=True),
        empty_label="All Procedures",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Setup rotation queryset based on user role
        if user:
            from sims.rotations.models import Rotation

            if user.role == "admin":
                self.fields["rotation"].queryset = Rotation.objects.select_related(
                    "department", "hospital"
                )
            elif user.role == "supervisor":
                self.fields["rotation"].queryset = Rotation.objects.filter(
                    pg__supervisor=user
                ).select_related("department", "hospital")
            elif user.role == "pg":
                self.fields["rotation"].queryset = Rotation.objects.filter(pg=user).select_related(
                    "department", "hospital"
                )


class LogbookFilterForm(forms.Form):
    """
    Advanced filtering form for logbook entries.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    SORT_CHOICES = [
        ("-date", "Date (Newest First)"),
        ("date", "Date (Oldest First)"),
        ("-created_at", "Created (Newest First)"),
        ("created_at", "Created (Oldest First)"),
        ("case_title", "Case Title (A-Z)"),
        ("-case_title", "Case Title (Z-A)"),
        ("pg__last_name", "PG Name (A-Z)"),
        ("-pg__last_name", "PG Name (Z-A)"),
        ("status", "Status"),
        ("primary_diagnosis__name", "Diagnosis (A-Z)"),
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

    diagnosis_category = forms.ChoiceField(
        required=False,
        choices=[("", "All Categories")] + Diagnosis.CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    procedure_category = forms.ChoiceField(
        required=False,
        choices=[("", "All Categories")] + Procedure.CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    skill_category = forms.ChoiceField(
        required=False,
        choices=[("", "All Categories")] + Skill.CATEGORY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    template_type = forms.ModelChoiceField(
        required=False,
        queryset=LogbookTemplate.objects.filter(is_active=True),
        empty_label="All Templates",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    score_range_min = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min score"}),
    )

    score_range_max = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max score"}),
    )

    overdue_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Show only overdue draft entries",
    )

    reviewed_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Show only reviewed entries",
    )

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial="-date",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter querysets based on user role
        if user:
            if user.role == "supervisor":
                self.fields["pg"].queryset = User.objects.filter(
                    role="pg", supervisor=user, is_active=True
                )
                # Remove supervisor field for supervisors
                del self.fields["supervisor"]
            elif user.role == "pg":
                # PGs don't need these filters
                del self.fields["pg"]
                del self.fields["supervisor"]


class BulkLogbookActionForm(forms.Form):
    """
    Form for bulk actions on logbook entries.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    ACTION_CHOICES = [
        ("approve", "Approve Selected"),
        ("request_revision", "Request Revision"),
        ("archive", "Archive Selected"),
        ("assign_supervisor", "Assign Supervisor"),
    ]

    entries = forms.ModelMultipleChoiceField(
        queryset=LogbookEntry.objects.none(),  # Set in __init__
        widget=forms.CheckboxSelectMultiple,
        help_text="Select entries to process",
    )

    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect,
        help_text="Action to perform on selected entries",
    )

    bulk_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Optional comments to apply to all selected entries...",
            }
        ),
        help_text="Comments will be added to all selected entries",
    )

    new_supervisor = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(role="supervisor", is_active=True),
        empty_label="Select Supervisor",
        widget=forms.Select(attrs={"class": "form-control"}),
        help_text="New supervisor for selected entries (only for assign_supervisor action)",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter entries based on user role
        if self.user:
            if self.user.role == "supervisor":
                self.fields["entries"].queryset = LogbookEntry.objects.filter(
                    pg__supervisor=self.user, status__in=["submitted", "approved"]
                ).select_related("pg", "primary_diagnosis")

                # Remove assign_supervisor action for supervisors
                self.fields["action"].choices = [
                    choice for choice in self.ACTION_CHOICES if choice[0] != "assign_supervisor"
                ]

            elif self.user.role == "admin":
                self.fields["entries"].queryset = LogbookEntry.objects.filter(
                    status__in=["submitted", "approved"]
                ).select_related("pg", "primary_diagnosis")

    def clean(self):
        """Validate bulk action data"""
        cleaned_data = super().clean()
        entries = cleaned_data.get("entries")
        action = cleaned_data.get("action")
        new_supervisor = cleaned_data.get("new_supervisor")

        if not entries:
            raise ValidationError("Please select at least one entry")

        # Validate action-specific requirements
        if action == "request_revision" and not cleaned_data.get("bulk_comments"):
            raise ValidationError(
                {"bulk_comments": "Comments are required when requesting revision"}
            )

        if action == "assign_supervisor" and not new_supervisor:
            raise ValidationError({"new_supervisor": "Please select a supervisor for assignment"})

        # Check permissions for each entry
        if self.user and self.user.role == "supervisor":
            for entry in entries:
                if entry.pg.supervisor != self.user:
                    raise ValidationError(
                        f"You don't have permission to process entry: {entry.case_title}"
                    )

        return cleaned_data


class QuickLogbookEntryForm(forms.ModelForm):
    """
    Simplified form for quick logbook entry creation.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    class Meta:
        model = LogbookEntry
        fields = [
            "date",
            "rotation",
            "case_title",
            "patient_age",
            "patient_gender",
            "patient_chief_complaint",
            "primary_diagnosis",
            "procedures",
            "learning_points",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "case_title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Brief case title..."}
            ),
            "patient_age": forms.NumberInput(attrs={"class": "form-control", "min": 0, "max": 150}),
            "patient_gender": forms.Select(attrs={"class": "form-control"}),
            "patient_chief_complaint": forms.Textarea(
                attrs={
                    "rows": 2,
                    "class": "form-control",
                    "placeholder": "Main presenting complaint...",
                }
            ),
            "primary_diagnosis": forms.Select(attrs={"class": "form-control"}),
            "procedures": forms.SelectMultiple(attrs={"class": "form-control", "size": "4"}),
            "learning_points": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "Key learning points..."}
            ),
            "rotation": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Set default date
        if not self.initial.get("date"):
            self.fields["date"].initial = timezone.now().date()

        # Filter querysets based on user role
        if self.user:
            self._setup_quick_querysets()

        # Mark all fields as required for quick entry
        for field in self.fields.values():
            if field != self.fields["procedures"]:  # Procedures optional
                field.required = True

    def _setup_quick_querysets(self):
        """Setup simplified querysets for quick entry"""
        # Only active items
        self.fields["primary_diagnosis"].queryset = Diagnosis.objects.filter(
            is_active=True
        ).order_by("name")

        self.fields["procedures"].queryset = Procedure.objects.filter(
            is_active=True, category__in=["basic", "intermediate"]
        ).order_by("name")

        # User-specific rotations
        if self.user.role == "pg":
            from sims.rotations.models import Rotation

            self.fields["rotation"].queryset = Rotation.objects.filter(pg=self.user).select_related(
                "department"
            )


class LogbookTemplateForm(forms.ModelForm):
    """
    Form for creating and editing logbook templates.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    class Meta:
        model = LogbookTemplate
        fields = [
            "name",
            "template_type",
            "description",
            "is_default",
            "is_active",
            "completion_guidelines",
            "example_entries",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "template_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "completion_guidelines": forms.Textarea(attrs={"rows": 6, "class": "form-control"}),
            "example_entries": forms.Textarea(attrs={"rows": 8, "class": "form-control"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    # Additional fields for template structure
    template_sections = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "class": "form-control",
                "placeholder": "Enter sections separated by new lines...",
            }
        ),
        help_text="Enter template sections, one per line",
    )

    required_fields_list = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Enter required field names separated by new lines...",
            }
        ),
        help_text="Enter required field names, one per line",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate additional fields from JSON if editing
        if self.instance and self.instance.pk:
            sections = self.instance.get_template_sections()
            if sections:
                self.fields["template_sections"].initial = "\n".join(sections)

            required_fields = self.instance.get_required_fields_list()
            if required_fields:
                self.fields["required_fields_list"].initial = "\n".join(required_fields)

    def clean(self):
        """Validate and process template data"""
        cleaned_data = super().clean()

        # Process template sections
        sections_text = cleaned_data.get("template_sections", "")
        if sections_text:
            sections = [s.strip() for s in sections_text.split("\n") if s.strip()]
            cleaned_data["template_structure"] = {"sections": sections}
        else:
            cleaned_data["template_structure"] = {}

        # Process required fields
        required_text = cleaned_data.get("required_fields_list", "")
        if required_text:
            required_fields = [f.strip() for f in required_text.split("\n") if f.strip()]
            cleaned_data["required_fields"] = required_fields
        else:
            cleaned_data["required_fields"] = []

        return cleaned_data

    def save(self, commit=True):
        """Save template with processed structure"""
        instance = super().save(commit=False)

        # Set JSON fields from cleaned data
        if hasattr(self, "cleaned_data"):
            instance.template_structure = self.cleaned_data.get("template_structure", {})
            instance.required_fields = self.cleaned_data.get("required_fields", [])

        if commit:
            instance.save()

        return instance


class LogbookComplianceReportForm(forms.Form):
    """
    Form for generating logbook compliance reports.

    Created: 2025-05-29 17:27:00 UTC
    Author: SMIB2012
    """

    REPORT_TYPE_CHOICES = [
        ("individual", "Individual PG Performance"),
        ("supervisor", "Supervisor Summary"),
        ("department", "Department Overview"),
        ("system", "System-wide Metrics"),
        ("compliance", "Compliance Report"),
    ]

    report_type = forms.ChoiceField(
        choices=REPORT_TYPE_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    date_range_start = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    date_range_end = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    pg_filter = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(role="pg", is_active=True),
        empty_label="All PGs",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    include_drafts = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Include draft entries in the report",
    )

    include_scores = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        help_text="Include assessment scores in the report",
    )

    export_format = forms.ChoiceField(
        choices=[
            ("html", "View in Browser"),
            ("csv", "Export as CSV"),
            ("pdf", "Export as PDF"),
        ],
        initial="html",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Set default date range (last 3 months)
        today = timezone.now().date()
        three_months_ago = today - timedelta(days=90)

        self.fields["date_range_start"].initial = three_months_ago
        self.fields["date_range_end"].initial = today

        # Filter PG choices based on user role
        if self.user and self.user.role == "supervisor":
            self.fields["pg_filter"].queryset = User.objects.filter(
                role="pg", supervisor=self.user, is_active=True
            )


# --- Appended Forms Start ---


# New form for PG logbook entry creation as per feature requirements
class PGLogbookEntryForm(forms.ModelForm):
    # Additional fields that can be stored in extra fields or handled separately
    specialty = forms.ChoiceField(
        choices=[
            ("general_medicine", "General Medicine"),
            ("surgery", "Surgery"),
            ("pediatrics", "Pediatrics"),
            ("obstetrics_gynecology", "Obstetrics & Gynecology"),
            ("psychiatry", "Psychiatry"),
            ("radiology", "Radiology"),
            ("pathology", "Pathology"),
            ("anesthesiology", "Anesthesiology"),
            ("emergency_medicine", "Emergency Medicine"),
            ("family_medicine", "Family Medicine"),
            ("internal_medicine", "Internal Medicine"),
            ("cardiology", "Cardiology"),
            ("neurology", "Neurology"),
            ("orthopedics", "Orthopedics"),
            ("dermatology", "Dermatology"),
            ("ophthalmology", "Ophthalmology"),
            ("ent", "ENT"),
            ("urology", "Urology"),
            ("oncology", "Oncology"),
            ("other", "Other"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    clinical_setting = forms.ChoiceField(
        choices=[
            ("inpatient", "Inpatient Ward"),
            ("outpatient", "Outpatient Clinic"),
            ("emergency", "Emergency Department"),
            ("icu", "Intensive Care Unit"),
            ("operating_room", "Operating Room"),
            ("laboratory", "Laboratory"),
            ("radiology", "Radiology Department"),
            ("community", "Community Setting"),
            ("other", "Other"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    competency_level = forms.ChoiceField(
        choices=[
            ("1", "Level 1 - Novice"),
            ("2", "Level 2 - Beginner"),
            ("3", "Level 3 - Competent"),
            ("4", "Level 4 - Proficient"),
            ("5", "Level 5 - Expert"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # Fields for procedures and investigations (as text for now)
    procedure_performed = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Procedures performed or observed during this case...",
            }
        ),
    )

    secondary_diagnosis = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "class": "form-control",
                "placeholder": "Secondary or differential diagnoses...",
            }
        ),
    )

    management_plan = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Treatment plan and management decisions...",
            }
        ),
    )

    cme_points = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.5", "min": "0"}),
    )

    class Meta:
        model = LogbookEntry
        fields = [
            "case_title",
            "date",
            "location_of_activity",
            "patient_age",
            "patient_gender",
            "patient_chief_complaint",
            "patient_history_summary",  # Corresponds to "Brief history"
            "primary_diagnosis",
            "management_action",
            "topic_subtopic",
            "learning_points",
            "challenges_faced",
            "follow_up_required",
            "self_assessment_score",
            "investigations_ordered",
        ]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "max": timezone.now().date().isoformat(),
                }
            ),
            "case_title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of case or diagnosis"}
            ),
            "location_of_activity": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "E.g., Ward A, OPD Clinic 2, Emergency Room",
                }
            ),
            "patient_age": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "max": 150,
                    "placeholder": "Patient age in years",
                }
            ),
            "patient_gender": forms.Select(attrs={"class": "form-control"}),
            "patient_chief_complaint": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Patient's main presenting complaint...",
                }
            ),
            "patient_history_summary": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Brief relevant history of the patient",
                }
            ),
            "primary_diagnosis": forms.Select(attrs={"class": "form-control"}),
            "management_action": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Management actions taken",
                }
            ),
            "topic_subtopic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "E.g., Cardiology/Arrhythmia"}
            ),
            "learning_points": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Key learning points from this case...",
                }
            ),
            "challenges_faced": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Difficulties encountered and how addressed...",
                }
            ),
            "follow_up_required": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Follow-up actions or further learning needed...",
                }
            ),
            "self_assessment_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                    "placeholder": "Rate your performance (1-10)",
                }
            ),
            "investigations_ordered": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Laboratory tests, imaging, and other investigations...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # PG user
        super().__init__(*args, **kwargs)

        if not self.initial.get("date"):
            self.fields["date"].initial = timezone.now().date()

        # Set up querysets for foreign key fields
        if "primary_diagnosis" in self.fields:
            self.fields["primary_diagnosis"].queryset = Diagnosis.objects.filter(
                is_active=True
            ).order_by("name")
            self.fields["primary_diagnosis"].empty_label = "Select primary diagnosis..."

        # Field requirements
        self.fields["case_title"].required = True
        self.fields["date"].required = True
        self.fields["location_of_activity"].required = True
        self.fields["patient_history_summary"].required = True
        self.fields["management_action"].required = True
        self.fields["topic_subtopic"].required = False

        # New field requirements
        self.fields["patient_age"].required = False
        self.fields["patient_gender"].required = False
        self.fields["patient_chief_complaint"].required = False
        self.fields["primary_diagnosis"].required = False
        self.fields["learning_points"].required = False
        self.fields["challenges_faced"].required = False
        self.fields["follow_up_required"].required = False
        self.fields["self_assessment_score"].required = False
        self.fields["investigations_ordered"].required = False

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise ValidationError("The date cannot be in the future.")
        return date

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle custom fields that aren't directly in the model
        if hasattr(self, "cleaned_data"):
            # Store custom fields in a temporary way or handle them differently
            # For now, we'll just save the model fields
            pass

        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PGLogbookEntryEditForm(forms.ModelForm):
    supervisor_feedback_display = forms.CharField(
        widget=forms.Textarea(
            attrs={"readonly": "readonly", "rows": 4, "class": "form-control bg-light"}
        ),
        required=False,
        label="Latest Supervisor Feedback",
    )

    class Meta:
        model = LogbookEntry
        fields = [
            "case_title",
            "date",
            "location_of_activity",
            "patient_history_summary",
            "management_action",
            "topic_subtopic",
            "supervisor_feedback_display",
        ]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "max": timezone.now().date().isoformat(),
                }
            ),
            "case_title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of case or diagnosis"}
            ),
            "location_of_activity": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "E.g., Ward A, OPD Clinic 2, Emergency Room",
                }
            ),
            "patient_history_summary": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Brief relevant history of the patient",
                }
            ),
            "management_action": forms.Textarea(
                attrs={
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Management actions taken",
                }
            ),
            "topic_subtopic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "E.g., Cardiology/Arrhythmia"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["supervisor_feedback_display"].initial = self.instance.supervisor_feedback

        self.fields["case_title"].required = True
        self.fields["date"].required = True
        self.fields["location_of_activity"].required = True
        self.fields["patient_history_summary"].required = True
        self.fields["management_action"].required = True
        self.fields["topic_subtopic"].required = False

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > timezone.now().date():
            raise ValidationError("The date cannot be in the future.")
        return date

    def save(self, commit=True):
        self.cleaned_data.pop("supervisor_feedback_display", None)
        return super().save(commit=commit)


class SupervisorLogbookReviewForm(forms.Form):
    ACTION_CHOICES = [
        ("", "---------"),
        ("approve", "Approve"),
        ("reject", "Reject"),
        ("return_for_edits", "Return for Edits"),
    ]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select form-select-lg mb-3"}),
    )
    supervisor_comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Provide feedback or reason for rejection/return (optional for approval).",
            }
        ),
        required=False,
        label="Feedback / Comments",
    )

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        comment = cleaned_data.get("supervisor_comment")

        if action in ["reject", "return_for_edits"] and not comment:
            self.add_error(
                "supervisor_comment",
                "Comments are required when rejecting or returning an entry for edits.",
            )

        return cleaned_data


class SupervisorBulkActionForm(forms.Form):
    """Form for selecting entries and action for bulk review"""

    BULK_ACTION_CHOICES = [
        ("", "---------"),
        ("approve", "Approve Selected"),
        ("reject", "Reject Selected"),
        ("return", "Return for Revision"),
    ]

    entry_ids = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, required=True, label="Select Entries"
    )

    action = forms.ChoiceField(
        choices=BULK_ACTION_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Optional comment for all selected entries...",
            }
        ),
        required=False,
        label="Comment (Optional)",
    )

    def __init__(self, *args, **kwargs):
        entries = kwargs.pop("entries", None)
        super().__init__(*args, **kwargs)

        if entries:
            self.fields["entry_ids"].choices = [
                (
                    entry.id,
                    f"{entry.pg.get_full_name()} - {entry.case_title[:50]}{'...' if len(entry.case_title) > 50 else ''}",
                )
                for entry in entries
            ]

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        comment = cleaned_data.get("comment")
        entry_ids = cleaned_data.get("entry_ids")

        if not entry_ids:
            self.add_error("entry_ids", "Please select at least one entry.")

        if action in ["reject", "return"] and not comment:
            self.add_error("comment", "Comment is required when rejecting or returning entries.")

        return cleaned_data


class SupervisorBulkApproveForm(forms.Form):
    """Simplified form for bulk approval"""

    entry_ids = forms.CharField(widget=forms.HiddenInput())
    action = forms.CharField(initial="approve", widget=forms.HiddenInput())
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "class": "form-control",
                "placeholder": "Optional approval comment...",
            }
        ),
        required=False,
        label="Approval Comment (Optional)",
    )


class SupervisorBulkRejectForm(forms.Form):
    """Form for bulk rejection with required feedback"""

    entry_ids = forms.CharField(widget=forms.HiddenInput())
    action = forms.CharField(initial="reject", widget=forms.HiddenInput())
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "Please provide reason for rejection...",
            }
        ),
        required=True,
        label="Rejection Reason (Required)",
    )


# --- Appended Forms End ---
