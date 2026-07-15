from django.contrib.auth import get_user_model
from rest_framework import serializers

from sims.academics.models import Department, Specialty, Designation, AcademicSession
from sims.academics.serializers import DepartmentSerializer as CanonicalDepartmentSerializer
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    DepartmentMembership,
    HospitalAssignment,
    AdminProfile,
    ResidentProfile,
    SupervisorProfile,
    SupportStaffProfile,
)

User = get_user_model()


class UserRefSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "role", "is_active"]


class DepartmentRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "code", "active"]


class HospitalSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = Hospital
        fields = ["id", "name", "code", "active", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class HospitalDepartmentSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    department = CanonicalDepartmentSerializer(read_only=True)
    hospital_id = serializers.IntegerField(write_only=True)
    department_id = serializers.IntegerField(write_only=True)
    active = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = HospitalDepartment
        fields = [
            "id",
            "hospital",
            "department",
            "hospital_id",
            "department_id",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return HospitalDepartment.objects.create(
            hospital_id=validated_data.pop("hospital_id"),
            department_id=validated_data.pop("department_id"),
            **validated_data,
        )

    def update(self, instance, validated_data):
        if "hospital_id" in validated_data:
            instance.hospital_id = validated_data.pop("hospital_id")
        if "department_id" in validated_data:
            instance.department_id = validated_data.pop("department_id")
        return super().update(instance, validated_data)


class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = AdminProfile
        fields = [
            "id",
            "user",
            "user_id",
            "designation",
            "phone",
            "email",
            "admin_scope",
            "profile_status",
            "profile_schema_version",
            "completed_schema_version",
            "profile_completed_at",
            "extra_data",
        ]
        read_only_fields = ["id", "profile_status", "profile_schema_version", "completed_schema_version", "profile_completed_at"]


class ResidentProfileSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    academic_session_ref = serializers.SlugRelatedField(
        slug_field="code", queryset=AcademicSession.objects.all(), required=False, allow_null=True
    )
    specialty_ref = serializers.SlugRelatedField(
        slug_field="code", queryset=Specialty.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ResidentProfile
        fields = [
            "id",
            "user",
            "user_id",
            "registration_no",
            "cnic",
            "phone",
            "email",
            "hospital",
            "department_ref",
            "program_ref",
            "academic_session_ref",
            "specialty_ref",
            "profile_status",
            "profile_schema_version",
            "completed_schema_version",
            "profile_completed_at",
            "extra_data",
            "is_archived",
        ]
        read_only_fields = ["id", "profile_status", "profile_schema_version", "completed_schema_version", "profile_completed_at"]


class SupervisorProfileSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    designation_ref = serializers.SlugRelatedField(
        slug_field="code", queryset=Designation.objects.all(), required=False, allow_null=True
    )
    specialty_ref = serializers.SlugRelatedField(
        slug_field="code", queryset=Specialty.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = SupervisorProfile
        fields = [
            "id",
            "user",
            "user_id",
            "pmdc_no",
            "official_email",
            "phone",
            "email",
            "hospital",
            "department_ref",
            "designation_ref",
            "program_ref",
            "specialty_ref",
            "profile_status",
            "profile_schema_version",
            "completed_schema_version",
            "profile_completed_at",
            "extra_data",
            "is_archived",
        ]
        read_only_fields = ["id", "profile_status", "profile_schema_version", "completed_schema_version", "profile_completed_at"]


class SupportStaffProfileSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = SupportStaffProfile
        fields = [
            "id",
            "user",
            "user_id",
            "designation",
            "department_ref",
            "hospital",
            "phone",
            "email",
            "scope_notes",
            "profile_status",
            "profile_schema_version",
            "completed_schema_version",
            "profile_completed_at",
            "extra_data",
            "is_archived",
        ]
        read_only_fields = ["id", "profile_status", "profile_schema_version", "completed_schema_version", "profile_completed_at"]


# Backward compatibility alias
class StaffProfileSerializer(SupervisorProfileSerializer):
    pass


class UserManagementSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    
    admin_profile = AdminProfileSerializer(read_only=True)
    resident_profile = ResidentProfileSerializer(read_only=True)
    supervisor_profile = SupervisorProfileSerializer(read_only=True)
    support_staff_profile = SupportStaffProfileSerializer(read_only=True)
    
    departments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "specialty",
            "year",
            "is_active",
            "supervisor",
            "home_department",
            "home_hospital",
            "registration_number",
            "phone_number",
            "admin_profile",
            "resident_profile",
            "supervisor_profile",
            "support_staff_profile",
            "departments",
            "date_joined",
            "must_change_password",
            "is_profile_complete",
        ]
        read_only_fields = ["date_joined"]

    def get_departments(self, obj) -> list[dict]:
        memberships = (
            obj.department_memberships.filter(active=True)
            .select_related("department")
            .order_by("-is_primary", "department__name")
        )
        return [
            {
                "id": membership.department_id,
                "name": membership.department.name,
                "code": membership.department.code,
                "member_type": membership.member_type,
                "is_primary": membership.is_primary,
            }
            for membership in memberships
        ]


class DepartmentMembershipSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    department = DepartmentRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    department_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = DepartmentMembership
        fields = [
            "id",
            "user",
            "department",
            "user_id",
            "department_id",
            "member_type",
            "is_primary",
            "active",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return DepartmentMembership.objects.create(
            user_id=validated_data.pop("user_id"),
            department_id=validated_data.pop("department_id"),
            **validated_data,
        )

    def update(self, instance, validated_data):
        validated_data.pop("user_id", None)
        validated_data.pop("department_id", None)
        return super().update(instance, validated_data)


class HospitalAssignmentSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    hospital_department_id = serializers.IntegerField(write_only=True)
    hospital_department = HospitalDepartmentSerializer(read_only=True)

    class Meta:
        model = HospitalAssignment
        fields = [
            "id",
            "user",
            "user_id",
            "hospital_department",
            "hospital_department_id",
            "assignment_type",
            "start_date",
            "end_date",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return HospitalAssignment.objects.create(
            user_id=validated_data.pop("user_id"),
            hospital_department_id=validated_data.pop("hospital_department_id"),
            **validated_data,
        )

    def update(self, instance, validated_data):
        validated_data.pop("user_id", None)
        validated_data.pop("hospital_department_id", None)
        return super().update(instance, validated_data)
