"""
Serializers for User model and authentication.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for profile display."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)
    display_name = serializers.CharField(source="get_display_name", read_only=True)
    profile_completed = serializers.SerializerMethodField()
    login_generated = serializers.SerializerMethodField()
    login_issued = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "display_name",
            "role",
            "specialty",
            "year",
            "registration_number",
            "cnic",
            "phone_number",
            "force_password_change",
            "profile_completed",
            "login_generated",
            "login_issued",
            "date_joined",
            "is_active",
        ]
        read_only_fields = ["id", "date_joined", "full_name", "display_name"]

    def _resident_profile(self, obj):
        return getattr(obj, "resident_profile", None)

    def get_profile_completed(self, obj) -> bool:
        profile = self._resident_profile(obj)
        return bool(profile.profile_completed) if profile else True

    def get_login_generated(self, obj) -> bool:
        profile = self._resident_profile(obj)
        return bool(profile.login_generated) if profile else False

    def get_login_issued(self, obj) -> bool:
        profile = self._resident_profile(obj)
        return bool(profile.login_issued) if profile else False


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "role",
            "specialty",
            "year",
            "supervisor",
            "registration_number",
            "phone_number",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "role": {"required": True},
        }

    def validate(self, attrs):
        """Validate registration data."""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Role-specific validation
        role = attrs.get("role")

        if role == "pg":
            if not attrs.get("specialty"):
                raise serializers.ValidationError(
                    {"specialty": "Specialty is required for PG students"}
                )
            if not attrs.get("year"):
                raise serializers.ValidationError({"year": "Year is required for PG students"})
            if not attrs.get("supervisor"):
                raise serializers.ValidationError(
                    {"supervisor": "Supervisor is required for PG students"}
                )

        elif role == "supervisor":
            if not attrs.get("specialty"):
                raise serializers.ValidationError(
                    {"specialty": "Specialty is required for supervisors"}
                )

        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop("password2")
        password = validated_data.pop("password")

        return User.objects.create_user(password=password, **validated_data)


class UserDetailSerializer(UserSerializer):
    """Extended user serializer with more details."""

    supervisor_name = serializers.CharField(source="supervisor.get_full_name", read_only=True)
    assigned_pgs_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "supervisor",
            "supervisor_name",
            "bio",
            "profile_picture",
            "qualifications",
            "institution",
            "is_archived",
            "assigned_pgs_count",
        ]

    def get_assigned_pgs_count(self, obj):
        """Get count of assigned PG students for supervisors."""
        if obj.role == "supervisor":
            return obj.assigned_pgs.filter(is_active=True, is_archived=False).count()
        return 0


class AssignedPGSerializer(serializers.ModelSerializer):
    """Minimal serializer for supervisor-assigned PGs."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "specialty",
            "year",
            "is_active",
        ]
