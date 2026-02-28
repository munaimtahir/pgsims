# Rewire Audit Findings

## Repo-wide audit
- Raw token scan (`\bweb\b`) evidence: `OUT/rg_web_after_raw.txt`
- Strict service/host dependency scan evidence: `OUT/rg_web_after.txt`
- Strict service/host matches remaining: **0**

## ✅ Removed/Updated references
- Compose service keys standardized to `backend`.
- Docker command references (`exec/logs/restart web`) standardized to `backend`.
- Internal compose host references `http://web:` standardized to `http://backend:`.

## ⚠️ Remaining `web` token references (classified)
- README.md:3:A comprehensive Django web application for managing postgraduate medical residents' academic and training records.
- README.md:26:SIMS (Surgical Information Management System) is a comprehensive web-based management system designed specifically for postgraduate medical training programs. It provides a complete solution for tracking trainee progress, managing rotations, maintaining digital logbooks, and handling clinical case submissions.
- frontend/.eslintrc.json:2:  "extends": ["next/core-web-vitals", "next/typescript"]

Classification:
- `README.md` narrative uses (`web application`, `web-based`) -> **OK (terminology, not service dependency)**
- `frontend/.eslintrc.json` (`core-web-vitals`) -> **OK (framework preset name)**
- Historical outputs under `OUT/` and `docs/_archive/` -> **OK (historical evidence content)**

## Must-fix count
- Service/host dependency references to `web`: **0**
