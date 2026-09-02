"""Serializers for certificates API endpoints."""

from rest_framework import serializers

from sims.certificates.models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    """Serializer for the Certificate model."""

    certificate_type_name = serializers.CharField(source="certificate_type.name", read_only=True)
    has_file = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "title",
            "certificate_type_name",
            "issue_date",
            "status",
            "has_file",
            "file_name",
        ]

    def get_has_file(self, obj: Certificate) -> bool:
        return bool(obj.certificate_file)

    def get_file_name(self, obj: Certificate) -> str:
        if obj.certificate_file:
            return obj.certificate_file.name.split("/")[-1]
        return ""
