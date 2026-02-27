# Security Baseline

## Demo/Pilot Seed Users Policy
- Use least-privilege role assignments for pilot accounts.
- No shared admin credentials.
- Disable or rotate temporary credentials after demos.

## Password Rotation Checklist
- Rotate Django admin/service user passwords on schedule.
- Rotate DB credentials in `.env` and restart services in maintenance window.
- Confirm old credentials are invalidated.

## Network Exposure Baseline
- Backend should bind loopback only (`127.0.0.1:8014`).
- Frontend should bind loopback only (`127.0.0.1:8082`).
- Public exposure should occur only through Caddy TLS proxy.
- Verify with:
  - `ss -tulpn`
  - `sudo caddy validate --config /etc/caddy/Caddyfile`
