# 80 — RELEASE DEPLOY RUNBOOK

## Phase A — Confirm commit and push

### git status --short
```
?? OUT/80_RELEASE_DEPLOY_RUNBOOK.md
```

### git log -1 --oneline
```
64e9550 Userbase foundation: hospitals/departments matrix, users, assignments, linking, HOD roster, RBAC, tests, cleanup
```

### git rev-parse HEAD
```
64e9550ae9e729d12e16016b335a3b3266cd9da6
```

### git push origin main
```
Tno github.com:munaimtahir/pgsims
   c816659..64e9550  main -> main
```

Push exit code: 0

## Phase B — Deploy

### git pull origin main
```
Already up to date.
```

### docker compose up -d --build --remove-orphans
```
#1 [internal] load local bake definitions
#1 reading from stdin 1.92kB done
#1 DONE 0.0s

#2 [backend internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.94kB done
#2 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
#2 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
#2 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
#2 DONE 0.0s

#3 [frontend internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.53kB 0.0s done
#3 DONE 0.0s

#4 [worker internal] load metadata for docker.io/library/python:3.11-slim
#4 ...

#5 [frontend internal] load metadata for docker.io/library/node:20-alpine
#5 DONE 0.6s

#6 [frontend internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s

#7 [frontend deps 1/5] FROM docker.io/library/node:20-alpine@sha256:09e2b3d9726018aecf269bd35325f46bf75046a643a66d28360ec71132750ec8
#7 resolve docker.io/library/node:20-alpine@sha256:09e2b3d9726018aecf269bd35325f46bf75046a643a66d28360ec71132750ec8 0.0s done
#7 DONE 0.0s

#8 [frontend internal] load build context
#8 ...

#4 [beat internal] load metadata for docker.io/library/python:3.11-slim
#4 DONE 1.1s

#9 [beat internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s

#8 [frontend internal] load build context
#8 ...

#10 [beat builder 1/5] FROM docker.io/library/python:3.11-slim@sha256:c8271b1f627d0068857dce5b53e14a9558603b527e46f1f901722f935b786a39
#10 resolve docker.io/library/python:3.11-slim@sha256:c8271b1f627d0068857dce5b53e14a9558603b527e46f1f901722f935b786a39 0.1s done
#10 DONE 0.1s

#8 [frontend internal] load build context
#8 ...

#11 [worker internal] load build context
#11 transferring context: 16.50MB 3.0s done
#11 DONE 3.0s

#8 [frontend internal] load build context
#8 ...

#12 [beat stage-1 2/6] RUN apt-get update && apt-get install -y --no-install-recommends     libpq5     curl     && rm -rf /var/lib/apt/lists/*
#12 CACHED

#13 [beat builder 2/5] RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev     && rm -rf /var/lib/apt/lists/*
#13 CACHED

#14 [beat builder 3/5] WORKDIR /app
#14 CACHED

#15 [beat builder 4/5] COPY requirements.txt .
#15 CACHED

#16 [beat stage-1 3/6] RUN useradd -m -u 1000 sims &&     mkdir -p /app /app/staticfiles /app/media /app/logs &&     chown -R sims:sims /app
#16 CACHED

#17 [beat builder 5/5] RUN pip install --user -r requirements.txt
#17 CACHED

#18 [beat stage-1 4/6] COPY --from=builder --chown=sims:sims /root/.local /home/sims/.local
#18 CACHED

#19 [beat stage-1 5/6] WORKDIR /app
#19 CACHED

#8 [frontend internal] load build context
#8 transferring context: 167.06MB 5.6s done
#8 DONE 5.6s

#20 [beat stage-1 6/6] COPY --chown=sims:sims . .
#20 ...

#21 [frontend deps 5/5] RUN npm ci
#21 CACHED

#22 [frontend builder 2/5] WORKDIR /app
#22 CACHED

#23 [frontend deps 3/5] WORKDIR /app
#23 CACHED

#24 [frontend deps 2/5] RUN apk add --no-cache libc6-compat
#24 CACHED

#25 [frontend deps 4/5] COPY package.json package-lock.json* ./
#25 CACHED

#26 [frontend builder 3/5] COPY --from=deps /app/node_modules ./node_modules
#26 CACHED

#27 [frontend builder 4/5] COPY . .
#27 ...

#20 [worker stage-1 6/6] COPY --chown=sims:sims . .
#20 DONE 11.3s

#28 [beat] exporting to image
#28 exporting layers
#28 ...

#29 [worker] exporting to image
#29 ...

#30 [backend] exporting to image
#30 ...

#29 [worker] exporting to image
#29 exporting layers 14.3s done
#29 exporting manifest sha256:627369d478a637a0900a166c6bbe9775c9dc6855cec26496d7358cf6b9840746
#29 exporting manifest sha256:627369d478a637a0900a166c6bbe9775c9dc6855cec26496d7358cf6b9840746 0.0s done
#29 exporting config sha256:fd9b9b37714b89b6ce91cf5d2251521a13e316663ca352f44f51b063b205718a 0.1s done
#29 exporting attestation manifest sha256:f054df606083d81217eca755f5efd66df8800eb3b6b75f83382c1b8b69990fca 0.1s done
#29 exporting manifest list sha256:24c93ac9cccc762f669dd15910526feeb27f9001dc88f71648c5287a57d4e43b
#29 exporting manifest list sha256:24c93ac9cccc762f669dd15910526feeb27f9001dc88f71648c5287a57d4e43b 0.1s done
#29 naming to docker.io/library/docker-worker:latest 0.0s done
#29 unpacking to docker.io/library/docker-worker:latest
#29 ...

#30 [backend] exporting to image
#30 exporting layers 14.4s done
#30 exporting manifest sha256:af2cb52d3597c6b86f0755befdf6920ef87c29ebda9ff4df65ff7c7886930ac5 0.0s done
#30 exporting config sha256:8a7e2d61342d5d6aaacd937e3fc2aed324f26f36a19e1dee96013b6e0a55a9f2 0.1s done
#30 exporting attestation manifest sha256:da372a67b437b83275b0b9b80e51913cc94ff1a337a1533c7f3f600fddc4414e 0.1s done
#30 exporting manifest list sha256:7e8b705e38a54fadfb15cd7fb135321b0aa5a358df895ab7c46645637bc6db48 0.0s done
#30 naming to docker.io/library/docker-backend:latest done
#30 unpacking to docker.io/library/docker-backend:latest
#30 ...

#28 [beat] exporting to image
#28 exporting layers 14.3s done
#28 exporting manifest sha256:580cdd4ec7d734c2e7e15fddefa0c97931747b18a072f49db9bcf60ced6a1a31 0.0s done
#28 exporting config sha256:03d77327f80f3ca24542d4a11eec2093c8a1bd28fe40923ae189ffb1a0210907 0.1s done
#28 exporting attestation manifest sha256:91904e69a771a29dc3225b563109031886f37d22685f8de47ee22e9cfda4e4fc 0.1s done
#28 exporting manifest list sha256:6f319bf8a99736b063a3bafa5a475602796da070ba1d4627d542553fb75efed0 0.0s done
#28 naming to docker.io/library/docker-beat:latest 0.0s done
#28 unpacking to docker.io/library/docker-beat:latest
#28 ...

#30 [backend] exporting to image
#30 unpacking to docker.io/library/docker-backend:latest 14.2s done
#30 DONE 29.0s

#28 [beat] exporting to image
#28 unpacking to docker.io/library/docker-beat:latest 14.2s done
#28 DONE 29.0s

#29 [worker] exporting to image
#29 unpacking to docker.io/library/docker-worker:latest 14.4s done
#29 DONE 29.1s

#27 [frontend builder 4/5] COPY . .
#27 ...

#31 [backend] resolving provenance for metadata file
#31 ...

#32 [beat] resolving provenance for metadata file
#32 DONE 0.2s

#31 [backend] resolving provenance for metadata file
#31 DONE 0.2s

#33 [worker] resolving provenance for metadata file
#33 DONE 0.1s

#27 [frontend builder 4/5] COPY . .
#27 DONE 49.7s

#34 [frontend builder 5/5] RUN npm run build
#34 1.202 
#34 1.202 > frontend@0.1.0 build
#34 1.202 > next build
#34 1.202 
#34 2.214 Attention: Next.js now collects completely anonymous telemetry regarding usage.
#34 2.216 This information is used to shape Next.js' roadmap and prioritize features.
#34 2.216 You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
#34 2.216 https://nextjs.org/telemetry
#34 2.216 
#34 2.343   ▲ Next.js 14.2.33
#34 2.344 
#34 4.104    Creating an optimized production build ...
#34 40.58  ✓ Compiled successfully
#34 40.58    Skipping validation of types
#34 40.58    Skipping linting
#34 41.06    Collecting page data ...
#34 43.87    Generating static pages (0/39) ...
#34 45.31    Generating static pages (9/39) 
#34 45.56    Generating static pages (19/39) 
#34 46.03    Generating static pages (29/39) 
#34 46.53  ✓ Generating static pages (39/39)
#34 47.33    Finalizing page optimization ...
#34 47.33    Collecting build traces ...
#34 64.74 
#34 64.75 Route (app)                                   Size     First Load JS
#34 64.75 ┌ ○ /                                         2.87 kB        98.9 kB
#34 64.75 ├ ○ /_not-found                               876 B          88.2 kB
#34 64.75 ├ ○ /dashboard                                2.77 kB        90.1 kB
#34 64.75 ├ ○ /dashboard/admin                          2.04 kB         126 kB
#34 64.75 ├ ○ /dashboard/admin/analytics                3.97 kB         131 kB
#34 64.75 ├ ○ /dashboard/admin/audit-logs               1.99 kB         132 kB
#34 64.75 ├ ○ /dashboard/admin/bulk-import              2.17 kB         126 kB
#34 64.75 ├ ○ /dashboard/admin/exports                  1.39 kB         125 kB
#34 64.75 ├ ○ /dashboard/admin/reports                  2.15 kB         123 kB
#34 64.75 ├ ○ /dashboard/admin/users                    1.23 kB         122 kB
#34 64.75 ├ ○ /dashboard/pg                             2 kB            126 kB
#34 64.75 ├ ○ /dashboard/pg/cases                       2.72 kB         124 kB
#34 64.75 ├ ○ /dashboard/pg/certificates                3.84 kB         131 kB
#34 64.75 ├ ƒ /dashboard/pg/departments/[id]/roster     1.06 kB         122 kB
#34 64.75 ├ ○ /dashboard/pg/logbook                     3.97 kB         134 kB
#34 64.75 ├ ○ /dashboard/pg/notifications               2.49 kB         132 kB
#34 64.75 ├ ○ /dashboard/pg/results                     1.8 kB          132 kB
#34 64.75 ├ ○ /dashboard/pg/rotations                   2.65 kB         132 kB
#34 64.75 ├ ○ /dashboard/search                         2.28 kB         132 kB
#34 64.75 ├ ○ /dashboard/supervisor                     2.85 kB         133 kB
#34 64.75 ├ ○ /dashboard/supervisor/cases               1.8 kB          123 kB
#34 64.75 ├ ○ /dashboard/supervisor/logbooks            3.48 kB         133 kB
#34 64.75 ├ ○ /dashboard/supervisor/pgs                 1.99 kB         132 kB
#34 64.75 ├ ○ /dashboard/utrmc                          2.25 kB         123 kB
#34 64.75 ├ ○ /dashboard/utrmc/cases                    1.56 kB         123 kB
#34 64.75 ├ ○ /dashboard/utrmc/departments              1.39 kB         123 kB
#34 64.75 ├ ƒ /dashboard/utrmc/departments/[id]/roster  1.24 kB         122 kB
#34 64.75 ├ ○ /dashboard/utrmc/hospitals                1.33 kB         123 kB
#34 64.75 ├ ○ /dashboard/utrmc/linking/hod              1.56 kB         123 kB
#34 64.75 ├ ○ /dashboard/utrmc/linking/supervision      1.7 kB          123 kB
#34 64.75 ├ ○ /dashboard/utrmc/matrix                   1.5 kB          123 kB
#34 64.75 ├ ○ /dashboard/utrmc/reports                  2.09 kB         123 kB
#34 64.75 ├ ○ /dashboard/utrmc/users                    1.59 kB         123 kB
#34 64.75 ├ ƒ /dashboard/utrmc/users/[id]               1.84 kB         123 kB
#34 64.75 ├ ○ /dashboard/utrmc/users/new                1.57 kB         123 kB
#34 64.75 ├ ○ /forgot-password                          1.1 kB         97.1 kB
#34 64.75 ├ ○ /login                                    3.16 kB         121 kB
#34 64.75 ├ ○ /register                                 177 B          96.2 kB
#34 64.75 └ ○ /unauthorized                             655 B          96.7 kB
#34 64.75 + First Load JS shared by all                 87.3 kB
#34 64.75   ├ chunks/2117-013b7850c2cfec07.js           31.7 kB
#34 64.75   ├ chunks/fd9d1056-79a1b9afeb5feadf.js       53.6 kB
#34 64.75   └ other shared chunks (total)               1.95 kB
#34 64.75 
#34 64.75 
#34 64.75 ƒ Middleware                                  26.9 kB
#34 64.75 
#34 64.75 ○  (Static)   prerendered as static content
#34 64.75 ƒ  (Dynamic)  server-rendered on demand
#34 64.75 
#34 64.81 npm notice
#34 64.81 npm notice New major version of npm available! 10.8.2 -> 11.11.0
#34 64.81 npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.11.0
#34 64.81 npm notice To update run: npm install -g npm@11.11.0
#34 64.81 npm notice
#34 DONE 65.1s

#35 [frontend runner 3/7] RUN addgroup --system --gid 1001 nodejs
#35 CACHED

#36 [frontend runner 4/7] RUN adduser --system --uid 1001 nextjs
#36 CACHED

#37 [frontend runner 5/7] COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
#37 DONE 0.5s

#38 [frontend runner 6/7] COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
#38 DONE 0.1s

#39 [frontend runner 7/7] COPY --from=builder --chown=nextjs:nodejs /app/public ./public
#39 DONE 0.1s

#40 [frontend] exporting to image
#40 exporting layers
#40 exporting layers 1.3s done
#40 exporting manifest sha256:a318253a684a643c90398a753df32f8503bf431f5abb4972e257bdd1f19b6acc 0.0s done
#40 exporting config sha256:a2ae1cae20e8014be37f46499dd33c4ad33c9923f165ebb5633539e70f04377b 0.0s done
#40 exporting attestation manifest sha256:44cffcbcde37daf445000c06ee52c946b6a551d12ea0d83c72c7953ad4a3a14f 0.0s done
#40 exporting manifest list sha256:3b2701e0d1054d505a889b7ce108b4bb15d0ba9d2f8ba907e31c61731ffe1561 done
#40 naming to docker.io/library/docker-frontend:latest done
#40 unpacking to docker.io/library/docker-frontend:latest
#40 unpacking to docker.io/library/docker-frontend:latest 0.5s done
#40 DONE 1.9s

#41 [frontend] resolving provenance for metadata file
#41 DONE 0.0s
```

### docker compose ps
```
NAME                   IMAGE                COMMAND                  SERVICE    CREATED          STATUS                           PORTS
pgsims_backend_prod    docker-backend       "sh -c 'python manag…"   backend    24 seconds ago   Up 1 second (health: starting)   127.0.0.1:8014->8014/tcp
pgsims_beat            docker-beat          "celery -A sims_proj…"   beat       24 seconds ago   Up 3 seconds                     8014/tcp
pgsims_db_prod         postgres:15-alpine   "docker-entrypoint.s…"   db         25 seconds ago   Up 12 seconds (healthy)          5432/tcp
pgsims_frontend_prod   docker-frontend      "docker-entrypoint.s…"   frontend   13 seconds ago   Up 1 second (health: starting)   127.0.0.1:8082->3000/tcp
pgsims_redis_prod      redis:7-alpine       "docker-entrypoint.s…"   redis      35 hours ago     Up 35 hours (healthy)            6379/tcp
pgsims_worker          docker-worker        "celery -A sims_proj…"   worker     24 seconds ago   Up Less than a second            8014/tcp
```

### backend logs (last 150 lines)
```
pgsims_backend_prod  | Traceback (most recent call last):
pgsims_backend_prod  |   File "/app/manage.py", line 24, in <module>
pgsims_backend_prod  |     main()
pgsims_backend_prod  |   File "/app/manage.py", line 21, in main
pgsims_backend_prod  |     execute_from_command_line(sys.argv)
pgsims_backend_prod  |   File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
pgsims_backend_prod  |     utility.execute()
pgsims_backend_prod  |   File "/home/sims/.local/lib/python3.11/site-packages/django/core/management/__init__.py", line 382, in execute
pgsims_backend_prod  |     settings.INSTALLED_APPS
pgsims_backend_prod  |   File "/home/sims/.local/lib/python3.11/site-packages/django/conf/__init__.py", line 102, in __getattr__
pgsims_backend_prod  |     self._setup(name)
pgsims_backend_prod  |   File "/home/sims/.local/lib/python3.11/site-packages/django/conf/__init__.py", line 89, in _setup
pgsims_backend_prod  |     self._wrapped = Settings(settings_module)
pgsims_backend_prod  |                     ^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_backend_prod  |   File "/home/sims/.local/lib/python3.11/site-packages/django/conf/__init__.py", line 217, in __init__
pgsims_backend_prod  |     mod = importlib.import_module(self.SETTINGS_MODULE)
pgsims_backend_prod  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_backend_prod  |   File "/usr/local/lib/python3.11/importlib/__init__.py", line 126, in import_module
pgsims_backend_prod  |     return _bootstrap._gcd_import(name[level:], package, level)
pgsims_backend_prod  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pgsims_backend_prod  |   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
pgsims_backend_prod  |   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
pgsims_backend_prod  |   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
pgsims_backend_prod  |   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
pgsims_backend_prod  |   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
pgsims_backend_prod  |   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
pgsims_backend_prod  |   File "/app/sims_project/settings.py", line 41, in <module>
pgsims_backend_prod  |     raise RuntimeError("SECRET_KEY environment variable is required")
pgsims_backend_prod  | RuntimeError: SECRET_KEY environment variable is required
```

### remediation: compose up with --env-file .env
```
#1 [internal] load local bake definitions
#1 reading from stdin 1.92kB done
#1 DONE 0.0s

#2 [backend internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.94kB done
#2 transferring dockerfile: 1.94kB done
#2 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
#2 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
#2 WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 5)
#2 DONE 0.0s

#3 [frontend internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.53kB done
#3 DONE 0.0s

#4 [frontend internal] load metadata for docker.io/library/node:20-alpine
#4 DONE 0.0s

#5 [frontend internal] load .dockerignore
#5 transferring context: 2B done
#5 DONE 0.0s

#6 [frontend deps 1/5] FROM docker.io/library/node:20-alpine@sha256:09e2b3d9726018aecf269bd35325f46bf75046a643a66d28360ec71132750ec8
#6 resolve docker.io/library/node:20-alpine@sha256:09e2b3d9726018aecf269bd35325f46bf75046a643a66d28360ec71132750ec8 0.0s done
#6 DONE 0.0s

#7 [frontend internal] load build context
#7 ...

#8 [worker internal] load metadata for docker.io/library/python:3.11-slim
#8 DONE 0.2s

#9 [backend internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s

#10 [beat builder 1/5] FROM docker.io/library/python:3.11-slim@sha256:c8271b1f627d0068857dce5b53e14a9558603b527e46f1f901722f935b786a39
#10 resolve docker.io/library/python:3.11-slim@sha256:c8271b1f627d0068857dce5b53e14a9558603b527e46f1f901722f935b786a39 0.0s done
#10 DONE 0.0s

#7 [frontend internal] load build context
#7 ...

#11 [backend internal] load build context
#11 transferring context: 3.74MB 2.5s done
#11 DONE 2.6s

#12 [beat builder 2/5] RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev     && rm -rf /var/lib/apt/lists/*
#12 CACHED

#13 [beat builder 3/5] WORKDIR /app
#13 CACHED

#14 [beat builder 4/5] COPY requirements.txt .
#14 CACHED

#15 [beat stage-1 5/6] WORKDIR /app
#15 CACHED

#16 [beat stage-1 2/6] RUN apt-get update && apt-get install -y --no-install-recommends     libpq5     curl     && rm -rf /var/lib/apt/lists/*
#16 CACHED

#17 [beat builder 5/5] RUN pip install --user -r requirements.txt
#17 CACHED

#18 [beat stage-1 3/6] RUN useradd -m -u 1000 sims &&     mkdir -p /app /app/staticfiles /app/media /app/logs &&     chown -R sims:sims /app
#18 CACHED

#19 [beat stage-1 4/6] COPY --from=builder --chown=sims:sims /root/.local /home/sims/.local
#19 CACHED

#20 [beat stage-1 6/6] COPY --chown=sims:sims . .
#20 CACHED

#7 [frontend internal] load build context
#7 ...

#21 [backend] exporting to image
#21 exporting layers done
#21 exporting manifest sha256:af2cb52d3597c6b86f0755befdf6920ef87c29ebda9ff4df65ff7c7886930ac5 done
#21 exporting config sha256:8a7e2d61342d5d6aaacd937e3fc2aed324f26f36a19e1dee96013b6e0a55a9f2 done
#21 exporting attestation manifest sha256:acb16cf90ba4ccf7bf6636b396d002e1450cffec5344e7535495c80e6e7b12d0 0.1s done
#21 exporting manifest list sha256:8bd7cc70cdec3ef4cd5bd114cfd851b63e7559649329c005b27f345a3753580d 0.0s done
#21 naming to docker.io/library/docker-backend:latest 0.0s done
#21 unpacking to docker.io/library/docker-backend:latest 0.0s done
#21 DONE 0.3s

#7 [frontend internal] load build context
#7 ...

#22 [beat] exporting to image
#22 exporting layers 0.0s done
#22 exporting manifest sha256:580cdd4ec7d734c2e7e15fddefa0c97931747b18a072f49db9bcf60ced6a1a31 done
#22 exporting config sha256:03d77327f80f3ca24542d4a11eec2093c8a1bd28fe40923ae189ffb1a0210907 0.0s done
#22 exporting attestation manifest sha256:f8e56c5c3f80149fbe8853b10790f761c5ac8538ab15ddf2502bf93740de4f5a 0.1s done
#22 exporting manifest list sha256:ec12ec5e938a66e97ad3df5fecd44c605afcfc3d2f800fe4307fcc91f548bd80 0.0s done
#22 naming to docker.io/library/docker-beat:latest done
#22 unpacking to docker.io/library/docker-beat:latest 0.1s done
#22 DONE 0.3s

#23 [worker] exporting to image
#23 exporting layers 0.0s done
#23 exporting manifest sha256:627369d478a637a0900a166c6bbe9775c9dc6855cec26496d7358cf6b9840746 done
#23 exporting config sha256:fd9b9b37714b89b6ce91cf5d2251521a13e316663ca352f44f51b063b205718a done
#23 exporting attestation manifest sha256:43170f501a958aa71c97b536de03db70b689b47aa5ed868aa48f7c61e26a62ed 0.1s done
#23 exporting manifest list sha256:eb6cae456ccc42c694fe841fa41b87d16347948757324628b3c03081e750ced3 0.0s done
#23 naming to docker.io/library/docker-worker:latest done
#23 unpacking to docker.io/library/docker-worker:latest 0.1s done
#23 DONE 0.4s

#7 [frontend internal] load build context
#7 transferring context: 7.68MB 3.2s done
#7 DONE 3.3s

#24 [beat] resolving provenance for metadata file
#24 DONE 0.0s

#25 [worker] resolving provenance for metadata file
#25 DONE 0.1s

#26 [backend] resolving provenance for metadata file
#26 DONE 0.1s

#27 [frontend deps 5/5] RUN npm ci
#27 CACHED

#28 [frontend builder 2/5] WORKDIR /app
#28 CACHED

#29 [frontend deps 4/5] COPY package.json package-lock.json* ./
#29 CACHED

#30 [frontend deps 3/5] WORKDIR /app
#30 CACHED

#31 [frontend deps 2/5] RUN apk add --no-cache libc6-compat
#31 CACHED

#32 [frontend builder 3/5] COPY --from=deps /app/node_modules ./node_modules
#32 CACHED

#33 [frontend builder 4/5] COPY . .
#33 DONE 33.3s

#34 [frontend builder 5/5] RUN npm run build
#34 0.915 
#34 0.915 > frontend@0.1.0 build
#34 0.915 > next build
#34 0.915 
#34 1.638 Attention: Next.js now collects completely anonymous telemetry regarding usage.
#34 1.638 This information is used to shape Next.js' roadmap and prioritize features.
#34 1.638 You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
#34 1.638 https://nextjs.org/telemetry
#34 1.638 
#34 1.723   ▲ Next.js 14.2.33
#34 1.723 
#34 2.497    Creating an optimized production build ...
#34 23.50  ✓ Compiled successfully
#34 23.50    Skipping validation of types
#34 23.50    Skipping linting
#34 23.79    Collecting page data ...
#34 25.76    Generating static pages (0/39) ...
#34 26.65    Generating static pages (9/39) 
#34 26.81    Generating static pages (19/39) 
#34 27.11    Generating static pages (29/39) 
#34 27.42  ✓ Generating static pages (39/39)
#34 28.63    Finalizing page optimization ...
#34 28.63    Collecting build traces ...
#34 43.28 
#34 43.29 Route (app)                                   Size     First Load JS
#34 43.29 ┌ ○ /                                         2.87 kB        98.9 kB
#34 43.29 ├ ○ /_not-found                               876 B          88.2 kB
#34 43.29 ├ ○ /dashboard                                2.77 kB        90.1 kB
#34 43.29 ├ ○ /dashboard/admin                          2.04 kB         126 kB
#34 43.29 ├ ○ /dashboard/admin/analytics                3.97 kB         131 kB
#34 43.29 ├ ○ /dashboard/admin/audit-logs               1.99 kB         132 kB
#34 43.29 ├ ○ /dashboard/admin/bulk-import              2.17 kB         126 kB
#34 43.29 ├ ○ /dashboard/admin/exports                  1.39 kB         125 kB
#34 43.29 ├ ○ /dashboard/admin/reports                  2.15 kB         123 kB
#34 43.29 ├ ○ /dashboard/admin/users                    1.23 kB         122 kB
#34 43.29 ├ ○ /dashboard/pg                             2 kB            126 kB
#34 43.29 ├ ○ /dashboard/pg/cases                       2.72 kB         124 kB
#34 43.29 ├ ○ /dashboard/pg/certificates                3.84 kB         131 kB
#34 43.29 ├ ƒ /dashboard/pg/departments/[id]/roster     1.06 kB         122 kB
#34 43.29 ├ ○ /dashboard/pg/logbook                     3.97 kB         134 kB
#34 43.29 ├ ○ /dashboard/pg/notifications               2.49 kB         132 kB
#34 43.29 ├ ○ /dashboard/pg/results                     1.8 kB          132 kB
#34 43.29 ├ ○ /dashboard/pg/rotations                   2.65 kB         132 kB
#34 43.29 ├ ○ /dashboard/search                         2.28 kB         132 kB
#34 43.29 ├ ○ /dashboard/supervisor                     2.85 kB         133 kB
#34 43.29 ├ ○ /dashboard/supervisor/cases               1.8 kB          123 kB
#34 43.29 ├ ○ /dashboard/supervisor/logbooks            3.48 kB         133 kB
#34 43.29 ├ ○ /dashboard/supervisor/pgs                 1.99 kB         132 kB
#34 43.29 ├ ○ /dashboard/utrmc                          2.25 kB         123 kB
#34 43.29 ├ ○ /dashboard/utrmc/cases                    1.56 kB         123 kB
#34 43.29 ├ ○ /dashboard/utrmc/departments              1.39 kB         123 kB
#34 43.29 ├ ƒ /dashboard/utrmc/departments/[id]/roster  1.24 kB         122 kB
#34 43.29 ├ ○ /dashboard/utrmc/hospitals                1.33 kB         123 kB
#34 43.29 ├ ○ /dashboard/utrmc/linking/hod              1.56 kB         123 kB
#34 43.29 ├ ○ /dashboard/utrmc/linking/supervision      1.7 kB          123 kB
#34 43.29 ├ ○ /dashboard/utrmc/matrix                   1.5 kB          123 kB
#34 43.29 ├ ○ /dashboard/utrmc/reports                  2.09 kB         123 kB
#34 43.29 ├ ○ /dashboard/utrmc/users                    1.59 kB         123 kB
#34 43.29 ├ ƒ /dashboard/utrmc/users/[id]               1.84 kB         123 kB
#34 43.29 ├ ○ /dashboard/utrmc/users/new                1.57 kB         123 kB
#34 43.29 ├ ○ /forgot-password                          1.1 kB         97.1 kB
#34 43.29 ├ ○ /login                                    3.16 kB         121 kB
#34 43.29 ├ ○ /register                                 177 B          96.2 kB
#34 43.29 └ ○ /unauthorized                             655 B          96.7 kB
#34 43.29 + First Load JS shared by all                 87.3 kB
#34 43.29   ├ chunks/2117-013b7850c2cfec07.js           31.7 kB
#34 43.29   ├ chunks/fd9d1056-79a1b9afeb5feadf.js       53.6 kB
#34 43.29   └ other shared chunks (total)               1.95 kB
#34 43.29 
#34 43.29 
#34 43.29 ƒ Middleware                                  26.9 kB
#34 43.29 
#34 43.29 ○  (Static)   prerendered as static content
#34 43.29 ƒ  (Dynamic)  server-rendered on demand
#34 43.29 
#34 43.33 npm notice
#34 43.33 npm notice New major version of npm available! 10.8.2 -> 11.11.0
#34 43.33 npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.11.0
#34 43.33 npm notice To update run: npm install -g npm@11.11.0
#34 43.33 npm notice
#34 DONE 43.4s

#35 [frontend runner 3/7] RUN addgroup --system --gid 1001 nodejs
#35 CACHED

#36 [frontend runner 4/7] RUN adduser --system --uid 1001 nextjs
#36 CACHED

#37 [frontend runner 5/7] COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
#37 DONE 0.3s

#38 [frontend runner 6/7] COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
#38 DONE 0.1s

#39 [frontend runner 7/7] COPY --from=builder --chown=nextjs:nodejs /app/public ./public
#39 DONE 0.0s

#40 [frontend] exporting to image
#40 exporting layers
#40 exporting layers 0.9s done
#40 exporting manifest sha256:9f2addbb17ad4d7ca0f6f97576f7fbfced322b63fb526416e0fd09a6dc8ef646 0.0s done
#40 exporting config sha256:8d3c2e854f02e2d995f7f5ecc42d9618cad5977f03a69bd56bc8cbf0beb3e70a 0.0s done
#40 exporting attestation manifest sha256:5ab650dbf28d1a334b02fe2c909dd30a7b790f02f975043b389d806d12fc47ef 0.0s done
#40 exporting manifest list sha256:90217624c5b5de285617908412d60e38ec5126469ed03fbc5ad2ddd8e2a881c6 done
#40 naming to docker.io/library/docker-frontend:latest done
#40 unpacking to docker.io/library/docker-frontend:latest
#40 unpacking to docker.io/library/docker-frontend:latest 0.4s done
#40 DONE 1.4s

#41 [frontend] resolving provenance for metadata file
#41 DONE 0.0s
```

### remediation: docker compose ps
```
NAME                   IMAGE                COMMAND                  SERVICE    CREATED          STATUS                                     PORTS
pgsims_backend_prod    docker-backend       "sh -c 'python manag…"   backend    12 seconds ago   Up Less than a second (health: starting)   127.0.0.1:8014->8014/tcp
pgsims_beat            docker-beat          "celery -A sims_proj…"   beat       12 seconds ago   Up 10 seconds                              8014/tcp
pgsims_db_prod         postgres:15-alpine   "docker-entrypoint.s…"   db         13 seconds ago   Up 11 seconds (healthy)                    5432/tcp
pgsims_frontend_prod   docker-frontend      "docker-entrypoint.s…"   frontend   12 seconds ago   Up Less than a second (health: starting)   127.0.0.1:8082->3000/tcp
pgsims_redis_prod      redis:7-alpine       "docker-entrypoint.s…"   redis      35 hours ago     Up 35 hours (healthy)                      6379/tcp
pgsims_worker          docker-worker        "celery -A sims_proj…"   worker     12 seconds ago   Up 10 seconds                              8014/tcp
```

### remediation: backend logs (last 80 lines)
```
```

### remediation: post-wait docker compose ps
```
NAME                   IMAGE                COMMAND                  SERVICE    CREATED              STATUS                        PORTS
pgsims_backend_prod    docker-backend       "sh -c 'python manag…"   backend    About a minute ago   Up About a minute (healthy)   127.0.0.1:8014->8014/tcp
pgsims_beat            docker-beat          "celery -A sims_proj…"   beat       About a minute ago   Up About a minute             8014/tcp
pgsims_db_prod         postgres:15-alpine   "docker-entrypoint.s…"   db         About a minute ago   Up About a minute (healthy)   5432/tcp
pgsims_frontend_prod   docker-frontend      "docker-entrypoint.s…"   frontend   About a minute ago   Up About a minute (healthy)   127.0.0.1:8082->3000/tcp
pgsims_redis_prod      redis:7-alpine       "docker-entrypoint.s…"   redis      35 hours ago         Up 35 hours (healthy)         6379/tcp
pgsims_worker          docker-worker        "celery -A sims_proj…"   worker     About a minute ago   Up About a minute             8014/tcp
```

### remediation: curl -I https://pgsims.alshifalab.pk/api/auth/login/
```
HTTP/2 405 
allow: POST, OPTIONS
alt-svc: h3=":443"; ma=2592000
content-type: application/json
cross-origin-opener-policy: same-origin
date: Sat, 28 Feb 2026 10:58:13 GMT
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
vary: Accept, origin
via: 1.1 Caddy
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-request-id: 7ae2c04cb56049ba94616943ff00200d
x-response-time: 22ms
content-length: 41

```

## Final health check (post-remediation)

### docker compose --env-file .env -f docker/docker-compose.prod.yml ps
```
NAME                   IMAGE                COMMAND                  SERVICE    CREATED          STATUS                    PORTS
pgsims_backend_prod    docker-backend       "sh -c 'python manag…"   backend    36 minutes ago   Up 36 minutes (healthy)   127.0.0.1:8014->8014/tcp
pgsims_beat            docker-beat          "celery -A sims_proj…"   beat       37 minutes ago   Up 37 minutes             8014/tcp
pgsims_db_prod         postgres:15-alpine   "docker-entrypoint.s…"   db         37 minutes ago   Up 37 minutes (healthy)   5432/tcp
pgsims_frontend_prod   docker-frontend      "docker-entrypoint.s…"   frontend   43 minutes ago   Up 43 minutes (healthy)   127.0.0.1:8082->3000/tcp
pgsims_redis_prod      redis:7-alpine       "docker-entrypoint.s…"   redis      35 hours ago     Up 35 hours (healthy)     6379/tcp
pgsims_worker          docker-worker        "celery -A sims_proj…"   worker     37 minutes ago   Up 37 minutes             8014/tcp
```

### backend logs (tail 40)
```
pgsims_backend_prod  |  boundary="===============3530224990377041194=="
pgsims_backend_prod  | MIME-Version: 1.0
pgsims_backend_prod  | Subject: Logbook entry submitted by E2E PG
pgsims_backend_prod  | From: SIMS System <noreply@sims.medical.edu>
pgsims_backend_prod  | To: e2e_supervisor@pgsims.local
pgsims_backend_prod  | Date: Sat, 28 Feb 2026 11:39:15 -0000
pgsims_backend_prod  | Message-ID: <177227875515.29.11141530415641157897@c4b931dd1bbc>
pgsims_backend_prod  | 
pgsims_backend_prod  | --===============3530224990377041194==
pgsims_backend_prod  | Content-Type: text/plain; charset="utf-8"
pgsims_backend_prod  | MIME-Version: 1.0
pgsims_backend_prod  | Content-Transfer-Encoding: 7bit
pgsims_backend_prod  | 
pgsims_backend_prod  | Hello E2E Supervisor,
pgsims_backend_prod  | 
pgsims_backend_prod  | E2E PG has submitted a logbook entry titled "E2E live feed 1772278714161" for your review.
pgsims_backend_prod  | 
pgsims_backend_prod  | Current status: Pending Supervisor Review
pgsims_backend_prod  | Submitted on: 28 Feb 2026 11:39
pgsims_backend_prod  | 
pgsims_backend_prod  | Please review the entry at your earliest convenience.
pgsims_backend_prod  | 
pgsims_backend_prod  | --===============3530224990377041194==
pgsims_backend_prod  | Content-Type: text/html; charset="utf-8"
pgsims_backend_prod  | MIME-Version: 1.0
pgsims_backend_prod  | Content-Transfer-Encoding: 7bit
pgsims_backend_prod  | 
pgsims_backend_prod  | <p>Hello E2E Supervisor,</p>
pgsims_backend_prod  | <p><strong>E2E PG</strong> has submitted a logbook entry titled "E2E live feed 1772278714161" for your review.</p>
pgsims_backend_prod  | <ul>
pgsims_backend_prod  |   <li>Status: Pending Supervisor Review</li>
pgsims_backend_prod  |   <li>Submitted: 28 Feb 2026 11:39</li>
pgsims_backend_prod  | </ul>
pgsims_backend_prod  | <p>Please review the entry at your earliest convenience.</p>
pgsims_backend_prod  | 
pgsims_backend_prod  | --===============3530224990377041194==--
pgsims_backend_prod  | 
pgsims_backend_prod  | -------------------------------------------------------------------------------
pgsims_backend_prod  | [WARNING] 2026-02-28 11:39:29,228 sims.performance Slow request: GET /healthz/ took 1007ms
pgsims_backend_prod  | [WARNING] 2026-02-28 11:40:00,281 sims.performance Slow request: GET /healthz/ took 1006ms
```
