#!/bin/bash
set -e

# check_brick_12_production_hardening.sh - Gate Check for Brick 12

echo "Verifying Brick 12 deliverables..."

# 1. Environment & Backup Scripts
[ -f "docs/ENVIRONMENT_VARIABLES.md" ] || (echo "Missing ENVIRONMENT_VARIABLES.md" && exit 1)
[ -f "scripts/backup_pgms_db.sh" ] || (echo "Missing backup_pgms_db.sh" && exit 1)
[ -f "scripts/restore_pgms_db.sh" ] || (echo "Missing restore_pgms_db.sh" && exit 1)
[ -f "scripts/verify_pgms_backup.sh" ] || (echo "Missing verify_pgms_backup.sh" && exit 1)

# 2. Manuals & Operating Guides
[ -f "docs/ADMIN_OPERATING_MANUAL.md" ] || (echo "Missing ADMIN_OPERATING_MANUAL.md" && exit 1)
[ -f "docs/RESIDENT_QUICK_GUIDE.md" ] || (echo "Missing RESIDENT_QUICK_GUIDE.md" && exit 1)
[ -f "docs/SUPERVISOR_QUICK_GUIDE.md" ] || (echo "Missing SUPERVISOR_QUICK_GUIDE.md" && exit 1)

# 3. System Health checks
[ -f "scripts/check_pgms_health.sh" ] || (echo "Missing check_pgms_health.sh" && exit 1)

# 4. Brick 12 Launch Pack Docs
LAUNCH_DIR="docs/implementation/20260718_brick_12_production_hardening_launch"
[ -f "${LAUNCH_DIR}/DISCOVERY.md" ] || (echo "Missing DISCOVERY.md" && exit 1)
[ -f "${LAUNCH_DIR}/DECISION_LOCK.md" ] || (echo "Missing DECISION_LOCK.md" && exit 1)
[ -f "${LAUNCH_DIR}/CHANGES.md" ] || (echo "Missing CHANGES.md" && exit 1)
[ -f "${LAUNCH_DIR}/SECURITY_PERMISSION_AUDIT.md" ] || (echo "Missing SECURITY_PERMISSION_AUDIT.md" && exit 1)
[ -f "${LAUNCH_DIR}/BACKUP_RESTORE_GUIDE.md" ] || (echo "Missing BACKUP_RESTORE_GUIDE.md" && exit 1)
[ -f "${LAUNCH_DIR}/PRODUCTION_SETTINGS_REVIEW.md" ] || (echo "Missing PRODUCTION_SETTINGS_REVIEW.md" && exit 1)
[ -f "${LAUNCH_DIR}/EXPORT_SAFETY_REVIEW.md" ] || (echo "Missing EXPORT_SAFETY_REVIEW.md" && exit 1)
[ -f "${LAUNCH_DIR}/SEED_AND_RESET_POLICY.md" ] || (echo "Missing SEED_AND_RESET_POLICY.md" && exit 1)
[ -f "${LAUNCH_DIR}/HEALTH_CHECK_SPEC.md" ] || (echo "Missing HEALTH_CHECK_SPEC.md" && exit 1)
[ -f "${LAUNCH_DIR}/LOGGING_AND_ERROR_HANDLING.md" ] || (echo "Missing LOGGING_AND_ERROR_HANDLING.md" && exit 1)
[ -f "${LAUNCH_DIR}/AUDIT_LOG_VERIFICATION.md" ] || (echo "Missing AUDIT_LOG_VERIFICATION.md" && exit 1)
[ -f "${LAUNCH_DIR}/PILOT_LAUNCH_DATA_POLICY.md" ] || (echo "Missing PILOT_LAUNCH_DATA_POLICY.md" && exit 1)
[ -f "${LAUNCH_DIR}/DEPLOYMENT_CHECKLIST.md" ] || (echo "Missing DEPLOYMENT_CHECKLIST.md" && exit 1)
[ -f "${LAUNCH_DIR}/SMOKE_TEST_CHECKLIST.md" ] || (echo "Missing SMOKE_TEST_CHECKLIST.md" && exit 1)
[ -f "${LAUNCH_DIR}/FRONTEND_PRODUCTION_REVIEW.md" ] || (echo "Missing FRONTEND_PRODUCTION_REVIEW.md" && exit 1)
[ -f "${LAUNCH_DIR}/TEST_RESULTS.md" ] || (echo "Missing TEST_RESULTS.md" && exit 1)
[ -f "${LAUNCH_DIR}/KNOWN_LIMITATIONS.md" ] || (echo "Missing KNOWN_LIMITATIONS.md" && exit 1)
[ -f "${LAUNCH_DIR}/FINAL_VERDICT.md" ] || (echo "Missing FINAL_VERDICT.md" && exit 1)

# 5. Check executable state
[ -x "scripts/backup_pgms_db.sh" ] || (echo "backup_pgms_db.sh is not executable" && exit 1)
[ -x "scripts/restore_pgms_db.sh" ] || (echo "restore_pgms_db.sh is not executable" && exit 1)
[ -x "scripts/verify_pgms_backup.sh" ] || (echo "verify_pgms_backup.sh is not executable" && exit 1)
[ -x "scripts/check_pgms_health.sh" ] || (echo "check_pgms_health.sh is not executable" && exit 1)

# 6. Legacy regression constraints
if grep -rn "SupervisorResidentLink" backend/sims/academics/ | grep -v "_legacy" || false; then
    echo "Warning: found active reference to SupervisorResidentLink!"
    exit 1
fi

echo "Brick 12 production hardening gate: PASS"
