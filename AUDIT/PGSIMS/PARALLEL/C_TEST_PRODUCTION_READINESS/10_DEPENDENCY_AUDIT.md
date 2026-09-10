# Dependency Audit

## Backend (pip)
Audited via `pip-audit`.

**Findings:**
- `django` version `4.2.30` is installed due to a restriction (`Django>=4.2,<5.0`) in `requirements.txt`.
- **Confirmed EOL Fact:** Django 4.2 security support ended in April 2026. PGSIMS remains pinned to Django 4.2.30 and therefore depends on an unsupported core framework branch that no longer receives security updates.
- **Scanner-only findings:** `pip-audit` flags 7 specific vulnerabilities (e.g. PYSEC-2026-3717, CVE-2026-48587) in `4.2.30`. These are scanner-reported advisories against the general framework version and have not been individually confirmed as exploitable via PGSIMS's specific code paths.
- **Recommendation:** Upgrade Django to a currently supported branch (`5.2`+ or `6.0`+) by adjusting `requirements.txt`.

## Frontend (npm)
Audited via `npm audit`.

**Findings:**
- 20 total vulnerabilities found: 1 critical, 14 high, 3 moderate, 2 low.
- Most vulnerabilities (like `postcss-selector-parser` and `ws`) are embedded deep within Next.js dev/build dependencies, not production runtime dependencies exposed to end-users via the standalone server build.
- **Recommendation:** Run `npm audit fix` for safe upgrades, and plan a major version upgrade for Next.js to address the remainder.

## Android
Android dependencies typically tracked via Gradle. The build succeeded without major dependency errors.
