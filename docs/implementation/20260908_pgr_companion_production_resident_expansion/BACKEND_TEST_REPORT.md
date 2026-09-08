# Backend test report

The new fixture command is syntactically compiled locally. The development shell has no Django
installation, so Django checks/tests are not claimed locally. Before production fixture use, the
rebuilt production image must pass `check`, `makemigrations --check --dry-run`, migration plan, and
the targeted command guard tests. No migration is included.
