@echo off
echo 🗂️ Organizing SIMS Project Structure...

cd /d "d:\PMC\sims_project-1"

echo Creating folders...
if not exist "docs" mkdir docs
if not exist "tests" mkdir tests  
if not exist "scripts" mkdir scripts
if not exist "deployment" mkdir deployment
if not exist "utils" mkdir utils

echo Moving documentation files...
if exist "*.md" move "*.md" docs\ >nul 2>&1
if exist "File Tree" move "File Tree" docs\ >nul 2>&1

echo Moving test files...
if exist "test_*.py" move "test_*.py" tests\ >nul 2>&1
if exist "verify_*.py" move "verify_*.py" tests\ >nul 2>&1
if exist "validate_*.py" move "validate_*.py" tests\ >nul 2>&1
if exist "diagnose_*.py" move "diagnose_*.py" tests\ >nul 2>&1
if exist "quick_*.py" move "quick_*.py" tests\ >nul 2>&1
if exist "simple_*.py" move "simple_*.py" tests\ >nul 2>&1
if exist "final_*.py" move "final_*.py" tests\ >nul 2>&1
if exist "django_verification.py" move "django_verification.py" tests\ >nul 2>&1
if exist "login_system_verification.py" move "login_system_verification.py" tests\ >nul 2>&1
if exist "run_verification.py" move "run_verification.py" tests\ >nul 2>&1
if exist "url_test.py" move "url_test.py" tests\ >nul 2>&1
if exist "system_health_check.py" move "system_health_check.py" tests\ >nul 2>&1

echo Moving script files...
if exist "*.ps1" move "*.ps1" scripts\ >nul 2>&1
if exist "*.bat" move "*.bat" scripts\ >nul 2>&1

echo Moving deployment files...
if exist "*.conf" move "*.conf" deployment\ >nul 2>&1
if exist "*.service" move "*.service" deployment\ >nul 2>&1
if exist "*.sh" move "*.sh" deployment\ >nul 2>&1
if exist "gunicorn.conf.py" move "gunicorn.conf.py" deployment\ >nul 2>&1
if exist "server_config.env" move "server_config.env" deployment\ >nul 2>&1
if exist "deployment_fix.py" move "deployment_fix.py" deployment\ >nul 2>&1

echo Moving utility files...
if exist "create_*.py" move "create_*.py" utils\ >nul 2>&1

echo 🎉 Project organization complete!
echo.
echo 📂 New Project Structure:
echo ├── 📁 docs/         (Documentation)
echo ├── 📁 tests/        (Tests ^& Verification)  
echo ├── 📁 scripts/      (Utility Scripts)
echo ├── 📁 deployment/   (Deployment Configs)
echo ├── 📁 utils/        (Admin Utilities)
echo ├── 📁 sims/         (Django App)
echo ├── 📁 templates/    (Django Templates)
echo ├── 📁 static/       (Static Files)
echo └── 📄 manage.py     (Django Management)
pause
