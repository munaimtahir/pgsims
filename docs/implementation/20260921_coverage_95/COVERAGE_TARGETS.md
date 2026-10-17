# Coverage target profiles

The authoritative targets are machine-readable in
`scripts/coverage_manifest.json` and enforced by `scripts/coverage_gate.py`.
Coverage is evaluated independently by platform, functional area, and metric;
it is never averaged across them.

## Current sprint — `sprint_risk_reduction`

Android is deliberately deferred from this sprint because this VPS cannot run
the dedicated Laptop `pgsims` emulator and isolated loopback backend required
for connected JaCoCo evidence.

| Platform | Overall target | Per-area target |
| --- | --- | --- |
| Backend | 85% lines; 70% branches | 80% lines; 65% branches in every source-bearing area |
| Frontend | 60% lines; 50% branches; 58% statements; 55% functions | Exact area overrides below |

| Frontend area | Lines | Branches | Statements | Functions |
| --- | ---: | ---: | ---: | ---: |
| identity | 82 | 76 | 82 | 72 |
| onboarding | 70 | 50 | 65 | 55 |
| directories | 92 | 90 | 92 | 92 |
| training | 85 | 75 | 85 | 90 |
| academics | 55 | 40 | 55 | 60 |
| notifications | 60 | N/A | 60 | 55 |
| imports_reporting | 50 | 35 | 50 | 45 |
| backup_integrations | 70 | 55 | 70 | 60 |
| infrastructure | 65 | 60 | 60 | 55 |

`N/A` is retained when a source area has no executable decision branches; it
is not fabricated as 100%. Areas without source for a platform are outside
that platform's denominator.

Run the current gate after fresh evidence:

```bash
.venv/bin/python scripts/coverage_gate.py backend
.venv/bin/python scripts/coverage_gate.py report --target-profile sprint_risk_reduction --platform backend
.venv/bin/python scripts/coverage_gate.py frontend
.venv/bin/python scripts/coverage_gate.py report --target-profile sprint_risk_reduction --platform frontend
```

## Subsequent profiles

| Profile | Backend overall / area | Frontend overall / area | Android |
| --- | --- | --- | --- |
| `phase_2_hardening` | 92/85 lines/branches; 90/80 per area | 75/65/73/70; 70/60/70/65 per area | Deferred |
| `phase_3_release_floor` | 95% lines and branches everywhere | 95% all four metrics everywhere | 95% lines, branches, methods per area after Laptop connected coverage |
| `phase_4_preferred` | 99% lines and branches everywhere executable | 99% all four metrics everywhere executable | 99% lines, branches, methods everywhere executable |

Before claiming a later phase, investigate every residual executable line or
branch and document any structural non-executable rationale in test evidence.
