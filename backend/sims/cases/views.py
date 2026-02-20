from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CaseFilterForm, CaseReviewForm, CaseSearchForm, ClinicalCaseForm
from .models import CaseCategory, CaseReview, CaseStatistics, ClinicalCase


class RoleRequiredMixin:
    """Mixin to enforce role-based access control"""

    required_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "role") or request.user.role not in self.required_roles:
            raise PermissionDenied("You don't have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)


class CaseListView(LoginRequiredMixin, ListView):
    """List view for clinical cases with filtering and role-based access"""

    model = ClinicalCase
    template_name = "cases/case_list.html"
    context_object_name = "cases"
    paginate_by = 20

    def get_queryset(self):
        """Filter cases based on user role and search parameters"""
        queryset = ClinicalCase.objects.select_related(
            "pg", "supervisor", "category", "primary_diagnosis", "rotation"
        ).prefetch_related("secondary_diagnoses", "procedures_performed")

        # Role-based filtering
        if hasattr(self.request.user, "role"):
            if self.request.user.role == "pg":
                queryset = queryset.filter(pg=self.request.user)
            elif self.request.user.role == "supervisor":
                queryset = queryset.filter(
                    Q(supervisor=self.request.user) | Q(rotation__supervisor=self.request.user)
                )

        # Apply search filters
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(case_title__icontains=search_query)
                | Q(patient_initials__icontains=search_query)
                | Q(primary_diagnosis__name__icontains=search_query)
                | Q(learning_points__icontains=search_query)
            )

        # Apply filters
        status_filter = self.request.GET.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        category_filter = self.request.GET.get("category")
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)

        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        if date_from:
            queryset = queryset.filter(date_encountered__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_encountered__lte=date_to)

        return queryset.order_by("-date_encountered", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = CaseSearchForm(self.request.GET)
        context["filter_form"] = CaseFilterForm(self.request.GET)
        context["categories"] = CaseCategory.objects.filter(is_active=True)

        # Add statistics for the current user
        if hasattr(self.request.user, "role") and self.request.user.role == "pg":
            stats, created = CaseStatistics.objects.get_or_create(
                pg=self.request.user, defaults={"total_cases": 0}
            )
            context["user_stats"] = stats

        return context


class CaseDetailView(LoginRequiredMixin, DetailView):
    """Detailed view of a clinical case"""

    model = ClinicalCase
    template_name = "cases/case_detail.html"
    context_object_name = "case"

    def get_queryset(self):
        """Ensure user can only view cases they have access to"""
        queryset = ClinicalCase.objects.select_related(
            "pg", "supervisor", "category", "primary_diagnosis", "rotation"
        ).prefetch_related("secondary_diagnoses", "procedures_performed")

        if hasattr(self.request.user, "role"):
            if self.request.user.role == "pg":
                return queryset.filter(pg=self.request.user)
            elif self.request.user.role == "supervisor":
                return queryset.filter(
                    Q(supervisor=self.request.user) | Q(rotation__supervisor=self.request.user)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get related reviews
        context["reviews"] = (
            CaseReview.objects.filter(case=self.object)
            .select_related("reviewer")
            .order_by("-review_date")
        )

        # Check if current user can review this case
        context["can_review"] = (
            hasattr(self.request.user, "role")
            and self.request.user.role == "supervisor"
            and (
                self.object.supervisor == self.request.user
                or (self.object.rotation and self.object.rotation.supervisor == self.request.user)
            )
        )

        # Check if user can edit this case
        context["can_edit"] = self._can_edit_case()

        return context

    def _can_edit_case(self):
        """Check if current user can edit this case"""
        if hasattr(self.request.user, "role"):
            if self.request.user.role == "pg":
                return self.object.pg == self.request.user and self.object.status not in [
                    "approved"
                ]
            elif self.request.user.role == "supervisor":
                return self.object.supervisor == self.request.user or (
                    self.object.rotation and self.object.rotation.supervisor == self.request.user
                )
        return False


class CaseCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Create new clinical case"""

    model = ClinicalCase
    form_class = ClinicalCaseForm
    template_name = "cases/case_form.html"
    required_roles = ["pg", "supervisor", "admin"]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set the PG and handle initial status"""
        if hasattr(self.request.user, "role") and self.request.user.role == "pg":
            form.instance.pg = self.request.user

        form.instance.status = "draft"
        response = super().form_valid(form)

        messages.success(self.request, "Clinical case created successfully!")
        return response

    def get_success_url(self):
        return reverse("cases:case_detail", kwargs={"pk": self.object.pk})


class CaseUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing clinical case"""

    model = ClinicalCase
    form_class = ClinicalCaseForm
    template_name = "cases/case_form.html"

    def get_queryset(self):
        """Ensure user can only edit cases they have permission for"""
        queryset = ClinicalCase.objects.all()

        if hasattr(self.request.user, "role"):
            if self.request.user.role == "pg":
                return queryset.filter(pg=self.request.user, status__in=["draft", "needs_revision"])
            elif self.request.user.role == "supervisor":
                return queryset.filter(
                    Q(supervisor=self.request.user) | Q(rotation__supervisor=self.request.user)
                )

        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Clinical case updated successfully!")
        return response

    def get_success_url(self):
        return reverse("cases:case_detail", kwargs={"pk": self.object.pk})


class CaseDeleteView(LoginRequiredMixin, DeleteView):
    """Delete clinical case (only for draft cases)"""

    model = ClinicalCase
    template_name = "cases/case_confirm_delete.html"
    success_url = reverse_lazy("cases:case_list")

    def get_queryset(self):
        """Only allow deletion of draft cases by their owners"""
        queryset = ClinicalCase.objects.filter(status="draft")

        if hasattr(self.request.user, "role") and self.request.user.role == "pg":
            return queryset.filter(pg=self.request.user)

        return queryset

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Clinical case deleted successfully!")
        return super().delete(request, *args, **kwargs)


@login_required
def submit_case(request, pk):
    """Submit a case for review"""
    case = get_object_or_404(ClinicalCase, pk=pk)

    # Check permissions
    if not (
        hasattr(request.user, "role") and request.user.role == "pg" and case.pg == request.user
    ):
        raise PermissionDenied("You can only submit your own cases.")

    if case.status != "draft":
        messages.error(request, "Only draft cases can be submitted.")
        return redirect("cases:case_detail", pk=pk)

    # Validate case completeness
    if not case.is_complete():
        messages.error(request, "Please complete all required fields before submitting.")
        return redirect("cases:case_update", pk=pk)

    case.status = "submitted"
    case.submitted_at = timezone.now()
    case.save()

    messages.success(request, "Case submitted for review successfully!")
    return redirect("cases:case_detail", pk=pk)


class CaseReviewCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """Create a review for a clinical case"""

    model = CaseReview
    form_class = CaseReviewForm
    template_name = "cases/review_form.html"
    required_roles = ["supervisor", "admin"]

    def dispatch(self, request, *args, **kwargs):
        self.case = get_object_or_404(ClinicalCase, pk=kwargs["case_pk"])

        # Check if supervisor can review this case
        if hasattr(request.user, "role") and request.user.role == "supervisor":
            if not (
                self.case.supervisor == request.user
                or (self.case.rotation and self.case.rotation.supervisor == request.user)
            ):
                raise PermissionDenied("You can only review cases assigned to you.")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["case"] = self.case
        return kwargs

    def form_valid(self, form):
        form.instance.case = self.case
        form.instance.reviewer = self.request.user
        form.instance.review_date = timezone.now()

        response = super().form_valid(form)

        # Update case status based on review status
        if form.instance.status == "approved":
            self.case.status = "approved"
        elif form.instance.status == "needs_revision":
            self.case.status = "needs_revision"
        elif form.instance.status == "rejected":
            self.case.status = "rejected"

        self.case.reviewed_at = timezone.now()
        self.case.save()

        messages.success(self.request, "Case review completed successfully!")
        return response

    def get_success_url(self):
        return reverse("cases:case_detail", kwargs={"pk": self.case.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["case"] = self.case
        return context


@login_required
def case_statistics_view(request):
    """Display case statistics dashboard"""
    if not hasattr(request.user, "role"):
        raise PermissionDenied("Access denied.")

    context = {}

    if request.user.role == "pg":
        # PG dashboard - personal statistics
        stats, created = CaseStatistics.objects.get_or_create(
            pg=request.user, defaults={"total_cases": 0}
        )

        # Refresh statistics
        stats.update_statistics()
        stats.save()

        context.update(
            {
                "user_stats": stats,
                "recent_cases": ClinicalCase.objects.filter(pg=request.user).order_by(
                    "-created_at"
                )[:5],
                "pending_reviews": ClinicalCase.objects.filter(
                    pg=request.user, status__in=["submitted", "under_review"]
                ).count(),
            }
        )

    elif request.user.role == "supervisor":
        # Supervisor dashboard - overview of supervised cases
        supervised_cases = ClinicalCase.objects.filter(
            Q(supervisor=request.user) | Q(rotation__supervisor=request.user)
        )

        # Get unique PGs supervised by this supervisor
        supervised_pgs_count = supervised_cases.values("pg").distinct().count()

        # Create supervisor stats object
        supervisor_stats = {
            "total_pgs": supervised_pgs_count,
            "total_cases": supervised_cases.count(),
            "pending_reviews": supervised_cases.filter(
                status__in=["submitted", "under_review"]
            ).count(),
        }

        context.update(
            {
                "supervisor_stats": supervisor_stats,
                "total_supervised_cases": supervised_cases.count(),
                "pending_reviews": supervised_cases.filter(
                    status__in=["submitted", "under_review"]
                ).count(),
                "recent_submissions": supervised_cases.filter(status="submitted").order_by(
                    "-created_at"
                )[:10],
                "case_stats_by_status": supervised_cases.values("status").annotate(
                    count=Count("id")
                ),
                "average_scores": supervised_cases.filter(
                    supervisor_assessment_score__isnull=False
                ).aggregate(avg_score=Avg("supervisor_assessment_score")),
            }
        )

    elif request.user.role == "admin":
        # Admin dashboard - system-wide statistics
        from django.contrib.auth import get_user_model

        User = get_user_model()

        total_cases = ClinicalCase.objects.all()
        total_pgs = User.objects.filter(role="pg", is_active=True).count()
        total_supervisors = User.objects.filter(role="supervisor", is_active=True).count()
        pending_reviews = total_cases.filter(status__in=["submitted", "under_review"]).count()

        system_stats = {
            "total_cases": total_cases.count(),
            "total_pgs": total_pgs,
            "total_supervisors": total_supervisors,
            "pending_reviews": pending_reviews,
        }

        context.update(
            {
                "system_stats": system_stats,
                "total_cases": total_cases.count(),
                "cases_by_status": total_cases.values("status").annotate(count=Count("id")),
                "cases_by_category": total_cases.values(
                    "category__name", "category__color_code"
                ).annotate(count=Count("id")),
                "recent_activity": total_cases.order_by("-created_at")[:10],
                "top_performers": total_cases.values("pg__first_name", "pg__last_name")
                .annotate(case_count=Count("id"), avg_score=Avg("supervisor_assessment_score"))
                .filter(case_count__gt=0)
                .order_by("-case_count")[:10],
            }
        )

    return render(request, "cases/statistics.html", context)


@login_required
def case_export_data(request):
    """Export case data for analytics (JSON endpoint)"""
    if not hasattr(request.user, "role") or request.user.role not in ["supervisor", "admin"]:
        raise PermissionDenied("Access denied.")

    # Get cases based on user role
    if request.user.role == "supervisor":
        cases = ClinicalCase.objects.filter(
            Q(supervisor=request.user) | Q(rotation__supervisor=request.user)
        )
    else:  # admin
        cases = ClinicalCase.objects.all()

    # Prepare data for export
    data = []
    for case in cases.select_related("pg", "category", "primary_diagnosis"):
        data.append(
            {
                "id": case.id,
                "title": case.case_title,
                "pg": case.pg.get_full_name() if case.pg else "",
                "category": case.category.name if case.category else "",
                "date": case.date.isoformat() if case.date else "",
                "status": case.status,
                "score": case.completion_score,
                "primary_diagnosis": case.primary_diagnosis.name if case.primary_diagnosis else "",
            }
        )

    return JsonResponse({"cases": data})


# AJAX endpoints for dynamic functionality
@login_required
def get_diagnoses_json(request):
    """Get diagnoses for autocomplete (AJAX endpoint)"""
    term = request.GET.get("term", "")
    if len(term) >= 2:
        from sims.logbook.models import Diagnosis

        diagnoses = Diagnosis.objects.filter(name__icontains=term)[:10]

        results = [{"id": d.id, "text": d.name} for d in diagnoses]
        return JsonResponse({"results": results})

    return JsonResponse({"results": []})


@login_required
def get_procedures_json(request):
    """Get procedures for autocomplete (AJAX endpoint)"""
    term = request.GET.get("term", "")
    if len(term) >= 2:
        from sims.logbook.models import Procedure

        procedures = Procedure.objects.filter(name__icontains=term)[:10]

        results = [{"id": p.id, "text": p.name} for p in procedures]
        return JsonResponse({"results": results})

    return JsonResponse({"results": []})
