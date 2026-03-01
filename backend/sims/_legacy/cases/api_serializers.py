from rest_framework import serializers

from sims.cases.models import CaseCategory, CaseReview, ClinicalCase


class CaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseCategory
        fields = ["id", "name", "description", "color_code"]


class ClinicalCaseSerializer(serializers.ModelSerializer):
    pg_name = serializers.CharField(source="pg.get_full_name", read_only=True)
    supervisor_name = serializers.CharField(source="supervisor.get_full_name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = ClinicalCase
        fields = [
            "id",
            "case_title",
            "status",
            "date_encountered",
            "patient_age",
            "patient_gender",
            "complexity",
            "chief_complaint",
            "history_of_present_illness",
            "physical_examination",
            "management_plan",
            "clinical_reasoning",
            "learning_points",
            "supervisor_feedback",
            "category",
            "category_name",
            "primary_diagnosis",
            "rotation",
            "pg",
            "pg_name",
            "supervisor",
            "supervisor_name",
            "created_at",
            "updated_at",
            "reviewed_at",
        ]
        read_only_fields = [
            "status",
            "pg",
            "pg_name",
            "supervisor",
            "supervisor_name",
            "created_at",
            "updated_at",
            "reviewed_at",
            "supervisor_feedback",
        ]
        extra_kwargs = {
            "category": {"required": False, "allow_null": True},
            "primary_diagnosis": {"required": False, "allow_null": True},
            "rotation": {"required": False, "allow_null": True},
        }


class CaseReviewSerializer(serializers.ModelSerializer):
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
