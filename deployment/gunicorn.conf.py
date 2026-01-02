# Gunicorn configuration for SIMS
# Save as: /opt/sims_project/gunicorn.conf.py

import multiprocessing

# Server socket
bind = "unix:/opt/sims_project/sims.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/opt/sims_project/logs/gunicorn_access.log"
errorlog = "/opt/sims_project/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "sims_gunicorn"

# Server mechanics
daemon = False
pidfile = "/opt/sims_project/sims.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (when certificate is available)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
