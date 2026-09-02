from __future__ import annotations

from datetime import datetime

from django.http import HttpResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import ActivityLog, AuditReport
from .serializers import ActivityLogSerializer, AuditReportSerializer


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminUser]
    queryset = ActivityLog.objects.select_related("actor").order_by("-created_at")
    filterset_fields = {
        "actor": ["exact"],
        "action": ["exact"],
        "is_sensitive": ["exact"],
    }
    ordering_fields = ["created_at"]
    search_fields = ["verb", "target_repr", "metadata"]

    @action(detail=False, methods=["get"], url_path="export")
    def export_csv(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())[:1000]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=audit-log.csv"
        response.write("timestamp,actor,action,verb,target,ip\n")
        for log in queryset:
            response.write(
                f"{log.created_at.isoformat()},{log.actor_id or ''},{log.action},{log.verb},"
                f"{log.target_repr},{log.ip_address or ''}\n"
            )
        return response


class AuditReportViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AuditReportSerializer
    permission_classes = [IsAdminUser]
    queryset = AuditReport.objects.all()

    def create(self, request, *args, **kwargs):
        start_raw = request.data.get("start")
        end_raw = request.data.get("end")
        if not start_raw or not end_raw:
            return Response(
                {"detail": "start and end are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start = datetime.fromisoformat(start_raw)
            end = datetime.fromisoformat(end_raw)
        except ValueError:
            return Response(
                {"detail": "Invalid datetime format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if start >= end:
            return Response(
                {"detail": "start must be before end"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report = AuditReport.generate(start=start, end=end, created_by=request.user)
        serializer = self.get_serializer(report)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["get"], url_path="latest")
    def latest(self, request, *args, **kwargs):
        report = self.get_queryset().order_by("-generated_at").first()
        if not report:
            return Response({"detail": "No reports"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(report)
        return Response(serializer.data)
