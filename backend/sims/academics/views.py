from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer
from sims.common_permissions import ReadAnyWriteAdminOnly


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [ReadAnyWriteAdminOnly]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if getattr(user, "is_superuser", False) or getattr(user, "role", None) in {"ADMIN", "ADMIN"}:
            return queryset
        return queryset.filter(active=True)
