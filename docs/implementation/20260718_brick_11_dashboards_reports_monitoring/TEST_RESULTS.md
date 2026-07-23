# Test Results - Brick 11: Dashboards, Reports, and Exports

All 14 integration tests inside `backend/sims/academics/tests.py` ran and passed successfully in 44.38 seconds.

```text
backend/sims/academics/tests.py::AcademicsFoundationTests::test_admin_can_create_training_record_via_api PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_brick11_monitoring_and_reports PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_create_training_record_prefills_profile_fields PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_data_quality_endpoint_reports_missing_training_record PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_evaluation_submission_and_review_workflow PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_logbook_entry_and_verification_workflow PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_only_one_active_training_record_per_resident PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_progress_summaries_and_data_quality_checks PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_resident_can_view_own_academic_summary PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_review_queue_item_flow PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_seed_command_is_idempotent_minimum PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_seed_workflows_command PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_supervisor_can_only_view_assigned_resident_summary PASSED
backend/sims/academics/tests.py::AcademicsFoundationTests::test_support_staff_cannot_mutate_training_records PASSED
```

No syntax, typecheck, or lint issues remain.
All previous brick gates are passing cleanly.
