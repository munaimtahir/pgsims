# Gunicorn configuration for PHC (SIMS) on port 8014
# Located at: /home/munaim/srv/apps/sims/gunicorn_phc.conf.py

import multiprocessing

# Server socket
bind = "127.0.0.1:8014"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 2

# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/home/munaim/srv/apps/sims/logs/gunicorn_access.log"
errorlog = "/home/munaim/srv/apps/sims/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "phc_gunicorn"

# Server mechanics
daemon = False
tmp_upload_dir = None
