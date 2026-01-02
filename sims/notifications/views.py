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
        return Notification.objects.filter(recipient=user).select_related("actor")


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
