# Health Check Specifications - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

PGMS provides dual-layered health check endpoints:

## 1. Gateway Level Health Check
- **Endpoint**: `GET /health/`
- **Format**: Plain text `OK` (HTTP 200).
- **Usage**: Used by frontend load balancers or proxy routes (like Nginx/Caddy) to verify that the container is reachable.

## 2. API Level Health Check
- **Endpoint**: `GET /api/health/`
- **Format**: JSON
- **Response Structure**:
  ```json
  {
    "status": "ok",
    "database": "ok",
    "app": "pgms",
    "version": "v0.12"
  }
  ```
- **Integrity**: Actively verifies connection to PostgreSQL. If the database connection is lost, it returns `database: failed` with an HTTP status indicating failure.
- **Verification**: Tested using `scripts/check_pgms_health.sh` and covered in academics tests.
