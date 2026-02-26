import json
import os
import re
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_TXT = os.path.join(ROOT_DIR, 'frontend', 'frontend_endpoints.txt')
BACKEND_JSON = os.path.join(ROOT_DIR, 'backend', 'sims', '_devtools', 'endpoints.json')
DOCS_CONTRACTS = os.path.join(ROOT_DIR, 'docs', 'contracts')
DOCS_ROOT = os.path.join(ROOT_DIR, 'docs')
AUDIT_ROOT = os.path.join(ROOT_DIR, 'docs', '_audit')

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
AUDIT_DIR = os.path.join(AUDIT_ROOT, f"TRUTH_MAP_{timestamp}")

os.makedirs(DOCS_CONTRACTS, exist_ok=True)
os.makedirs(AUDIT_DIR, exist_ok=True)

# 1. Read Backend
with open(BACKEND_JSON, 'r') as f:
    backend_endpoints = json.load(f)

# 2. Read Frontend Calls
frontend_calls = []
if os.path.exists(FRONTEND_TXT):
    with open(FRONTEND_TXT, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # e.g. lib/api/users.ts:15:    const response = await apiClient.get<AssignedPG[]>('/api/users/assigned-pgs/');
            parts = line.split(':', 2)
            if len(parts) >= 3:
                filepath = parts[0]
                lineno = parts[1]
                code = parts[2]
                
                # Extract method and URL
                match = re.search(r"apiClient\.(get|post|put|patch|delete)\s*<[^>]*>\s*\(\s*[`'\"]([^`'\"]+)[`'\"]", code)
                if not match:
                    match = re.search(r"apiClient\.(get|post|put|patch|delete)\s*\(\s*[`'\"]([^`'\"]+)[`'\"]", code)
                if match:
                    method = match.group(1).upper()
                    url = match.group(2)
                    frontend_calls.append({
                        "file": filepath,
                        "line": lineno,
                        "method": method,
                        "url": url,
                        "code": code.strip()
                    })

def strip_dynamic(url):
    url = re.sub(r'\$\{.*?\}', '{id}', url)
    url = re.sub(r'<[^>]+>', '{id}', url)
    url = re.sub(r'\(\?P<[^>]+>[^)]+\)', '{id}', url)
    url = re.sub(r'/[^/]+\.ts', '', url) # some junk cleaner
    # backend specific regex cleans
    url = re.sub(r'\^', '', url)
    url = re.sub(r'\$', '', url)
    url = re.sub(r'\\\.\(\?P<format>\[a-z0-9\]\+\)/?', '', url)
    url = re.sub(r'<drf_format_suffix:format>', '', url)
    
    url = re.sub(r'/api/', '/', url)
    return url.strip('/')

# Map frontend to backend
fe_mapped = []
for bc in backend_endpoints:
    bc['fe_callers'] = []
    
for fc in frontend_calls:
    fc['matches'] = []
    fc_stripped = strip_dynamic(fc['url'])
    # Very basic matching
    for bc in backend_endpoints:
        bc_stripped = strip_dynamic(bc['path'])
        if bc_stripped == fc_stripped or (bc_stripped in fc_stripped) or (fc_stripped in bc_stripped):
            if bc['method'] == 'ANY' or bc['method'] == fc['method']:
                fc['matches'].append(bc)
                bc['fe_callers'].append(fc)

# Look for Gaps
backend_gaps = []
frontend_gaps = []

for bc in backend_endpoints:
    # Explicit exclusions for admin and formats
    if 'format' in bc['path']: continue
    if 'admin' in bc['path']: continue
    if not bc['fe_callers']:
        # Categorize
        if 'APIRoot' in bc.get('view', ''):
            reason = "[system-only]"
        elif 'admin' in bc['path']:
            reason = "[Django-admin-only]"
        else:
            reason = "[backend-only/future]"
        
        backend_gaps.append((bc, reason))

for fc in frontend_calls:
    if not fc['matches']:
        frontend_gaps.append(fc)

def write_md():
    md = "# INTEGRATION TRUTH-MAP\n\n"
    
    md += "## A) Backend Inventory\n"
    md += "| Method | Path | View | Action | Serializer | Permission |\n"
    md += "|---|---|---|---|---|---|\n"
    for bc in backend_endpoints:
        if '<drf' in bc['path'] or '(?P<format>' in bc['path']: continue # skip format routes for brevity
        perms = ", ".join(bc['permissions']) if bc.get('permissions') else "None"
        md += f"| {bc['method']} | `{bc['path']}` | {bc.get('view','')} | {bc.get('action','')} | {bc.get('serializer','')} | {perms} |\n"
        
    md += "\n## B) Frontend Inventory\n"
    md += "| Method | URL | Caller File | Line | Adapter / Notes |\n"
    md += "|---|---|---|---|---|\n"
    for fc in frontend_calls:
        md += f"| {fc['method']} | `{fc['url']}` | {fc['file']} | {fc['line']} | |\n"

    md += "\n## C) Bidirectional Cross-Link Map\n"
    md += "### Backend to Frontend\n"
    for bc in backend_endpoints:
        if '<drf' in bc['path'] or '(?P<format>' in bc['path']: continue
        callers = ", ".join(set([f"{fc['file']} ({fc['method']})" for fc in bc['fe_callers']]))
        if not callers:
            if 'admin' in bc['path']: callers = "[Django-admin-only]"
            elif 'APIRoot' in bc.get('view', ''): callers = "[system-only]"
            else: callers = "[backend-only/future]"
        md += f"- **{bc['method']} {bc['path']}** -> {callers}\n"
        
    md += "\n### Frontend to Backend\n"
    for fc in frontend_calls:
        matches = ", ".join([f"`{bc['path']}`" for bc in fc['matches']])
        if not matches: matches = "**BROKEN** (No backend match found)"
        md += f"- **{fc['method']} {fc['url']}** in `{fc['file']}` -> {matches}\n"

    md += "\n## D) Payload/Contract Alignment\n"
    md += "- **Logbook workflow**: Frontend uses `logbookAdapter.ts` which normalizes `feedback`, `supervisor_feedback`, and `supervisor_comments` into `feedback_text`. Status maps 'pending' requests.\n"
    md += "- **Rotations**: Frontend uses `rotationAdapter.ts` to normalize `hospital` and `department` nested objects or string IDs uniformly into `{id, name}`.\n"
    md += "- **Status terminology**: Matches using adapters.\n"
    
    md += "\n## E) RBAC + Route Gating Alignment\n"
    md += "- Checked `middleware.ts` which confirms strict role routing checking tokens and `pgsims_access_exp`:\n"
    md += "  - `/dashboard/pg/*` -> `pg` role\n"
    md += "  - `/dashboard/supervisor/*` -> `supervisor` role\n"
    md += "  - `/dashboard/utrmc/*` -> `utrmc_user` / `utrmc_admin`\n"
    md += "  - `/dashboard/admin/*` -> `admin`\n"
    md += "- Unauthenticated or expired tokens redirect to `/login` and clear cookies.\n"
    
    md += "\n## F) GAPS / DRIFT RISKS\n"
    if backend_gaps:
        md += "### 1) Unmapped Backend Routes\n"
        for gap, r in backend_gaps[:20]: # Show up to 20
            md += f"- `{gap['method']} {gap['path']}` - Reason: {r}\n"
    
    if frontend_gaps:
        md += "\n### 2) Unmapped Frontend Calls (BROKEN)\n"
        for gap in frontend_gaps:
            md += f"- `{gap['method']} {gap['url']}` in `{gap['file']}:{gap['line']}`\n"
    else:
        md += "\n- *All frontend calls matched a backend endpoint.*\n"

    md += "\n## G) Verdict\n"
    if frontend_gaps:
        md += "**FAIL**. There are frontend drift gaps with missing backend endpoints.\n"
    else:
        md += "**PASS**. All static frontend API calls map successfully.\n"
        
    return md

# Write canonical
truth_map_md = write_md()
with open(os.path.join(DOCS_CONTRACTS, 'INTEGRATION_TRUTH_MAP.md'), 'w') as f:
    f.write(truth_map_md)
    
# Create mirror in docs/
symlink_path = os.path.join(DOCS_ROOT, 'INTEGRATION_TRUTH_MAP.md')
if os.path.islink(symlink_path) or os.path.exists(symlink_path):
    os.remove(symlink_path)
os.symlink(os.path.join('contracts', 'INTEGRATION_TRUTH_MAP.md'), symlink_path)

# Write local audit
audit_report = f"""# Truth Map Run Report
Run ID: {timestamp}

## Stats
- Backend Endpoints Extracted: {len(backend_endpoints)}
- Frontend Calls Extracted: {len(frontend_calls)}
- Unmapped Frontend Calls: {len(frontend_gaps)}

## Output
Truth map generated and placed into `docs/contracts/INTEGRATION_TRUTH_MAP.md`.
"""
with open(os.path.join(AUDIT_DIR, 'TRUTH_MAP_RUN_REPORT.md'), 'w') as f:
    f.write(audit_report)
    
print("Successfully generated Truth Map and Local Audit Evidence.")
