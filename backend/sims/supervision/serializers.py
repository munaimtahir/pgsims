from rest_framework import serializers
from sims.users.models import ResidentProfile, SupervisorProfile
from .models import ResidentSupervisorAssignment


class ResidentSummarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.get_full_name")
    username = serializers.CharField(source="user.username")
    department = serializers.CharField(source="department_ref.name", default="")
    training_site = serializers.CharField(source="hospital.name", default="")

    class Meta:
        model = ResidentProfile
        fields = ["id", "name", "username", "department", "training_site"]


class SupervisorSummarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.get_full_name")
    department = serializers.CharField(source="department_ref.name", default="")
    training_site = serializers.CharField(source="hospital.name", default="")
    designation = serializers.CharField(source="designation_ref.name", default="")

    class Meta:
        model = SupervisorProfile
        fields = ["id", "name", "department", "training_site", "designation"]


class ResidentSupervisorAssignmentSerializer(serializers.ModelSerializer):
    resident_id = serializers.PrimaryKeyRelatedField(
        queryset=ResidentProfile.objects.all(),
        source="resident",
        write_only=True,
    )
    supervisor_id = serializers.PrimaryKeyRelatedField(
        queryset=SupervisorProfile.objects.all(),
        source="supervisor",
        write_only=True,
    )
    resident = ResidentSummarySerializer(read_only=True)
    supervisor = SupervisorSummarySerializer(read_only=True)

    class Meta:
        model = ResidentSupervisorAssignment
        fields = [
            "id",
            "resident_id",
            "supervisor_id",
            "resident",
            "supervisor",
            "assignment_type",
            "status",
            "is_active",
            "start_date",
            "end_date",
            "notes",
            "reason_for_change",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        ]
