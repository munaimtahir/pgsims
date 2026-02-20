"""API views for reporting."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.reports.models import ReportTemplate, ScheduledReport
from sims.reports.serializers import (
    ReportRequestSerializer,
    ReportTemplateSerializer,
    ScheduledReportSerializer,
)
from sims.reports.services import ReportService


class ReportTemplateListView(generics.ListAPIView):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ReportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = get_object_or_404(
            ReportTemplate, slug=serializer.validated_data["template_slug"]
        )
        params = serializer.validated_data.get("params", {})
        service = ReportService(request.user)
        report = service.generate(template, params, serializer.validated_data["format"])
        payload = {
            "filename": report.filename,
            "content_type": report.content_type,
            "content": report.as_base64(),
        }
        return Response(payload, status=status.HTTP_200_OK)


class ScheduledReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduledReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScheduledReport.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer: ScheduledReportSerializer) -> None:
        serializer.save(created_by=self.request.user)


class ScheduledReportDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ScheduledReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScheduledReport.objects.filter(created_by=self.request.user)


__all__ = [
    "ReportTemplateListView",
    "ReportGenerateView",
    "ScheduledReportListCreateView",
    "ScheduledReportDetailView",
]
