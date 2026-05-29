# PGSIMS Caddy Routine (Canonical)

This is the only supported production routing routine:

- Docker Compose: `docker/docker-compose.prod.yml`
- Caddy source of truth: `deploy/Caddyfile.pgsims`
- Active Caddy file: `/etc/caddy/Caddyfile`

## 1) Start application stack

```bash
cd /srv/apps/pgsims
docker compose -f docker/docker-compose.prod.yml up -d --build
```

## 2) Sync Caddyfile to active path

```bash
cd /srv/apps/pgsims
sudo cp deploy/Caddyfile.pgsims /etc/caddy/Caddyfile
```

## 3) Validate + reload Caddy

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

## 4) Verification checks

```bash
curl -I https://<domain>/
curl -I https://<domain>/api/health/
curl -I https://<domain>/admin/
curl -I https://<domain>/static/admin/css/base.css
curl -I https://<domain>/media/
```

## 5) Static/media alignment

- Caddy serves from host paths:
  - `/srv/apps/pgsims/backend/staticfiles`
  - `/srv/apps/pgsims/backend/media`
- Docker Compose writes to those same host paths via bind mounts in `docker/docker-compose.prod.yml`.
