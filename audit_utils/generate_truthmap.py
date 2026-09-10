import re

backend_routes = []
with open("backend_endpoints.txt") as f:
    for line in f:
        backend_routes.append(line.strip())

frontend_calls = []
with open("frontend_api_calls.txt") as f:
    for line in f:
        frontend_calls.append(line.strip().strip("'\"`"))

frontend_calls_clean = [re.sub(r'\$\{.*?\}', '{id}', x) for x in frontend_calls]

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/04_FRONTEND_BACKEND_TRUTH_MAP.md", "w") as f:
    f.write("# Frontend to Backend Truth Map\n\n")
    f.write("| Frontend Route/Component | API Call | Backend Route | Match Status | Notes |\n")
    f.write("|---|---|---|---|---|\n")

    # Very basic matching logic for static file generation
    for fc in frontend_calls_clean:
        matched = False

        for br in backend_routes:
            parts = br.split(" | ")
            if len(parts) >= 4:
                br_route = parts[1]
                # Replace django parameters with generic placeholder for string matching
                br_clean = re.sub(r'<[^>]+>', '{id}', br_route)

                # Strip trailing slashes for loose comparison
                fc_cmp = fc.rstrip('/')
                br_cmp = br_clean.rstrip('/')

                if fc_cmp == br_cmp:
                    f.write(f"| N/A | `{fc}` | `{br_route}` | CONNECTED_UNVERIFIED_RUNTIME | - |\n")
                    matched = True
                    break
        if not matched:
            f.write(f"| N/A | `{fc}` | Unknown | BROKEN | No exact backend route found |\n")
