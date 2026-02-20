import csv

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import FormView

from .forms import (
    BulkRotationAssignmentForm,
    RotationCreateForm,
    RotationEvaluationForm,
    RotationSearchForm,
    RotationUpdateForm,
)
from .models import Department, Hospital, Rotation, RotationEvaluation

User = get_user_model()


class RotationAccessMixin(UserPassesTestMixin):
    """
    Mixin to control access to rotation views based on user role.

    Created: 2025-05-29 16:30:20 UTC
    Author: SMIB2012
    """

    def test_func(self):
        """Test if user has access to rotation features"""
        if not self.request.user.is_authenticated:
            return False

        # Admins have full access
        if self.request.user.role == "admin" or self.request.user.is_superuser:
            return True

        # Supervisors have access to their rotations
        if self.request.user.role == "supervisor":
            return True

        # PGs have access to their own rotations
        if self.request.user.role == "pg":
            return True

        return False


class RotationListView(LoginRequiredMixin, RotationAccessMixin, ListView):
    """View for listing rotations with filtering and search"""

    model = Rotation
    template_name = "rotations/rotation_list.html"
    context_object_name = "rotations"
    paginate_by = 25

    def get_queryset(self):
        """Filter rotations based on user role and search parameters"""
        queryset = Rotation.objects.select_related(
            "pg", "department", "hospital", "supervisor"
        ).prefetch_related("evaluations")

        # Role-based filtering
        if self.request.user.role == "supervisor":
            queryset = queryset.filter(
                Q(supervisor=self.request.user) | Q(pg__supervisor=self.request.user)
            )
        elif self.request.user.role == "pg":
            queryset = queryset.filter(pg=self.request.user)

        # Search and filter
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(pg__first_name__icontains=search_query)
                | Q(pg__last_name__icontains=search_query)
                | Q(pg__username__icontains=search_query)
                | Q(department__name__icontains=search_query)
                | Q(hospital__name__icontains=search_query)
            )

        # Status filter
        status_filter = self.request.GET.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Date range filter
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        # Department filter
        department = self.request.GET.get("department")
        if department:
            queryset = queryset.filter(department_id=department)

        # Hospital filter
        hospital = self.request.GET.get("hospital")
        if hospital:
            queryset = queryset.filter(hospital_id=hospital)

        # Supervisor filter
        supervisor = self.request.GET.get("supervisor")
        if supervisor:
            queryset = queryset.filter(supervisor_id=supervisor)

        # Sorting
        sort_by = self.request.GET.get("sort", "-start_date")
        queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)

        # Add search form
        context["search_form"] = RotationSearchForm(self.request.GET)

        # Add filter options
        context["departments"] = Department.objects.filter(is_active=True)
        context["hospitals"] = Hospital.objects.filter(is_active=True)

        if self.request.user.role == "admin":
            context["supervisors"] = User.objects.filter(role="supervisor", is_active=True)

        # Add statistics
        rotations = self.get_queryset()
        context["stats"] = {
            "total": rotations.count(),
            "ongoing": rotations.filter(status="ongoing").count(),
            "completed": rotations.filter(status="completed").count(),
            "planned": rotations.filter(status="planned").count(),
            "pending": rotations.filter(status="pending").count(),
        }

        # Add current filters for display
        context["current_filters"] = {
            "search": self.request.GET.get("search", ""),
            "status": self.request.GET.get("status", ""),
            "department": self.request.GET.get("department", ""),
            "hospital": self.request.GET.get("hospital", ""),
            "supervisor": self.request.GET.get("supervisor", ""),
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
        }

        return context


class RotationDetailView(LoginRequiredMixin, RotationAccessMixin, DetailView):
    """Detailed view of a single rotation"""

    model = Rotation
    template_name = "rotations/rotation_detail.html"
    context_object_name = "rotation"

    def get_object(self):
        """Get rotation with permission check"""
        rotation = get_object_or_404(Rotation, pk=self.kwargs["pk"])

        # Check if user has permission to view this rotation
        if self.request.user.role == "supervisor":
            if (
                rotation.supervisor != self.request.user
                and rotation.pg.supervisor != self.request.user
            ):
                raise PermissionDenied("You don't have permission to view this rotation")
        elif self.request.user.role == "pg":
            if rotation.pg != self.request.user:
                raise PermissionDenied("You can only view your own rotations")

        return rotation

    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)

        rotation = self.object

        # Add evaluations
        context["evaluations"] = rotation.evaluations.select_related("evaluator").order_by(
            "-created_at"
        )

        # Add evaluation statistics
        evaluations = rotation.evaluations.filter(score__isnull=False)
        if evaluations.exists():
            context["average_score"] = evaluations.aggregate(Avg("score"))["score__avg"]
            context["evaluation_count"] = evaluations.count()

        # Add progress information
        context["completion_percentage"] = rotation.get_completion_percentage()
        context["remaining_days"] = rotation.get_remaining_days()
        context["duration_months"] = rotation.get_duration_months()

        # Add permission flags
        context["can_evaluate"] = self.can_user_evaluate(rotation)
        context["can_edit"] = self.can_user_edit(rotation)
        context["can_delete"] = self.can_user_delete(rotation)

        # Add related rotations for the PG
        if rotation.pg:
            context["related_rotations"] = (
                Rotation.objects.filter(pg=rotation.pg)
                .exclude(pk=rotation.pk)
                .order_by("-start_date")[:5]
            )

        return context

    def can_user_evaluate(self, rotation):
        """Check if current user can evaluate this rotation"""
        user = self.request.user

        if user.role == "admin":
            return True
        elif user.role == "supervisor":
            return user == rotation.supervisor or user == rotation.pg.supervisor
        elif user.role == "pg" and user == rotation.pg:
            return rotation.can_be_evaluated()

        return False

    def can_user_edit(self, rotation):
        """Check if current user can edit this rotation"""
        user = self.request.user

        if user.role == "admin":
            return rotation.can_be_edited()
        elif user.role == "supervisor":
            return user == rotation.supervisor and rotation.can_be_edited()

        return False

    def can_user_delete(self, rotation):
        """Check if current user can delete this rotation"""
        user = self.request.user

        if user.role == "admin":
            return rotation.can_be_cancelled()

        return False


class RotationCreateView(LoginRequiredMixin, RotationAccessMixin, CreateView):
    """View for creating new rotations"""

    model = Rotation
    form_class = RotationCreateForm
    template_name = "rotations/rotation_form.html"

    def test_func(self):
        """Only admins and supervisors can create rotations"""
        return super().test_func() and self.request.user.role in ["admin", "supervisor"]

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set created_by field and handle success"""
        form.instance.created_by = self.request.user

        # Auto-set supervisor for supervisor users
        if self.request.user.role == "supervisor":
            form.instance.supervisor = self.request.user

        messages.success(
            self.request, f"Rotation created successfully for {form.instance.pg.get_full_name()}"
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to rotation detail page"""
        return reverse("rotations:detail", kwargs={"pk": self.object.pk})


class RotationUpdateView(LoginRequiredMixin, RotationAccessMixin, UpdateView):
    """View for updating existing rotations"""

    model = Rotation
    form_class = RotationUpdateForm
    template_name = "rotations/rotation_form.html"

    def get_object(self):
        """Get rotation with permission check"""
        rotation = get_object_or_404(Rotation, pk=self.kwargs["pk"])

        # Check if user has permission to edit this rotation
        if self.request.user.role == "supervisor":
            if rotation.supervisor != self.request.user:
                raise PermissionDenied("You can only edit rotations you supervise")
        elif self.request.user.role == "pg":
            raise PermissionDenied("PGs cannot edit rotations")

        if not rotation.can_be_edited():
            raise PermissionDenied("This rotation cannot be edited")

        return rotation

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, "Rotation updated successfully")

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to rotation detail page"""
        return reverse("rotations:detail", kwargs={"pk": self.object.pk})


class RotationDeleteView(LoginRequiredMixin, RotationAccessMixin, DeleteView):
    """View for deleting rotations"""

    model = Rotation
    template_name = "rotations/rotation_confirm_delete.html"
    success_url = reverse_lazy("rotations:list")

    def test_func(self):
        """Only admins can delete rotations"""
        return super().test_func() and self.request.user.role == "admin"

    def get_object(self):
        """Get rotation with permission check"""
        rotation = get_object_or_404(Rotation, pk=self.kwargs["pk"])

        if not rotation.can_be_cancelled():
            raise PermissionDenied("This rotation cannot be deleted")

        return rotation

    def delete(self, request, *args, **kwargs):
        """Handle deletion with success message"""
        rotation = self.get_object()
        messages.success(request, f"Rotation for {rotation.pg.get_full_name()} has been cancelled")

        return super().delete(request, *args, **kwargs)


class RotationEvaluationCreateView(LoginRequiredMixin, RotationAccessMixin, CreateView):
    """View for creating rotation evaluations"""

    model = RotationEvaluation
    form_class = RotationEvaluationForm
    template_name = "rotations/evaluation_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Get rotation and check permissions"""
        self.rotation = get_object_or_404(Rotation, pk=kwargs["rotation_pk"])

        # Check if user can evaluate this rotation
        if request.user.role == "supervisor":
            if (
                self.rotation.supervisor != request.user
                and self.rotation.pg.supervisor != request.user
            ):
                raise PermissionDenied("You can only evaluate rotations you supervise")
        elif request.user.role == "pg":
            if self.rotation.pg != request.user:
                raise PermissionDenied("You can only evaluate your own rotations")

        if not self.rotation.can_be_evaluated():
            raise PermissionDenied("This rotation cannot be evaluated yet")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass rotation and user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["rotation"] = self.rotation
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set rotation and evaluator fields"""
        form.instance.rotation = self.rotation
        form.instance.evaluator = self.request.user

        messages.success(self.request, "Evaluation submitted successfully")

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to rotation detail page"""
        return reverse("rotations:detail", kwargs={"pk": self.rotation.pk})

    def get_context_data(self, **kwargs):
        """Add rotation to context"""
        context = super().get_context_data(**kwargs)
        context["rotation"] = self.rotation
        return context


class RotationEvaluationDetailView(LoginRequiredMixin, RotationAccessMixin, DetailView):
    """View for displaying evaluation details"""

    model = RotationEvaluation
    template_name = "rotations/evaluation_detail.html"
    context_object_name = "evaluation"

    def get_object(self):
        """Get evaluation with permission check"""
        evaluation = get_object_or_404(RotationEvaluation, pk=self.kwargs["pk"])

        # Check if user has permission to view this evaluation
        user = self.request.user
        rotation = evaluation.rotation

        if user.role == "supervisor":
            if (
                rotation.supervisor != user
                and rotation.pg.supervisor != user
                and evaluation.evaluator != user
            ):
                raise PermissionDenied("You don't have permission to view this evaluation")
        elif user.role == "pg":
            if rotation.pg != user and evaluation.evaluator != user:
                raise PermissionDenied("You can only view your own evaluations")

        return evaluation


class RotationDashboardView(LoginRequiredMixin, RotationAccessMixin, TemplateView):
    """Dashboard view for rotation overview"""

    template_name = "rotations/dashboard.html"

    def get_context_data(self, **kwargs):
        """Add dashboard statistics and data"""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Base queryset based on user role
        if user.role == "admin":
            rotations = Rotation.objects.all()
        elif user.role == "supervisor":
            rotations = Rotation.objects.filter(Q(supervisor=user) | Q(pg__supervisor=user))
        elif user.role == "pg":
            rotations = Rotation.objects.filter(pg=user)
        else:
            rotations = Rotation.objects.none()

        # Current date for calculations
        today = timezone.now().date()

        # Statistics
        context["stats"] = {
            "total_rotations": rotations.count(),
            "ongoing_rotations": rotations.filter(status="ongoing").count(),
            "upcoming_rotations": rotations.filter(status="planned", start_date__gt=today).count(),
            "completed_rotations": rotations.filter(status="completed").count(),
            "pending_approvals": rotations.filter(status="pending").count(),
        }

        # Current rotations
        context["current_rotations"] = rotations.filter(status="ongoing").select_related(
            "pg", "department", "hospital", "supervisor"
        )[:5]

        # Upcoming rotations
        context["upcoming_rotations"] = (
            rotations.filter(status="planned", start_date__gt=today)
            .select_related("pg", "department", "hospital", "supervisor")
            .order_by("start_date")[:5]
        )

        # Recent evaluations (for supervisors and admins)
        if user.role in ["admin", "supervisor"]:
            context["recent_evaluations"] = (
                RotationEvaluation.objects.filter(rotation__in=rotations)
                .select_related("rotation__pg", "evaluator")
                .order_by("-created_at")[:5]
            )

        # Overdue rotations
        context["overdue_rotations"] = rotations.filter(
            end_date__lt=today, status="ongoing"
        ).select_related("pg", "department", "hospital")[:5]

        # Performance metrics (for admins)
        if user.role == "admin":
            context["performance_metrics"] = self.get_performance_metrics(rotations)

        return context

    def get_performance_metrics(self, rotations):
        """Calculate performance metrics for admin dashboard"""
        evaluations = RotationEvaluation.objects.filter(rotation__in=rotations, score__isnull=False)

        if not evaluations.exists():
            return {}

        return {
            "average_score": evaluations.aggregate(Avg("score"))["score__avg"],
            "total_evaluations": evaluations.count(),
            "passing_rate": (evaluations.filter(score__gte=60).count() / evaluations.count() * 100),
            "excellence_rate": (
                evaluations.filter(score__gte=90).count() / evaluations.count() * 100
            ),
        }


class BulkRotationAssignmentView(LoginRequiredMixin, RotationAccessMixin, FormView):
    """View for bulk rotation assignment"""

    template_name = "rotations/bulk_assignment.html"
    form_class = BulkRotationAssignmentForm
    success_url = reverse_lazy("rotations:list")

    def test_func(self):
        """Allow admins and supervisors to do bulk assignments"""
        return super().test_func() and self.request.user.role in ["admin", "supervisor"]

    def get_form_kwargs(self):
        """Pass user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Process bulk assignment"""
        created_count = 0

        try:
            # For supervisors, ensure they can only create rotations for their PGs
            supervisor = form.cleaned_data["supervisor"]
            if self.request.user.role == "supervisor":
                supervisor = self.request.user

            for pg in form.cleaned_data["pgs"]:
                # Additional permission check for supervisors
                if self.request.user.role == "supervisor" and pg.supervisor != self.request.user:
                    continue  # Skip PGs not supervised by current user

                _rotation = Rotation.objects.create(
                    pg=pg,
                    department=form.cleaned_data["department"],
                    hospital=form.cleaned_data["hospital"],
                    supervisor=supervisor,
                    start_date=form.cleaned_data["start_date"],
                    end_date=form.cleaned_data["end_date"],
                    objectives=form.cleaned_data["objectives"],
                    status="planned",
                    created_by=self.request.user,
                )
                created_count += 1

            messages.success(self.request, f"Successfully created {created_count} rotations")

        except Exception as e:
            messages.error(self.request, f"Error creating rotations: {str(e)}")

        return super().form_valid(form)


# API Views for AJAX functionality


@login_required
def rotation_calendar_api(request):
    """API endpoint for calendar view of rotations"""
    user = request.user

    # Get rotations based on user role
    if user.role == "admin":
        rotations = Rotation.objects.all()
    elif user.role == "supervisor":
        rotations = Rotation.objects.filter(Q(supervisor=user) | Q(pg__supervisor=user))
    elif user.role == "pg":
        rotations = Rotation.objects.filter(pg=user)
    else:
        rotations = Rotation.objects.none()

    # Format for calendar
    events = []
    for rotation in rotations.select_related("pg", "department"):
        events.append(
            {
                "id": rotation.id,
                "title": f"{rotation.pg.get_full_name()} - {rotation.department.name}",
                "start": rotation.start_date.isoformat(),
                "end": rotation.end_date.isoformat(),
                "color": {
                    "planned": "#007bff",
                    "ongoing": "#28a745",
                    "completed": "#6c757d",
                    "cancelled": "#dc3545",
                    "pending": "#ffc107",
                }.get(rotation.status, "#007bff"),
                "url": reverse("rotations:detail", kwargs={"pk": rotation.pk}),
            }
        )

    return JsonResponse(events, safe=False)


@login_required
def department_by_hospital_api(request, hospital_id):
    """API endpoint to get departments by hospital"""
    try:
        departments = Department.objects.filter(hospital_id=hospital_id, is_active=True).values(
            "id", "name"
        )

        return JsonResponse(list(departments), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
def rotation_stats_api(request):
    """API endpoint for rotation statistics"""
    user = request.user

    # Get rotations based on user role
    if user.role == "admin":
        rotations = Rotation.objects.all()
    elif user.role == "supervisor":
        rotations = Rotation.objects.filter(Q(supervisor=user) | Q(pg__supervisor=user))
    elif user.role == "pg":
        rotations = Rotation.objects.filter(pg=user)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Calculate statistics
    stats = {
        "total": rotations.count(),
        "by_status": {
            status[0]: rotations.filter(status=status[0]).count()
            for status in Rotation.STATUS_CHOICES
        },
        "by_department": list(
            rotations.values("department__name").annotate(count=Count("id")).order_by("-count")[:10]
        ),
        "by_month": [],  # Could add monthly statistics here
    }

    return JsonResponse(stats)


@login_required
def export_rotations_csv(request):
    """Export rotations to CSV"""
    user = request.user

    # Get rotations based on user role
    if user.role == "admin":
        rotations = Rotation.objects.all()
    elif user.role == "supervisor":
        rotations = Rotation.objects.filter(Q(supervisor=user) | Q(pg__supervisor=user))
    elif user.role == "pg":
        rotations = Rotation.objects.filter(pg=user)
    else:
        raise PermissionDenied("You don't have permission to export rotations")

    # Create CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="rotations_export.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow(
        [
            "PG Name",
            "PG Username",
            "Department",
            "Hospital",
            "Supervisor",
            "Start Date",
            "End Date",
            "Status",
            "Duration (Days)",
            "Created Date",
        ]
    )

    # Write data
    for rotation in rotations.select_related("pg", "department", "hospital", "supervisor"):
        writer.writerow(
            [
                rotation.pg.get_full_name() if rotation.pg else "",
                rotation.pg.username if rotation.pg else "",
                rotation.department.name if rotation.department else "",
                rotation.hospital.name if rotation.hospital else "",
                rotation.supervisor.get_full_name() if rotation.supervisor else "",
                rotation.start_date,
                rotation.end_date,
                rotation.get_status_display(),
                rotation.get_duration_days() or "",
                rotation.created_at.date(),
            ]
        )

    return response


# Utility Views


@login_required
def rotation_quick_stats(request):
    """Quick stats widget for dashboard"""
    user = request.user

    if user.role == "admin":
        rotations = Rotation.objects.all()
    elif user.role == "supervisor":
        rotations = Rotation.objects.filter(Q(supervisor=user) | Q(pg__supervisor=user))
    elif user.role == "pg":
        rotations = Rotation.objects.filter(pg=user)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    today = timezone.now().date()

    stats = {
        "ongoing": rotations.filter(status="ongoing").count(),
        "upcoming": rotations.filter(status="planned", start_date__gt=today).count(),
        "overdue": rotations.filter(end_date__lt=today, status="ongoing").count(),
        "pending_approval": rotations.filter(status="pending").count(),
    }

    return JsonResponse(stats)
