"""
JWT Authentication API endpoints for SIMS.

Provides:
- Register (create new user)
- Login (obtain JWT tokens)
- Refresh (refresh access token)
- Logout (optional, client-side token removal)
- Password reset flow
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer


class LoginRateThrottle(AnonRateThrottle):
    """Custom throttle for login attempts - 5 per minute by default."""

    rate = settings.LOGIN_RATE_LIMIT


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer to include user data in token response."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["role"] = user.role
        token["full_name"] = user.get_full_name()

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user data to response
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "full_name": self.user.get_full_name(),
        }

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with extended user data and rate limiting."""

    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user.

    POST /api/auth/register/
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "password2": "string",
        "first_name": "string",
        "last_name": "string",
        "role": "pg|supervisor|admin"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout (blacklist refresh token if implemented).

    POST /api/auth/logout/
    {
        "refresh": "refresh_token_string"
    }
    """
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            # Note: Blacklisting requires rest_framework_simplejwt.token_blacklist
            # which is not enabled by default
            # token.blacklist()

        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Get current user's profile.

    GET /api/auth/profile/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Update current user's profile.

    PUT/PATCH /api/auth/profile/
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_request_view(request):
    """
    Request password reset email.

    POST /api/auth/password-reset/
    {
        "email": "user@example.com"
    }
    """
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        # Generate reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Create reset URL (adjust for your frontend)
        reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"

        # Send email
        subject = "Password Reset Request - SIMS"
        message = f"""
        Hello {user.get_full_name()},

        You requested a password reset for your SIMS account.

        Please click the link below to reset your password:
        {reset_url}

        If you did not request this reset, please ignore this email.

        This link will expire in 24 hours.

        Best regards,
        SIMS Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        # Don't reveal if user exists or not (security best practice)
        return Response(
            {
                "message": "If an account with that email exists, a password reset email has been sent"
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"error": "Failed to send reset email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm_view(request):
    """
    Confirm password reset with token.

    POST /api/auth/password-reset/confirm/
    {
        "uid": "encoded_user_id",
        "token": "reset_token",
        "new_password": "new_password",
        "new_password2": "new_password"
    }
    """
    uid = request.data.get("uid")
    token = request.data.get("token")
    new_password = request.data.get("new_password")
    new_password2 = request.data.get("new_password2")

    if not all([uid, token, new_password, new_password2]):
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != new_password2:
        return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Decode user ID
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)

        # Validate token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid or expired reset token"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

    except (User.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Change password for authenticated user.

    POST /api/auth/change-password/
    {
        "old_password": "current_password",
        "new_password": "new_password",
        "new_password2": "new_password"
    }
    """
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    new_password2 = request.data.get("new_password2")

    if not all([old_password, new_password, new_password2]):
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response(
            {"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != new_password2:
        return Response({"error": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
