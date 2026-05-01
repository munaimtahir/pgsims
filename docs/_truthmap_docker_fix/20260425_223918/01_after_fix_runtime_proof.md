# Runtime Proof After Frontend Rebuild

- Timestamp window: `2026-04-25 22:40 UTC` to `2026-04-25 22:57 UTC`
- Evidence JSON:
  - `json/stage3_browser_proof.json`
  - `json/stage4_route_smoke.json`
  - `json/stage5_api_checks.json`
  - `json/stage5_ui_checks.json`

## 1. Container / Image Proof

### Before rebuild

- Frontend image: `docker-frontend:latest`
- Frontend image ID: `27dcafb0173a`
- Frontend container: missing

### After rebuild

- Frontend image: `docker-frontend:latest`
- Frontend image ID: `fa0d04397dab`
- Frontend container ID: `f1ace7c48edc4e30f6ca874053e7b5b2491b4677be1547441ca084853611e313`
- Frontend container created: `2026-04-25T22:47:08.217188265Z`
- Frontend port binding: `127.0.0.1:8082 -> 3000`
- Frontend state after rebuild: `running`

### Compose / image observations

- `docker/docker-compose.yml` has no frontend bind mount.
- `frontend/Dockerfile` is a clean multi-stage Next.js standalone build:
  - builder runs `npm run build`
  - runner copies `.next/standalone`, `.next/static`, and `public`
- No mounted host `.next` directory overrides the built image.
- Frontend logs after rebuild:

```text
▲ Next.js 14.2.33
- Local:   http://localhost:3000
- Network: http://0.0.0.0:3000
✓ Starting...
✓ Ready in 146ms
```

## 2. Runtime Proof

### Direct HTTP checks

- `curl http://127.0.0.1:8082/login` -> `200 OK`
- `curl http://127.0.0.1:8082/dashboard/resident` (unauthenticated) -> `307 Temporary Redirect` to `/login`
- `curl http://127.0.0.1:8014/healthz/` -> `200 OK`

Interpretation:

- The rebuilt frontend is serving current routes.
- Protected dashboard routes resolve through app routing and redirect to auth; they are not stale `404`s.

## 3. Browser Proof

Playwright UI login was run against the rebuilt container. Dashboard screenshots are in `screenshots/` and traces are in `traces/`.

### Roles verified

| Role | Final URL | Heading | Nav matched current source? |
|---|---|---|---|
| `resident_user` | `/dashboard/resident` | `My Training Dashboard` | Yes |
| `supervisor_user` | `/dashboard/supervisor` | `Supervisor Dashboard` | Yes |
| `utrmc_admin_user` | `/dashboard/utrmc` | `UTRMC Overview` | Yes |
| `utrmc_staff_user` | `/dashboard/utrmc` | `UTRMC Overview` | Yes |
| `e2e_admin` | `/dashboard/utrmc` | `UTRMC Overview` | Yes |

### Source-of-truth nav compared against runtime

Source: `frontend/lib/navRegistry.ts`

- Resident nav expected and observed:
  - `My Dashboard`
  - `My Schedule`
  - `Logbook`
- Supervisor nav expected and observed:
  - `Overview`
  - `My Residents`
- UTRMC/admin nav expected and observed:
  - `Overview`
  - `Hospitals`
  - `Departments`
  - `H-D Matrix`
  - `Users`
  - `Supervision Links`
  - `HOD Assignments`
  - `Programmes`
  - `Eligibility Monitor`

## 4. Freshness Verdict

Frontend freshness is proven.

- The previously missing `frontend` container was rebuilt from scratch.
- The running image ID changed from `27dcafb0173a` to `fa0d04397dab`.
- The new container creation time is post-rebuild.
- The rebuilt runtime serves current dashboard routes and current nav structure from source.

## 5. Important Runtime Note

`docker compose up -d frontend` recreated `db` and `backend`, which exposed a local env drift:

- repo `.env` is effectively empty
- previous backend runtime had non-empty `SECRET_KEY` and DB password
- backend briefly crash-looped until it was restarted with the pre-rebuild runtime env

That was an environment/config baseline problem, not an application feature gap.
