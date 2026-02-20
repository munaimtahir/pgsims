# SIMS Localhost Deployment Script for Windows PowerShell
# This script sets up and deploys SIMS on localhost

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SIMS Localhost Deployment Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.localhost exists
if (-not (Test-Path ".env.localhost")) {
    Write-Host "Error: .env.localhost file not found!" -ForegroundColor Red
    Write-Host "Please create .env.localhost file first." -ForegroundColor Yellow
    exit 1
}

# Copy .env.localhost to .env
Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "Warning: .env already exists. Backing up to .env.backup" -ForegroundColor Yellow
    Copy-Item ".env" ".env.backup"
}
Copy-Item ".env.localhost" ".env"
Write-Host "✓ Environment configuration copied" -ForegroundColor Green

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not installed!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop for Windows" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
try {
    $composeVersion = docker compose version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $DOCKER_COMPOSE = "docker compose"
        Write-Host "Using Docker Compose v2" -ForegroundColor Green
    } else {
        $composeVersion = docker-compose --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $DOCKER_COMPOSE = "docker-compose"
            Write-Host "Using Docker Compose v1" -ForegroundColor Green
        } else {
            Write-Host "Error: Docker Compose is not installed!" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "Error: Docker Compose is not installed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting services with Docker Compose..." -ForegroundColor Yellow
Write-Host "Using: $DOCKER_COMPOSE -f docker-compose.localhost.yml" -ForegroundColor Cyan

# Build and start services
& docker compose -f docker-compose.localhost.yml up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error starting Docker services!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Services started" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
& docker compose -f docker-compose.localhost.yml exec -T web python manage.py migrate --noinput
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Migrations completed" -ForegroundColor Green
} else {
    Write-Host "Warning: Migrations may have failed. Check logs." -ForegroundColor Yellow
}

# Collect static files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
& docker compose -f docker-compose.localhost.yml exec -T web python manage.py collectstatic --noinput
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Static files collected" -ForegroundColor Green
} else {
    Write-Host "Warning: Static files collection may have failed. Check logs." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Cyan
Write-Host "  - Django Admin: http://localhost:8000/admin/" -ForegroundColor White
Write-Host "  - Main App:    http://localhost:8000/" -ForegroundColor White
Write-Host "  - Health Check: http://localhost:8000/healthz/" -ForegroundColor White
Write-Host ""
Write-Host "To create a superuser, run:" -ForegroundColor Yellow
Write-Host "  docker compose -f docker-compose.localhost.yml exec web python manage.py createsuperuser" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  docker compose -f docker-compose.localhost.yml logs -f" -ForegroundColor White
Write-Host ""
Write-Host "To stop services:" -ForegroundColor Yellow
Write-Host "  docker compose -f docker-compose.localhost.yml down" -ForegroundColor White
Write-Host ""

