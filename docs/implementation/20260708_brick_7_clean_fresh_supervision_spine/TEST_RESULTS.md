# TEST RESULTS — PGMS Brick 7 Clean Fresh Pilot Supervision Spine

This document records the unit and API test execution results for **Brick 7**.

---

## 1. Summary of Test Execution

- **Total Test Cases**: 391 passed, 8 skipped
- **Status**: 100% Success
- **Runtime**: ~102.99 seconds

---

## 2. Test Execution Output Logs

```text
sims/users/test_demo_data_reset.py::ResetDemoDataCommandTests::test_confirm_removes_fake_graph_and_preserves_canonical_data PASSED
sims/users/test_demo_data_reset.py::ResetDemoDataCommandTests::test_dry_run_does_not_delete_anything PASSED
sims/users/test_demo_data_reset.py::InitializeBaselineCommandTests::test_baseline_creates_canonical_org_data PASSED
sims/users/test_demo_data_reset.py::InitializeBaselineCommandTests::test_initialize_is_idempotent PASSED
sims/users/test_registration_api.py::PublicRegistrationAPITests::test_public_registration_creates_pg_when_enabled PASSED
sims/users/test_registration_api.py::PublicRegistrationAPITests::test_public_registration_disabled_by_default PASSED
sims/users/test_registration_api.py::PublicRegistrationAPITests::test_public_registration_rejects_privileged_roles PASSED
sims/users/test_seed_demo_data.py::SeedDemoDataCommandTests::test_seed_demo_data_creates_demo_graph_and_admin_login PASSED
sims/users/test_seed_demo_data.py::SeedDemoDataCommandTests::test_seed_demo_data_is_idempotent PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_hospital_department_pair_is_unique PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_resident_cannot_create_departments PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_supervision_link_role_constraints PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_supervisor_cannot_create_users PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_utrmc_admin_can_create_supervision_link PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_utrmc_admin_org_graph_routes_cover_roster_and_matrix_actions PASSED
sims/users/test_userbase_api.py::UserbasePermissionAndConstraintTests::test_utrmc_user_is_read_only_on_org_graph_mutations PASSED
sims/users/test_userbase_api.py::UserbaseReadScopeTests::test_supervisor_can_retrieve_self_but_not_other_users PASSED
sims/users/test_userbase_api.py::UserbaseReadScopeTests::test_supervisor_get_users_list_returns_only_self PASSED
sims/users/test_userbase_api.py::DataQualityAdminApiTests::test_recompute_and_patch_generate_audit PASSED
sims/users/test_userbase_api.py::DataQualityAdminApiTests::test_resident_without_training_record_or_supervisor_link_is_incomplete PASSED
sims/users/test_userbase_api.py::DataQualityAdminApiTests::test_summary_and_users_require_admin PASSED
sims/users/test_userbase_api.py::DataQualityAdminApiTests::test_training_record_issues_propagate_to_user_issues PASSED
sims/users/test_userbase_api.py::ImportCorrectionsCommandTests::test_apply_updates_and_audits PASSED
sims/users/test_userbase_api.py::ImportCorrectionsCommandTests::test_dry_run_does_not_mutate PASSED
sims/users/tests.py::UserModelBasicTests::test_is_admin_property PASSED
sims/users/tests.py::UserModelBasicTests::test_pilot_pg_bootstrap_creates_active_training_record PASSED
sims/users/tests.py::UserModelBasicTests::test_roles_set PASSED
sims/users/tests.py::UserModelBasicTests::test_str PASSED
sims/users/tests.py::UserAPIAuthTests::test_login_returns_token PASSED
sims/users/tests.py::UserAPIAuthTests::test_me_returns_user PASSED
sims/users/tests.py::UserAPIAuthTests::test_password_reset_returns_generic_success_when_email_send_fails PASSED
sims/users/tests.py::UserAPIAuthTests::test_unauthenticated_me_rejected PASSED
sims/users/tests.py::UserbaseReadOnlyScopeTests::test_support_staff_cannot_list_supervision_links PASSED
sims/users/tests.py::UserbaseReadOnlyScopeTests::test_support_staff_user_list_is_self_scoped PASSED
sims/users/tests.py::UserbaseReadOnlyScopeTests::test_utrmc_user_cannot_create_users PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_model_creation_and_constraints PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_business_rules_matching PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_primary_supervisor_uniqueness PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_change_primary_supervisor PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_api_supervision_endpoints PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_supervision_options_api PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_data_quality_endpoint PASSED
sims/supervision/tests/test_supervision.py::TestSupervisionSpine::test_supervision_import_view PASSED

======================== 391 passed, 8 skipped in 102.99s (0:01:42) =========================
```
