import os
import shutil
import glob

PROJECT_ROOT = "/home/munaim/srv/apps/pgsims"
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
ARCHIVE_DIR = os.path.join(DOCS_DIR, "ARCHIVE")

# Ensure ARCHIVE directory exists
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# List of folders to archive from docs/
folders_to_archive = [
    "_archive",
    "_cleanup",
    "_discovery",
    "_milestones",
    "_mobile_android",
    "_pilot_cleanup",
    "_pilot_import",
    "_pilot_launch",
    "_recovery",
    "_truthmap",
    "_truthmap_docker_fix",
    "_ui_audit",
    "_verification",
    "deploy",
    "integration",
    "testing",
]

# Move folders to ARCHIVE if they exist
for folder in folders_to_archive:
    src = os.path.join(DOCS_DIR, folder)
    if os.path.exists(src) and folder != "ARCHIVE":
        dst = os.path.join(ARCHIVE_DIR, folder)
        # Avoid moving into itself if run multiple times
        if not os.path.exists(dst):
            print(f"Moving folder {src} -> {dst}")
            shutil.move(src, dst)
        else:
            print(f"Destination already exists, deleting source: {src}")
            shutil.rmtree(src)

# Move obsolete files in docs/ to docs/ARCHIVE/
files_to_archive = [
    "AI_AGENT_ENTRY_POINTS.md",
    "ANALYTICS_BLUEPRINT.md",
    "ANALYTICS_DIMENSIONS.md",
    "ANALYTICS_GOVERNANCE.md",
    "ANALYTICS_LIVE_FEED.md",
    "ANALYTICS_MEGAPASS_REPORT.md",
    "ANALYTICS_OPENAPI.md",
    "ANALYTICS_PERFORMANCE.md",
    "ANALYTICS_RUNBOOK.md",
    "ANALYTICS_UI_SPEC.md",
    "ANTI_DRIFT_GUARDRAILS.md",
    "FINAL_RELEASE_FREEZE.md",
    "MCP_PLAYWRIGHT_AGENT.md",
]

for file in files_to_archive:
    src = os.path.join(DOCS_DIR, file)
    if os.path.exists(src):
        dst = os.path.join(ARCHIVE_DIR, file)
        print(f"Moving file {src} -> {dst}")
        shutil.move(src, dst)

# Move obsolete files from root to docs/ARCHIVE/
root_files_to_archive = [
    "copilot_session.md",
    "HANDOFF_PROD_GATE_20260422.md",
    "HANDOFF_PROD_GATE_20260422T221254Z.md",
    "REMEDIATION_SPRINT_SUMMARY.md",
    "PGSIMS_Demo_CaseSeed_3Months.csv",
    "PGSIMS_Demo_CaseSeed_3Months.xlsx",
]

for file in root_files_to_archive:
    src = os.path.join(PROJECT_ROOT, file)
    if os.path.exists(src):
        dst = os.path.join(ARCHIVE_DIR, file)
        print(f"Moving root file {src} -> {dst}")
        shutil.move(src, dst)

print("Documentation and directory archiving completed successfully.")
