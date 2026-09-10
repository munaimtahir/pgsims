import re

backend_routes = []
with open("backend_endpoints.txt") as f:
    for line in f:
        backend_routes.append(line.strip())

frontend_calls = []
with open("frontend_api_calls.txt") as f:
    for line in f:
        frontend_calls.append(line.strip().strip("'\"`"))

android_calls = []
with open('AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/09_ANDROID_BACKEND_MAP.md', 'r') as f:
    for line in f:
        if line.startswith('| `/api/'):
            android_calls.append(line.split('|')[1].strip().strip('`'))

frontend_calls_clean = [re.sub(r'\$\{.*?\}', '{id}', x).rstrip('/') for x in frontend_calls]
android_calls_clean = [x.rstrip('/') for x in android_calls]

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/05_BACKEND_CLIENT_REVERSE_MAP.md", "w") as f:
    f.write("# Backend to Client Reverse Map\n\n")
    f.write("| Backend Endpoint | Handler | Consumers | Status |\n")
    f.write("|---|---|---|---|\n")

    for br in backend_routes:
        parts = br.split(" | ")
        if len(parts) >= 4:
            kind = parts[0]
            br_route = parts[1]
            handler = parts[2]

            br_clean = re.sub(r'<[^>]+>', '{id}', br_route).rstrip('/')
            br_clean_android = br_clean.replace('{id}', '{residentId}')

            consumers = []

            if kind == "ADMIN":
                consumers.append("Django Admin")
            elif kind == "WEB":
                consumers.append("Django Templates")
            else:
                if br_clean in frontend_calls_clean:
                    consumers.append("React Web")
                if br_clean in android_calls_clean or br_clean_android in android_calls_clean:
                    consumers.append("Android")

            if not consumers:
                if 'dummy' in handler or 'redirect' in handler:
                    status = "LEGACY_COMPATIBILITY"
                else:
                    status = "ORPHAN_SUSPECTED"
            else:
                status = "MAPPED"

            f.write(f"| `{br_route}` | `{handler}` | {', '.join(consumers) if consumers else 'None Found'} | {status} |\n")
