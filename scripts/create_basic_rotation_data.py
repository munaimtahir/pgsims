PGSIMS / UTRMC — INTEGRATION TRUTH-MAP GENERATOR (Backend ↔ Frontend) — SINGLE AGENT PROMPT

You are an Integration Truth-Map Agent. Your job is to generate an evidence-backed, repo-derived mapping proving:
(1) every backend endpoint has a corresponding frontend consumer OR is explicitly “backend-only/admin-only/system-only”, and
(2) every frontend API call maps to an actual backend endpoint with correct method/path and payload fields,
including adapters/status normalization and RBAC implications.

HARD CONSTRAINTS
- Do NOT change routes or redesign UI.
- Do NOT change business logic, RBAC policy, or contracts except to ADD documentation artifacts.
- docs/_audit is LOCAL-ONLY and must NOT be committed.
- Canonical docs live in docs/contracts/. If mirrors exist, use symlinks; otherwise create minimal stub files pointing to canonical.
- Postgres is production target; do not introduce SQLite-only behavior (but this task is documentation/audit only).

REPO PATH ASSUMPTION
- Repo root contains /backend and /frontend.
- You are running in the repo root (or you can infer it).

PRIMARY OUTPUTS (must create)
1) docs/contracts/INTEGRATION_TRUTH_MAP.md  (canonical)
2) docs/INTEGRATION_TRUTH_MAP.md           (symlink mirror to docs/contracts/INTEGRATION_TRUTH_MAP.md; if symlink not feasible, create a stub pointing to canonical)
3) docs/_audit/TRUTH_MAP_<YYYYMMDD_HHMMSS>/TRUTH_MAP_RUN_REPORT.md (local-only evidence, not committed)
4) (Optional) scripts/truthmap/ generated helper scripts if needed, but keep minimal and documented.

WHAT THE TRUTH MAP MUST CONTAIN (MANDATORY SECTIONS)
A) “Backend Inventory”
   - Enumerate ALL backend API endpoints: method + path + view/function + action (list/retrieve/create/custom) + serializer (if known) + permission class + scope rule (OWN/SUPERVISEES/ALL).
   - Source of truth: backend URL/router registrations (e.g., api_urls.py, routers, urlpatterns, viewsets) and any custom @action routes.
   - Output as a table.

B) “Frontend Inventory”
   - Enumerate ALL frontend outbound API calls:
     - caller file + function name
     - HTTP method + URL path template
     - where token/cookies are applied (client.ts/auth.ts)
     - which adapter normalizes response (logbookAdapter/rotationAdapter/etc.)
     - which pages invoke the call (grep import/call sites where feasible)
   - Include Next.js middleware gating notes: which cookies are read; which routes are gated.
   - Output as a table.

C) “Bidirectional Cross-Link Map”
   - For EACH backend endpoint, list:
     - frontend callers (files/functions/pages) OR “no frontend consumer” with explicit reason:
       [backend-only], [system-only], [Django-admin-only], [future], [deprecated], [internal].
   - For EACH frontend call, list:
     - matching backend endpoint(s) with method/path confirmation.
     - If no match: mark as BROKEN and show evidence.

D) “Payload/Contract Alignment”
   - For key flows, list expected request/response fields and where they are normalized:
     - Logbook workflow: status, supervisor_feedback/feedback alias, submitted_at alias.
     - Rotations: hospital + department object shape and display fields.
     - Status terminology: pending -> Submitted mapping must be referenced via the single status utility.
   - Detect mismatches by static scan (field names used in frontend vs serializer fields).

E) “RBAC + Route Gating Alignment”
   - Confirm that each frontend dashboard route group maps to backend permissions:
     - /dashboard/pg/* -> pg + admin
     - /dashboard/supervisor/* -> supervisor + admin
     - /dashboard/utrmc/* -> utrmc_user/utrmc_admin + admin
     - /dashboard/admin/* -> admin
   - Confirm middleware cookie contract: access + role + exp only; invalid/expired => redirect /login and clear cookies.

F) “GAPS / DRIFT RISKS”
   - List:
     1) Backend endpoints with no frontend consumer (with allowed reasons).
     2) Frontend calls with no backend match.
     3) Method/path mismatches (GET vs POST etc.)
     4) Payload field mismatches (frontend sending/reading fields not in serializer)
     5) Duplicate/overlapping endpoints that could cause confusion
     6) Any scattered status mapping usage outside the shared utility
   - Each item must include file/line evidence references (path + a short snippet description; no huge dumps).

G) “Verdict”
   - PASS only if:
     - every frontend call has a backend match (or explicitly justified if it’s mocked/test-only),
     - every backend endpoint is either used or explicitly classified with an allowed reason,
     - no critical payload mismatch is found in core flows (logbook + rotations + auth).
   - Otherwise FAIL with prioritized fixes (but do NOT implement fixes in this run unless they are purely documentation).

IMPLEMENTATION PLAN (DO IN THIS ORDER)
1) Backend endpoint extraction:
   - Locate URL router registrations:
     - backend/**/api_urls.py, urls.py, router.register(...)
     - DRF viewsets, @action decorators
   - Produce a normalized list of endpoints.
   - If needed, write a small Python script under backend/sims/_devtools/truthmap_extract.py that:
     - imports Django URL resolver (WITHOUT requiring DB migration changes)
     - prints endpoints (method/path/view)
   - If import-based extraction is too heavy, do a conservative static parse of router registrations and @action paths.

2) Frontend call extraction:
   - Identify the API client module(s): frontend/lib/api/client.ts, auth.ts, any fetch wrappers.
   - Grep for `.get(` `.post(` `fetch(` usage in lib/api and pages.
   - Enumerate base URL + path composition rules (env vars, prefixes).
   - Map calls to pages where used (basic grep for function name imports/usages).

3) Cross-link:
   - Join on (method, path). Support path parameters (:id, [id], {id}) with normalization.
   - If frontend uses `/api/...` proxy paths vs backend direct paths, document the mapping explicitly.

4) Payload alignment scan (lightweight static):
   - For logbook + rotations + auth:
     - extract request body keys used in frontend calls
     - extract response keys read in UI and in adapters
     - compare against backend serializers / response construction
   - Flag mismatches.

5) Write docs/contracts/INTEGRATION_TRUTH_MAP.md:
   - Must be clean, readable, and structured with the mandatory sections A–G.

6) Write local-only audit evidence:
   - docs/_audit/TRUTH_MAP_<RUN_ID>/TRUTH_MAP_RUN_REPORT.md:
     - commands executed
     - counts: #backend endpoints, #frontend calls, #matched, #unmatched
     - list of gaps/drift risks
     - final PASS/FAIL

COMMANDS / EVIDENCE (RUN THESE)
- Backend:
  cd backend
  ../.venv/bin/python manage.py check
  (If you used import-based endpoint extraction) run the extractor script and capture output.
- Frontend:
  cd ../frontend
  npm run build  (SERIAL ONLY; do not run in parallel with Playwright)
  npx playwright test (optional; only if already stable and fast)
- For static scans:
  use ripgrep (rg) and save key command outputs into the audit report.

DO NOT COMMIT
- Any docs/_audit content.

COMMIT (OK)
- docs/contracts/INTEGRATION_TRUTH_MAP.md
- docs/INTEGRATION_TRUTH_MAP.md mirror (symlink or stub)
- any small helper script if created (document it in the truth map).

END WITH
- A TODO checklist with checkmarks:
  - [ ] backend inventory extracted
  - [ ] frontend inventory extracted
  - [ ] cross-link completed
  - [ ] payload alignment checked (logbook/rotations/auth)
  - [ ] RBAC + middleware cookie contract verified
  - [ ] gaps list produced with evidence
  - [ ] truth map doc written + mirror created
  - [ ] local-only audit report written
  - [ ] final PASS/FAIL stated#!/usr/bin/env python3
"""
Script to create basic departments and hospitals for rotation creation.

Created: 2025-01-27
Author: GitHub Copilot
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.rotations.models import Department, Hospital

def create_basic_data():
    """Create basic departments and hospitals if they don't exist"""
    print("=== Creating Basic Rotation Data ===")
    
    # Create hospitals if they don't exist
    hospitals_data = [
        {"name": "Main Teaching Hospital", "address": "Main Street, City", "type": "teaching"},
        {"name": "City General Hospital", "address": "Central Avenue, City", "type": "general"},
        {"name": "Specialty Medical Center", "address": "Health Complex, City", "type": "specialty"},
    ]
    
    for hospital_data in hospitals_data:
        hospital, created = Hospital.objects.get_or_create(
            name=hospital_data["name"],
            defaults=hospital_data
        )
        if created:
            print(f"✓ Created hospital: {hospital.name}")
        else:
            print(f"- Hospital already exists: {hospital.name}")
    
    # Create departments if they don't exist
    departments_data = [
        {"name": "Internal Medicine", "description": "General internal medicine rotation"},
        {"name": "Surgery", "description": "General surgery rotation"},
        {"name": "Pediatrics", "description": "Pediatric medicine rotation"},
        {"name": "Emergency Medicine", "description": "Emergency department rotation"},
        {"name": "Cardiology", "description": "Cardiovascular medicine rotation"},
        {"name": "Radiology", "description": "Medical imaging rotation"},
        {"name": "Anesthesiology", "description": "Anesthesiology rotation"},
        {"name": "Psychiatry", "description": "Mental health rotation"},
    ]
    
    for dept_data in departments_data:
        department, created = Department.objects.get_or_create(
            name=dept_data["name"],
            defaults=dept_data
        )
        if created:
            print(f"✓ Created department: {department.name}")
        else:
            print(f"- Department already exists: {department.name}")
    
    print(f"\nTotal hospitals: {Hospital.objects.count()}")
    print(f"Total departments: {Department.objects.count()}")

if __name__ == "__main__":
    create_basic_data()
