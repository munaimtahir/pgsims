from rest_framework import serializers
from .models import Department, Batch, StudentProfile


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source="head.get_full_name", read_only=True)

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "code",
            "description",
            "head",
            "head_name",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class BatchSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    coordinator_name = serializers.CharField(source="coordinator.get_full_name", read_only=True)
    current_strength = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)

    class Meta:
        model = Batch
        fields = [
            "id",
            "name",
            "program",
            "department",
            "department_name",
            "start_date",
            "end_date",
            "coordinator",
            "coordinator_name",
            "capacity",
            "current_strength",
            "is_full",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "current_strength", "is_full"]

    def validate(self, data):
        """Validate batch dates."""
        if data.get("start_date") and data.get("end_date"):
            if data["start_date"] >= data["end_date"]:
                raise serializers.ValidationError("End date must be after start date")
        return data


class StudentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    batch_name = serializers.CharField(source="batch.name", read_only=True)
    department_name = serializers.CharField(source="batch.department.name", read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    duration = serializers.IntegerField(source="duration_in_program", read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "batch",
            "batch_name",
            "department_name",
            "roll_number",
            "admission_date",
            "expected_graduation_date",
            "actual_graduation_date",
            "status",
            "status_updated_at",
            "cgpa",
            "previous_institution",
            "previous_qualification",
            "emergency_contact_name",
            "emergency_contact_phone",
            "emergency_contact_relation",
            "remarks",
            "is_active",
            "duration",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "status_updated_at",
            "is_active",
            "duration",
        ]
