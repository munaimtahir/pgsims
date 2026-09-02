from django.db import models
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exam, Score
from .serializers import ExamSerializer, ScoreSerializer


class ExamViewSet(viewsets.ModelViewSet):
    """ViewSet for Exam CRUD operations."""

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["exam_type", "status", "rotation", "requires_eligibility"]
    search_fields = ["title", "module_name"]
    ordering_fields = ["date", "title", "created_at"]

    @action(detail=True, methods=["get"])
    def scores(self, request, pk=None):
        """Get all scores for this exam."""
        exam = self.get_object()
        scores = exam.scores.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def statistics(self, request, pk=None):
        """Get exam statistics."""
        exam = self.get_object()
        scores = exam.scores.all()

        if not scores.exists():
            return Response({"message": "No scores recorded yet"})

        total_students = scores.count()
        passed = scores.filter(is_passing=True).count()
        failed = total_students - passed
        average_marks = scores.aggregate(avg=models.Avg("marks_obtained"))["avg"]

        return Response(
            {
                "total_students": total_students,
                "passed": passed,
                "failed": failed,
                "pass_percentage": (
                    round((passed / total_students) * 100, 2) if total_students > 0 else 0
                ),
                "average_marks": round(average_marks, 2) if average_marks else 0,
                "max_marks": exam.max_marks,
                "passing_marks": exam.passing_marks,
            }
        )


class ScoreViewSet(viewsets.ModelViewSet):
    """ViewSet for Score CRUD operations."""

    queryset = Score.objects.select_related("exam", "student", "entered_by")
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["exam", "student", "is_passing", "is_eligible", "grade"]
    search_fields = ["student__first_name", "student__last_name", "exam__title"]
    ordering_fields = ["exam__date", "marks_obtained", "percentage"]

    def get_queryset(self):
        """Filter based on user role."""
        user = self.request.user
        queryset = super().get_queryset()

        if user.role == "pg":
            # PG students can only see their own scores
            return queryset.filter(student=user)
        elif user.role == "supervisor":
            # Supervisors can see scores of assigned students
            return queryset.filter(student__supervisor=user)
        # Admins can see all
        return queryset

    def perform_create(self, serializer):
        """Set entered_by to current user and check eligibility."""
        score = serializer.save(entered_by=self.request.user)

        # Check eligibility if required
        if score.exam.requires_eligibility:
            is_eligible, reason = score.check_eligibility()
            score.is_eligible = is_eligible
            score.ineligibility_reason = reason
            score.save()

    @action(detail=False, methods=["get"])
    def my_scores(self, request):
        """Get current user's scores."""
        if request.user.role != "pg":
            return Response(
                {"error": "Only PG students can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN,
            )

        scores = Score.objects.filter(student=request.user)
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)
