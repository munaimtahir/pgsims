# Multi-stage Dockerfile for SIMS
# Builds a production-ready Docker image

# Stage 1: Builder
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/sims/.local/bin:$PATH

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 sims && \
    mkdir -p /app /app/staticfiles /app/media /app/logs && \
    chown -R sims:sims /app

# Copy Python dependencies from builder
COPY --from=builder --chown=sims:sims /root/.local /home/sims/.local

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=sims:sims . .

# Switch to app user
USER sims

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/healthz/', timeout=5)" || exit 1

# Default command (can be overridden)
CMD ["gunicorn", "sims_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60"]
