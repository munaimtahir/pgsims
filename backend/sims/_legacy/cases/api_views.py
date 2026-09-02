from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.cases.api_serializers import (
    CaseCategorySerializer,
    CaseReviewSerializer,
    ClinicalCaseSerializer,
)
from sims.cases.models import CaseCategory, CaseReview, ClinicalCase
from sims.logbook.models import Diagnosis


def _is_supervisor_of_case(user, case):
    return bool(case.pg and case.pg.supervisor_id == user.id)


def _can_read_case(user, case):
    if user.role == "pg":
        return case.pg_id == user.id
    if user.role == "supervisor":
        return _is_supervisor_of_case(user, case)
    return user.role in {"admin", "utrmc_user", "utrmc_admin"}


class CaseCategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = CaseCategory.objects.filter(is_active=True).order_by("sort_order", "name")
        return Response(CaseCategorySerializer(queryset, many=True).data)


class PGCaseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "pg":
            return Response({"detail": "Only PG users can access this endpoint."}, status=403)
        queryset = ClinicalCase.objects.filter(pg=request.user, is_active=True).order_by("-created_at")
        return Response(ClinicalCaseSerializer(queryset, many=True).data)

    def post(self, request):
        if request.user.role != "pg":
            return Response({"detail": "Only PG users can create cases."}, status=403)
        payload = request.data.copy()
        if not payload.get("category"):
            default_category, _ = CaseCategory.objects.get_or_create(
                name="General",
                defaults={"description": "Default category", "is_active": True},
            )
            payload["category"] = default_category.id
        if not payload.get("primary_diagnosis"):
            default_diagnosis, _ = Diagnosis.objects.get_or_create(
                name="General diagnosis",
                category="other",
                defaults={"description": "Auto-assigned default diagnosis"},
            )
            payload["primary_diagnosis"] = default_diagnosis.id

        serializer = ClinicalCaseSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        case = serializer.save(pg=request.user, supervisor=request.user.supervisor, status="draft")
        return Response(ClinicalCaseSerializer(case).data, status=status.HTTP_201_CREATED)


class PGCaseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        case = ClinicalCase.objects.filter(pk=pk, is_active=True).first()
        if not case or not _can_read_case(request.user, case):
            return None
        return case

    def get(self, request, pk):
        case = self.get_object(request, pk)
        if not case:
            return Response({"detail": "Not found."}, status=404)
        return Response(ClinicalCaseSerializer(case).data)

    def patch(self, request, pk):
        case = self.get_object(request, pk)
        if not case:
            return Response({"detail": "Not found."}, status=404)
        if request.user.role != "pg" or case.pg_id != request.user.id:
            return Response({"detail": "Only case owner can edit."}, status=403)
        if case.status not in {"draft", "needs_revision"}:
            return Response({"detail": "Only draft or needs_revision cases are editable."}, status=400)
        serializer = ClinicalCaseSerializer(case, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        case = self.get_object(request, pk)
        if not case:
            return Response({"detail": "Not found."}, status=404)
        if request.user.role != "pg" or case.pg_id != request.user.id:
            return Response({"detail": "Only case owner can delete."}, status=403)
        if case.status != "draft":
            return Response({"detail": "Only draft cases can be deleted."}, status=400)
        case.is_active = False
        case.save(update_fields=["is_active", "updated_at"])
        return Response(status=204)


class PGCaseSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != "pg":
            return Response({"detail": "Only PG users can submit."}, status=403)
        case = ClinicalCase.objects.filter(pk=pk, pg=request.user, is_active=True).first()
        if not case:
            return Response({"detail": "Not found."}, status=404)
        if case.status not in {"draft", "needs_revision"}:
            return Response({"detail": "Case is not in a submittable status."}, status=400)
        if not case.is_complete():
            return Response({"detail": "Complete all required fields before submit."}, status=400)
        case.status = "submitted"
        case.save(update_fields=["status", "updated_at"])
        return Response(ClinicalCaseSerializer(case).data)


class PendingCaseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ClinicalCase.objects.filter(status="submitted", is_active=True)
        if request.user.role == "supervisor":
            queryset = queryset.filter(pg__supervisor=request.user)
        elif request.user.role not in {"admin", "utrmc_user", "utrmc_admin"}:
            return Response({"detail": "Permission denied."}, status=403)
        queryset = queryset.order_by("-created_at")
        return Response(ClinicalCaseSerializer(queryset, many=True).data)


class CaseReviewActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        case = ClinicalCase.objects.filter(pk=pk, is_active=True).first()
        if not case or not _can_read_case(request.user, case):
            return Response({"detail": "Not found."}, status=404)
        if request.user.role == "utrmc_user":
            return Response({"detail": "UTRMC read-only users cannot review cases."}, status=403)
        if request.user.role == "supervisor" and not _is_supervisor_of_case(request.user, case):
            return Response({"detail": "You can only review assigned PG cases."}, status=403)
        if request.user.role not in {"supervisor", "admin", "utrmc_admin"}:
            return Response({"detail": "Permission denied."}, status=403)

        serializer = CaseReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data["status"]
        if action not in {"approved", "needs_revision", "rejected"}:
            return Response({"detail": "Invalid review action."}, status=400)

        review, _ = CaseReview.objects.update_or_create(
            case=case,
            reviewer=request.user,
            review_date=timezone.now().date(),
            defaults=serializer.validated_data,
        )
        return Response(
            {
                "case": ClinicalCaseSerializer(review.case).data,
                "review_status": review.status,
            }
        )


class CaseStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ClinicalCase.objects.filter(is_active=True)
        if request.user.role == "pg":
            queryset = queryset.filter(pg=request.user)
        elif request.user.role == "supervisor":
            queryset = queryset.filter(pg__supervisor=request.user)
        elif request.user.role not in {"admin", "utrmc_user", "utrmc_admin"}:
            return Response({"detail": "Permission denied."}, status=403)

        by_status = {
            item["status"]: item["count"]
            for item in queryset.values("status").annotate(count=Count("id"))
        }
        payload = {
            "total_cases": queryset.count(),
            "pending_cases": by_status.get("submitted", 0),
            "approved_cases": by_status.get("approved", 0),
            "needs_revision_cases": by_status.get("needs_revision", 0),
            "rejected_cases": by_status.get("rejected", 0),
            "draft_cases": by_status.get("draft", 0),
            "by_complexity": {
                item["complexity"]: item["count"]
                for item in queryset.values("complexity").annotate(count=Count("id"))
            },
            "recent_overdue_drafts": queryset.filter(
                status="draft", date_encountered__lt=timezone.now().date() - timedelta(days=30)
            ).count(),
        }
        return Response(payload)
