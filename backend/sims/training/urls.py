from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    TrainingProgramViewSet,
    ProgramRotationTemplateViewSet,
    ResidentTrainingRecordViewSet,
    RotationAssignmentViewSet,
    LeaveRequestViewSet,
    DeputationPostingViewSet,
    RotationApprovalInboxView,
    LeaveApprovalInboxView,
    MyRotationsView,
    MyLeavesView,
    SupervisorPendingRotationsView,
)

router = DefaultRouter()
router.register(r"programs", TrainingProgramViewSet, basename="training-program")
router.register(r"program-templates", ProgramRotationTemplateViewSet, basename="program-template")
router.register(r"resident-training", ResidentTrainingRecordViewSet, basename="resident-training")
router.register(r"rotations", RotationAssignmentViewSet, basename="rotation-assignment")
router.register(r"leaves", LeaveRequestViewSet, basename="leave-request")
router.register(r"postings", DeputationPostingViewSet, basename="deputation-posting")

urlpatterns = [
    path("", include(router.urls)),
    path("utrmc/approvals/rotations/", RotationApprovalInboxView.as_view(), name="rotation-approvals-inbox"),
    path("utrmc/approvals/leaves/", LeaveApprovalInboxView.as_view(), name="leave-approvals-inbox"),
    path("my/rotations/", MyRotationsView.as_view(), name="my-rotations"),
    path("my/leaves/", MyLeavesView.as_view(), name="my-leaves"),
    path("supervisor/rotations/pending/", SupervisorPendingRotationsView.as_view(), name="supervisor-pending-rotations"),
]
