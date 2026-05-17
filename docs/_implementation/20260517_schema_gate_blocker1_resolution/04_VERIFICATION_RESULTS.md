# Verification Results

## Django Check

Command:

```bash
cd backend && python3 manage.py check
```

Result:

```text
System check identified no issues (0 silenced).
Exit code: 0
```

## Strict Schema Gate

Command:

```bash
cd backend && python3 manage.py spectacular --file /tmp/pgsims_schema.yaml --validate --fail-on-warn
```

Result:

```text
Exit code: 0
No schema warnings or errors emitted.
Schema file written to /tmp/pgsims_schema.yaml.
```

## Targeted Backend Tests

Command:

```bash
cd backend && pytest sims/users sims/bulk sims/notifications sims/training -q
```

Result:

```text
117 passed in 40.44s
Exit code: 0
```

Follow-up command after final operation ID correction:

```bash
cd backend && pytest sims/bulk sims/training -q
```

Result:

```text
80 passed in 30.34s
Exit code: 0
```

