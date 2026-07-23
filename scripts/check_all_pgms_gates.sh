#!/bin/bash
set -e

# check_all_pgms_gates.sh - Run all PGMS coding gates and constraints checks

echo "=========================================================="
echo "Running All PGMS Gate Checks..."
echo "=========================================================="

# Configure PATH for local dev tools (ripgrep)
export PATH="$PATH:$(pwd)/scripts/local_dev"

bash scripts/check_update_0_identity_cleanup.sh
bash scripts/check_brick_6_masters_directory_data_quality.sh
bash scripts/check_brick_7_clean_fresh_supervision_spine.sh
bash scripts/check_brick_8_academic_workflow_foundation.sh
bash scripts/check_canonical_frontend_roles.sh
bash scripts/check_legacy_delete_candidates.sh
bash scripts/check_brick_9_10_academic_workflows.sh
bash scripts/check_brick_11_dashboards_reports_monitoring.sh
bash scripts/check_brick_12_production_hardening.sh

echo "=========================================================="
echo "ALL GATES PASS"
echo "=========================================================="
