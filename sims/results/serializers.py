from rest_framework import serializers
from .models import Exam, Score


class ExamSerializer(serializers.ModelSerializer):
    conducted_by_name = serializers.CharField(source="conducted_by.get_full_name", read_only=True)
    rotation_name = serializers.CharField(source="rotation.name", read_only=True)
    total_scores = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = [
            "id",
            "title",
            "exam_type",
            "rotation",
            "rotation_name",
            "module_name",
            "date",
            "start_time",
            "duration_minutes",
            "max_marks",
            "passing_marks",
            "requires_eligibility",
            "status",
            "conducted_by",
            "conducted_by_name",
            "instructions",
            "remarks",
            "total_scores",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "total_scores"]

    def validate(self, data):
        """Validate exam data."""
        if data.get("passing_marks") and data.get("max_marks"):
            if data["passing_marks"] > data["max_marks"]:
                raise serializers.ValidationError("Passing marks cannot exceed max marks")
        return data


class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    student_roll = serializers.CharField(
        source="student.student_profile.roll_number", read_only=True
    )
    exam_title = serializers.CharField(source="exam.title", read_only=True)
    exam_date = serializers.DateField(source="exam.date", read_only=True)
    entered_by_name = serializers.CharField(source="entered_by.get_full_name", read_only=True)

    class Meta:
        model = Score
        fields = [
            "id",
            "exam",
            "exam_title",
            "exam_date",
            "student",
            "student_name",
            "student_roll",
            "marks_obtained",
            "percentage",
            "grade",
            "is_passing",
            "is_eligible",
            "ineligibility_reason",
            "remarks",
            "entered_by",
            "entered_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["percentage", "grade", "is_passing", "created_at", "updated_at"]

    def validate_marks_obtained(self, value):
        """Validate marks are within exam max marks."""
        exam = self.initial_data.get("exam")
        if exam:
            exam_obj = Exam.objects.get(pk=exam)
            if value > exam_obj.max_marks:
                raise serializers.ValidationError(
                    f"Marks cannot exceed maximum marks ({exam_obj.max_marks})"
                )
        return value
