"""Routing for notification APIs."""

from django.urls import path

from sims.notifications.views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationPreferenceView,
    NotificationUnreadCountView,
)

app_name = "notifications_api"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path("mark-read/", NotificationMarkReadView.as_view(), name="mark_read"),
    path("preferences/", NotificationPreferenceView.as_view(), name="preferences"),
    path("unread-count/", NotificationUnreadCountView.as_view(), name="unread_count"),
]
