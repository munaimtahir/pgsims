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
    LogbookEntryViewSet,
    LogbookReviewQueueView,
    LogbookThresholdConfigViewSet,
    LogbookMyThresholdView,
    SubmissionRequirementTemplateViewSet,
    SynopsisSubmissionView,
    SynopsisSubmissionDocumentsView,
    SynopsisSubmissionSubmitView,
    SynopsisReviewQueueView,
    SynopsisReviewActionView,
    ThesisSubmissionView,
    ThesisSubmissionDocumentsView,
    ThesisSubmissionSubmitView,
    ThesisReviewQueueView,
    ThesisReviewActionView,
    SubmissionCertificatesView,
    ProgramRotationRequirementViewSet,
    RotationCompletionsView,
    RotationCompletionVerifyView,
    ResidentOperationalDashboardView,
    SupervisorOperationalDashboardView,
    HODOperationalDashboardView,
    UTRMCOperationalDashboardView,
)

router = DefaultRouter()
router.register(r"programs", TrainingProgramViewSet, basename="training-program")
router.register(r"program-templates", ProgramRotationTemplateViewSet, basename="program-template")
router.register(r"resident-training", ResidentTrainingRecordViewSet, basename="resident-training")
router.register(r"rotations", RotationAssignmentViewSet, basename="rotation-assignment")
router.register(r"leaves", LeaveRequestViewSet, basename="leave-request")
router.register(r"postings", DeputationPostingViewSet, basename="deputation-posting")
router.register(r"workshops", WorkshopViewSet, basename="workshop")
router.register(r"logbook", LogbookEntryViewSet, basename="logbook-entry")
router.register(r"logbook/config", LogbookThresholdConfigViewSet, basename="logbook-threshold-config")
router.register(
    r"submissions/requirements",
    SubmissionRequirementTemplateViewSet,
    basename="submission-requirement-template",
)
router.register(
    r"rotations/requirements",
    ProgramRotationRequirementViewSet,
    basename="program-rotation-requirement",
)

milestone_router = DefaultRouter()
milestone_router.register(r"", ProgramMilestoneViewSet, basename="program-milestone")

urlpatterns = [
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
    path("logbook/review-queue/", LogbookReviewQueueView.as_view(), name="logbook-review-queue"),
    path("logbook/my-threshold/", LogbookMyThresholdView.as_view(), name="logbook-my-threshold"),
    # Synopsis/thesis submission completeness workflows
    path("submissions/synopsis/", SynopsisSubmissionView.as_view(), name="synopsis-submission"),
    path(
        "submissions/synopsis/documents/",
        SynopsisSubmissionDocumentsView.as_view(),
        name="synopsis-submission-documents",
    ),
    path(
        "submissions/synopsis/submit/",
        SynopsisSubmissionSubmitView.as_view(),
        name="synopsis-submission-submit",
    ),
    path(
        "submissions/synopsis/review-queue/",
        SynopsisReviewQueueView.as_view(),
        name="synopsis-review-queue",
    ),
    path(
        "submissions/synopsis/<int:submission_id>/review/",
        SynopsisReviewActionView.as_view(),
        name="synopsis-review-action",
    ),
    path("submissions/thesis/", ThesisSubmissionView.as_view(), name="thesis-submission"),
    path(
        "submissions/thesis/documents/",
        ThesisSubmissionDocumentsView.as_view(),
        name="thesis-submission-documents",
    ),
    path(
        "submissions/thesis/submit/",
        ThesisSubmissionSubmitView.as_view(),
        name="thesis-submission-submit",
    ),
    path(
        "submissions/thesis/review-queue/",
        ThesisReviewQueueView.as_view(),
        name="thesis-review-queue",
    ),
    path(
        "submissions/thesis/<int:submission_id>/review/",
        ThesisReviewActionView.as_view(),
        name="thesis-review-action",
    ),
    path("submissions/certificates/", SubmissionCertificatesView.as_view(), name="submission-certificates"),
    # Rotation completion verification
    path("rotations/completions/", RotationCompletionsView.as_view(), name="rotation-completions"),
    path(
        "rotations/completions/<int:completion_id>/verify/",
        RotationCompletionVerifyView.as_view(),
        name="rotation-completion-verify",
    ),
    # Operational dashboards and readiness views
    path("dashboard/resident/", ResidentOperationalDashboardView.as_view(), name="dashboard-resident"),
    path(
        "dashboard/supervisor/",
        SupervisorOperationalDashboardView.as_view(),
        name="dashboard-supervisor",
    ),
    path("dashboard/hod/", HODOperationalDashboardView.as_view(), name="dashboard-hod"),
    path("dashboard/utrmc/", UTRMCOperationalDashboardView.as_view(), name="dashboard-utrmc"),
    path("", include(router.urls)),
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
