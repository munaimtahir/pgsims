from datetime import date, timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import CaseCategory, CaseReview, ClinicalCase

User = get_user_model()


class CaseCategoryForm(forms.ModelForm):
    """Form for creating and editing case categories"""

    class Meta:
        model = CaseCategory
        fields = ["name", "description", "color_code", "sort_order", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "color_code": forms.TextInput(attrs={"type": "color"}),
            "sort_order": forms.NumberInput(attrs={"min": 0}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            # Check for duplicate names (excluding current instance if editing)
            qs = CaseCategory.objects.filter(name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("A category with this name already exists.")
        return name


class ClinicalCaseForm(forms.ModelForm):
    """Form for creating and editing clinical cases"""

    def __init__(self, *args, **kwargs):
        # Extract user from kwargs if provided
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Filter supervisors and rotations based on user context if needed
        if self.user and hasattr(self.user, "role"):
            if self.user.role == "pg":
                # For PG users, limit supervisor choices to their actual supervisors
                if hasattr(self.user, "supervisor") and self.user.supervisor:
                    self.fields["supervisor"].queryset = self.fields["supervisor"].queryset.filter(
                        id=self.user.supervisor.id
                    )
                    self.fields["supervisor"].initial = self.user.supervisor

    class Meta:
        model = ClinicalCase
        fields = [
            "date_encountered",
            "rotation",
            "supervisor",
            "case_title",
            "category",
            "patient_age",
            "patient_gender",
            "chief_complaint",
            "history_of_present_illness",
            "physical_examination",
            "primary_diagnosis",
            "differential_diagnosis",
            "management_plan",
            "learning_objectives",
            "clinical_reasoning",
            "learning_points",
            "challenges_faced",
            "outcome",
            "follow_up_plan",
            "case_files",
            "case_images",
        ]

        widgets = {
            "date_encountered": forms.DateInput(attrs={"type": "date"}),
            "chief_complaint": forms.Textarea(attrs={"rows": 2}),
            "history_of_present_illness": forms.Textarea(attrs={"rows": 3}),
            "physical_examination": forms.Textarea(attrs={"rows": 3}),
            "differential_diagnosis": forms.Textarea(attrs={"rows": 2}),
            "management_plan": forms.Textarea(attrs={"rows": 3}),
            "learning_objectives": forms.Textarea(attrs={"rows": 2}),
            "clinical_reasoning": forms.Textarea(attrs={"rows": 3}),
            "learning_points": forms.Textarea(attrs={"rows": 3}),
            "challenges_faced": forms.Textarea(attrs={"rows": 3}),
            "outcome": forms.Textarea(attrs={"rows": 3}),
            "follow_up_plan": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_date_encountered(self):
        case_date = self.cleaned_data.get("date_encountered")
        if case_date:
            # Case date cannot be in the future
            if case_date > date.today():
                raise ValidationError("Case date cannot be in the future.")

            # Case date cannot be more than 6 months old
            six_months_ago = date.today() - timedelta(days=180)
            if case_date < six_months_ago:
                raise ValidationError("Case date cannot be more than 6 months old.")

        return case_date

    def clean_patient_age(self):
        age = self.cleaned_data.get("patient_age")
        if age is not None:
            if age < 0 or age > 150:
                raise ValidationError("Please enter a valid patient age (0-150).")
        return age

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Set pg from user if provided and not already set
        if self.user and not instance.pg_id:
            if hasattr(self.user, "role") and self.user.role == "pg":
                instance.pg = self.user

        if commit:
            instance.save()

        return instance


class CaseReviewForm(forms.ModelForm):
    """Form for case reviews"""

    class Meta:
        model = CaseReview
        fields = [
            "status",
            "overall_feedback",
            "clinical_reasoning_feedback",
            "documentation_feedback",
            "learning_points_feedback",
            "strengths_identified",
            "areas_for_improvement",
            "recommendations",
            "follow_up_required",
            "clinical_knowledge_score",
            "clinical_reasoning_score",
            "documentation_score",
            "overall_score",
        ]
        widgets = {
            "overall_feedback": forms.Textarea(attrs={"rows": 4}),
            "clinical_reasoning_feedback": forms.Textarea(attrs={"rows": 3}),
            "documentation_feedback": forms.Textarea(attrs={"rows": 3}),
            "learning_points_feedback": forms.Textarea(attrs={"rows": 3}),
            "strengths_identified": forms.Textarea(attrs={"rows": 3}),
            "areas_for_improvement": forms.Textarea(attrs={"rows": 3}),
            "recommendations": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.case = kwargs.pop("case", None)
        self.reviewer = kwargs.pop("reviewer", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.case:
            instance.case = self.case
        if self.reviewer:
            instance.reviewer = self.reviewer
        if commit:
            instance.save()
        return instance


class CaseSearchForm(forms.Form):
    """Form for searching and filtering clinical cases"""

    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search cases by title, patient complaint, or diagnosis...",
                "class": "form-control",
            }
        ),
    )

    category = forms.ModelChoiceField(
        queryset=CaseCategory.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    status = forms.ChoiceField(
        choices=[("", "All Statuses")] + ClinicalCase.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )


class CaseFilterForm(forms.Form):
    """Form for case filtering"""

    filter_option = forms.CharField(max_length=100, required=False)
