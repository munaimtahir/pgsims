from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Department, Batch, StudentProfile
from .serializers import DepartmentSerializer, BatchSerializer, StudentProfileSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["active", "code"]
    search_fields = ["name", "code", "description"]
    ordering_fields = ["name", "code", "created_at"]


class BatchViewSet(viewsets.ModelViewSet):
    """ViewSet for Batch CRUD operations."""

    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["program", "department", "active"]
    search_fields = ["name", "department__name"]
    ordering_fields = ["name", "start_date", "created_at"]

    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        """Get all students in this batch."""
        batch = self.get_object()
        students = batch.student_profiles.all()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)


class StudentProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for StudentProfile CRUD operations."""

    queryset = StudentProfile.objects.select_related("user", "batch", "batch__department")
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status", "batch", "batch__department"]
    search_fields = ["roll_number", "user__first_name", "user__last_name", "user__email"]
    ordering_fields = ["roll_number", "admission_date", "cgpa"]

    def get_queryset(self):
        """Filter based on user role."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.role == "pg":
            # PG students can only see their own profile
            return queryset.filter(user=user)
        elif user.role == "supervisor":
            # Supervisors can see assigned students
            return queryset.filter(user__supervisor=user)
        # Admins can see all
        return queryset

    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        """Update student status."""
        student = self.get_object()
        new_status = request.data.get("status")

        if new_status in dict(StudentProfile.STATUS_CHOICES):
            student.update_status(new_status)
            serializer = self.get_serializer(student)
            return Response(serializer.data)

        return Response({"error": "Invalid status"}, status=400)
