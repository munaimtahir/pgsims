# Urology institutional demonstration bootstrap

Source: `urology_pgsims_institutional_demo_ready.xlsx` (SHA-256 `8c0c5ad1125b7a396924f6425795309d9cb1eed2f56053545a17ddb511d066de`).

The runtime importer is `backend/sims/users/management/commands/bootstrap_urology_demo.py`.
It requires the workbook at invocation time because the workbook contains resident personal data.

## Safe invocation

```bash
python manage.py bootstrap_urology_demo /path/to/urology_pgsims_institutional_demo_ready.xlsx --dry-run
python manage.py bootstrap_urology_demo /path/to/urology_pgsims_institutional_demo_ready.xlsx
```

The command validates exactly 28 approved rows, runs in one transaction, reuses canonical masters,
normalizes supervisor names/titles, creates individual workshop completion records, and stores the
normalized research stage in `ResidentTrainingRecord.extra_data["demo_research_stage"]`.

## Evidence

- Laptop: branch `main`, SHA `c1d8c1e`; VPS baseline: branch `main`, SHA `6ed50a4` (not synchronized).
- Target: VPS Docker backend, `sims_project.settings`, PostgreSQL database `sims_db`; pre-import dump saved as `/tmp/pgsims_pre_urology_20260910.dump`.
- VPS post-import: 1 FMU, 1 AHF-I, 1 Urology department, 2 programmes, 28 residents (21 MS / 7 FCPS), 28 years, 28 induction dates, 28 primary assignments, 5 workshops, 45 workshop completions, and 28 research stages.
- A corrected second execution completed without increasing these counts.

Web/API and Android smoke verification remain pending in this repository state.
