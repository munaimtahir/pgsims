"""
Custom Admin Configuration for SIMS
Provides enhanced admin dashboard with statistics
"""

from django.contrib.admin import AdminSite
from django.utils import timezone

from sims.users.models import User


class SIMSAdminSite(AdminSite):
    """Custom admin site for SIMS with enhanced dashboard"""

    site_header = "SIMS Administration"
    site_title = "SIMS Admin"
    index_title = "SIMS Administration Dashboard"

    def index(self, request, extra_context=None):
        """
        Custom admin index view with dashboard statistics
        """
        extra_context = extra_context or {}

        # Get statistics for the dashboard
        try:
            total_users = User.objects.filter(is_archived=False).count()
            total_pgs = User.objects.filter(role="pg", is_archived=False).count()
            total_supervisors = User.objects.filter(role="supervisor", is_archived=False).count()
            new_users_this_month = User.objects.filter(
                date_joined__month=timezone.now().month,
                date_joined__year=timezone.now().year,
                is_archived=False,
            ).count()
        except Exception as e:
            print(f"Error getting admin stats: {e}")
            total_users = 0
            total_pgs = 0
            total_supervisors = 0
            new_users_this_month = 0

        # Add statistics to context
        extra_context.update(
            {
                "total_users": total_users,
                "total_pgs": total_pgs,
                "total_supervisors": total_supervisors,
                "new_users_this_month": new_users_this_month,
                "system_status": "online",
                "debug": settings.DEBUG if "settings" in globals() else False,
            }
        )

        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = SIMSAdminSite(name="admin")

# Import settings for debug check
try:
    from django.conf import settings
except ImportError:
    pass
