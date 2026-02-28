"""Serializers for userbase/org graph APIs."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    DepartmentMembership,
    HODAssignment,
    HospitalAssignment,
    ResidentProfile,
    StaffProfile,
    SupervisorResidentLink,
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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "code", "description", "active", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class HospitalDepartmentSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
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


class UserManagementSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    resident_profile = serializers.JSONField(write_only=True, required=False)
    staff_profile = serializers.JSONField(write_only=True, required=False)
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
            "resident_profile",
            "staff_profile",
            "departments",
            "date_joined",
        ]
        read_only_fields = ["date_joined"]

    def get_departments(self, obj):
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

    def _upsert_profiles(self, user, resident_payload, staff_payload):
        if resident_payload and user.role in {"pg", "resident"}:
            existing = ResidentProfile.objects.filter(user=user).first()
            training_start = resident_payload.get(
                "training_start",
                existing.training_start if existing else None,
            )
            if not training_start:
                raise serializers.ValidationError(
                    {"resident_profile": "training_start is required for resident profile."}
                )
            defaults = {
                "pgr_id": resident_payload.get("pgr_id", ""),
                "training_start": training_start,
                "training_end": resident_payload.get("training_end"),
                "training_level": resident_payload.get("training_level", ""),
                "active": resident_payload.get("active", True),
            }
            ResidentProfile.objects.update_or_create(user=user, defaults=defaults)
        if staff_payload and user.role in {"supervisor", "faculty"}:
            defaults = {
                "designation": staff_payload.get("designation", ""),
                "phone": staff_payload.get("phone", ""),
                "active": staff_payload.get("active", True),
            }
            StaffProfile.objects.update_or_create(user=user, defaults=defaults)

    def create(self, validated_data):
        resident_payload = validated_data.pop("resident_profile", None)
        staff_payload = validated_data.pop("staff_profile", None)
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        self._upsert_profiles(user, resident_payload, staff_payload)
        return user

    def update(self, instance, validated_data):
        resident_payload = validated_data.pop("resident_profile", None)
        staff_payload = validated_data.pop("staff_profile", None)
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        self._upsert_profiles(instance, resident_payload, staff_payload)
        return instance


class ResidentProfileSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ResidentProfile
        fields = [
            "id",
            "user",
            "user_id",
            "pgr_id",
            "training_start",
            "training_end",
            "training_level",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        if "user_id" in validated_data:
            validated_data["user_id"] = validated_data.pop("user_id")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("user_id", None)
        return super().update(instance, validated_data)


class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserRefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = StaffProfile
        fields = [
            "id",
            "user",
            "user_id",
            "designation",
            "phone",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        if "user_id" in validated_data:
            validated_data["user_id"] = validated_data.pop("user_id")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("user_id", None)
        return super().update(instance, validated_data)


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


class SupervisorResidentLinkSerializer(serializers.ModelSerializer):
    supervisor_user = UserRefSerializer(read_only=True)
    resident_user = UserRefSerializer(read_only=True)
    department = DepartmentRefSerializer(read_only=True)
    supervisor_user_id = serializers.IntegerField(write_only=True)
    resident_user_id = serializers.IntegerField(write_only=True)
    department_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = SupervisorResidentLink
        fields = [
            "id",
            "supervisor_user",
            "resident_user",
            "department",
            "supervisor_user_id",
            "resident_user_id",
            "department_id",
            "start_date",
            "end_date",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return SupervisorResidentLink.objects.create(
            supervisor_user_id=validated_data.pop("supervisor_user_id"),
            resident_user_id=validated_data.pop("resident_user_id"),
            department_id=validated_data.pop("department_id", None),
            **validated_data,
        )

    def update(self, instance, validated_data):
        validated_data.pop("supervisor_user_id", None)
        validated_data.pop("resident_user_id", None)
        validated_data.pop("department_id", None)
        return super().update(instance, validated_data)


class HODAssignmentSerializer(serializers.ModelSerializer):
    department = DepartmentRefSerializer(read_only=True)
    hod_user = UserRefSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    hod_user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = HODAssignment
        fields = [
            "id",
            "department",
            "hod_user",
            "department_id",
            "hod_user_id",
            "start_date",
            "end_date",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        return HODAssignment.objects.create(
            department_id=validated_data.pop("department_id"),
            hod_user_id=validated_data.pop("hod_user_id"),
            **validated_data,
        )

    def update(self, instance, validated_data):
        validated_data.pop("department_id", None)
        validated_data.pop("hod_user_id", None)
        return super().update(instance, validated_data)
