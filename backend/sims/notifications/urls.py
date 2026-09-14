"""Routing for notification APIs."""

from django.urls import path

from sims.notifications.views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkUnreadView,
    NotificationPreferenceView,
    NotificationUnreadCountView,
    MobileDeviceRegistrationView,
)

app_name = "notifications_api"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path("mark-read/", NotificationMarkReadView.as_view(), name="mark_read"),
    path("mark-unread/", NotificationMarkUnreadView.as_view(), name="mark_unread"),
    path("preferences/", NotificationPreferenceView.as_view(), name="preferences"),
    path("unread-count/", NotificationUnreadCountView.as_view(), name="unread_count"),
    path("devices/", MobileDeviceRegistrationView.as_view(), name="devices"),
]
