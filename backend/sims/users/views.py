import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, View

from .decorators import (
    AdminRequiredMixin,
    ResidentRequiredMixin,
    SupervisorOrAdminRequiredMixin,
    SupervisorRequiredMixin,
    admin_required,
    resident_required,
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
                elif user.is_resident():
                    messages.success(request, f"Welcome back, {user.get_display_name()}!")
                    return redirect("users:resident_dashboard")
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
        "dashboard_type": "SUPERVISOR",
    }
    return render(request, "users/supervisor_dashboard.html", context)


@resident_required
def pg_dashboard(request):
    """Resident dashboard with personal progress overview"""

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
        from sims.training.models import RotationAssignment

        rotations_count = RotationAssignment.objects.filter(resident_training__resident_user=request.user).count()
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
        "SUPERVISOR": supervisor,
        "recent_submissions": recent_submissions[:10],
        "progress_stats": progress_stats,
        "dashboard_type": "RESIDENT",
    }
    return render(request, "users/pg_dashboard.html", context)


class DashboardRedirectView(LoginRequiredMixin, View):
    """Redirect users to appropriate dashboard based on their role"""

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_admin():
            return redirect("users:admin_dashboard")  # Changed from admin:index to show dashboard with navigation
        elif user.is_supervisor():
            return redirect("users:supervisor_dashboard")
        elif user.is_resident():
            return redirect("users:resident_dashboard")
        else:
            return redirect("users:profile")


class AdminDashboardView(AdminRequiredMixin, View):
    """Admin dashboard class-based view with navigation and stats"""

    def get(self, request, *args, **kwargs):
        from django.db.models import Count
        from django.utils import timezone
        import json

        # Get user statistics
        total_users = User.objects.filter(is_archived=False).count()
        total_pgs = User.objects.filter(role="RESIDENT", is_archived=False).count()
        total_supervisors = User.objects.filter(role="SUPERVISOR", is_archived=False).count()

        # Get new users this month
        current_month_start = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        new_users_this_month = User.objects.filter(
            is_archived=False, date_joined__gte=current_month_start
        ).count()

        # Get recent users (last 5)
        recent_users = User.objects.filter(is_archived=False).order_by("-date_joined")[:5]

        # Get specialty distribution for chart
        specialty_distribution = (
            User.objects.filter(role__in=["RESIDENT", "SUPERVISOR"], is_archived=False, specialty__isnull=False)
            .values("specialty")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Convert to JSON for JavaScript chart
        specialty_stats_json = json.dumps(
            [
                {"specialty": item["specialty"] or "Unspecified", "count": item["count"]}
                for item in specialty_distribution
            ]
        )

        context = {
            "total_users": total_users,
            "total_pgs": total_pgs,
            "total_supervisors": total_supervisors,
            "new_users_this_month": new_users_this_month,
            "recent_users": recent_users,
            "specialty_stats_json": specialty_stats_json,
        }
        return render(request, "users/admin_dashboard.html", context)


class SupervisorDashboardView(SupervisorRequiredMixin, View):
    """Supervisor dashboard class-based view"""

    def get(self, request, *args, **kwargs):
        return supervisor_dashboard(request)


class ResidentDashboardView(ResidentRequiredMixin, View):
    """Resident dashboard class-based view"""

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

            # Also check for 'SUPERVISOR' field as backup
            if not supervisor_id:
                supervisor_id = request.POST.get("SUPERVISOR", "").strip()

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
            if role in ["RESIDENT", "SUPERVISOR"] and not specialty:
                errors.append("Specialty is required for PGs and Supervisors")

            if role == "RESIDENT":
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
                specialty=specialty if role in ["RESIDENT", "SUPERVISOR"] else None,
                year=year if role == "RESIDENT" else None,
                phone_number=phone_number,
                registration_number=registration_number,
                is_active=True,
            )

            # Set supervisor for PG users
            if role == "RESIDENT" and supervisor_id:
                try:
                    supervisor = User.objects.get(id=supervisor_id, role="SUPERVISOR")
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
        "SUPERVISOR",
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
            if "SUPERVISOR" in form.fields:
                form.fields["SUPERVISOR"].queryset = User.objects.filter(
                    role="SUPERVISOR", is_active=True
                ).order_by("first_name", "last_name")
                form.fields["SUPERVISOR"].empty_label = "No Supervisor (for Supervisors/Admins)"

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
        return User.objects.filter(role="SUPERVISOR", is_archived=False)


class SupervisorPGsView(LoginRequiredMixin, DetailView):
    """View supervisor's assigned PGs"""

    model = User
    template_name = "users/supervisor_pgs.html"
    context_object_name = "SUPERVISOR"

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
        pgs = User.objects.filter(role="RESIDENT", is_archived=False)

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
        from sims.bulk.services import BulkService
        from django.core.exceptions import ValidationError
        
        if 'file' not in request.FILES:
            return JsonResponse({"success": False, "error": "No file uploaded"}, status=400)
        
        uploaded_file = request.FILES['file']
        dry_run = request.POST.get('dry_run', 'false').lower() == 'true'
        allow_partial = request.POST.get('allow_partial', 'false').lower() == 'true'
        
        try:
            service = BulkService(request.user)
            operation = service.import_trainees(
                uploaded_file,
                dry_run=dry_run,
                allow_partial=allow_partial,
            )
            
            response_data = {
                "success": True,
                "total_items": operation.total_items,
                "success_count": operation.success_count,
                "failure_count": operation.failure_count,
                "details": operation.details,
                "dry_run": dry_run,
            }
            
            if operation.status == operation.STATUS_COMPLETED:
                if not dry_run:
                    messages.success(
                        request,
                        f"Successfully imported {operation.success_count} PGs. "
                        f"{operation.failure_count} rows failed."
                    )
                return JsonResponse(response_data)
            else:
                # Operation failed - include details in response
                response_data["success"] = False
                response_data["error"] = "Import failed. Check details for errors."
                response_data["status"] = operation.status
                # Ensure details are included even when failed
                if not response_data.get("details"):
                    response_data["details"] = operation.details or {}
                return JsonResponse(response_data, status=400)
                
        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"An error occurred: {str(e)}"}, status=500)


class TraineeTemplateDownloadView(AdminRequiredMixin, View):
    """Download template Excel file for trainee import"""
    
    def get(self, request):
        from sims.bulk.services import generate_trainee_template
        
        template_file = generate_trainee_template()
        response = HttpResponse(
            template_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="trainee_import_template.xlsx"'
        return response


class ExcelConverterView(AdminRequiredMixin, View):
    """Convert Excel file to required trainee import format"""
    
    def post(self, request):
        from sims.bulk.services import convert_excel_to_trainee_format
        from django.core.exceptions import ValidationError
        
        if 'file' not in request.FILES:
            return JsonResponse({"success": False, "error": "No file uploaded"}, status=400)
        
        uploaded_file = request.FILES['file']
        
        try:
            converted_file = convert_excel_to_trainee_format(uploaded_file)
            response = HttpResponse(
                converted_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="converted_trainee_template.xlsx"'
            return response
        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": f"An error occurred: {str(e)}"}, status=500)


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
        # Get basic statistics for the template
        total_users = User.objects.filter(is_archived=False).count()
        total_pgs = User.objects.filter(role="RESIDENT", is_archived=False).count()
        total_supervisors = User.objects.filter(role="SUPERVISOR", is_archived=False).count()
        
        # Get new users this month
        current_month_start = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        new_users_this_month = User.objects.filter(
            is_archived=False, date_joined__gte=current_month_start
        ).count()
        
        context = {
            "total_users": total_users,
            "total_pgs": total_pgs,
            "total_supervisors": total_supervisors,
            "new_users_this_month": new_users_this_month,
        }
        return render(request, "users/user_reports.html", context)


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
