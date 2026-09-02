# Baseline Seed And Reset

## Seed Command
```bash
cd frontend && npm run test:e2e:feature-layer:seed
```

This executes `scripts/e2e_seed.sh`:
- `python manage.py migrate --noinput`
- `python manage.py seed_org_data --apply`
- `python manage.py seed_active_surface_baseline`
- `python manage.py seed_e2e`
- cache clear

## Verified Roles
- `e2e_pg / Pg123456!`
- `e2e_supervisor / Supervisor123!`
- `e2e_utrmc_admin / UtrmcAdmin123!`
- `e2e_utrmc_user / Utrmc123!`
- `resident_user / ResidentUser123!`
- `supervisor_user / SupervisorUser123!`
- `utrmc_admin_user / UtrmcAdminUser123!`
- `utrmc_staff_user / UtrmcStaffUser123!`

## Result
Seed was run repeatedly in this gate and produced deterministic no-op/update output after the first pass.

