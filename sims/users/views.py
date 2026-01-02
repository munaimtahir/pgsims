import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, View

from .decorators import (
    AdminRequiredMixin,
    PGRequiredMixin,
    SupervisorOrAdminRequiredMixin,
    SupervisorRequiredMixin,
    admin_required,
    pg_required,
    supervisor_or_admin_required,
    supervisor_required,
)
from .forms import PGSearchForm, SupervisorAssignmentForm, UserProfileForm
from .models import User


# Authentication Views
def login_view(request):
    """Custom login view with role-based redirection"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and not user.is_archived:
                login(request, user)

                # Role-based redirection
                if user.is_admin():
                    messages.success(request, f"Welcome back, Admin {user.get_display_name()}!")
                    return redirect("admin:index")
                elif user.is_supervisor():
                    messages.success(request, f"Welcome back, Dr. {user.get_display_name()}!")
                    return redirect("users:supervisor_dashboard")
                elif user.is_pg():
                    messages.success(request, f"Welcome back, {user.get_display_name()}!")
                    return redirect("users:pg_dashboard")
                else:
                    return redirect("users:profile")
            else:
                messages.error(request, "Your account is inactive. Please contact admin.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")


def logout_view(request):
    """Custom logout view with PMC themed template"""
    user_name = None
    user_role = None

    # Handle both GET and POST requests
    if request.method in ["GET", "POST"]:
        # Get user info before logout if authenticated
        if request.user.is_authenticated:
            user_name = request.user.get_display_name()
            user_role = request.user.role
            logout(request)

        # Context for template
        context = {"user_name": user_name, "user_role": user_role, "logout_time": timezone.now()}

        return render(request, "users/logged_out.html", context)

    # If somehow other method, redirect to login
    return redirect("users:login")


# Dashboard Views (Note: Admin dashboard now redirects to Django admin)


@supervisor_required
def supervisor_dashboard(request):
    """Supervisor dashboard with assigned PGs overview"""

    # Get assigned PGs
    assigned_pgs = request.user.get_assigned_pgs()

    # Get pending documents count
    pending_count = request.user.get_documents_pending_count()

    # Recent submissions from assigned PGs
    # Import here to avoid circular imports

    recent_submissions = []

    # Get recent activity from all assigned PGs
    for pg in assigned_pgs:
        # You can add logic here to get recent submissions
        pass

    context = {
        "assigned_pgs": assigned_pgs,
        "assigned_pgs_count": assigned_pgs.count(),
        "pending_documents": pending_count,
        "recent_submissions": recent_submissions[:10],
        "dashboard_type": "supervisor",
    }
    return render(request, "users/supervisor_dashboard.html", context)


@pg_required
def pg_dashboard(request):
    """PG dashboard with personal progress overview"""

    # Get supervisor info
    supervisor = request.user.supervisor

    # Get recent submissions
    recent_submissions = []

    # Get progress statistics
    # Import here to avoid circular imports
    try:
        from sims.certificates.models import Certificate

        certificates_count = Certificate.objects.filter(pg=request.user).count()
    except Exception:
        certificates_count = 0

    try:
        from sims.rotations.models import Rotation

        rotations_count = Rotation.objects.filter(pg=request.user).count()
    except Exception:
        rotations_count = 0

    try:
        from sims.logbook.models import LogbookEntry

        logbook_entries_count = LogbookEntry.objects.filter(pg=request.user).count()
    except Exception:
        logbook_entries_count = 0

    try:
        from sims.cases.models import ClinicalCase

        clinical_cases_count = ClinicalCase.objects.filter(pg=request.user).count()
    except Exception:
        clinical_cases_count = 0

    progress_stats = {
        "certificates": certificates_count,
        "rotations": rotations_count,
        "logbook_entries": logbook_entries_count,
        "clinical_cases": clinical_cases_count,
    }

    # Calculate documents submitted (sum of all submissions)
    documents_submitted = sum(progress_stats.values())

    context = {
        "documents_submitted": documents_submitted,
        "supervisor": supervisor,
        "recent_submissions": recent_submissions[:10],
        "progress_stats": progress_stats,
        "dashboard_type": "pg",
    }
    return render(request, "users/pg_dashboard.html", context)


class DashboardRedirectView(LoginRequiredMixin, View):
    """Redirect users to appropriate dashboard based on their role"""

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin():
            return redirect("admin:index")
        elif user.is_supervisor():
            return redirect("users:supervisor_dashboard")
        elif user.is_pg():
            return redirect("users:pg_dashboard")
        else:
            return redirect("users:profile")


class AdminDashboardView(AdminRequiredMixin, View):
    """Admin dashboard class-based view - redirects to Django admin"""

    def get(self, request, *args, **kwargs):
        return redirect("admin:index")


class SupervisorDashboardView(SupervisorRequiredMixin, View):
    """Supervisor dashboard class-based view"""

    def get(self, request, *args, **kwargs):
        return supervisor_dashboard(request)


class PGDashboardView(PGRequiredMixin, View):
    """PG dashboard class-based view"""

    def get(self, request, *args, **kwargs):
        return pg_dashboard(request)


# Profile Views
class ProfileView(LoginRequiredMixin, DetailView):
    """User's own profile view"""

    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self):
        return self.request.user


class ProfileDetailView(SupervisorOrAdminRequiredMixin, DetailView):
    """View another user's profile (admin/supervisor only)"""

    model = User
    template_name = "users/profile_detail.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Add recent activities if needed
        try:
            recent_activities = []
            # Add logbook entries as activities
            for entry in user.logbook_entries.all()[:3]:
                recent_activities.append(
                    {
                        "icon": "book",
                        "color": "primary",
                        "description": f"Created logbook entry: {entry.case_title}",
                        "created_at": entry.created_at,
                    }
                )

            # Add cases as activities
            for case in user.cases.all()[:2]:
                recent_activities.append(
                    {
                        "icon": "folder",
                        "color": "success",
                        "description": f"Added case: {case.case_title}",
                        "created_at": case.created_at,
                    }
                )

            # Sort by date
            recent_activities = sorted(
                recent_activities, key=lambda x: x["created_at"], reverse=True
            )[:5]
            context["recent_activities"] = recent_activities
        except Exception:
            context["recent_activities"] = []

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user's own profile"""

    model = User
    form_class = UserProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user


# User Management Views (Admin only)
class UserListView(AdminRequiredMixin, ListView):
    """List all users (admin only)"""

    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        return User.objects.filter(is_archived=False).order_by("last_name", "first_name")


class UserCreateView(AdminRequiredMixin, View):
    """Create new user (admin only)"""

    def get(self, request):
        return render(request, "users/user_create.html")

    def post(self, request):
        try:
            # Get form data
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            role = request.POST.get("role", "").strip()
            specialty = request.POST.get("specialty", "").strip()
            year = request.POST.get("year", "").strip()
            phone_number = request.POST.get("phone_number", "").strip()
            registration_number = request.POST.get("registration_number", "").strip()
            password1 = request.POST.get("password1", "").strip()
            password2 = request.POST.get("password2", "").strip()
            supervisor_id = request.POST.get("supervisor_choice", "").strip()

            # Also check for 'supervisor' field as backup
            if not supervisor_id:
                supervisor_id = request.POST.get("supervisor", "").strip()

            # Validation
            errors = []

            if not username:
                errors.append("Username is required")
            elif User.objects.filter(username=username).exists():
                errors.append("Username already exists")

            if not email:
                errors.append("Email is required")
            elif User.objects.filter(email=email).exists():
                errors.append("Email already exists")

            if not first_name:
                errors.append("First name is required")

            if not last_name:
                errors.append("Last name is required")

            if not role:
                errors.append("Role is required")

            if not password1:
                errors.append("Password is required")
            elif password1 != password2:
                errors.append("Passwords do not match")
            elif len(password1) < 8:
                errors.append("Password must be at least 8 characters")

            # Role-specific validation
            if role in ["pg", "supervisor"] and not specialty:
                errors.append("Specialty is required for PGs and Supervisors")

            if role == "pg":
                if not year:
                    errors.append("Year is required for PGs")
                if not supervisor_id:
                    errors.append("Supervisor is required for PGs")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, "users/user_create.html")

            # Create user
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role,
                specialty=specialty if role in ["pg", "supervisor"] else None,
                year=year if role == "pg" else None,
                phone_number=phone_number,
                registration_number=registration_number,
                is_active=True,
            )

            # Set supervisor for PG users
            if role == "pg" and supervisor_id:
                try:
                    supervisor = User.objects.get(id=supervisor_id, role="supervisor")
                    user.supervisor = supervisor
                except User.DoesNotExist:
                    messages.error(request, "Selected supervisor not found")
                    return render(request, "users/user_create.html")

            user.set_password(password1)
            user.save()

            messages.success(request, f"User {user.get_display_name()} created successfully!")
            return redirect("users:user_list")

        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return render(request, "users/user_create.html")


class UserEditView(AdminRequiredMixin, UpdateView):
    """Edit user (admin only)"""

    model = User
    fields = [
        "first_name",
        "last_name",
        "email",
        "role",
        "specialty",
        "year",
        "supervisor",
        "is_active",
        "phone_number",
        "registration_number",
    ]
    template_name = "users/user_edit.html"

    def get_success_url(self):
        return reverse("users:profile_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit User - {self.object.get_full_name()}"

        # Customize supervisor field queryset to show only active supervisors
        if "form" in context:
            form = context["form"]
            if "supervisor" in form.fields:
                form.fields["supervisor"].queryset = User.objects.filter(
                    role="supervisor", is_active=True
                ).order_by("first_name", "last_name")
                form.fields["supervisor"].empty_label = "No Supervisor (for Supervisors/Admins)"

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            f"User profile for {self.object.get_full_name()} has been updated successfully.",
        )
        return super().form_valid(form)


class UserDeleteView(AdminRequiredMixin, View):
    """Archive user (admin only)"""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_archived = True
        user.save()
        messages.success(request, f"User {user.get_display_name()} has been archived.")
        return redirect("users:user_list")


class UserActivateView(AdminRequiredMixin, View):
    """Activate/deactivate user (admin only)"""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.get_display_name()} has been {status}.")
        return redirect("users:user_list")


class UserDeactivateView(AdminRequiredMixin, View):
    """Deactivate user (admin only)"""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_active:
            user.is_active = False
            user.save()
            messages.success(request, f"User {user.get_display_name()} has been deactivated.")
        else:
            messages.info(request, f"User {user.get_display_name()} is already deactivated.")
        return redirect("users:user_list")


class UserArchiveView(AdminRequiredMixin, View):
    """Archive user (admin only)"""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_archived = True
        user.save()
        messages.success(request, f"User {user.get_display_name()} has been archived.")
        return redirect("users:user_list")


# Supervisor Management Views
class SupervisorListView(AdminRequiredMixin, ListView):
    """List all supervisors (admin only)"""

    model = User
    template_name = "users/supervisor_list.html"
    context_object_name = "supervisors"

    def get_queryset(self):
        return User.objects.filter(role="supervisor", is_archived=False)


class SupervisorPGsView(LoginRequiredMixin, DetailView):
    """View supervisor's assigned PGs"""

    model = User
    template_name = "users/supervisor_pgs.html"
    context_object_name = "supervisor"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_admin() or request.user.pk == kwargs.get("pk")):
            raise PermissionDenied("Only admins or the supervisor themselves can view this")
        return super().dispatch(request, *args, **kwargs)


class AssignSupervisorView(AdminRequiredMixin, View):
    """Assign supervisor to PG (admin only)"""

    def get(self, request):
        form = SupervisorAssignmentForm()
        return render(request, "users/assign_supervisor.html", {"form": form})

    def post(self, request):
        form = SupervisorAssignmentForm(request.POST)
        if form.is_valid():
            # Implementation for supervisor assignment
            messages.success(request, "Supervisor assigned successfully.")
            return redirect("users:pg_list")
        return render(request, "users/assign_supervisor.html", {"form": form})


# PG Management Views
@supervisor_or_admin_required
@login_required
def pg_list_view(request):
    """List PGs for supervisors and admins"""

    # Check if user has the required role
    if not (request.user.is_supervisor() or request.user.is_admin()):
        raise PermissionDenied("You don't have permission to view this page.")

    if request.user.is_supervisor():
        # Supervisors see only their assigned PGs
        pgs = request.user.get_assigned_pgs()
    elif request.user.is_admin():
        # Admins see all PGs
        pgs = User.objects.filter(role="pg", is_archived=False)

    # Search functionality
    form = PGSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get("search")
        if search_query:
            pgs = pgs.filter(
                Q(first_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
                | Q(username__icontains=search_query)
            )

        specialty = form.cleaned_data.get("specialty")
        if specialty:
            pgs = pgs.filter(specialty=specialty)

        year = form.cleaned_data.get("year")
        if year:
            pgs = pgs.filter(year=year)

    paginator = Paginator(pgs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "form": form,
        "total_pgs": pgs.count(),
    }
    return render(request, "users/pg_list.html", context)


class PGListView(LoginRequiredMixin, View):
    """List PGs - class-based wrapper"""

    def get(self, request):
        return pg_list_view(request)


class PGBulkUploadView(AdminRequiredMixin, View):
    """Bulk upload PGs (admin only)"""

    def get(self, request):
        return render(request, "users/pg_bulk_upload.html")

    def post(self, request):
        # Implementation for bulk upload
        messages.success(request, "PGs uploaded successfully.")
        return redirect("users:pg_list")


class PGProgressView(LoginRequiredMixin, DetailView):
    """View PG's progress"""

    model = User
    template_name = "users/pg_progress.html"
    context_object_name = "pg_user"

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if not (
            request.user.is_admin() or request.user.is_supervisor() or request.user.pk == user.pk
        ):
            raise PermissionDenied("Access denied")
        return super().dispatch(request, *args, **kwargs)


# Reports and Analytics Views
class UserReportsView(AdminRequiredMixin, View):
    """User reports (admin only)"""

    def get(self, request):
        return render(request, "users/user_reports.html")


class UserExportView(AdminRequiredMixin, View):
    """Export user data (admin only)"""

    def get(self, request):
        # Implementation for data export
        return JsonResponse({"status": "success"})


class ActivityLogView(AdminRequiredMixin, ListView):
    """Activity log view (admin only)"""

    template_name = "users/activity_log.html"
    context_object_name = "activities"
    paginate_by = 50

    def get_queryset(self):
        # Placeholder - would need an ActivityLog model
        return []


# API Views
class UserSearchAPIView(LoginRequiredMixin, View):
    """Search users API"""

    def get(self, request):
        query = request.GET.get("q", "")
        users = User.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(username__icontains=query)
        )[:10]

        results = [{"id": user.id, "name": user.get_display_name()} for user in users]
        return JsonResponse({"results": results})


class SupervisorsBySpecialtyAPIView(LoginRequiredMixin, View):
    """Get supervisors by specialty API"""

    def get(self, request, specialty):
        supervisors = User.objects.filter(
            role="supervisor", specialty=specialty, is_active=True, is_archived=False
        )

        results = [{"id": sup.id, "name": sup.get_display_name()} for sup in supervisors]
        return JsonResponse({"supervisors": results})


class UserStatsAPIView(LoginRequiredMixin, View):
    """Get user statistics API"""

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # Check permissions
        if not (
            request.user.is_admin() or request.user.is_supervisor() or request.user.pk == user.pk
        ):
            return JsonResponse({"error": "Permission denied"}, status=403)

        stats = {
            "total_cases": 0,  # Would come from cases app
            "total_certificates": 0,  # Would come from certificates app
            "total_rotations": 0,  # Would come from rotations app
            "logbook_entries": 0,  # Would come from logbook app
            "overall_progress": 0,  # Calculate based on various metrics
        }

        return JsonResponse(stats)


class UserListStatsAPIView(LoginRequiredMixin, View):
    """Get user list statistics API for dashboard updates"""

    def get(self, request):
        # Check permissions - allow admin and supervisor access
        if not (request.user.is_admin() or request.user.is_supervisor()):
            return JsonResponse({"error": "Permission denied"}, status=403)

        # Get user counts
        total_users = User.objects.filter(is_archived=False).count()
        active_users = User.objects.filter(is_active=True, is_archived=False).count()
        pg_count = User.objects.filter(role="pg", is_archived=False).count()
        supervisor_count = User.objects.filter(role="supervisor", is_archived=False).count()

        # Get specialty count for PGs
        specialty_count = (
            User.objects.filter(role="pg", is_archived=False, specialty__isnull=False)
            .values("specialty")
            .distinct()
            .count()
        )

        # Get new users this month
        current_month_start = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        new_this_month = User.objects.filter(
            role="pg", is_archived=False, date_joined__gte=current_month_start
        ).count()

        stats = {
            "total_users": total_users,
            "active_users": active_users,
            "pg_count": pg_count,
            "supervisor_count": supervisor_count,
            "specialty_count": specialty_count,
            "new_this_month": new_this_month,
        }

        return JsonResponse(stats)


# Analytics Views
@admin_required
def admin_analytics_view(request):
    """Admin analytics with system-wide statistics"""

    # System overview stats
    total_users = User.objects.filter(is_archived=False).count()
    active_users = User.objects.filter(is_active=True, is_archived=False).count()
    total_pgs = User.objects.filter(role="pg", is_archived=False).count()
    total_supervisors = User.objects.filter(role="supervisor", is_archived=False).count()
    # Monthly user registration stats
    from django.db.models import Count

    # Specialty distribution
    specialty_distribution = (
        User.objects.filter(role__in=["pg", "supervisor"], is_archived=False)
        .values("specialty")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Convert to JSON for JavaScript consumption
    specialty_stats_json = json.dumps(
        [
            {"specialty": item["specialty"] or "Unspecified", "count": item["count"]}
            for item in specialty_distribution
        ]
    )

    # Progress tracking statistics
    context = {
        "total_users": total_users,
        "active_users": active_users,
        "total_pgs": total_pgs,
        "total_supervisors": total_supervisors,
        "specialty_distribution": list(specialty_distribution),
        "specialty_stats_json": specialty_stats_json,
        "analytics_type": "admin",
    }
    return render(request, "users/admin_analytics.html", context)


@supervisor_required
def supervisor_analytics_view(request):
    """Supervisor analytics with assigned PGs statistics"""

    # Get assigned PGs
    assigned_pgs = request.user.get_assigned_pgs()
    assigned_pgs_count = assigned_pgs.count()

    # PG progress statistics
    pg_progress_stats = []
    for pg in assigned_pgs:
        try:
            from sims.certificates.models import Certificate
            from sims.logbook.models import LogbookEntry
            from sims.rotations.models import Rotation

            pg_stats = {
                "pg": pg,
                "certificates": Certificate.objects.filter(pg=pg).count(),
                "logbook_entries": LogbookEntry.objects.filter(pg=pg).count(),
                "rotations": Rotation.objects.filter(pg=pg).count(),
                "completion_percentage": 0,  # Calculate based on requirements
            }
            pg_progress_stats.append(pg_stats)
        except ImportError:
            pg_stats = {
                "pg": pg,
                "certificates": 0,
                "logbook_entries": 0,
                "rotations": 0,
                "completion_percentage": 0,
            }
            pg_progress_stats.append(pg_stats)

    # Monthly progress data for assigned PGs
    from django.utils import timezone

    current_month = timezone.now().month
    current_year = timezone.now().year

    try:
        from sims.logbook.models import LogbookEntry

        monthly_entries = LogbookEntry.objects.filter(
            pg__in=assigned_pgs, created_at__month=current_month, created_at__year=current_year
        ).count()
    except ImportError:
        monthly_entries = 0

    try:
        from sims.certificates.models import Certificate

        monthly_certificates = Certificate.objects.filter(
            pg__in=assigned_pgs, created_at__month=current_month, created_at__year=current_year
        ).count()
    except ImportError:
        monthly_certificates = 0

    context = {
        "assigned_pgs_count": assigned_pgs_count,
        "pg_progress_stats": pg_progress_stats,
        "monthly_entries": monthly_entries,
        "monthly_certificates": monthly_certificates,
        "analytics_type": "supervisor",
    }
    return render(request, "users/supervisor_analytics.html", context)


@pg_required
def pg_analytics_view(request):
    """PG analytics with personal progress tracking"""

    # Personal progress statistics
    try:
        from sims.certificates.models import Certificate

        my_certificates = Certificate.objects.filter(pg=request.user).count()
        certificates_this_month = Certificate.objects.filter(
            pg=request.user,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        ).count()
    except ImportError:
        my_certificates = 0
        certificates_this_month = 0

    try:
        from sims.logbook.models import LogbookEntry

        my_logbook_entries = LogbookEntry.objects.filter(pg=request.user).count()
        entries_this_month = LogbookEntry.objects.filter(
            pg=request.user,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        ).count()

        # Monthly progress chart data (last 6 months)
        from datetime import timedelta

        six_months_ago = timezone.now().date() - timedelta(days=180)
        monthly_progress = (
            LogbookEntry.objects.filter(pg=request.user, created_at__date__gte=six_months_ago)
            .extra(select={"month": 'strftime("%%Y-%%m", created_at)'})
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

    except ImportError:
        my_logbook_entries = 0
        entries_this_month = 0
        monthly_progress = []

    try:
        from sims.rotations.models import Rotation

        my_rotations = Rotation.objects.filter(pg=request.user).count()
        completed_rotations = Rotation.objects.filter(pg=request.user, status="completed").count()
        current_rotation = Rotation.objects.filter(pg=request.user, status="active").first()
    except ImportError:
        my_rotations = 0
        completed_rotations = 0
        current_rotation = None

    try:
        from sims.cases.models import ClinicalCase

        my_cases = ClinicalCase.objects.filter(pg=request.user).count()
    except ImportError:
        my_cases = 0

    # Calculate overall completion percentage
    # This would be based on program requirements
    total_required = 100  # Placeholder - should come from program requirements
    completed = my_certificates + completed_rotations
    completion_percentage = (
        min((completed / total_required) * 100, 100) if total_required > 0 else 0
    )

    context = {
        "my_certificates": my_certificates,
        "certificates_this_month": certificates_this_month,
        "my_logbook_entries": my_logbook_entries,
        "entries_this_month": entries_this_month,
        "my_rotations": my_rotations,
        "completed_rotations": completed_rotations,
        "current_rotation": current_rotation,
        "my_cases": my_cases,
        "completion_percentage": round(completion_percentage, 1),
        "monthly_progress": list(monthly_progress),
        "analytics_type": "pg",
    }
    return render(request, "users/pg_analytics.html", context)


@staff_member_required
def admin_stats_api(request):
    """Enhanced API endpoint for admin dashboard statistics with filters"""
    from django.http import JsonResponse

    # Get filter parameters
    role_filter = request.GET.get("role", "all")
    period_filter = request.GET.get("period", "all")

    # Base queryset for active users
    base_qs = User.objects.filter(is_archived=False)

    # Apply role filter
    if role_filter == "pg":
        filtered_qs = base_qs.filter(role="pg")
    elif role_filter == "supervisor":
        filtered_qs = base_qs.filter(role="supervisor")
    elif role_filter == "all":
        filtered_qs = base_qs.filter(role__in=["pg", "supervisor"])
    else:
        filtered_qs = base_qs

    # Apply period filter
    if period_filter == "year":
        filtered_qs = filtered_qs.filter(date_joined__year=timezone.now().year)
    elif period_filter == "month":
        filtered_qs = filtered_qs.filter(
            date_joined__month=timezone.now().month, date_joined__year=timezone.now().year
        )

    # Get basic statistics
    total_users = base_qs.count()
    total_pgs = base_qs.filter(role="pg").count()
    total_supervisors = base_qs.filter(role="supervisor").count()
    new_users_this_month = base_qs.filter(
        date_joined__month=timezone.now().month, date_joined__year=timezone.now().year
    ).count()

    # Recent users (last 5)
    recent_users_qs = base_qs.order_by("-date_joined")[:5]
    recent_users = []
    for user in recent_users_qs:
        recent_users.append(
            {
                "username": user.username,
                "full_name": user.get_full_name(),
                "role_display": user.get_role_display(),
                "specialty": user.specialty or "Unspecified",
                "date_joined_display": f"{(timezone.now() - user.date_joined).days} days ago",
            }
        )

    # Enhanced specialty distribution with more details
    specialty_stats_qs = (
        filtered_qs.values("specialty").annotate(count=Count("id")).order_by("-count")
    )

    specialty_stats = []
    total_count = filtered_qs.count()

    for item in specialty_stats_qs:
        specialty_name = item["specialty"] or "Unspecified"
        count = item["count"]
        percentage = round((count / total_count * 100), 1) if total_count > 0 else 0

        specialty_stats.append(
            {"specialty": specialty_name, "count": count, "percentage": percentage}
        )

    # Calculate summary statistics
    total_specialties = len(specialty_stats)
    most_popular = specialty_stats[0]["specialty"] if specialty_stats else "None"
    average_per_specialty = (
        round(total_count / total_specialties, 1) if total_specialties > 0 else 0
    )
    unspecified_count = sum(1 for item in specialty_stats if item["specialty"] == "Unspecified")

    # Enhanced medical specialty color mapping for better visualization
    specialty_colors = {
        "Internal Medicine": "#3b82f6",  # Blue
        "Surgery": "#ef4444",  # Red
        "Pediatrics": "#10b981",  # Green
        "Obstetrics & Gynecology": "#ec4899",  # Pink
        "Psychiatry": "#8b5cf6",  # Purple
        "Radiology": "#06b6d4",  # Cyan
        "Anesthesiology": "#f59e0b",  # Orange
        "Emergency Medicine": "#dc2626",  # Dark Red
        "Family Medicine": "#059669",  # Emerald
        "Cardiology": "#be123c",  # Rose
        "Neurology": "#7c3aed",  # Violet
        "Orthopedics": "#64748b",  # Slate
        "Dermatology": "#a855f7",  # Purple Light
        "Pathology": "#374151",  # Gray
        "Ophthalmology": "#0ea5e9",  # Sky
        "ENT": "#84cc16",  # Lime
        "Urology": "#06b6d4",  # Teal
        "Oncology": "#6366f1",  # Indigo
        "Unspecified": "#9ca3af",  # Gray Light
    }

    # Vibrant color palette for any specialty not in the predefined list
    vibrant_colors = [
        "#3b82f6",
        "#ef4444",
        "#10b981",
        "#ec4899",
        "#8b5cf6",
        "#06b6d4",
        "#f59e0b",
        "#dc2626",
        "#059669",
        "#be123c",
        "#7c3aed",
        "#a855f7",
        "#0ea5e9",
        "#84cc16",
        "#6366f1",
        "#f97316",
        "#14b8a6",
        "#8b5a3c",
        "#db2777",
        "#7c2d12",
    ]

    # Add colors to specialty stats - ensure NO grey colors are used
    for index, item in enumerate(specialty_stats):
        specialty_name = item["specialty"]
        if specialty_name in specialty_colors:
            # Use predefined color, but avoid grey ones
            color = specialty_colors[specialty_name]
            if color in ["#64748b", "#374151", "#6b7280", "#9ca3af"]:
                # Replace grey colors with vibrant alternatives
                color = vibrant_colors[index % len(vibrant_colors)]
            item["color"] = color
        else:
            # Use vibrant color from palette for unknown specialties
            item["color"] = vibrant_colors[index % len(vibrant_colors)]

    return JsonResponse(
        {
            "total_users": total_users,
            "total_pgs": total_pgs,
            "total_supervisors": total_supervisors,
            "new_users_this_month": new_users_this_month,
            "recent_users": recent_users,
            "specialty_stats": specialty_stats,
            "filter_applied": {
                "role": role_filter,
                "period": period_filter,
                "total_filtered": total_count,
            },
            "summary": {
                "total_specialties": total_specialties,
                "most_popular": most_popular,
                "average_per_specialty": average_per_specialty,
                "unspecified_count": unspecified_count,
            },
            "status": "success",
        }
    )
