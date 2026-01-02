import csv
from datetime import timedelta

from django.conf import settings  # Import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import FormView

from .forms import PGLogbookEntryEditForm  # Added EditForm
from .forms import (
    BulkLogbookActionForm,
    LogbookEntryCreateForm,
    LogbookEntryUpdateForm,
    LogbookReviewForm,
    LogbookSearchForm,
    PGLogbookEntryForm,
    QuickLogbookEntryForm,
    SupervisorBulkActionForm,
    SupervisorBulkApproveForm,
    SupervisorBulkRejectForm,
    SupervisorLogbookReviewForm,
)
from .models import (
    Diagnosis,
    LogbookEntry,
    LogbookReview,
    LogbookStatistics,
    LogbookTemplate,
    Procedure,
)

User = get_user_model()


# Mixin to ensure user is a Postgraduate Resident
class PGRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "pg"

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        if self.request.user.is_authenticated:
            # Redirect to a relevant dashboard or home page if logged in but wrong role
            # This depends on your project's URL structure
            # For example, redirect to a generic dashboard or user profile
            # return redirect(reverse_lazy('users:dashboard')) # Adjust as needed
            return redirect(reverse_lazy("home"))  # Fallback to home
        return redirect(settings.LOGIN_URL)


# Mixin to ensure user is a Supervisor
class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "supervisor"

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy("home"))  # Fallback to home or user's specific dashboard
        return redirect(settings.LOGIN_URL)


class LogbookAccessMixin(UserPassesTestMixin):
    """
    Mixin to control access to logbook views based on user role.

    Created: 2025-05-29 17:21:58 UTC
    Author: SMIB2012
    """

    def test_func(self):
        """Test if user has access to logbook features"""
        if not self.request.user.is_authenticated:
            return False

        # Admins have full access
        if self.request.user.role == "admin" or self.request.user.is_superuser:
            return True

        # Supervisors have access to their PGs' logbook entries
        if self.request.user.role == "supervisor":
            return True

        # PGs have access to their own logbook
        if self.request.user.role == "pg":
            return True

        return False


class LogbookEntryListView(LoginRequiredMixin, LogbookAccessMixin, ListView):
    """View for listing logbook entries with filtering and search"""

    model = LogbookEntry
    template_name = "logbook/entry_list.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        """Filter entries based on user role and search parameters"""
        queryset = LogbookEntry.objects.select_related(
            "pg", "rotation__department", "primary_diagnosis", "supervisor"
        ).prefetch_related("procedures", "skills", "secondary_diagnoses", "reviews")

        # Role-based filtering
        if self.request.user.role == "supervisor":
            queryset = queryset.filter(pg__supervisor=self.request.user)
        elif self.request.user.role == "pg":
            queryset = queryset.filter(pg=self.request.user)

        # Search functionality
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(case_title__icontains=search_query)
                | Q(pg__first_name__icontains=search_query)
                | Q(pg__last_name__icontains=search_query)
                | Q(pg__username__icontains=search_query)
                | Q(patient_chief_complaint__icontains=search_query)
                | Q(primary_diagnosis__name__icontains=search_query)
                | Q(learning_points__icontains=search_query)
                | Q(clinical_reasoning__icontains=search_query)
            )

        # Status filter
        status_filter = self.request.GET.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Date range filter
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Rotation filter
        rotation_filter = self.request.GET.get("rotation")
        if rotation_filter:
            queryset = queryset.filter(rotation_id=rotation_filter)

        # Diagnosis filter
        diagnosis_filter = self.request.GET.get("diagnosis")
        if diagnosis_filter:
            queryset = queryset.filter(
                Q(primary_diagnosis_id=diagnosis_filter)
                | Q(secondary_diagnoses__id=diagnosis_filter)
            ).distinct()

        # Procedure filter
        procedure_filter = self.request.GET.get("procedure")
        if procedure_filter:
            queryset = queryset.filter(procedures__id=procedure_filter)

        # Supervisor filter (for admins)
        supervisor_filter = self.request.GET.get("supervisor")
        if supervisor_filter and self.request.user.role == "admin":
            queryset = queryset.filter(supervisor_id=supervisor_filter)

        # PG filter (for supervisors and admins)
        pg_filter = self.request.GET.get("pg")
        if pg_filter:
            if self.request.user.role == "supervisor":
                # Ensure supervisor can only filter their own PGs
                if self.request.user.assigned_pgs.filter(id=pg_filter).exists():
                    queryset = queryset.filter(pg_id=pg_filter)
            elif self.request.user.role == "admin":
                queryset = queryset.filter(pg_id=pg_filter)

        # Overdue filter
        overdue_filter = self.request.GET.get("overdue")
        if overdue_filter == "true":
            cutoff_date = timezone.now().date() - timedelta(days=7)
            queryset = queryset.filter(status="draft", date__lt=cutoff_date)

        # Review status filter
        review_filter = self.request.GET.get("review_status")
        if review_filter == "pending":
            queryset = queryset.filter(status="pending")
        elif review_filter == "reviewed":
            queryset = queryset.filter(reviews__isnull=False).distinct()
        elif review_filter == "unreviewed":
            queryset = queryset.filter(reviews__isnull=True)

        # Sorting
        sort_by = self.request.GET.get("sort", "-date")
        valid_sort_fields = [
            "date",
            "-date",
            "created_at",
            "-created_at",
            "status",
            "pg__last_name",
            "case_title",
            "primary_diagnosis__name",
        ]
        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by("-date", "-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)

        # Add search form
        context["search_form"] = LogbookSearchForm(self.request.GET)

        # Add filter options
        context["rotations"] = self._get_rotation_choices()
        context["diagnoses"] = Diagnosis.objects.filter(is_active=True).order_by("name")
        context["procedures"] = Procedure.objects.filter(is_active=True).order_by("name")

        if self.request.user.role == "admin":
            context["supervisors"] = User.objects.filter(role="supervisor", is_active=True)
            context["pgs"] = User.objects.filter(role="pg", is_active=True)
        elif self.request.user.role == "supervisor":
            context["pgs"] = self.request.user.assigned_pgs.filter(is_active=True)

        # Add statistics
        entries = self.get_queryset()
        context["stats"] = {
            "total": entries.count(),
            "draft": entries.filter(status="draft").count(),
            "pending": entries.filter(status="pending").count(),
            "approved": entries.filter(status="approved").count(),
            "needs_revision": entries.filter(status="returned").count(),
            "overdue": entries.filter(
                status="draft", date__lt=timezone.now().date() - timedelta(days=7)
            ).count(),
        }

        # Add current filters for display
        context["current_filters"] = {
            "search": self.request.GET.get("search", ""),
            "status": self.request.GET.get("status", ""),
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
            "rotation": self.request.GET.get("rotation", ""),
            "diagnosis": self.request.GET.get("diagnosis", ""),
            "procedure": self.request.GET.get("procedure", ""),
            "supervisor": self.request.GET.get("supervisor", ""),
            "pg": self.request.GET.get("pg", ""),
            "overdue": self.request.GET.get("overdue", ""),
            "review_status": self.request.GET.get("review_status", ""),
        }

        return context

    def _get_rotation_choices(self):
        """Get rotation choices based on user role"""
        from sims.rotations.models import Rotation

        if self.request.user.role == "admin":
            return Rotation.objects.select_related("department", "hospital")
        elif self.request.user.role == "supervisor":
            return Rotation.objects.filter(pg__supervisor=self.request.user).select_related(
                "department", "hospital"
            )
        elif self.request.user.role == "pg":
            return Rotation.objects.filter(pg=self.request.user).select_related(
                "department", "hospital"
            )

        return Rotation.objects.none()


class LogbookEntryDetailView(LoginRequiredMixin, LogbookAccessMixin, DetailView):
    """Detailed view of a single logbook entry"""

    model = LogbookEntry
    template_name = "logbook/entry_detail.html"
    context_object_name = "entry"

    def get_object(self):
        """Get entry with permission check"""
        entry = get_object_or_404(LogbookEntry, pk=self.kwargs["pk"])

        # Check if user has permission to view this entry
        if self.request.user.role == "supervisor":
            if entry.pg.supervisor != self.request.user:
                raise PermissionDenied("You don't have permission to view this entry")
        elif self.request.user.role == "pg":
            if entry.pg != self.request.user:
                raise PermissionDenied("You can only view your own entries")

        return entry

    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)

        entry = self.object

        # Add reviews
        context["reviews"] = entry.reviews.select_related("reviewer").order_by("-created_at")

        # Add entry metrics
        context["complexity_score"] = entry.get_complexity_score()
        context["cme_points"] = entry.get_cme_points()
        context["is_overdue"] = entry.is_overdue()
        context["duration_since_creation"] = entry.get_duration_since_creation()

        if entry.verified_at:
            context["review_duration"] = entry.get_review_duration()

        # Add permission flags
        context["can_review"] = self.can_user_review(entry)
        context["can_edit"] = self.can_user_edit(entry)
        context["can_delete"] = self.can_user_delete(entry)

        # Add related entries for the PG
        if entry.pg:
            context["related_entries"] = (
                LogbookEntry.objects.filter(pg=entry.pg).exclude(pk=entry.pk).order_by("-date")[:5]
            )

        # Add procedure and skill details
        context["procedures_list"] = entry.procedures.all().order_by("difficulty_level")
        context["skills_list"] = entry.skills.all().order_by("category", "level")
        context["secondary_diagnoses_list"] = entry.secondary_diagnoses.all()

        # Add template information if used
        if entry.template:
            context["template_sections"] = entry.template.get_template_sections()

        return context

    def can_user_review(self, entry):
        """Check if current user can review this entry"""
        user = self.request.user

        if user.role == "admin":
            return entry.status == "submitted"
        elif user.role == "supervisor":
            return user == entry.pg.supervisor and entry.status == "submitted"

        return False

    def can_user_edit(self, entry):
        """Check if current user can edit this entry"""
        user = self.request.user

        if user.role == "admin":
            return entry.can_be_edited()
        elif user.role == "pg" and user == entry.pg:
            return entry.can_be_edited()

        return False

    def can_user_delete(self, entry):
        """Check if current user can delete this entry"""
        user = self.request.user

        if user.role == "admin":
            return entry.can_be_deleted()
        elif user.role == "pg" and user == entry.pg:
            return entry.can_be_deleted()

        return False


class LogbookEntryCreateView(LoginRequiredMixin, LogbookAccessMixin, CreateView):
    """View for creating new logbook entries"""

    model = LogbookEntry
    form_class = LogbookEntryCreateForm
    template_name = "logbook/entry_form.html"

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        """Set initial form values"""
        initial = super().get_initial()

        # Set default date to today
        initial["date"] = timezone.now().date()

        # Pre-populate template if specified
        template_id = self.request.GET.get("template")
        if template_id:
            try:
                template = LogbookTemplate.objects.get(id=template_id, is_active=True)
                initial["template"] = template
            except LogbookTemplate.DoesNotExist:
                pass

        # Pre-populate rotation if specified
        rotation_id = self.request.GET.get("rotation")
        if rotation_id:
            try:
                from sims.rotations.models import Rotation

                rotation = Rotation.objects.get(id=rotation_id)
                # Check if user has access to this rotation
                if (
                    (self.request.user.role == "pg" and rotation.pg == self.request.user)
                    or (
                        self.request.user.role == "supervisor"
                        and rotation.pg.supervisor == self.request.user
                    )
                    or (self.request.user.role == "admin")
                ):
                    initial["rotation"] = rotation
            except Exception:
                pass

        return initial

    def form_valid(self, form):
        """Set created_by field and handle success"""
        form.instance.created_by = self.request.user

        # For PGs, set themselves as the entry owner
        if self.request.user.role == "pg":
            form.instance.pg = self.request.user

        # Auto-assign supervisor if not set
        if not form.instance.supervisor and form.instance.pg:
            form.instance.supervisor = form.instance.pg.supervisor

        messages.success(
            self.request,
            f"Logbook entry '{form.instance.case_title or 'New Entry'}' created successfully",
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect based on save action"""
        if "save_and_continue" in self.request.POST:
            return reverse("logbook:edit", kwargs={"pk": self.object.pk})
        elif "save_and_submit" in self.request.POST:
            # Change status to pending
            self.object.status = "pending"
            self.object.save()
            messages.info(self.request, "Entry submitted for review")
            return reverse("logbook:detail", kwargs={"pk": self.object.pk})
        else:
            return reverse("logbook:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add additional context"""
        context = super().get_context_data(**kwargs)
        context["is_create"] = True
        context["templates"] = LogbookTemplate.objects.filter(is_active=True)
        return context


class LogbookEntryUpdateView(LoginRequiredMixin, LogbookAccessMixin, UpdateView):
    """View for updating existing logbook entries"""

    model = LogbookEntry
    form_class = LogbookEntryUpdateForm
    template_name = "logbook/entry_form.html"

    def get_object(self):
        """Get entry with permission check"""
        entry = get_object_or_404(LogbookEntry, pk=self.kwargs["pk"])

        # Check if user has permission to edit this entry
        if self.request.user.role == "supervisor":
            if entry.pg.supervisor != self.request.user:
                raise PermissionDenied("You can only edit entries of your assigned PGs")
        elif self.request.user.role == "pg":
            if entry.pg != self.request.user:
                raise PermissionDenied("You can only edit your own entries")

        if not entry.can_be_edited():
            raise PermissionDenied("This entry cannot be edited")

        return entry

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Handle successful form submission"""
        # Reset status to draft if entry was in needs_revision status
        if self.object.status == "needs_revision":
            form.instance.status = "draft"

        messages.success(
            self.request,
            f"Logbook entry '{form.instance.case_title or 'Entry'}' updated successfully",
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect based on save action"""
        if "save_and_continue" in self.request.POST:
            return reverse("logbook:edit", kwargs={"pk": self.object.pk})
        elif "save_and_submit" in self.request.POST:
            # Change status to pending
            self.object.status = "pending"
            self.object.save()
            messages.info(self.request, "Entry submitted for review")
            return reverse("logbook:detail", kwargs={"pk": self.object.pk})
        else:
            return reverse("logbook:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add additional context"""
        context = super().get_context_data(**kwargs)
        context["is_create"] = False
        return context


class LogbookEntryDeleteView(LoginRequiredMixin, LogbookAccessMixin, DeleteView):
    """View for deleting logbook entries"""

    model = LogbookEntry
    template_name = "logbook/entry_confirm_delete.html"
    success_url = reverse_lazy("logbook:list")

    def get_object(self):
        """Get entry with permission check"""
        entry = get_object_or_404(LogbookEntry, pk=self.kwargs["pk"])

        # Check permissions
        if self.request.user.role == "supervisor":
            raise PermissionDenied("Supervisors cannot delete entries")
        elif self.request.user.role == "pg":
            if entry.pg != self.request.user:
                raise PermissionDenied("You can only delete your own entries")

        if not entry.can_be_deleted():
            raise PermissionDenied("This entry cannot be deleted")

        return entry

    def delete(self, request, *args, **kwargs):
        """Handle deletion with success message"""
        entry = self.get_object()
        messages.success(request, f"Logbook entry '{entry.case_title or 'Entry'}' has been deleted")

        return super().delete(request, *args, **kwargs)


class LogbookReviewCreateView(LoginRequiredMixin, LogbookAccessMixin, CreateView):
    """View for creating logbook reviews"""

    model = LogbookReview
    form_class = LogbookReviewForm
    template_name = "logbook/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Get entry and check permissions"""
        self.entry = get_object_or_404(LogbookEntry, pk=kwargs["entry_pk"])

        # Check if user can review this entry
        if request.user.role == "supervisor":
            if self.entry.pg.supervisor != request.user:
                raise PermissionDenied("You can only review entries of your assigned PGs")
        elif request.user.role != "admin":
            raise PermissionDenied("You don't have permission to review entries")

        if self.entry.status not in ["pending", "submitted"]:
            raise PermissionDenied("This entry is not ready for review")

        # Check if user has already reviewed this entry
        if LogbookReview.objects.filter(logbook_entry=self.entry, reviewer=request.user).exists():
            messages.warning(request, "You have already reviewed this entry")
            return redirect("logbook:detail", pk=self.entry.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass entry and user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["entry"] = self.entry
        kwargs["user"] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        """Get form and pre-populate reviewer for validation"""
        form = super().get_form(form_class)
        # Set reviewer on the form instance so model validation can access it
        if hasattr(form, "instance"):
            form.instance.logbook_entry = self.entry
            form.instance.reviewer = self.request.user
        return form

    def form_valid(self, form):
        """Set entry and reviewer fields"""
        form.instance.logbook_entry = self.entry
        form.instance.reviewer = self.request.user

        messages.success(
            self.request, f"Review submitted for entry '{self.entry.case_title or 'Entry'}'"
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to entry detail page"""
        return reverse("logbook:detail", kwargs={"pk": self.entry.pk})

    def get_context_data(self, **kwargs):
        """Add entry to context"""
        context = super().get_context_data(**kwargs)
        context["entry"] = self.entry
        return context


class LogbookReviewDetailView(LoginRequiredMixin, LogbookAccessMixin, DetailView):
    """View for displaying review details"""

    model = LogbookReview
    template_name = "logbook/review_detail.html"
    context_object_name = "review"

    def get_object(self):
        """Get review with permission check"""
        review = get_object_or_404(LogbookReview, pk=self.kwargs["pk"])

        # Check if user has permission to view this review
        user = self.request.user
        entry = review.logbook_entry

        if user.role == "supervisor":
            if entry.pg.supervisor != user and review.reviewer != user:
                raise PermissionDenied("You don't have permission to view this review")
        elif user.role == "pg":
            if entry.pg != user:
                raise PermissionDenied("You can only view reviews of your own entries")

        return review


class LogbookDashboardView(LoginRequiredMixin, LogbookAccessMixin, TemplateView):
    """Dashboard view for logbook overview"""

    template_name = "logbook/dashboard.html"

    def get_context_data(self, **kwargs):
        """Add dashboard statistics and data"""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Base queryset based on user role
        if user.role == "admin":
            entries = LogbookEntry.objects.all()
        elif user.role == "supervisor":
            entries = LogbookEntry.objects.filter(pg__supervisor=user)
        elif user.role == "pg":
            entries = LogbookEntry.objects.filter(pg=user)
        else:
            entries = LogbookEntry.objects.none()

        # Current date for calculations
        today = timezone.now().date()

        # Basic statistics
        context["stats"] = {
            "total_entries": entries.count(),
            "draft_entries": entries.filter(status="draft").count(),
            "pending_entries": entries.filter(status="pending").count(),
            "approved_entries": entries.filter(status="approved").count(),
            "revision_entries": entries.filter(status="returned").count(),
            "overdue_entries": entries.filter(
                status="draft", date__lt=today - timedelta(days=7)
            ).count(),
        }

        # Recent entries
        context["recent_entries"] = entries.select_related(
            "pg", "primary_diagnosis", "rotation__department"
        ).order_by("-created_at")[:5]

        # Pending reviews (for supervisors and admins)
        if user.role in ["admin", "supervisor"]:
            context["pending_reviews"] = entries.filter(status="pending").select_related(
                "pg", "primary_diagnosis"
            )[:5]

        # Overdue entries
        context["overdue_entries"] = entries.filter(
            status="draft", date__lt=today - timedelta(days=7)
        ).select_related("pg", "primary_diagnosis")[:5]

        # Monthly activity (last 6 months)
        monthly_data = self.get_monthly_activity(entries)
        context["monthly_activity"] = monthly_data

        # Top diagnoses
        context["top_diagnoses"] = (
            entries.values("primary_diagnosis__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        # Top procedures
        context["top_procedures"] = (
            entries.filter(procedures__isnull=False)
            .values("procedures__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        # Performance metrics (for PGs)
        if user.role == "pg":
            context["performance_metrics"] = self.get_pg_performance_metrics(entries)

        # Supervision metrics (for supervisors)
        elif user.role == "supervisor":
            context["supervision_metrics"] = self.get_supervisor_metrics(user)

        # System metrics (for admins)
        elif user.role == "admin":
            context["system_metrics"] = self.get_system_metrics()

        return context

    def get_monthly_activity(self, entries):
        """Get monthly activity data for the last 6 months"""
        today = timezone.now().date()
        six_months_ago = today - timedelta(days=180)

        monthly_counts = (
            entries.filter(date__gte=six_months_ago)
            .extra({"month": "DATE_TRUNC('month', date)"})
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        # Convert to list for JSON serialization
        return [
            {"month": item["month"].strftime("%Y-%m"), "count": item["count"]}
            for item in monthly_counts
        ]

    def get_pg_performance_metrics(self, entries):
        """Calculate performance metrics for PG"""
        approved_entries = entries.filter(status="approved")

        metrics = {
            "completion_rate": 0,
            "average_score": None,
            "cme_points": 0,
            "unique_procedures": 0,
            "unique_diagnoses": 0,
            "on_time_rate": 0,
        }

        if entries.exists():
            # Completion rate
            metrics["completion_rate"] = (approved_entries.count() / entries.count()) * 100

            # Average scores
            scored_entries = entries.filter(supervisor_assessment_score__isnull=False)
            if scored_entries.exists():
                metrics["average_score"] = scored_entries.aggregate(
                    avg=Avg("supervisor_assessment_score")
                )["avg"]

            # CME points
            metrics["cme_points"] = sum(e.get_cme_points() for e in approved_entries)

            # Unique procedures and diagnoses
            metrics["unique_procedures"] = (
                entries.filter(procedures__isnull=False).values("procedures").distinct().count()
            )

            metrics["unique_diagnoses"] = (
                entries.filter(primary_diagnosis__isnull=False)
                .values("primary_diagnosis")
                .distinct()
                .count()
            )

            # On-time submission rate
            on_time_count = 0
            for entry in entries:
                days_to_submit = (entry.created_at.date() - entry.date).days
                if days_to_submit <= 7:
                    on_time_count += 1

            metrics["on_time_rate"] = (on_time_count / entries.count()) * 100

        return metrics

    def get_supervisor_metrics(self, supervisor):
        """Calculate metrics for supervisor"""
        pgs = supervisor.assigned_pgs.filter(is_active=True)
        all_entries = LogbookEntry.objects.filter(pg__in=pgs)

        metrics = {
            "total_pgs": pgs.count(),
            "active_pgs": pgs.filter(
                logbook_entries__date__gte=timezone.now().date() - timedelta(days=30)
            )
            .distinct()
            .count(),
            "pending_reviews": all_entries.filter(status="pending").count(),
            "average_review_time": 0,
            "pg_performance": [],
        }

        # Calculate average review time
        reviewed_entries = all_entries.filter(verified_at__isnull=False)
        if reviewed_entries.exists():
            review_times = []
            for entry in reviewed_entries:
                if entry.get_review_duration():
                    review_times.append(entry.get_review_duration().days)

            if review_times:
                metrics["average_review_time"] = sum(review_times) / len(review_times)

        # PG performance summary
        for pg in pgs:
            pg_entries = all_entries.filter(pg=pg)
            pg_data = {
                "pg": pg,
                "total_entries": pg_entries.count(),
                "approved_entries": pg_entries.filter(status="approved").count(),
                "pending_entries": pg_entries.filter(status="pending").count(),
                "last_entry": pg_entries.order_by("-date").first(),
            }
            metrics["pg_performance"].append(pg_data)

        return metrics

    def get_system_metrics(self):
        """Calculate system-wide metrics for admin"""
        all_entries = LogbookEntry.objects.all()
        all_pgs = User.objects.filter(role="pg", is_active=True)

        metrics = {
            "total_pgs": all_pgs.count(),
            "active_pgs": all_pgs.filter(
                logbook_entries__date__gte=timezone.now().date() - timedelta(days=30)
            )
            .distinct()
            .count(),
            "total_entries": all_entries.count(),
            "entries_this_month": all_entries.filter(
                date__month=timezone.now().month, date__year=timezone.now().year
            ).count(),
            "approval_rate": 0,
            "average_entries_per_pg": 0,
            "top_performing_pgs": [],
            "underperforming_pgs": [],
        }

        if all_entries.exists():
            # Approval rate
            approved_count = all_entries.filter(status="approved").count()
            metrics["approval_rate"] = (approved_count / all_entries.count()) * 100

            # Average entries per PG
            metrics["average_entries_per_pg"] = all_entries.count() / all_pgs.count()

        # Top and underperforming PGs
        pg_stats = []
        for pg in all_pgs:
            pg_entries = all_entries.filter(pg=pg)
            approved_entries = pg_entries.filter(status="approved")

            pg_stat = {
                "pg": pg,
                "total_entries": pg_entries.count(),
                "approved_entries": approved_entries.count(),
                "completion_rate": (
                    (approved_entries.count() / pg_entries.count() * 100)
                    if pg_entries.exists()
                    else 0
                ),
            }
            pg_stats.append(pg_stat)

        # Sort by completion rate
        pg_stats.sort(key=lambda x: x["completion_rate"], reverse=True)

        metrics["top_performing_pgs"] = pg_stats[:5]
        metrics["underperforming_pgs"] = [pg for pg in pg_stats if pg["completion_rate"] < 50][:5]

        return metrics


class QuickLogbookEntryView(LoginRequiredMixin, LogbookAccessMixin, CreateView):
    """Quick entry form for rapid logbook entry creation"""

    model = LogbookEntry
    form_class = QuickLogbookEntryForm
    template_name = "logbook/quick_entry.html"

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set required fields and create entry"""
        form.instance.created_by = self.request.user

        if self.request.user.role == "pg":
            form.instance.pg = self.request.user
            form.instance.supervisor = self.request.user.supervisor

        messages.success(
            self.request, "Quick entry created successfully. You can add more details later."
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to edit page for completion"""
        return reverse("logbook:edit", kwargs={"pk": self.object.pk})


class BulkLogbookActionView(LoginRequiredMixin, LogbookAccessMixin, FormView):
    """View for bulk actions on logbook entries"""

    template_name = "logbook/bulk_actions.html"
    form_class = BulkLogbookActionForm
    success_url = reverse_lazy("logbook:list")

    def test_func(self):
        """Only supervisors and admins can perform bulk actions"""
        return super().test_func() and self.request.user.role in ["admin", "supervisor"]

    def form_valid(self, form):
        """Process bulk actions"""
        action = form.cleaned_data["action"]
        entries = form.cleaned_data["entries"]

        processed_count = 0

        try:
            for entry in entries:
                # Check permissions
                if (
                    self.request.user.role == "supervisor"
                    and entry.pg.supervisor != self.request.user
                ):
                    continue

                if action == "approve":
                    if entry.status == "pending":
                        entry.status = "approved"
                        entry.verified_by = self.request.user
                        entry.verified_at = timezone.now()
                        entry.save()
                        processed_count += 1

                elif action == "request_revision":
                    if entry.status == "pending":
                        entry.status = "returned"
                        entry.save()
                        processed_count += 1

                elif action == "archive":
                    if entry.status in ["approved", "needs_revision"]:
                        entry.status = "archived"
                        entry.save()
                        processed_count += 1

            messages.success(self.request, f"Successfully processed {processed_count} entries")

        except Exception as e:
            messages.error(self.request, f"Error processing entries: {str(e)}")

        return super().form_valid(form)


# API Views for AJAX functionality


@login_required
def logbook_stats_api(request):
    """API endpoint for logbook statistics"""
    user = request.user

    # Get entries based on user role
    if user.role == "admin":
        entries = LogbookEntry.objects.all()
    elif user.role == "supervisor":
        entries = LogbookEntry.objects.filter(pg__supervisor=user)
    elif user.role == "pg":
        entries = LogbookEntry.objects.filter(pg=user)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Calculate statistics
    stats = {
        "total": entries.count(),
        "by_status": {
            status[0]: entries.filter(status=status[0]).count()
            for status in LogbookEntry.STATUS_CHOICES
        },
        "by_month": list(
            entries.extra({"month": "DATE_TRUNC('month', date)"})
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        ),
        "overdue": entries.filter(
            status="draft", date__lt=timezone.now().date() - timedelta(days=7)
        ).count(),
    }

    return JsonResponse(stats)


@login_required
def export_logbook_csv(request):
    """Export logbook entries to CSV"""
    user = request.user

    # Get entries based on user role
    if user.role == "admin":
        entries = LogbookEntry.objects.all()
    elif user.role == "supervisor":
        entries = LogbookEntry.objects.filter(pg__supervisor=user)
    elif user.role == "pg":
        entries = LogbookEntry.objects.filter(pg=user)
    else:
        raise PermissionDenied("You don't have permission to export entries")

    # Create CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="logbook_export.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow(
        [
            "PG Name",
            "PG Username",
            "Date",
            "Case Title",
            "Primary Diagnosis",
            "Patient Age",
            "Patient Gender",
            "Procedures",
            "Skills",
            "Status",
            "Self Score",
            "Supervisor Score",
            "CME Points",
            "Created Date",
        ]
    )

    # Write data
    for entry in entries.select_related("pg", "primary_diagnosis").prefetch_related(
        "procedures", "skills"
    ):
        procedures = ", ".join([p.name for p in entry.procedures.all()])
        skills = ", ".join([s.name for s in entry.skills.all()])

        writer.writerow(
            [
                entry.pg.get_full_name() if entry.pg else "",
                entry.pg.username if entry.pg else "",
                entry.date,
                entry.case_title or "",
                entry.primary_diagnosis.name if entry.primary_diagnosis else "",
                entry.patient_age,
                entry.get_patient_gender_display(),
                procedures,
                skills,
                entry.get_status_display(),
                entry.self_assessment_score or "",
                entry.supervisor_assessment_score or "",
                entry.get_cme_points(),
                entry.created_at.date(),
            ]
        )

    return response


@login_required
def template_preview_api(request, template_id):
    """API endpoint to preview template structure"""
    template = get_object_or_404(LogbookTemplate, id=template_id, is_active=True)

    data = {
        "name": template.name,
        "description": template.description,
        "sections": template.get_template_sections(),
        "required_fields": template.get_required_fields_list(),
        "guidelines": template.completion_guidelines,
    }

    return JsonResponse(data)


@login_required
def update_logbook_statistics(request):
    """Update logbook statistics for all PGs"""
    if request.user.role != "admin":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        LogbookStatistics.update_all_statistics()
        return JsonResponse({"success": True, "message": "Statistics updated successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def entry_complexity_api(request, entry_id):
    """API endpoint to get entry complexity metrics"""
    entry = get_object_or_404(LogbookEntry, id=entry_id)

    # Check permissions
    user = request.user
    if user.role == "supervisor":
        if entry.pg.supervisor != user:
            return JsonResponse({"error": "Unauthorized"}, status=403)
    elif user.role == "pg":
        if entry.pg != user:
            return JsonResponse({"error": "Unauthorized"}, status=403)
    elif user.role not in ["admin"]:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    complexity_data = {
        "complexity_score": entry.get_complexity_score(),
        "cme_points": entry.get_cme_points(),
        "procedure_count": entry.procedures.count(),
        "skill_count": entry.skills.count(),
        "procedures": [
            {"name": p.name, "difficulty": p.difficulty_level, "category": p.get_category_display()}
            for p in entry.procedures.all()
        ],
        "skills": [
            {"name": s.name, "level": s.get_level_display(), "category": s.get_category_display()}
            for s in entry.skills.all()
        ],
    }

    return JsonResponse(complexity_data)


# Utility Views


class LogbookAnalyticsView(LoginRequiredMixin, LogbookAccessMixin, TemplateView):
    """Analytics view for logbook data visualization"""

    template_name = "logbook/analytics.html"

    def test_func(self):
        """Only admins and supervisors can view analytics"""
        return super().test_func() and self.request.user.role in ["admin", "supervisor"]

    def get_context_data(self, **kwargs):
        """Add analytics data to context"""
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Get entries based on user role
        if user.role == "admin":
            entries = LogbookEntry.objects.all()
            pgs = User.objects.filter(role="pg", is_active=True)
        elif user.role == "supervisor":
            entries = LogbookEntry.objects.filter(pg__supervisor=user)
            pgs = user.assigned_pgs.filter(is_active=True)
        else:
            entries = LogbookEntry.objects.none()
            pgs = User.objects.none()

        # Time-based analytics
        context["monthly_trends"] = self.get_monthly_trends(entries)
        context["weekly_activity"] = self.get_weekly_activity(entries)

        # Performance analytics
        context["pg_performance"] = self.get_pg_performance_analytics(pgs)
        context["procedure_analytics"] = self.get_procedure_analytics(entries)
        context["diagnosis_analytics"] = self.get_diagnosis_analytics(entries)

        # Quality metrics
        context["quality_metrics"] = self.get_quality_metrics(entries)

        return context

    def get_monthly_trends(self, entries):
        """Get monthly entry trends for the last year"""
        twelve_months_ago = timezone.now().date() - timedelta(days=365)

        return (
            entries.filter(date__gte=twelve_months_ago)
            .extra({"month": "DATE_TRUNC('month', date)"})
            .values("month")
            .annotate(
                total=Count("id"),
                approved=Count("id", filter=Q(status="approved")),
                pending=Count("id", filter=Q(status="pending")),
                draft=Count("id", filter=Q(status="draft")),
            )
            .order_by("month")
        )

    def get_weekly_activity(self, entries):
        """Get weekly activity patterns"""
        return (
            entries.extra({"weekday": "EXTRACT(dow FROM date)"})
            .values("weekday")
            .annotate(count=Count("id"))
            .order_by("weekday")
        )

    def get_pg_performance_analytics(self, pgs):
        """Get detailed PG performance analytics"""
        performance_data = []

        for pg in pgs:
            pg_entries = LogbookEntry.objects.filter(pg=pg)
            approved_entries = pg_entries.filter(status="approved")

            # Calculate metrics
            total_entries = pg_entries.count()
            completion_rate = (
                (approved_entries.count() / total_entries * 100) if total_entries > 0 else 0
            )

            avg_score = approved_entries.aggregate(avg=Avg("supervisor_assessment_score"))["avg"]

            cme_points = sum(e.get_cme_points() for e in approved_entries)

            performance_data.append(
                {
                    "pg": pg,
                    "total_entries": total_entries,
                    "completion_rate": completion_rate,
                    "average_score": avg_score,
                    "cme_points": cme_points,
                    "last_entry": pg_entries.order_by("-date").first(),
                }
            )

        return sorted(performance_data, key=lambda x: x["completion_rate"], reverse=True)

    def get_procedure_analytics(self, entries):
        """Get procedure usage analytics"""
        return (
            entries.filter(procedures__isnull=False)
            .values("procedures__name", "procedures__category", "procedures__difficulty_level")
            .annotate(usage_count=Count("id"), avg_score=Avg("supervisor_assessment_score"))
            .order_by("-usage_count")
        )

    def get_diagnosis_analytics(self, entries):
        """Get diagnosis pattern analytics"""
        return (
            entries.filter(primary_diagnosis__isnull=False)
            .values("primary_diagnosis__name", "primary_diagnosis__category")
            .annotate(
                usage_count=Count("id"),
                avg_complexity=Avg(Count("procedures") + Count("secondary_diagnoses")),
            )
            .order_by("-usage_count")
        )

    def get_quality_metrics(self, entries):
        """Calculate quality metrics"""
        total_entries = entries.count()

        if total_entries == 0:
            return {}

        # Review turnaround time
        reviewed_entries = entries.filter(verified_at__isnull=False)  # Should be approved_at
        avg_review_time = 0

        if reviewed_entries.exists():
            review_times = []
            for entry in reviewed_entries:
                review_duration = entry.get_review_duration()
                if review_duration:
                    review_times.append(review_duration.days)

            if review_times:
                avg_review_time = sum(review_times) / len(review_times)

        # Other quality metrics
        return {
            "total_entries": total_entries,
            "approval_rate": (
                (entries.filter(status="approved").count() / total_entries) * 100
                if total_entries > 0
                else 0
            ),
            "revision_rate": (
                (entries.filter(status="returned").count() / total_entries) * 100
                if total_entries > 0
                else 0
            ),  # 'returned' not 'needs_revision'
            "average_review_time": avg_review_time,
            "overdue_rate": (
                (
                    entries.filter(
                        status="draft", date__lt=timezone.now().date() - timedelta(days=7)
                    ).count()
                    / total_entries
                )
                * 100
                if total_entries > 0
                else 0
            ),
        }


# --- New View for PG Logbook Entry Creation ---
class PGLogbookEntryCreateView(LoginRequiredMixin, PGRequiredMixin, CreateView):
    model = LogbookEntry
    form_class = PGLogbookEntryForm
    template_name = (
        "logbook/pg_logbook_entry_form_enhanced.html"  # Updated to use enhanced template
    )
    # success_url will be defined in get_success_url or by reversing a named URL for PG's list view

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.pg = self.request.user

        # Attempt to assign supervisor from PG's profile
        # The user model has 'supervisor' as a direct attribute on the PG user instance
        pg_supervisor = getattr(self.request.user, "supervisor", None)

        if pg_supervisor:
            entry.supervisor = pg_supervisor
            entry.status = "pending"  # Directly to pending if supervisor exists
            # entry.submitted_to_supervisor_at = timezone.now() # Model's save method handles this
            messages.success(
                self.request, f"Logbook entry '{entry.case_title}' submitted for supervisor review."
            )
        else:
            entry.status = "draft"  # Save as draft if no supervisor is assigned to the PG
            messages.warning(
                self.request,
                f"Logbook entry '{entry.case_title}' saved as draft. Please ensure a supervisor is assigned to you to enable submission for review.",
            )

        # created_by is handled by the model's save method.
        # supervisor_action_at is also handled by the model's save method.
        entry.save()
        self.object = entry  # Set self.object for get_success_url
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # Redirect to a logbook list view for the PG. This URL needs to be defined.
        # For now, placeholder, will be updated when PG list view is created.
        # Example: return reverse_lazy('logbook:pg_entry_list')
        # Fallback to detail view of the created entry for now, or a generic dashboard.
        if self.object:
            # Redirect to the PG's logbook list after creation.
            # Could also redirect to the detail page of the created entry:
            # return reverse('logbook:detail', kwargs={'pk': self.object.pk})
            return reverse_lazy("logbook:pg_logbook_list")
        return reverse_lazy("logbook:pg_logbook_list")  # Default fallback

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create New Logbook Entry"
        return context


# --- New View for PG to List their Logbook Entries ---
class PGLogbookEntryListView(LoginRequiredMixin, PGRequiredMixin, ListView):
    model = LogbookEntry
    template_name = "logbook/pg_logbook_list.html"  # Needs to be created
    context_object_name = "logbook_entries"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            LogbookEntry.objects.filter(pg=self.request.user)
            .select_related("supervisor")
            .order_by("-date", "-updated_at")
        )

        status_filter = self.request.GET.get("status", "")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "My Logbook Entries"
        context["current_status_filter"] = self.request.GET.get("status", "")

        # Provide status choices for filtering UI, excluding 'draft' perhaps, or handling it.
        # PGs should see all their entries including drafts.
        status_choices = [{"value": s[0], "display": s[1]} for s in LogbookEntry.STATUS_CHOICES]
        context["status_choices"] = status_choices
        # Add choices for quick links, e.g. only 'Pending', 'Approved', 'Returned', 'Rejected'
        context["quick_filter_statuses"] = [
            s
            for s in status_choices
            if s["value"] in ["pending", "approved", "returned", "rejected"]
        ]

        return context


# --- New View for PG to Edit their Returned/Draft Logbook Entries ---
class PGLogbookEntryUpdateView(LoginRequiredMixin, PGRequiredMixin, UpdateView):
    model = LogbookEntry
    form_class = PGLogbookEntryEditForm  # Use the new edit form
    template_name = "logbook/pg_logbook_entry_edit_form.html"  # Needs to be created
    context_object_name = "logbook_entry"

    def get_queryset(self):
        # PGs can only edit their own entries that are 'returned' or 'draft'
        return LogbookEntry.objects.filter(pg=self.request.user, status__in=["returned", "draft"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        entry = form.save(commit=False)
        original_status = (
            self.get_object().status
        )  # Get original status before it's changed by form save

        # If editing a 'returned' entry, it goes back to 'pending'.
        # If editing a 'draft', it stays 'draft' unless a specific action submits it.
        # For now, resaving a draft keeps it draft. Resaving 'returned' makes it 'pending'.
        if original_status == "returned":
            entry.status = "pending"
            # entry.submitted_to_supervisor_at = timezone.now() # Model's save will handle this
            # entry.supervisor_action_at = None # Model's save will handle this
            messages.success(
                self.request,
                f"Logbook entry '{entry.case_title}' has been updated and resubmitted for supervisor review.",
            )
        elif original_status == "draft":
            # Retain draft status, or add a "Submit" button to change to 'pending'
            entry.status = "draft"  # Explicitly keep as draft
            messages.success(self.request, f"Draft logbook entry '{entry.case_title}' updated.")

        # Ensure pg is still set (should be handled by form/model instance)
        entry.pg = self.request.user
        # Supervisor should already be on the entry if it was 'returned'. If 'draft' and PG now has supervisor, model's save might assign.

        # Handle explicit submission from draft
        if original_status == "draft" and "submit_for_review" in self.request.POST:
            pg_supervisor = getattr(self.request.user, "supervisor", None)
            if pg_supervisor:
                entry.supervisor = pg_supervisor  # Ensure supervisor is set if not already
                entry.status = "pending"
                # entry.submitted_to_supervisor_at = timezone.now() # Model's save handles this
                messages.success(
                    self.request,
                    f"Logbook entry '{entry.case_title}' submitted for supervisor review.",
                )
            else:
                # This case should ideally be prevented by not showing the button if no supervisor
                messages.error(
                    self.request, "Cannot submit for review: No supervisor assigned to you."
                )
                entry.status = "draft"  # Remain draft

        entry.save()
        self.object = entry
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit Logbook Entry: {self.object.case_title}"
        # The form itself now handles displaying supervisor_feedback_display
        # context['supervisor_feedback'] = self.object.supervisor_feedback
        return context

    def get_success_url(self):
        # Redirect to the PG's logbook list, perhaps with a filter for pending or drafts
        return reverse_lazy("logbook:pg_logbook_list")


# --- Supervisor Dashboard for Pending Reviews ---
class SupervisorLogbookDashboardView(LoginRequiredMixin, SupervisorRequiredMixin, ListView):
    model = LogbookEntry
    template_name = "logbook/supervisor_logbook_dashboard.html"  # Needs to be created
    context_object_name = "pending_entries"
    paginate_by = 10

    def get_queryset(self):
        # Supervisors see entries from their PGs that are 'pending'
        # Order by oldest submission first to encourage timely review
        return (
            LogbookEntry.objects.filter(supervisor=self.request.user, status="pending")
            .select_related("pg")
            .order_by("submitted_to_supervisor_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Pending Logbook Reviews"
        # Optionally, add counts of other statuses for context if needed
        # context['approved_count'] = LogbookEntry.objects.filter(supervisor=self.request.user, status='approved').count()
        # context['returned_count'] = LogbookEntry.objects.filter(supervisor=self.request.user, status='returned').count()
        return context


class SupervisorLogbookAllEntriesView(LoginRequiredMixin, SupervisorRequiredMixin, ListView):
    """
    Comprehensive view for supervisors to see all entries from their assigned PGs
    with filtering and review capabilities.
    """

    model = LogbookEntry
    template_name = "logbook/supervisor_all_entries.html"
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        """Get all entries from assigned PGs with filtering"""
        queryset = (
            LogbookEntry.objects.filter(pg__supervisor=self.request.user)
            .select_related("pg", "rotation__department", "primary_diagnosis", "supervisor")
            .prefetch_related("procedures", "skills", "secondary_diagnoses", "reviews")
        )

        # Apply filters similar to main LogbookEntryListView
        # Status filter
        status_filter = self.request.GET.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # PG filter (for this supervisor's PGs only)
        pg_filter = self.request.GET.get("pg")
        if pg_filter:
            if self.request.user.assigned_pgs.filter(id=pg_filter).exists():
                queryset = queryset.filter(pg_id=pg_filter)

        # Date range filter
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Review status filter
        review_status = self.request.GET.get("review_status")
        if review_status == "pending":
            queryset = queryset.filter(status="pending")
        elif review_status == "reviewed":
            queryset = queryset.filter(status__in=["approved", "rejected", "returned"])
        elif review_status == "needs_action":
            queryset = queryset.filter(status__in=["pending", "returned"])

        # Search functionality
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(case_title__icontains=search_query)
                | Q(pg__first_name__icontains=search_query)
                | Q(pg__last_name__icontains=search_query)
                | Q(patient_chief_complaint__icontains=search_query)
                | Q(primary_diagnosis__name__icontains=search_query)
                | Q(learning_points__icontains=search_query)
            )

        # Sorting
        sort_by = self.request.GET.get("sort", "-submitted_to_supervisor_at")
        valid_sort_fields = [
            "date",
            "-date",
            "created_at",
            "-created_at",
            "submitted_to_supervisor_at",
            "-submitted_to_supervisor_at",
            "status",
            "pg__last_name",
            "case_title",
        ]
        if sort_by in valid_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by("-submitted_to_supervisor_at", "-date")

        return queryset

    def get_context_data(self, **kwargs):
        """Add context for filtering and statistics"""
        context = super().get_context_data(**kwargs)

        # Add assigned PGs for filtering
        context["assigned_pgs"] = self.request.user.assigned_pgs.filter(is_active=True)

        # Add statistics for supervisor dashboard
        all_entries = LogbookEntry.objects.filter(pg__supervisor=self.request.user)
        context["stats"] = {
            "total": all_entries.count(),
            "pending": all_entries.filter(status="pending").count(),
            "approved": all_entries.filter(status="approved").count(),
            "rejected": all_entries.filter(status="rejected").count(),
            "returned": all_entries.filter(status="returned").count(),
            "draft": all_entries.filter(status="draft").count(),
        }

        # Add current filters for display
        context["current_filters"] = {
            "status": self.request.GET.get("status", ""),
            "pg": self.request.GET.get("pg", ""),
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
            "review_status": self.request.GET.get("review_status", ""),
            "search": self.request.GET.get("search", ""),
            "sort": self.request.GET.get("sort", "-submitted_to_supervisor_at"),
        }

        context["page_title"] = "All Logbook Entries - My PGs"

        return context


# --- Supervisor Review Action View ---
class SupervisorLogbookReviewActionView(LoginRequiredMixin, SupervisorRequiredMixin, FormView):
    form_class = SupervisorLogbookReviewForm
    template_name = "logbook/supervisor_review_form.html"  # Needs to be created
    # success_url = reverse_lazy('logbook:supervisor_logbook_dashboard') # Set in form_valid

    def get_logbook_entry(self):
        entry_pk = self.kwargs.get("entry_pk")
        # Ensure the entry belongs to this supervisor and is pending
        entry = get_object_or_404(
            LogbookEntry, pk=entry_pk, supervisor=self.request.user, status="pending"
        )
        return entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logbook_entry"] = self.get_logbook_entry()
        context["page_title"] = f"Review Logbook Entry: {context['logbook_entry'].case_title}"
        return context

    def form_valid(self, form):
        entry = self.get_logbook_entry()
        action = form.cleaned_data["action"]
        supervisor_comment = form.cleaned_data["supervisor_comment"]

        if action == "approve":
            entry.status = "approved"
            messages.success(self.request, f"Logbook entry '{entry.case_title}' approved.")
        elif action == "reject":
            entry.status = "rejected"
            messages.warning(self.request, f"Logbook entry '{entry.case_title}' rejected.")
        elif action == "return_for_edits":
            entry.status = "returned"
            messages.info(
                self.request, f"Logbook entry '{entry.case_title}' returned to resident for edits."
            )

        entry.supervisor_feedback = supervisor_comment
        # entry.supervisor_action_at = timezone.now() # Model's save method handles this
        entry.save()  # This will trigger LogbookEntry's save and _handle_status_change

        # Placeholder for notifying PG
        # self._notify_pg_of_supervisor_action(entry, action)

        return redirect(reverse_lazy("logbook:supervisor_logbook_dashboard"))

    # def _notify_pg_of_supervisor_action(self, entry, action):
    #     # Similar to _notify_supervisor_of_submission in the model
    #     # try:
    #     #     from sims.notifications.models import Notification
    #     #     if entry.pg and Notification:
    #     #         action_map = {
    #     #             'approved': 'approved',
    #     #             'rejected': 'rejected',
    #     #             'return_for_edits': 'returned for edits'
    #     #         }
    #     #         message = f"Your logbook entry '{entry.case_title}' has been {action_map.get(action, 'actioned by')} by your supervisor."
    #     #         Notification.objects.create(
    #     #             user=entry.pg,
    #     #             title=f"Logbook Entry Update: {entry.case_title}",
    #     #             message=message,
    #     #             type='logbook_review',
    #     #             related_object_id=entry.id
    #     #         )
    #     # except ImportError:
    #     #     pass
    #     # except Exception as e:
    #     #     pass # log error
    #     pass

    def get_initial(self):
        """Optionally pre-fill comment if editing a previous review action, though this view is for new actions."""
        # entry = self.get_logbook_entry()
        # return {'supervisor_comment': entry.supervisor_feedback}
        return super().get_initial()


class LogbookEntryCreateRedirectView(LoginRequiredMixin, RedirectView):
    """Redirect /logbook/entry/create/ to /logbook/entry/new/"""

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("logbook:entry_new")


class SupervisorBulkReviewView(LoginRequiredMixin, SupervisorRequiredMixin, FormView):
    """
    Allow supervisors to perform bulk review actions on multiple entries
    """

    template_name = "logbook/supervisor_bulk_review.html"

    def get_form_class(self):
        """Return different form based on action"""
        action = self.request.POST.get("action", self.request.GET.get("action"))
        if action == "bulk_approve":
            return SupervisorBulkApproveForm
        elif action == "bulk_reject":
            return SupervisorBulkRejectForm
        else:
            return SupervisorBulkActionForm

    def get_queryset(self):
        """Get entries that can be bulk reviewed"""
        return LogbookEntry.objects.filter(
            pg__supervisor=self.request.user, status="pending"
        ).select_related("pg", "primary_diagnosis")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_entries"] = self.get_queryset()
        context["page_title"] = "Bulk Review Logbook Entries"
        return context

    def form_valid(self, form):
        """Process bulk review actions"""
        entry_ids = form.cleaned_data.get("entry_ids", [])
        action = form.cleaned_data.get("action")
        comment = form.cleaned_data.get("comment", "")

        entries = self.get_queryset().filter(id__in=entry_ids)

        if not entries.exists():
            messages.error(self.request, "No valid entries selected for review.")
            return self.form_invalid(form)

        updated_count = 0

        for entry in entries:
            if action == "approve":
                entry.status = "approved"
                entry.supervisor_feedback = (
                    comment or f"Bulk approved by {self.request.user.get_full_name()}"
                )
                entry.verified_by = self.request.user
                entry.supervisor_action_at = timezone.now()
                entry.save()
                updated_count += 1

            elif action == "reject":
                entry.status = "rejected"
                entry.supervisor_feedback = comment or "Rejected in bulk review"
                entry.supervisor_action_at = timezone.now()
                entry.save()
                updated_count += 1

            elif action == "return":
                entry.status = "returned"
                entry.supervisor_feedback = comment or "Returned for revision in bulk review"
                entry.supervisor_action_at = timezone.now()
                entry.save()
                updated_count += 1

        if updated_count > 0:
            messages.success(
                self.request, f"Successfully {action}d {updated_count} logbook entries."
            )
        else:
            messages.warning(self.request, "No entries were updated.")

        return redirect("logbook:supervisor_logbook_dashboard")
