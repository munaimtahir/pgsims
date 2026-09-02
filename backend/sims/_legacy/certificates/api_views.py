"""API views for certificates endpoints."""

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.common_permissions import IsPGUser
from sims.certificates.models import Certificate
from sims.certificates.api_serializers import CertificateSerializer


class PGCertificatesListView(APIView):
    """
    List certificates for the authenticated PG user.
    
    GET /api/certificates/my/
    """
    permission_classes = [permissions.IsAuthenticated, IsPGUser]

    def get(self, request: Request) -> Response:
        queryset = (
            Certificate.objects.filter(pg=request.user)
            .select_related("certificate_type")
            .order_by("-issue_date")
        )
        serializer = CertificateSerializer(queryset, many=True)
        return Response({"count": len(serializer.data), "results": serializer.data})


class PGCertificateDownloadView(APIView):
    """
    Download a specific certificate for the authenticated PG user.
    
    GET /api/certificates/my/<id>/download/
    """
    permission_classes = [permissions.IsAuthenticated, IsPGUser]

    def get(self, request: Request, pk: int) -> FileResponse:
        certificate = get_object_or_404(Certificate, pk=pk)

        # Explicit permission check for user ownership
        if certificate.pg != request.user:
            raise PermissionDenied("You can only download your own certificates.")

        if not certificate.certificate_file:
            raise Http404("Certificate file not found")

        return FileResponse(
            certificate.certificate_file.open("rb"),
            as_attachment=True,
            filename=certificate.certificate_file.name.split("/")[-1],
        )
