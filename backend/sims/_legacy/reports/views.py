"""API views for reporting."""

from __future__ import annotations

from django.http import HttpResponse
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
from sims.reports.registry import export_rows, report_catalog_for, run_report_for
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


class ReportCatalogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response({"results": report_catalog_for(request.user)})


class ReportRunView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, key: str) -> Response:
        try:
            rows, summary = run_report_for(request.user, key, dict(request.query_params))
        except KeyError:
            return Response({"detail": "Unknown report key."}, status=404)
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=403)
        return Response({"key": key, "rows": rows, "summary": summary})


class ReportExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, key: str) -> HttpResponse:
        export_format = request.query_params.get("file_format", "xlsx").lower()
        try:
            rows, _summary = run_report_for(request.user, key, dict(request.query_params))
        except KeyError:
            return Response({"detail": "Unknown report key."}, status=404)
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=403)
        if export_format not in {"xlsx", "csv"}:
            return Response({"detail": "Format must be xlsx or csv."}, status=400)
        content, content_type, filename = export_rows(rows, key, export_format)
        response = HttpResponse(content, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


__all__ = [
    "ReportTemplateListView",
    "ReportGenerateView",
    "ScheduledReportListCreateView",
    "ScheduledReportDetailView",
    "ReportCatalogView",
    "ReportRunView",
    "ReportExportView",
]
