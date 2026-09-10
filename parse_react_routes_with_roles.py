import os

app_dir = 'frontend/app'
routes = []

def get_role_req(route):
    if route.startswith('/dashboard/pg') or route.startswith('/dashboard/resident'):
        return 'RESIDENT, ADMIN'
    if route.startswith('/dashboard/supervisor'):
        return 'SUPERVISOR, ADMIN'
    if route.startswith('/dashboard/admin'):
        return 'ADMIN'
    if route.startswith('/dashboard/utrmc'):
        return 'SUPPORT_STAFF, ADMIN'
    if any(route.startswith(p) for p in ['/users', '/residents', '/supervisors', '/support-staff', '/admins', '/masters', '/supervision', '/academics']):
        return 'ADMIN'
    return 'ANY'

def scan_dir(path, prefix='/'):
    try:
        entries = os.listdir(path)
    except FileNotFoundError:
        return

    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            if entry.startswith('(') and entry.endswith(')'):
                scan_dir(full_path, prefix)
            else:
                new_prefix = f"{prefix}{entry}/"
                scan_dir(full_path, new_prefix)
        elif entry == 'page.tsx' or entry == 'page.jsx':
            routes.append((prefix, get_role_req(prefix)))

scan_dir(app_dir)

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/02_FRONTEND_ROUTE_INVENTORY.md", "w") as f:
    f.write("# Frontend Route Inventory\n\n")
    f.write("| Route Path | Type | Role Requirement |\n")
    f.write("|---|---|---|\n")
    for r, role in sorted(routes):
        f.write(f"| {r} | PAGE | {role} |\n")
