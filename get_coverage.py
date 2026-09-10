import csv

total_frontend_routes = 0
total_frontend_mapped = 0

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/04_FRONTEND_BACKEND_TRUTH_MAP.md") as f:
    for line in f:
        if "CONNECTED" in line:
            total_frontend_mapped += 1
        if line.startswith("| N/A |"):
            total_frontend_routes += 1

total_backend_routes = 0
total_backend_mapped = 0

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/05_BACKEND_CLIENT_REVERSE_MAP.md") as f:
    for line in f:
        if line.startswith("| `/"):
            total_backend_routes += 1
            if "MAPPED" in line or "LEGACY_COMPATIBILITY" in line:
                total_backend_mapped += 1

with open("AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/06_ROUTE_COVERAGE.csv", "w") as f:
    f.write("Metric,Count,Percentage\n")
    f.write(f"Total Frontend API Calls Discovered,{total_frontend_routes},100%\n")
    f.write(f"Frontend Calls Mapped to Backend,{total_frontend_mapped},{round(total_frontend_mapped/total_frontend_routes*100) if total_frontend_routes else 0}%\n")
    f.write(f"Total Backend Routes Discovered,{total_backend_routes},100%\n")
    f.write(f"Backend Routes with Consumers,{total_backend_mapped},{round(total_backend_mapped/total_backend_routes*100) if total_backend_routes else 0}%\n")
