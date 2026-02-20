"""
Context processor for admin dashboard statistics
"""

from django.utils import timezone


def admin_stats_context(request):
    """
    Context processor that provides admin dashboard statistics
    """
    # Only add context for admin pages
    if not request.path.startswith("/admin/"):
        return {}

    try:
        from sims.users.models import User

        # Get statistics for the dashboard
        total_users = User.objects.filter(is_archived=False).count()
        total_pgs = User.objects.filter(role="pg", is_archived=False).count()
        total_supervisors = User.objects.filter(role="supervisor", is_archived=False).count()
        new_users_this_month = User.objects.filter(
            date_joined__month=timezone.now().month,
            date_joined__year=timezone.now().year,
            is_archived=False,
        ).count()

        return {
            "total_users": total_users,
            "total_pgs": total_pgs,
            "total_supervisors": total_supervisors,
            "new_users_this_month": new_users_this_month,
        }
    except Exception:
        return {
            "total_users": 0,
            "total_pgs": 0,
            "total_supervisors": 0,
            "new_users_this_month": 0,
        }
