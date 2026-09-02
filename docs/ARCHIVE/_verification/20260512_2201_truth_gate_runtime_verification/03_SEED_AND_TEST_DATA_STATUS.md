# Seed and Test Data Status

## Seed infrastructure

| Item | Exists | Safe? | Mutates DB? | Used by E2E? | Notes |
|---|---|---|---|---|---|
| `scripts/e2e_seed.sh` | yes | yes, on local docker only | yes | yes | official seed path |
| `seed_org_data` | yes | yes | yes | yes | creates canonical org data |
| `seed_active_surface_baseline` | yes | yes | yes | yes | creates `pilot_*` users |
| `seed_e2e` | yes | yes | yes | yes | creates `e2e_*` users |

## Safety strategy

**Strategy B** was used: the official seed path mutates the local Docker runtime DB, but this is acceptable because the stack is local/non-production.

## What happened

1. `./scripts/e2e_seed.sh` completed.
2. The runtime DB initially only showed the `pilot_*` baseline users.
3. Running `seed_e2e` directly made the `e2e_*` users visible in the runtime DB.
4. After that, login API and browser smoke flows succeeded.

## Seeded users now visible

`e2e_admin`, `e2e_utrmc_admin`, `e2e_utrmc_user`, `e2e_supervisor`, `e2e_pg`

## Classification

- **Issue type:** seed/test-data issue
- **Status:** resolved for this sprint by rerunning the official seed command
