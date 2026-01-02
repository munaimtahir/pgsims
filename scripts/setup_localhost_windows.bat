@echo off
REM SIMS Localhost Setup Script for Windows (Batch File)
REM This script checks prerequisites and sets up the localhost deployment environment

echo =========================================
echo SIMS Localhost Setup for Windows
echo =========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Python not found!
    echo   Download from: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    python --version
    echo   [OK] Python found
)
echo.

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] pip not found!
    echo   Install with: python -m ensurepip --upgrade
    pause
    exit /b 1
) else (
    pip --version
    echo   [OK] pip found
)
echo.

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Node.js not found!
    echo   Download from: https://nodejs.org/
    pause
    exit /b 1
) else (
    node --version
    echo   [OK] Node.js found
)
echo.

REM Check npm
echo Checking npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] npm not found!
    pause
    exit /b 1
) else (
    npm --version
    echo   [OK] npm found
)
echo.

REM Check Docker
echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Docker not found!
    echo   Download Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
) else (
    docker --version
    echo   [OK] Docker found
)
echo.

echo =========================================
echo All prerequisites are installed!
echo =========================================
echo.

REM Setup virtual environment
echo Setting up Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo   [OK] Virtual environment created
) else (
    echo   [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip wheel
pip install -r requirements.txt
echo   [OK] Python dependencies installed
echo.

REM Check .env.localhost
echo Checking environment configuration...
if not exist ".env.localhost" (
    echo   Creating .env.localhost...
    (
        echo SECRET_KEY=django-insecure-localhost-dev-key-change-this-min-50-chars
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://127.0.0.1:3000
        echo REDIS_URL=redis://localhost:6379/0
        echo CELERY_BROKER_URL=redis://localhost:6379/1
        echo CELERY_RESULT_BACKEND=redis://localhost:6379/1
        echo EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
        echo LOG_LEVEL=DEBUG
    ) > .env.localhost
    echo   [OK] .env.localhost created
) else (
    echo   [OK] .env.localhost exists
)
echo.

REM Setup frontend
if exist "frontend" (
    echo Setting up frontend...
    cd frontend
    if not exist "node_modules" (
        echo   Installing Node.js dependencies...
        call npm install
        echo   [OK] Frontend dependencies installed
    ) else (
        echo   [OK] Frontend dependencies already installed
    )
    
    if not exist ".env.localhost" (
        echo   Creating frontend/.env.localhost...
        echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.localhost
        echo   [OK] Frontend environment file created
    )
    cd ..
    echo.
)

echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo   1. Review and edit .env.localhost if needed
echo   2. Copy .env.localhost to .env: copy .env.localhost .env
echo   3. Run migrations: python manage.py migrate
echo   4. Create superuser: python manage.py createsuperuser
echo   5. Start development server: python manage.py runserver
echo.
echo Or use Docker:
echo   deployment\deploy_localhost.ps1
echo.
pause

