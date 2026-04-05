# 07 Import Execution

## Runtime Import Surface

Executed inside running backend container (`pgsims_backend`) with active application code under `/app`.

Importer surfaces used:

- userbase entities via `sims.bulk.userbase_engine.import_entity(...)`
  - `faculty-supervisors`
  - `residents`
  - `supervision-links`
- training entities via `sims.bulk.services.BulkService`
  - `import_training_programs(...)`
  - `import_resident_training_records(...)`

## Import Source Used During Apply

- Canonical package validated first: `pilot_data/first_pilot_run/`
- Apply executed from transformed compatibility package:
  - `/tmp/first_pilot_run_transformed/` (container copy of `pilot_data/first_pilot_run_transformed/`)

## Dependency Order Used

1. training programs
2. faculty/supervisors
3. residents
4. supervision links
5. resident training records

## Execution Notes

- Initial direct canonical apply failed due to strict required dates.
- After deterministic transform, import completed with all entities successful.
- Commands executed with strict mode and captured JSON summaries.

