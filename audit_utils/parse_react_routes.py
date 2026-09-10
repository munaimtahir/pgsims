import os
import re

app_dir = 'frontend/app'
routes = []

def scan_dir(path, prefix='/'):
    try:
        entries = os.listdir(path)
    except FileNotFoundError:
        return

    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            if entry.startswith('(') and entry.endswith(')'):
                # NextJS route group, doesn't add to URL
                scan_dir(full_path, prefix)
            else:
                new_prefix = f"{prefix}{entry}/"
                scan_dir(full_path, new_prefix)
        elif entry == 'page.tsx' or entry == 'page.jsx':
            routes.append(prefix)

scan_dir(app_dir)

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/02_FRONTEND_ROUTE_INVENTORY.md", "w") as f:
    f.write("# Frontend Route Inventory\n\n")
    f.write("| Route Path | Type | Role Requirement |\n")
    f.write("|---|---|---|\n")
    for r in sorted(routes):
        f.write(f"| {r} | PAGE | UNVERIFIED |\n")
