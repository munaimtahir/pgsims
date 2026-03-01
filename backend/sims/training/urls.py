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
    # Phase 6
    ProgramPolicyView,
    ProgramMilestoneViewSet,
    MilestoneResearchRequirementView,
    ResidentResearchProjectView,
    ResearchProjectActionView,
    ResidentThesisView,
    ThesisSubmitView,
    MyWorkshopCompletionsView,
    MyWorkshopCompletionDetailView,
    WorkshopViewSet,
    MyEligibilityView,
    UTRMCEligibilityView,
    SupervisorResearchApprovalsView,
    SystemSettingsView,
    # Phase 6B/6C — Summary endpoints
    ResidentSummaryView,
    SupervisorSummaryView,
    SupervisorResidentProgressView,
)

router = DefaultRouter()
router.register(r"programs", TrainingProgramViewSet, basename="training-program")
router.register(r"program-templates", ProgramRotationTemplateViewSet, basename="program-template")
router.register(r"resident-training", ResidentTrainingRecordViewSet, basename="resident-training")
router.register(r"rotations", RotationAssignmentViewSet, basename="rotation-assignment")
router.register(r"leaves", LeaveRequestViewSet, basename="leave-request")
router.register(r"postings", DeputationPostingViewSet, basename="deputation-posting")
router.register(r"workshops", WorkshopViewSet, basename="workshop")

milestone_router = DefaultRouter()
milestone_router.register(r"", ProgramMilestoneViewSet, basename="program-milestone")

urlpatterns = [
    path("", include(router.urls)),
    # Program policy
    path("programs/<int:program_id>/policy/", ProgramPolicyView.as_view(), name="program-policy"),
    # Program milestones
    path("programs/<int:program_id>/milestones/", include(milestone_router.urls)),
    path("milestones/<int:milestone_id>/requirements/research/", MilestoneResearchRequirementView.as_view(), name="milestone-research-req"),
    # Rotation approvals (UTRMC)
    path("utrmc/approvals/rotations/", RotationApprovalInboxView.as_view(), name="rotation-approvals-inbox"),
    path("utrmc/approvals/leaves/", LeaveApprovalInboxView.as_view(), name="leave-approvals-inbox"),
    # Eligibility (UTRMC)
    path("utrmc/eligibility/", UTRMCEligibilityView.as_view(), name="utrmc-eligibility"),
    # My (resident) routes
    path("my/rotations/", MyRotationsView.as_view(), name="my-rotations"),
    path("my/leaves/", MyLeavesView.as_view(), name="my-leaves"),
    path("my/research/", ResidentResearchProjectView.as_view(), name="my-research"),
    path("my/research/action/<str:action>/", ResearchProjectActionView.as_view(), name="research-action"),
    path("my/thesis/", ResidentThesisView.as_view(), name="my-thesis"),
    path("my/thesis/submit/", ThesisSubmitView.as_view(), name="thesis-submit"),
    path("my/workshops/", MyWorkshopCompletionsView.as_view(), name="my-workshops"),
    path("my/workshops/<int:pk>/", MyWorkshopCompletionDetailView.as_view(), name="my-workshop-detail"),
    path("my/eligibility/", MyEligibilityView.as_view(), name="my-eligibility"),
    # Supervisor routes
    path("supervisor/rotations/pending/", SupervisorPendingRotationsView.as_view(), name="supervisor-pending-rotations"),
    path("supervisor/research-approvals/", SupervisorResearchApprovalsView.as_view(), name="supervisor-research-approvals"),
    # Summary endpoints (Phase 6B/6C)
    path("residents/me/summary/", ResidentSummaryView.as_view(), name="resident-summary"),
    path("supervisors/me/summary/", SupervisorSummaryView.as_view(), name="supervisor-summary"),
    path("supervisors/residents/<int:resident_id>/progress/", SupervisorResidentProgressView.as_view(), name="supervisor-resident-progress"),
    # System settings
    path("system/settings/", SystemSettingsView.as_view(), name="system-settings"),
]
