# SIMS Localhost Setup Script for Windows
# This script checks prerequisites and sets up the localhost deployment environment

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SIMS Localhost Setup for Windows" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction SilentlyContinue) {
            return $true
        }
        return $false
    } catch {
        return $false
    }
}

# Function to check version
function Get-Version {
    param($Command, $VersionFlag)
    try {
        $version = & $Command $VersionFlag 2>&1
        return $version
    } catch {
        return $null
    }
}

Write-Host "Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

$missing = @()

# Check Python
Write-Host "Checking Python..." -ForegroundColor Cyan
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
    
    # Check if Python 3.11+
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "  ⚠ Warning: Python 3.11+ recommended (found $major.$minor)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host "    Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    $missing += "Python 3.11+"
}

# Check pip
Write-Host ""
Write-Host "Checking pip..." -ForegroundColor Cyan
if (Test-Command "pip") {
    $pipVersion = pip --version 2>&1
    Write-Host "  ✓ pip found: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ pip not found!" -ForegroundColor Red
    Write-Host "    Install with: python -m ensurepip --upgrade" -ForegroundColor Yellow
    $missing += "pip"
}

# Check Node.js
Write-Host ""
Write-Host "Checking Node.js..." -ForegroundColor Cyan
if (Test-Command "node") {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js found: $nodeVersion" -ForegroundColor Green
    
    # Check if Node.js 18+
    $versionMatch = $nodeVersion -match "v(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        if ($major -lt 18) {
            Write-Host "  ⚠ Warning: Node.js 18+ recommended (found v$major.x)" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  ✗ Node.js not found!" -ForegroundColor Red
    Write-Host "    Download from: https://nodejs.org/" -ForegroundColor Yellow
    $missing += "Node.js 18+"
}

# Check npm
Write-Host ""
Write-Host "Checking npm..." -ForegroundColor Cyan
if (Test-Command "npm") {
    $npmVersion = npm --version 2>&1
    Write-Host "  ✓ npm found: v$npmVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ npm not found!" -ForegroundColor Red
    $missing += "npm"
}

# Check Docker
Write-Host ""
Write-Host "Checking Docker..." -ForegroundColor Cyan
if (Test-Command "docker") {
    $dockerVersion = docker --version 2>&1
    Write-Host "  ✓ Docker found: $dockerVersion" -ForegroundColor Green
    
    # Check if Docker is running
    try {
        docker ps | Out-Null
        Write-Host "  ✓ Docker is running" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Warning: Docker Desktop may not be running" -ForegroundColor Yellow
        Write-Host "    Please start Docker Desktop" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ Docker not found!" -ForegroundColor Red
    Write-Host "    Download Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    $missing += "Docker Desktop"
}

# Check Git
Write-Host ""
Write-Host "Checking Git..." -ForegroundColor Cyan
if (Test-Command "git") {
    $gitVersion = git --version 2>&1
    Write-Host "  ✓ Git found: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Git not found (optional but recommended)" -ForegroundColor Yellow
    Write-Host "    Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan

if ($missing.Count -gt 0) {
    Write-Host "Missing prerequisites:" -ForegroundColor Red
    foreach ($item in $missing) {
        Write-Host "  - $item" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please install the missing prerequisites and run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "All prerequisites are installed!" -ForegroundColor Green
Write-Host ""

# Setup virtual environment
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  ✓ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Install Python dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install --upgrade pip wheel
pip install -r requirements.txt
Write-Host "  ✓ Python dependencies installed" -ForegroundColor Green

# Check if .env.localhost exists
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env.localhost")) {
    Write-Host "  ⚠ .env.localhost not found. Creating from template..." -ForegroundColor Yellow
    # Create basic .env.localhost
    @"
SECRET_KEY=django-insecure-localhost-dev-key-change-this-min-50-chars
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://127.0.0.1:3000
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
LOG_LEVEL=DEBUG
"@ | Out-File -FilePath ".env.localhost" -Encoding utf8
    Write-Host "  ✓ .env.localhost created" -ForegroundColor Green
} else {
    Write-Host "  ✓ .env.localhost exists" -ForegroundColor Green
}

# Setup frontend
if (Test-Path "frontend") {
    Write-Host ""
    Write-Host "Setting up frontend..." -ForegroundColor Yellow
    Push-Location frontend
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "  Installing Node.js dependencies..." -ForegroundColor Cyan
        npm install
        Write-Host "  ✓ Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Frontend dependencies already installed" -ForegroundColor Green
    }
    
    # Check frontend .env.localhost
    if (-not (Test-Path ".env.localhost")) {
        Write-Host "  Creating frontend/.env.localhost..." -ForegroundColor Cyan
        "NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath ".env.localhost" -Encoding utf8
        Write-Host "  ✓ Frontend environment file created" -ForegroundColor Green
    }
    
    Pop-Location
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review and edit .env.localhost if needed" -ForegroundColor White
Write-Host "  2. Copy .env.localhost to .env: Copy-Item .env.localhost .env" -ForegroundColor White
Write-Host "  3. Run migrations: python manage.py migrate" -ForegroundColor White
Write-Host "  4. Create superuser: python manage.py createsuperuser" -ForegroundColor White
Write-Host "  5. Start development server: python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Or use Docker:" -ForegroundColor Yellow
Write-Host "  .\deployment\deploy_localhost.ps1" -ForegroundColor White
Write-Host ""

