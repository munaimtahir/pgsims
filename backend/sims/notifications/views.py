"""API views for notification centre."""

from __future__ import annotations

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.notifications.models import Notification, NotificationPreference
from sims.notifications.serializers import (
    NotificationMarkReadSerializer,
    NotificationPreferenceSerializer,
    NotificationSerializer,
)


class NotificationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user).select_related("actor")
        
        # Support filtering by is_read via query parameter
        # is_read=True means read_at is not null, is_read=False means read_at is null
        is_read_param = self.request.query_params.get("is_read")
        if is_read_param is not None:
            try:
                is_read_bool = is_read_param.lower() in ("true", "1", "yes")
                if is_read_bool:
                    # Filter for read notifications (read_at is not null)
                    queryset = queryset.exclude(read_at__isnull=True)
                else:
                    # Filter for unread notifications (read_at is null)
                    queryset = queryset.filter(read_at__isnull=True)
            except (ValueError, AttributeError):
                # Invalid parameter, ignore filter
                pass
        
        return queryset


class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = NotificationMarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data["notification_ids"]
        queryset = Notification.objects.filter(recipient=request.user, pk__in=ids)
        updated = queryset.update(read_at=timezone.now())
        return Response({"marked": updated}, status=status.HTTP_200_OK)


class NotificationPreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        preference = NotificationPreference.for_user(request.user)
        serializer = NotificationPreferenceSerializer(preference)
        return Response(serializer.data)

    def patch(self, request: Request) -> Response:
        preference = NotificationPreference.for_user(request.user)
        serializer = NotificationPreferenceSerializer(preference, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class NotificationUnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        count = Notification.objects.filter(recipient=request.user, read_at__isnull=True).count()
        return Response({"unread": count})


__all__ = [
    "NotificationListView",
    "NotificationMarkReadView",
    "NotificationPreferenceView",
    "NotificationUnreadCountView",
]
