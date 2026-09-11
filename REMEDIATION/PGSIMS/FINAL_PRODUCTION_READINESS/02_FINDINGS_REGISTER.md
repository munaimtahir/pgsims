# Findings disposition

| Finding | Severity | Disposition |
|---|---:|---|
| PGSIMS-C-002 Django 4.2 constraint | P1 | Fixed: `Django>=5.2,<5.3`; compatibility gates recorded. |
| PGSIMS-C-006 disaster backup directory | P2 | Fixed and regression-tested. |
| PGSIMS-C-003 frontend advisories | P2 | Safe patch remediation applied; remaining major-upgrade advisories documented. |
| PGSIMS-C-004 Ruff debt | P3 | Deferred as broad legacy/dead-code cleanup; no functional auto-fix applied. |
| PGSIMS-C-005 generic exceptions | P3 | Deferred except where a behavior-preserving narrowing is proven. |
| F-A-002 legacy routes | P3 | Retained: repository tests and server-rendered compatibility routes still reference them. |
| F-B-001 `User.supervisor` | P3 | Retained and marked deprecated; canonical authorization uses assignment profiles. |
