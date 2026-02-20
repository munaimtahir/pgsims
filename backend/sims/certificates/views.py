import csv
import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
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
    BulkCertificateApprovalForm,
    CertificateCreateForm,
    CertificateReviewForm,
    CertificateSearchForm,
    CertificateUpdateForm,
)
from .models import Certificate, CertificateReview, CertificateStatistics, CertificateType

User = get_user_model()


class CertificateAccessMixin(UserPassesTestMixin):
    """
    Mixin to control access to certificate views based on user role.

    Created: 2025-05-29 16:58:20 UTC
    Author: SMIB2012
    """

    def test_func(self):
        """Test if user has access to certificate features"""
        if not self.request.user.is_authenticated:
            return False

        # Admins have full access
        if self.request.user.role == "admin" or self.request.user.is_superuser:
            return True

        # Supervisors have access to their PGs' certificates
        if self.request.user.role == "supervisor":
            return True

        # PGs have access to their own certificates
        if self.request.user.role == "pg":
            return True

        return False


class CertificateListView(LoginRequiredMixin, CertificateAccessMixin, ListView):
    """View for listing certificates with filtering and search"""

    model = Certificate
    template_name = "certificates/certificate_list.html"
    context_object_name = "certificates"
    paginate_by = 20

    def get_queryset(self):
        """Filter certificates based on user role and search parameters"""
        queryset = Certificate.objects.select_related(
            "pg", "certificate_type", "created_by", "verified_by"
        ).prefetch_related("reviews")

        # Role-based filtering
        if self.request.user.role == "supervisor":
            queryset = queryset.filter(pg__supervisor=self.request.user)
        elif self.request.user.role == "pg":
            queryset = queryset.filter(pg=self.request.user)

        # Search and filter
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(pg__first_name__icontains=search_query)
                | Q(pg__last_name__icontains=search_query)
                | Q(pg__username__icontains=search_query)
                | Q(issuing_organization__icontains=search_query)
                | Q(certificate_number__icontains=search_query)
            )

        # Status filter
        status_filter = self.request.GET.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Certificate type filter
        cert_type = self.request.GET.get("certificate_type")
        if cert_type:
            queryset = queryset.filter(certificate_type_id=cert_type)

        # Date range filter
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date:
            queryset = queryset.filter(issue_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(issue_date__lte=end_date)

        # Expiry filter
        expiry_filter = self.request.GET.get("expiry")
        if expiry_filter == "expiring":
            # Certificates expiring within 90 days
            expiry_date = timezone.now().date() + timedelta(days=90)
            queryset = queryset.filter(
                expiry_date__isnull=False,
                expiry_date__lte=expiry_date,
                expiry_date__gt=timezone.now().date(),
            )
        elif expiry_filter == "expired":
            queryset = queryset.filter(
                expiry_date__isnull=False, expiry_date__lt=timezone.now().date()
            )

        # Verification filter
        verified_filter = self.request.GET.get("verified")
        if verified_filter == "verified":
            queryset = queryset.filter(is_verified=True)
        elif verified_filter == "unverified":
            queryset = queryset.filter(is_verified=False)

        # Sorting
        sort_by = self.request.GET.get("sort", "-created_at")
        queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)

        # Add search form
        context["search_form"] = CertificateSearchForm(self.request.GET)

        # Add filter options
        context["certificate_types"] = CertificateType.objects.filter(is_active=True)

        # Add statistics
        certificates = self.get_queryset()
        context["stats"] = {
            "total": certificates.count(),
            "approved": certificates.filter(status="approved").count(),
            "pending": certificates.filter(status="pending").count(),
            "rejected": certificates.filter(status="rejected").count(),
            "expired": certificates.filter(status="expired").count(),
            "expiring_soon": certificates.filter(
                expiry_date__isnull=False,
                expiry_date__lte=timezone.now().date() + timedelta(days=30),
                expiry_date__gt=timezone.now().date(),
            ).count(),
        }

        # Add current filters for display
        context["current_filters"] = {
            "search": self.request.GET.get("search", ""),
            "status": self.request.GET.get("status", ""),
            "certificate_type": self.request.GET.get("certificate_type", ""),
            "start_date": self.request.GET.get("start_date", ""),
            "end_date": self.request.GET.get("end_date", ""),
            "expiry": self.request.GET.get("expiry", ""),
            "verified": self.request.GET.get("verified", ""),
        }

        return context


class CertificateDetailView(LoginRequiredMixin, CertificateAccessMixin, DetailView):
    """Detailed view of a single certificate"""

    model = Certificate
    template_name = "certificates/certificate_detail.html"
    context_object_name = "certificate"

    def get_object(self):
        """Get certificate with permission check"""
        certificate = get_object_or_404(Certificate, pk=self.kwargs["pk"])

        # Check if user has permission to view this certificate
        if self.request.user.role == "supervisor":
            if certificate.pg.supervisor != self.request.user:
                raise PermissionDenied("You don't have permission to view this certificate")
        elif self.request.user.role == "pg":
            if certificate.pg != self.request.user:
                raise PermissionDenied("You can only view your own certificates")

        return certificate

    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)

        certificate = self.object

        # Add reviews
        context["reviews"] = certificate.reviews.select_related("reviewer").order_by("-created_at")

        # Add validity information
        context["is_expired"] = certificate.is_expired()
        context["is_expiring_soon"] = certificate.is_expiring_soon()
        context["days_until_expiry"] = certificate.get_days_until_expiry()
        context["validity_status"] = certificate.get_validity_status()

        # Add permission flags
        context["can_review"] = self.can_user_review(certificate)
        context["can_edit"] = self.can_user_edit(certificate)
        context["can_delete"] = self.can_user_delete(certificate)
        context["can_download"] = self.can_user_download(certificate)

        # Add related certificates for the PG
        if certificate.pg:
            context["related_certificates"] = (
                Certificate.objects.filter(pg=certificate.pg)
                .exclude(pk=certificate.pk)
                .order_by("-issue_date")[:5]
            )

        return context

    def can_user_review(self, certificate):
        """Check if current user can review this certificate"""
        user = self.request.user

        if user.role == "admin":
            return True
        elif user.role == "supervisor":
            return user == certificate.pg.supervisor and certificate.status in [
                "pending",
                "under_review",
            ]

        return False

    def can_user_edit(self, certificate):
        """Check if current user can edit this certificate"""
        user = self.request.user

        if user.role == "admin":
            return certificate.can_be_edited()
        elif user.role == "pg" and user == certificate.pg:
            return certificate.can_be_edited()

        return False

    def can_user_delete(self, certificate):
        """Check if current user can delete this certificate"""
        user = self.request.user

        if user.role == "admin":
            return certificate.can_be_deleted()
        elif user.role == "pg" and user == certificate.pg:
            return certificate.can_be_deleted()

        return False

    def can_user_download(self, certificate):
        """Check if current user can download this certificate"""
        user = self.request.user

        if user.role == "admin":
            return True
        elif user.role == "supervisor":
            return user == certificate.pg.supervisor
        elif user.role == "pg":
            return user == certificate.pg

        return False


class CertificateCreateView(LoginRequiredMixin, CertificateAccessMixin, CreateView):
    """View for creating new certificates"""

    model = Certificate
    form_class = CertificateCreateForm
    template_name = "certificates/certificate_form.html"

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set created_by field and handle success"""
        form.instance.created_by = self.request.user

        # For PGs, set themselves as the certificate owner
        if self.request.user.role == "pg":
            form.instance.pg = self.request.user

        messages.success(
            self.request,
            f"Certificate '{form.instance.title}' uploaded successfully and is pending review",
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to certificate detail page"""
        return reverse("certificates:detail", kwargs={"pk": self.object.pk})


class CertificateUpdateView(LoginRequiredMixin, CertificateAccessMixin, UpdateView):
    """View for updating existing certificates"""

    model = Certificate
    form_class = CertificateUpdateForm
    template_name = "certificates/certificate_form.html"

    def get_object(self):
        """Get certificate with permission check"""
        certificate = get_object_or_404(Certificate, pk=self.kwargs["pk"])

        # Check if user has permission to edit this certificate
        if self.request.user.role == "supervisor":
            if certificate.pg.supervisor != self.request.user:
                raise PermissionDenied("You can only edit certificates of your assigned PGs")
        elif self.request.user.role == "pg":
            if certificate.pg != self.request.user:
                raise PermissionDenied("You can only edit your own certificates")

        if not certificate.can_be_edited():
            raise PermissionDenied("This certificate cannot be edited")

        return certificate

    def get_form_kwargs(self):
        """Pass current user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Handle successful form submission"""
        # Reset status to pending if certificate was rejected and now updated
        if self.object.status == "rejected":
            form.instance.status = "pending"

        messages.success(self.request, f"Certificate '{form.instance.title}' updated successfully")

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to certificate detail page"""
        return reverse("certificates:detail", kwargs={"pk": self.object.pk})


class CertificateDeleteView(LoginRequiredMixin, CertificateAccessMixin, DeleteView):
    """View for deleting certificates"""

    model = Certificate
    template_name = "certificates/certificate_confirm_delete.html"
    success_url = reverse_lazy("certificates:list")

    def get_object(self):
        """Get certificate with permission check"""
        certificate = get_object_or_404(Certificate, pk=self.kwargs["pk"])

        # Check permissions
        if self.request.user.role == "supervisor":
            raise PermissionDenied("Supervisors cannot delete certificates")
        elif self.request.user.role == "pg":
            if certificate.pg != self.request.user:
                raise PermissionDenied("You can only delete your own certificates")

        if not certificate.can_be_deleted():
            raise PermissionDenied("This certificate cannot be deleted")

        return certificate

    def delete(self, request, *args, **kwargs):
        """Handle deletion with success message"""
        certificate = self.get_object()
        messages.success(request, f"Certificate '{certificate.title}' has been deleted")

        return super().delete(request, *args, **kwargs)


class CertificateReviewCreateView(LoginRequiredMixin, CertificateAccessMixin, CreateView):
    """View for creating certificate reviews"""

    model = CertificateReview
    form_class = CertificateReviewForm
    template_name = "certificates/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Get certificate and check permissions"""
        self.certificate = get_object_or_404(Certificate, pk=kwargs["certificate_pk"])

        # Check if user can review this certificate
        if request.user.role == "supervisor":
            if self.certificate.pg.supervisor != request.user:
                raise PermissionDenied("You can only review certificates of your assigned PGs")
        elif request.user.role != "admin":
            raise PermissionDenied("You don't have permission to review certificates")

        if self.certificate.status not in ["pending", "under_review"]:
            raise PermissionDenied("This certificate cannot be reviewed")

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pass certificate and user to form"""
        kwargs = super().get_form_kwargs()
        kwargs["certificate"] = self.certificate
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set certificate and reviewer fields"""
        form.instance.certificate = self.certificate
        form.instance.reviewer = self.request.user

        messages.success(
            self.request, f"Review submitted for certificate '{self.certificate.title}'"
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to certificate detail page"""
        return reverse("certificates:detail", kwargs={"pk": self.certificate.pk})

    def get_context_data(self, **kwargs):
        """Add certificate to context"""
        context = super().get_context_data(**kwargs)
        context["certificate"] = self.certificate
        return context


class CertificateReviewDetailView(LoginRequiredMixin, CertificateAccessMixin, DetailView):
    """View for displaying review details"""

    model = CertificateReview
    template_name = "certificates/review_detail.html"
    context_object_name = "review"

    def get_object(self):
        """Get review with permission check"""
        review = get_object_or_404(CertificateReview, pk=self.kwargs["pk"])

        # Check if user has permission to view this review
        user = self.request.user
        certificate = review.certificate

        if user.role == "supervisor":
            if certificate.pg.supervisor != user and review.reviewer != user:
                raise PermissionDenied("You don't have permission to view this review")
        elif user.role == "pg":
            if certificate.pg != user:
                raise PermissionDenied("You can only view reviews of your own certificates")

        return review


class CertificateDashboardView(LoginRequiredMixin, CertificateAccessMixin, TemplateView):
    """Dashboard view for certificate overview"""

    template_name = "certificates/dashboard.html"

    def get_context_data(self, **kwargs):
        """Add dashboard statistics and data"""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Base queryset based on user role
        if user.role == "admin":
            certificates = Certificate.objects.all()
        elif user.role == "supervisor":
            certificates = Certificate.objects.filter(pg__supervisor=user)
        elif user.role == "pg":
            certificates = Certificate.objects.filter(pg=user)
        else:
            certificates = Certificate.objects.none()

        # Current date for calculations
        today = timezone.now().date()

        # Statistics
        context["stats"] = {
            "total_certificates": certificates.count(),
            "approved_certificates": certificates.filter(status="approved").count(),
            "pending_certificates": certificates.filter(status="pending").count(),
            "rejected_certificates": certificates.filter(status="rejected").count(),
            "expired_certificates": certificates.filter(status="expired").count(),
            "expiring_soon": certificates.filter(
                expiry_date__isnull=False,
                expiry_date__lte=today + timedelta(days=30),
                expiry_date__gt=today,
            ).count(),
        }

        # Recent certificates
        context["recent_certificates"] = certificates.select_related(
            "pg", "certificate_type", "created_by"
        ).order_by("-created_at")[:5]

        # Expiring certificates
        context["expiring_certificates"] = (
            certificates.filter(
                expiry_date__isnull=False,
                expiry_date__lte=today + timedelta(days=60),
                expiry_date__gt=today,
                status="approved",
            )
            .select_related("pg", "certificate_type")
            .order_by("expiry_date")[:5]
        )

        # Pending reviews (for supervisors and admins)
        if user.role in ["admin", "supervisor"]:
            context["pending_reviews"] = certificates.filter(
                status__in=["pending", "under_review"]
            ).select_related("pg", "certificate_type")[:5]
        # Certificate type distribution
        certificate_distribution = (
            certificates.values("certificate_type__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        context["certificate_distribution"] = certificate_distribution
        # JSON serialized data for JavaScript charts
        context["certificate_distribution_json"] = json.dumps(list(certificate_distribution))

        # CME/CPD totals (for PGs)
        if user.role == "pg":
            approved_certs = certificates.filter(status="approved")
            context["cme_points"] = sum(cert.cme_points_earned for cert in approved_certs)
            context["cpd_credits"] = sum(cert.cpd_credits_earned for cert in approved_certs)

            # Compliance status
            required_types = CertificateType.objects.filter(is_required=True)
            user_required_certs = (
                certificates.filter(certificate_type__in=required_types, status="approved")
                .values("certificate_type")
                .distinct()
                .count()
            )

            context["compliance_rate"] = (
                (user_required_certs / required_types.count() * 100)
                if required_types.count() > 0
                else 100
            )

        # Performance metrics (for admins)
        if user.role == "admin":
            context["performance_metrics"] = self.get_performance_metrics(certificates)

        return context

    def get_performance_metrics(self, certificates):
        """Calculate performance metrics for admin dashboard"""
        total_certs = certificates.count()
        if total_certs == 0:
            return {}

        approved_count = certificates.filter(status="approved").count()
        rejected_count = certificates.filter(status="rejected").count()

        return {
            "approval_rate": (approved_count / total_certs * 100) if total_certs > 0 else 0,
            "rejection_rate": (rejected_count / total_certs * 100) if total_certs > 0 else 0,
            "average_review_time": self.calculate_average_review_time(certificates),
            "top_issuers": certificates.values("issuing_organization")
            .annotate(count=Count("id"))
            .order_by("-count")[:5],
        }

    def calculate_average_review_time(self, certificates):
        """Calculate average time from upload to approval"""
        approved_certs = certificates.filter(status="approved", verified_at__isnull=False)

        if not approved_certs.exists():
            return 0

        total_days = 0
        count = 0

        for cert in approved_certs:
            days_diff = (cert.verified_at.date() - cert.created_at.date()).days
            total_days += days_diff
            count += 1

        return total_days / count if count > 0 else 0


class BulkCertificateApprovalView(LoginRequiredMixin, CertificateAccessMixin, FormView):
    """View for bulk certificate approval"""

    template_name = "certificates/bulk_approval.html"
    form_class = BulkCertificateApprovalForm
    success_url = reverse_lazy("certificates:list")

    def test_func(self):
        """Only admins and supervisors can do bulk approvals"""
        return super().test_func() and self.request.user.role in ["admin", "supervisor"]

    def form_valid(self, form):
        """Process bulk approval"""
        approved_count = 0
        rejected_count = 0

        try:
            for cert_id in form.cleaned_data["certificates"]:
                certificate = Certificate.objects.get(id=cert_id)

                # Check permissions
                if (
                    self.request.user.role == "supervisor"
                    and certificate.pg.supervisor != self.request.user
                ):
                    continue

                action = form.cleaned_data["action"]
                if action == "approve":
                    certificate.status = "approved"
                    certificate.verified_by = self.request.user
                    certificate.verified_at = timezone.now()
                    certificate.save()
                    approved_count += 1
                elif action == "reject":
                    certificate.status = "rejected"
                    certificate.save()
                    rejected_count += 1

            if approved_count > 0:
                messages.success(
                    self.request, f"Successfully approved {approved_count} certificates"
                )
            if rejected_count > 0:
                messages.success(
                    self.request, f"Successfully rejected {rejected_count} certificates"
                )

        except Exception as e:
            messages.error(self.request, f"Error processing certificates: {str(e)}")

        return super().form_valid(form)


# API Views for AJAX functionality


@login_required
def certificate_stats_api(request):
    """API endpoint for certificate statistics"""
    user = request.user

    # Get certificates based on user role
    if user.role == "admin":
        certificates = Certificate.objects.all()
    elif user.role == "supervisor":
        certificates = Certificate.objects.filter(pg__supervisor=user)
    elif user.role == "pg":
        certificates = Certificate.objects.filter(pg=user)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Calculate statistics
    stats = {
        "total": certificates.count(),
        "by_status": {
            status[0]: certificates.filter(status=status[0]).count()
            for status in Certificate.STATUS_CHOICES
        },
        "by_type": list(
            certificates.values("certificate_type__name")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        ),
        "expiring_soon": certificates.filter(
            expiry_date__isnull=False,
            expiry_date__lte=timezone.now().date() + timedelta(days=30),
            expiry_date__gt=timezone.now().date(),
        ).count(),
    }

    return JsonResponse(stats)


@login_required
def certificate_download(request, pk):
    """Download certificate file"""
    certificate = get_object_or_404(Certificate, pk=pk)

    # Check permissions
    user = request.user
    if user.role == "supervisor":
        if certificate.pg.supervisor != user:
            raise PermissionDenied("You don't have permission to download this certificate")
    elif user.role == "pg":
        if certificate.pg != user:
            raise PermissionDenied("You can only download your own certificates")
    elif user.role not in ["admin"]:
        raise PermissionDenied("You don't have permission to download certificates")

    if not certificate.certificate_file:
        raise Http404("Certificate file not found")

    return FileResponse(
        certificate.certificate_file.open("rb"),
        as_attachment=True,
        filename=certificate.certificate_file.name.split("/")[-1],
    )


@login_required
def export_certificates_csv(request):
    """Export certificates to CSV"""
    user = request.user

    # Get certificates based on user role
    if user.role == "admin":
        certificates = Certificate.objects.all()
    elif user.role == "supervisor":
        certificates = Certificate.objects.filter(pg__supervisor=user)
    elif user.role == "pg":
        certificates = Certificate.objects.filter(pg=user)
    else:
        raise PermissionDenied("You don't have permission to export certificates")

    # Create CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="certificates_export.csv"'

    writer = csv.writer(response)

    # Write header
    writer.writerow(
        [
            "PG Name",
            "PG Username",
            "Certificate Title",
            "Certificate Type",
            "Issuing Organization",
            "Issue Date",
            "Expiry Date",
            "Status",
            "Is Verified",
            "CME Points",
            "CPD Credits",
            "Created Date",
        ]
    )

    # Write data
    for cert in certificates.select_related("pg", "certificate_type"):
        writer.writerow(
            [
                cert.pg.get_full_name() if cert.pg else "",
                cert.pg.username if cert.pg else "",
                cert.title,
                cert.certificate_type.name if cert.certificate_type else "",
                cert.issuing_organization,
                cert.issue_date,
                cert.expiry_date or "",
                cert.get_status_display(),
                "Yes" if cert.is_verified else "No",
                cert.cme_points_earned,
                cert.cpd_credits_earned,
                cert.created_at.date(),
            ]
        )

    return response


@login_required
def certificate_verification_api(request, pk):
    """API endpoint to verify a certificate"""
    certificate = get_object_or_404(Certificate, pk=pk)

    # Check permissions
    if request.user.role not in ["admin", "supervisor"]:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.user.role == "supervisor":
        if certificate.pg.supervisor != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        certificate.is_verified = True
        certificate.verified_by = request.user
        certificate.verified_at = timezone.now()
        certificate.save()

        return JsonResponse({"success": True, "message": "Certificate verified successfully"})

    return JsonResponse({"error": "Method not allowed"}, status=405)


# Utility Views


@login_required
def certificate_quick_stats(request):
    """Quick stats widget for dashboard"""
    user = request.user

    if user.role == "admin":
        certificates = Certificate.objects.all()
    elif user.role == "supervisor":
        certificates = Certificate.objects.filter(pg__supervisor=user)
    elif user.role == "pg":
        certificates = Certificate.objects.filter(pg=user)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    today = timezone.now().date()

    stats = {
        "pending": certificates.filter(status="pending").count(),
        "approved": certificates.filter(status="approved").count(),
        "expiring_soon": certificates.filter(
            expiry_date__isnull=False,
            expiry_date__lte=today + timedelta(days=30),
            expiry_date__gt=today,
        ).count(),
        "expired": certificates.filter(status="expired").count(),
    }

    return JsonResponse(stats)


@login_required
def update_certificate_statistics(request):
    """Update certificate statistics for all PGs"""
    if request.user.role != "admin":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        CertificateStatistics.update_all_statistics()
        return JsonResponse({"success": True, "message": "Statistics updated successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


class CertificateComplianceView(LoginRequiredMixin, CertificateAccessMixin, TemplateView):
    """View for certificate compliance reporting"""

    template_name = "certificates/compliance.html"

    def test_func(self):
        """Only admins and supervisors can view compliance reports"""
        return super().test_func() and self.request.user.role in ["admin", "supervisor"]

    def get_context_data(self, **kwargs):
        """Add compliance data to context"""
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Get PGs based on user role
        if user.role == "admin":
            from sims.users.models import User

            pgs = User.objects.filter(role="pg", is_active=True)
        elif user.role == "supervisor":
            pgs = User.objects.filter(role="pg", supervisor=user, is_active=True)
        else:
            pgs = User.objects.none()

        # Get required certificate types
        required_types = CertificateType.objects.filter(is_required=True)

        # Calculate compliance for each PG
        compliance_data = []
        for pg in pgs:
            pg_certs = Certificate.objects.filter(pg=pg, status="approved")

            pg_cert_types = set(pg_certs.values_list("certificate_type", flat=True))
            required_type_ids = set(required_types.values_list("id", flat=True))

            missing_required = required_types.exclude(id__in=pg_cert_types)

            compliance_rate = (
                (len(pg_cert_types & required_type_ids) / len(required_type_ids) * 100)
                if required_type_ids
                else 100
            )

            compliance_data.append(
                {
                    "pg": pg,
                    "total_certificates": pg_certs.count(),
                    "required_certificates": len(pg_cert_types & required_type_ids),
                    "missing_required": missing_required,
                    "compliance_rate": compliance_rate,
                    "last_certificate": pg_certs.order_by("-issue_date").first(),
                }
            )

        # Sort by compliance rate (lowest first)
        compliance_data.sort(key=lambda x: x["compliance_rate"])

        context["compliance_data"] = compliance_data
        context["required_types"] = required_types
        context["overall_compliance"] = (
            sum(data["compliance_rate"] for data in compliance_data) / len(compliance_data)
            if compliance_data
            else 100
        )

        return context
