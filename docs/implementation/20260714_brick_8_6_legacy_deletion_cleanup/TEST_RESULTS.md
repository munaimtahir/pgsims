# Test Results

- `python3 backend/manage.py check` -> PASS
- `python3 backend/manage.py makemigrations --check --dry-run` -> PASS (`No changes detected`)
- `python3 backend/manage.py repair_identity_profiles` -> PASS
- `python3 -m pytest backend/sims --ignore=backend/sims/_legacy` -> PASS (`400 passed, 8 skipped`)
- `cd frontend && npm run lint` -> PASS
- `cd frontend && npm run build` -> PASS
- `cd frontend && npm run typecheck` -> PASS
- `docker compose --env-file .env -f docker/docker-compose.yml config` -> PASS
- `bash scripts/check_update_0_identity_cleanup.sh` -> PASS
- `bash scripts/check_brick_6_masters_directory_data_quality.sh` -> PASS
- `bash scripts/check_brick_7_clean_fresh_supervision_spine.sh` -> PASS
- `bash scripts/check_brick_8_academic_workflow_foundation.sh` -> PASS
- `bash scripts/check_canonical_frontend_roles.sh` -> PASS
- `bash scripts/check_canonical_source_of_truth.sh` -> PASS
- `bash scripts/check_legacy_delete_candidates.sh` -> PASS
