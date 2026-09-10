import re

backend_routes = []
with open("backend_endpoints.txt") as f:
    for line in f:
        backend_routes.append(line.strip())

android_calls = []
with open('AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/09_ANDROID_BACKEND_MAP.md', 'r') as f:
    for line in f:
        if line.startswith('| /api/'):
            android_calls.append(line.split('|')[1].strip())

with open('AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/09_ANDROID_BACKEND_MAP.md', 'w') as f:
    f.write("# Android to Backend API Map\n\n")
    f.write("| Android API Endpoint | Backend Route Match | Match Status | Notes |\n")
    f.write("|---|---|---|---|\n")
    for ac in android_calls:
        matched = False
        ac_clean = ac.rstrip('/')
        for br in backend_routes:
            parts = br.split(" | ")
            if len(parts) >= 4:
                br_route = parts[1]
                br_clean = re.sub(r'<[^>]+>', '{id}', br_route).rstrip('/')
                br_clean = br_clean.replace('{id}', '{residentId}') # handle diff naming

                if ac_clean == br_clean or ac_clean == br_clean.replace('{residentId}', '{id}'):
                    f.write(f"| `{ac}` | `{br_route}` | CONNECTED_UNVERIFIED_RUNTIME | - |\n")
                    matched = True
                    break
        if not matched:
            f.write(f"| `{ac}` | Unknown | BROKEN | No matching backend endpoint found |\n")
