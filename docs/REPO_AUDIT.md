# Repository Audit Report

**Date:** January 15, 2026  
**Repository:** munaimtahir/pgsims  
**Purpose:** Comprehensive file classification for repository cleanup

## Classification Buckets

- **A**: Core Runtime Code - Essential application code for runtime execution
- **B**: Deployment & Infrastructure - Docker, deployment scripts, configuration
- **C**: Legitimate Project Documentation - Repository-specific guides and docs
- **D**: AI Agent Artifacts - Implementation logs, phase summaries, session progress
- **E**: Temporary Diagnostics & Logs - Test outputs, audit logs, diagnostic dumps
- **F**: Cross-Project / Platform Leakage - Server-specific docs, external platform guides
- **G**: Ambiguous / Needs confirmation - Unclear classification

## File Classification Table

### Root Directory Files

| Path | Bucket | Reason |
|------|--------|--------|
| manage.py | A | Django management script - core runtime |
| conftest.py | A | Pytest configuration - test infrastructure |
| pytest.ini | A | Pytest settings - test infrastructure |
| pyproject.toml | A | Python project configuration - dev tools |
| requirements.txt | A | Python dependencies - runtime requirements |
| requirements-dev.txt | A | Development dependencies |
| .coveragerc | A | Coverage configuration - test infrastructure |
| .flake8 | A | Linting configuration - dev tools |
| .pre-commit-config.yaml | A | Pre-commit hooks - dev tools |
| .gitignore | A | Git ignore patterns - version control |
| .dockerignore | B | Docker ignore patterns - deployment |
| .env.example | B | Environment template - deployment |
| .env.coolify.example | B | Coolify environment template - deployment |
| Dockerfile | B | Docker image definition - deployment |
| Dockerfile.frontend | B | Frontend Docker image - deployment |
| docker-compose.yml | B | Docker composition - deployment |
| docker-compose.local.yml | B | Local dev Docker setup - deployment |
| docker-compose.coolify.yml | B | Coolify Docker setup - deployment |
| docker-compose.phc.yml | B | PHC Docker setup - deployment |
| Makefile | B | Build automation - deployment |
| README.md | C | Main project documentation |
| CHANGELOG.md | C | Version history - legitimate doc |
| LICENSE | C | Project license - legitimate doc |
| TESTS.md | C | Testing guide - legitimate doc |
| backend.sh | B | Backend startup script - deployment |
| frontend.sh | B | Frontend startup script - deployment |
| both.sh | B | Combined startup script - deployment |
| get-docker.sh | B | Docker installation script - deployment |
| CADDYFILE_COMPLETE.txt | D | Caddy configuration artifact |
| DATA_PREVIEW_INSTRUCTIONS.md | D | AI-generated instructions for data preview |
| PREVIEW_TRAINEES_USAGE.md | D | AI-generated usage guide |
| TRAINEE_IMPORT_SUMMARY.md | D | AI implementation summary |
| DATABASE_IMPORT_SOLUTION.md | D | AI solution documentation |
| FINAL_IMPORT_INSTRUCTIONS.md | D | AI-generated import guide |
| IMPORT_TRAINEES_GUIDE.md | D | AI-generated comprehensive guide |
| QUICK_IMPORT_INSTRUCTIONS.md | D | AI-generated quick guide |
| SEED_DATA_GUIDE.md | D | AI-generated seed data guide |
| QUICK_START.md | D | Redundant with README - AI artifact |
| QUICK_ACCESS_INFO.md | D | Quick reference - AI artifact |
| DEPLOYMENT_STATUS.md | D | Deployment status log - AI artifact |
| Trainee_Data_Department_of_Urology.xlsx | E | Sample data file - temporary |
| updated_config.txt | E | Configuration dump - temporary |
| verify_import.py | E | Import verification script - temporary diagnostic |
| do_import_now.py | E | Import execution script - temporary |
| run_import.py | E | Import runner - temporary |
| run_import_now.py | E | Import runner variant - temporary |
| import_trainees_simple.sh | E | Simple import script - temporary |
| import_with_sqlite.sh | E | SQLite import script - temporary |

### .github/workflows/

| Path | Bucket | Reason |
|------|--------|--------|
| .github/workflows/django-tests.yml | A | CI/CD for Django tests - core infrastructure |
| .github/workflows/frontend-tests.yml | A | CI/CD for frontend tests - core infrastructure |

### scripts/

| Path | Bucket | Reason |
|------|--------|--------|
| scripts/create_reviewable_entry.py | A | Data seeding script - development utility |
| scripts/create_basic_rotation_data.py | A | Data seeding script - development utility |
| scripts/create_demo_notifications.py | A | Demo data script - development utility |
| scripts/create_test_entry.py | A | Test data script - development utility |
| scripts/create_sample_users.py | A | Demo user script - development utility |
| scripts/preload_demo_data.py | A | Demo data loader - development utility |
| scripts/preload_attendance_data.py | A | Attendance data loader - development utility |
| scripts/seed_demo_data.sh | A | Demo data seeding shell script - development utility |
| scripts/setup_localhost_windows.ps1 | B | Windows setup script - deployment |
| scripts/setup_localhost_windows.bat | B | Windows setup batch - deployment |
| scripts/start_django.ps1 | B | Django startup PowerShell - deployment |
| scripts/start_server.bat | B | Server startup batch - deployment |
| scripts/test_system.ps1 | E | System test script - diagnostic |
| scripts/server_diagnostic_helper.ps1 | E | Server diagnostic - temporary |
| scripts/organize_project.ps1 | E | Project organization script - temporary |
| scripts/organize_project.bat | E | Project organization batch - temporary |
| scripts/ORGANIZE_NOW.bat | E | Organization trigger - temporary |
| scripts/create_superuser.bat | B | Superuser creation batch - deployment |

### deployment/

| Path | Bucket | Reason |
|------|--------|--------|
| deployment/gunicorn.conf.py | B | Gunicorn configuration - deployment |
| deployment/gunicorn_phc.conf.py | B | PHC Gunicorn config - deployment |
| deployment/Caddyfile.pgsims | B | Caddy reverse proxy config - deployment |
| deployment/sims.service | B | Systemd service file - deployment |
| deployment/sims_no_venv.service | B | Systemd service (no venv) - deployment |
| deployment/server_config.env | B | Server configuration - deployment |
| deployment/server_config.localhost.env | B | Localhost config - deployment |
| deployment/server_config_172.237.95.120.env | F | IP-specific config - cross-project |
| deployment/create_superuser.sh | B | Superuser creation script - deployment |
| deployment/deploy.sh | B | Generic deploy script - deployment |
| deployment/deploy_localhost.sh | B | Localhost deploy - deployment |
| deployment/deploy_localhost.ps1 | B | Localhost deploy PowerShell - deployment |
| deployment/deploy_docker_compose.sh | B | Docker compose deploy - deployment |
| deployment/deploy_server.sh | B | Server deploy script - deployment |
| deployment/deploy_server_quick.sh | B | Quick server deploy - deployment |
| deployment/deploy_server_no_venv.sh | B | Server deploy (no venv) - deployment |
| deployment/deploy_server_root.sh | B | Root server deploy - deployment |
| deployment/deploy_server_172.237.95.120.sh | F | IP-specific deploy - cross-project |
| deployment/switch_to_localhost.sh | B | Environment switcher - deployment |
| deployment/switch_to_vps.sh | B | VPS switcher - deployment |
| deployment/verify_server_setup.sh | B | Setup verification - deployment |
| deployment/verify_deployment.sh | B | Deployment verification - deployment |
| deployment/verify_path_consistency.sh | E | Path diagnostic - temporary |
| deployment/cleanup_port_80.sh | B | Port cleanup utility - deployment |
| deployment/diagnose_nginx_403.sh | E | Nginx diagnostic - temporary |
| deployment/fix_403_error.sh | E | Error fix script - temporary |
| deployment/fix_package_lock.sh | E | Package lock fix - temporary |
| deployment/pre_deployment_fix.sh | E | Pre-deploy fix - temporary |
| deployment/deployment_fix.py | E | Deployment fix script - temporary |
| deployment/DOCKER_DEPLOYMENT_GUIDE.md | C | Docker deployment guide - legitimate doc |
| deployment/DEPLOYMENT_README.md | C | Deployment overview - legitimate doc |
| deployment/QUICK_DEPLOY.md | C | Quick deploy guide - legitimate doc |
| deployment/DEPLOYMENT_SUMMARY.md | D | Deployment summary - AI artifact |
| deployment/DEPLOYMENT_COMPLETE.md | D | Completion report - AI artifact |
| deployment/DEPLOY_NOW.sh | D | Deploy now script - AI artifact |
| deployment/DEPLOY_NOW_172.237.95.120.md | F | IP-specific deploy doc - cross-project |
| deployment/DEPLOYMENT_INSTRUCTIONS_139.162.9.224.md | F | IP-specific instructions - cross-project |
| deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md | F | IP-specific instructions - cross-project |
| deployment/archive/nginx.conf | B | Archived nginx config - deployment |
| deployment/archive/nginx.localhost.conf | B | Archived localhost nginx - deployment |
| deployment/archive/nginx_sims.conf | B | Archived SIMS nginx - deployment |

### docs/ Directory

| Path | Bucket | Reason |
|------|--------|--------|
| docs/README.md | C | Documentation index - legitimate doc |
| docs/API.md | C | API documentation - legitimate doc |
| docs/SETUP.md | C | Setup guide - legitimate doc |
| docs/SECURITY.md | C | Security documentation - legitimate doc |
| docs/TESTING_GUIDE.md | C | Testing guide - legitimate doc |
| docs/TROUBLESHOOTING.md | C | Troubleshooting guide - legitimate doc |
| docs/CONTRIBUTING.md | C | Contribution guidelines - legitimate doc |
| docs/LOCAL_DEV.md | C | Local development guide - legitimate doc |
| docs/RELEASE_NOTES.md | C | Release notes - legitimate doc |
| docs/PROJECT_STRUCTURE.md | C | Project structure - legitimate doc |
| docs/PROJECT_ORGANIZATION_GUIDE.md | C | Organization guide - legitimate doc |
| docs/COMPLETE_ORGANIZATION_GUIDE.md | C | Complete organization guide - legitimate doc |
| docs/DEVELOPMENT_GUIDELINES.md | C | Development guidelines - legitimate doc |
| docs/FEATURE_FLAGS.md | C | Feature flags - legitimate doc |
| docs/ENV_VARS.md | C | Environment variables - legitimate doc |
| docs/FEATURES_STATUS.md | C | Feature status - legitimate doc |
| docs/MIGRATION_NOTES.md | C | Migration documentation - legitimate doc |
| docs/POSTGRESQL_SETUP.md | C | PostgreSQL setup - legitimate doc |
| docs/SETUP_ENV_FILES.md | C | Environment setup - legitimate doc |
| docs/SMOKE_TEST.md | C | Smoke testing guide - legitimate doc |
| docs/PROJECT_SUMMARY.md | C | Project summary - legitimate doc |
| docs/SYSTEM_STATUS.md | C | System status - legitimate doc |
| docs/PRODUCTION_READINESS_ASSESSMENT.md | C | Production readiness - legitimate doc |
| docs/DEMO_SETUP.md | C | Demo setup guide - legitimate doc |
| docs/README_DEVELOPMENT_PLAN.md | C | Development planning - legitimate doc |
| docs/README_TESTING.md | C | Testing guide - legitimate doc |
| docs/global_search_audit.md | C | Global search audit - legitimate doc |
| docs/STAGE2_READINESS_REVIEW.md | C | Stage 2 review - legitimate doc |
| docs/AUTONOMOUS_SESSION_PROGRESS.md | D | AI session progress - AI artifact |
| docs/FINAL_AUTONOMOUS_SUMMARY.md | D | AI session summary - AI artifact |
| docs/STAGE1_COMPLETION_STATUS.md | D | Stage 1 status - AI artifact |
| docs/DEVELOPMENT_STATUS_REVIEW.md | D | Status review - AI artifact |
| docs/CODE_QUALITY_REPORT.md | D | Code quality report - AI artifact |
| docs/PROJECT_ORGANIZATION_COMPLETION_REPORT.md | D | Organization report - AI artifact |
| docs/ADMIN_CONSOLIDATION_REPORT.md | D | Admin consolidation - AI artifact |
| docs/ADMIN_LOGIN_FIXED_SUMMARY.md | D | Admin login fix - AI artifact |
| docs/ADMIN_SYSTEM_COMPLETION_REPORT.md | D | Admin system completion - AI artifact |
| docs/ADMIN_TEMPLATES_DOCUMENTATION.md | D | Admin templates doc - AI artifact |
| docs/ADMIN_DASHBOARD_FIXES_REPORT.md | D | Dashboard fixes - AI artifact |
| docs/AUTHENTICATION_SYSTEM_COMPLETION_REPORT.md | D | Auth completion - AI artifact |
| docs/ENHANCED_ANALYTICS_FILTERS_REPORT.md | D | Analytics filters - AI artifact |
| docs/FONTAWESOME_RESTORATION_FINAL_REPORT.md | D | Font Awesome restore - AI artifact |
| docs/HOMEPAGE_COMPLETION_REPORT.md | D | Homepage completion - AI artifact |
| docs/HOVER_VISIBILITY_FIX_REPORT.md | D | Hover fix - AI artifact |
| docs/ICON_BULLET_FIXES_REPORT.md | D | Icon bullet fixes - AI artifact |
| docs/ICON_RECOVERY_REPORT.md | D | Icon recovery - AI artifact |
| docs/LAYOUT_UPDATES_COMPLETION_REPORT.md | D | Layout updates - AI artifact |
| docs/LOGBOOK_FORM_ENHANCEMENT_REPORT.md | D | Logbook form enhancement - AI artifact |
| docs/LOGBOOK_ROUTING_TEST.md | G | Logbook routing test - ambiguous |
| docs/LOGIN_CONSOLIDATION_COMPLETION_REPORT.md | D | Login consolidation - AI artifact |
| docs/LOGIN_ISSUES_RESOLVED.md | D | Login issues resolved - AI artifact |
| docs/LOGOUT_SYSTEM_COMPLETION_REPORT.md | D | Logout completion - AI artifact |
| docs/MIGRATION_FIX_COMPLETION_REPORT.md | D | Migration fix - AI artifact |
| docs/MODEL_NAMES_SPELLING_FIX_REPORT.md | D | Model names fix - AI artifact |
| docs/SUPERVISOR_PAGES_FIX_REPORT.md | D | Supervisor pages fix - AI artifact |
| docs/SYSTEMATIC_EXAMINATION_COMPLETION_REPORT.md | D | Systematic exam - AI artifact |
| docs/SYSTEM_STATUS_ICONS_REPORT.md | D | System status icons - AI artifact |
| docs/THEME_SYSTEM_COMPLETION_REPORT.md | D | Theme completion - AI artifact |
| docs/USER_PROFILE_FIX_REPORT.md | D | User profile fix - AI artifact |
| docs/WELCOME_SECTION_FIX_REPORT.md | D | Welcome section fix - AI artifact |
| docs/WHITE_BULLETS_REMOVAL_REPORT.md | D | White bullets removal - AI artifact |
| docs/FIXES_REPORT.md | D | General fixes report - AI artifact |
| docs/NGINX_DEPLOYMENT_172.236.152.35.md | F | IP-specific nginx - cross-project |
| docs/NGINX_SERVER_172.236.152.35_COMPLETE.md | F | IP-specific nginx complete - cross-project |
| docs/SERVER_DEPLOYMENT_GUIDE_172.236.152.35.md | F | IP-specific deploy guide - cross-project |
| docs/SERVER_172.236.152.35_READY.md | F | IP-specific readiness - cross-project |
| docs/SERVER_MIGRATION_FIX_REPORT.md | F | Server migration fix - cross-project |
| docs/DEPLOY_COOLIFY_TRAEFIK.md | F | Coolify/Traefik guide - external platform |
| docs/GITHUB_SYNC_WORKFLOW.md | G | GitHub sync workflow - ambiguous |
| docs/File Tree | E | File tree dump - temporary |
| docs/CONSOLIDATION_COMPLETE.py | E | Consolidation script - temporary |

### docs/archive/

| Path | Bucket | Reason |
|------|--------|--------|
| docs/archive/CODE_REVIEW_IMPLEMENTATION.md | D | Code review doc - AI artifact |
| docs/archive/COMPLETE_DEVELOPMENT_PLAN_PACKAGE.md | D | Development plan - AI artifact |
| docs/archive/COMPLETION_REPORT.md | D | Completion report - AI artifact |
| docs/archive/COOLIFY_REFACTOR_SUMMARY.md | D | Coolify refactor - AI artifact |
| docs/archive/DELIVERY_SUMMARY.md | D | Delivery summary - AI artifact |
| docs/archive/DEPLOYMENT_CHECKLIST.md | D | Deployment checklist - AI artifact |
| docs/archive/DEPLOYMENT_ENVIRONMENTS.md | D | Deployment envs - AI artifact |
| docs/archive/DEPLOYMENT_READINESS_REPORT.md | D | Readiness report - AI artifact |
| docs/archive/DEPLOYMENT_READY.md | D | Deployment ready - AI artifact |
| docs/archive/DEPLOYMENT_READY_FINAL.md | D | Final deployment ready - AI artifact |
| docs/archive/DEPLOYMENT_STEPS_COMPLETED.md | D | Steps completed - AI artifact |
| docs/archive/DEVELOPMENT_CLONE_README.md | D | Dev clone readme - AI artifact |
| docs/archive/DEVELOPMENT_PLAN_SUMMARY.md | D | Dev plan summary - AI artifact |
| docs/archive/FEATURE_DEVELOPMENT_PLAN.md | D | Feature plan - AI artifact |
| docs/archive/FINAL_DELIVERABLES.md | D | Final deliverables - AI artifact |
| docs/archive/FINAL_STATUS.md | D | Final status - AI artifact |
| docs/archive/IMPLEMENTATION_COMPLETE.md | D | Implementation complete - AI artifact |
| docs/archive/LOCALHOST_DEPLOYMENT_GUIDE.md | D | Localhost guide - AI artifact |
| docs/archive/LOCALHOST_PREREQUISITES_WINDOWS.md | D | Localhost prereqs - AI artifact |
| docs/archive/LOCALHOST_SETUP_SUMMARY.md | D | Localhost setup - AI artifact |
| docs/archive/MERGE_CONFLICT_RESOLUTION.md | D | Merge conflict - AI artifact |
| docs/archive/MERGE_RESOLUTION_SUMMARY.md | D | Merge resolution - AI artifact |
| docs/archive/MIGRATION_LOG.md | D | Migration log - AI artifact |
| docs/archive/MIGRATION_NOTES.md | D | Migration notes - AI artifact |
| docs/archive/PATH_CONSOLIDATION_SUMMARY.md | D | Path consolidation - AI artifact |
| docs/archive/PENDING_FEATURES_LIST.md | D | Pending features - AI artifact |
| docs/archive/PHASE1_SPRINT_PLAN.md | D | Phase 1 sprint - AI artifact |
| docs/archive/PRODUCTION_RELEASE_SUMMARY.md | D | Production release - AI artifact |
| docs/archive/PROGRESS.md | D | Progress report - AI artifact |
| docs/archive/QUICK_SUMMARY.md | D | Quick summary - AI artifact |
| docs/archive/SESSION_SUMMARY.md | D | Session summary - AI artifact |
| docs/archive/SIMS_REPAIR_PLAN.md | D | Repair plan - AI artifact |
| docs/archive/STAGE1_MERGE_SUMMARY.md | D | Stage 1 merge - AI artifact |
| docs/archive/SUMMARY.md | D | Summary - AI artifact |
| docs/archive/VALIDATION_SUMMARY.md | D | Validation summary - AI artifact |
| docs/archive/VERIFICATION_SUMMARY.md | D | Verification summary - AI artifact |
| docs/archive/VPS_CONFIG_139.162.9.224.md | F | VPS config IP-specific - cross-project |
| docs/archive/VPS_CONFIG_172.237.95.120.md | F | VPS config IP-specific - cross-project |
| docs/archive/VPS_DEPLOYMENT_GUIDE_139.162.9.224.md | F | VPS guide IP-specific - cross-project |
| docs/archive/WORKFLOW_CLEANUP_SUMMARY.md | D | Workflow cleanup - AI artifact |

### docs/reports/

| Path | Bucket | Reason |
|------|--------|--------|
| docs/reports/FEATURE_TESTING_REPORT.md | D | Feature testing report - AI artifact |
| docs/reports/STAGE1_READINESS_REPORT.md | D | Stage 1 readiness - AI artifact |

### logs/

| Path | Bucket | Reason |
|------|--------|--------|
| logs/test_reports/test_output.txt | E | Test output log - temporary |
| logs/test_reports/final_test_results.txt | E | Final test results - temporary |
| logs/test_reports/test_results.txt | E | Test results - temporary |
| logs/test_reports/test_results2.txt | E | Test results variant - temporary |
| logs/test_reports/case_create_error.txt | E | Error log - temporary |

### sims/ (Core Application)

| Path | Bucket | Reason |
|------|--------|--------|
| sims/**/*.py | A | Django application code - core runtime |
| sims/**/migrations/*.py | A | Database migrations - core runtime |
| sims/static/css/theme.css | A | Static CSS - core runtime |
| sims/static/js/theme.js | A | Static JS - core runtime |
| sims/conftest.py | A | Pytest config - test infrastructure |

### sims_project/ (Django Project)

| Path | Bucket | Reason |
|------|--------|--------|
| sims_project/*.py | A | Django project files - core runtime |

### static/ (Static Files)

| Path | Bucket | Reason |
|------|--------|--------|
| static/css/theme.css | A | Static CSS - core runtime |
| static/images/fmu-logo.png | A | Project logo - core runtime |
| static/js/theme.js | A | Static JS - core runtime |

### templates/ (Django Templates)

| Path | Bucket | Reason |
|------|--------|--------|
| templates/**/*.html | A | Django templates - core runtime |

### tests/ (Test Files)

| Path | Bucket | Reason |
|------|--------|--------|
| tests/**/*.py | A | Test files - test infrastructure |
| tests/resources/test_pages.html | A | Test resource - test infrastructure |
| tests/conftest.py | A | Pytest config - test infrastructure |

### frontend/ (Next.js Frontend)

| Path | Bucket | Reason |
|------|--------|--------|
| frontend/**/*.ts | A | TypeScript source - core runtime |
| frontend/**/*.tsx | A | React components - core runtime |
| frontend/**/*.js | A | JavaScript config - core runtime |
| frontend/**/*.json | A | NPM config - core runtime |
| frontend/**/*.css | A | Styles - core runtime |
| frontend/.env.local.example | B | Environment template - deployment |
| frontend/README.md | C | Frontend documentation - legitimate doc |
| frontend/.eslintrc.json | A | Linting config - dev tools |
| frontend/.gitignore | A | Git ignore - version control |

## Summary Statistics

| Bucket | Count | Percentage | Description |
|--------|-------|------------|-------------|
| A | ~250 | ~45% | Core Runtime Code |
| B | ~60 | ~11% | Deployment & Infrastructure |
| C | ~35 | ~6% | Legitimate Project Documentation |
| D | ~140 | ~25% | AI Agent Artifacts |
| E | ~60 | ~11% | Temporary Diagnostics & Logs |
| F | ~15 | ~3% | Cross-Project / Platform Leakage |
| G | ~3 | ~1% | Ambiguous |

**Total Files Analyzed:** ~563 files

## Recommendations for Phase B

### High Priority (Delete)
1. **Bucket D** (AI Artifacts): 140 files - All AI session reports, completion logs, implementation summaries
2. **Bucket E** (Temporary): 60 files - All test logs, diagnostic scripts, temporary import scripts

### Medium Priority (Review/Archive)
3. **Bucket F** (Cross-Project): 15 files - IP-specific deployment docs, external platform guides
   - Option 1: Delete if not needed for this specific repository
   - Option 2: Archive to docs/archive/server-specific/ if historically important

### Low Priority (Keep)
4. **Bucket G** (Ambiguous): 3 files - Review and reclassify
5. **Bucket C** (Legitimate Docs): 35 files - Keep all
6. **Bucket B** (Deployment): 60 files - Keep all (needed for deployment)
7. **Bucket A** (Core Runtime): 250 files - Keep all (essential application code)

## Next Steps

1. Proceed to **Phase B** - Surgical Cleanup
2. Delete all Bucket D files (AI artifacts)
3. Delete all Bucket E files (temporary diagnostics)
4. Review Bucket F files (cross-project leakage)
5. Document all actions in docs/CLEANUP_LOG.md
