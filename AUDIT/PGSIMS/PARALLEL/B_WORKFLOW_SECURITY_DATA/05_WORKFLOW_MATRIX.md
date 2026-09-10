# WORKFLOW MATRIX

The audit reviewed major workflow engines. Dynamic tests were executed using pytest API test cases, while others were verified via static source code review.

| Workflow | Verification Method | Exact Scenario Tested | Result | Final Classification |
|----------|---------------------|-----------------------|--------|----------------------|
| Resident onboarding | STATIC_CODE_REVIEW | Source inspection of `ResidentOnboardingView` | Permitted according to flow | STATIC_CODE_REVIEW |
| Document management lifecycle | STATIC_CODE_REVIEW | Source inspection of `ResidentDocumentViewSet` | Owner/assigned permissions enforced | STATIC_CODE_REVIEW |
| Logbook lifecycle | STATIC_CODE_REVIEW | Source inspection of `LogbookEntry` state transitions | State restrictions present | STATIC_CODE_REVIEW |
| Synopsis/Thesis workflow | DYNAMIC_API | Resident attempts to submit a Synopsis from `UNDER_REVIEW` state | Blocked (400 Bad Request) | DYNAMIC_API |
| Synopsis/Thesis workflow | DYNAMIC_API | Supervisor attempts to start review on `DRAFT` Synopsis | Blocked (400 Bad Request) | DYNAMIC_API |
| Supervision assignment | DYNAMIC_DATABASE | Attempt duplicate active `PRIMARY` assignment | Blocked (IntegrityError) | DYNAMIC_DATABASE |
| Supervisor pending/review workflow | STATIC_CODE_REVIEW | Source inspection of review queues | Filtered to assigned residents | STATIC_CODE_REVIEW |
| Administrative resident-supervisor linking | STATIC_CODE_REVIEW | Source inspection of `AssignSupervisorView` / Admin endpoints | Admin constrained | STATIC_CODE_REVIEW |
| Rotations/training/requirements | STATIC_CODE_REVIEW | Source inspection of rotation APIs | Owner/admin constrained | STATIC_CODE_REVIEW |

Dynamic verifications explicitly demonstrated that the API and Database layer blocks invalid workflow actions reliably. Workflows lacking dedicated dynamic tests in this session are classified as `STATIC_CODE_REVIEW`.
