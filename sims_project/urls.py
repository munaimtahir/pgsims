"""
URL configuration for sims_project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

SIMS - Postgraduate Medical Training System
Created: 2025-05-29 16:10:53 UTC
Author: SMIB2012
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import include, path

# Import health check views
from sims_project.health import healthz, liveness, readiness


# Custom admin logout view that handles GET requests
def admin_logout_view(request):
    """Custom admin logout that handles GET requests"""
    from django.contrib.admin import site
    from django.contrib.auth import logout

    if request.user.is_authenticated:
        logout(request)

    # Redirect to admin login page
    return redirect("/admin/")


def home_view(request):
    """
    Home page view - redirects authenticated users to dashboard,
    shows landing page for anonymous users
    """
    if request.user.is_authenticated:
        return redirect("users:dashboard")

    # Render the homepage template with context
    context = {
        "system_version": "2.1.0",
        "university_name": "Faisalabad Medical University",
        "current_year": "2025",
        "system_status": "online",
    }
    return TemplateResponse(request, "home/index.html", context)


def health_check(request):
    """Simple health check endpoint for monitoring"""
    return HttpResponse("OK", content_type="text/plain")


def robots_txt(request):
    """Robots.txt for SEO"""
    content = """User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /media/private/
Allow: /
"""
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    # Home and utility URLs
    path("", home_view, name="home"),
    path("health/", health_check, name="health_check"),
    path("healthz/", healthz, name="healthz"),
    path("readiness/", readiness, name="readiness"),
    path("liveness/", liveness, name="liveness"),
    path("robots.txt", robots_txt, name="robots_txt"),
    # Custom admin logout URL (must come before admin/ URL)
    path("admin/logout/", admin_logout_view, name="admin_logout"),
    # Django Admin
    path("admin/", admin.site.urls),
    # SIMS App URLs
    path("users/", include("sims.users.urls")),
    path("rotations/", include("sims.rotations.urls")),
    path("certificates/", include("sims.certificates.urls")),
    path("logbook/", include("sims.logbook.urls")),
    path("cases/", include("sims.cases.urls")),
    path("api/audit/", include("sims.audit.urls")),
    path("api/search/", include("sims.search.urls")),
    path("api/analytics/", include("sims.analytics.urls")),
    path("api/bulk/", include("sims.bulk.urls")),
    path("api/notifications/", include("sims.notifications.urls")),
    path("api/reports/", include("sims.reports.urls")),
    path("api/logbook/", include("sims.logbook.api_urls")),
    path("api/attendance/", include("sims.attendance.urls")),
    # New apps
    path("academics/", include("sims.academics.urls")),
    path("results/", include("sims.results.urls")),
    # JWT Authentication endpoints
    path("api/auth/", include("sims.users.api_urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = "SIMS Administration"
admin.site.site_title = "SIMS Admin"
admin.site.index_title = "Welcome to SIMS"
admin.site.site_url = "/"
admin.site.enable_nav_sidebar = True
