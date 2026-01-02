@echo off
echo ===============================================
echo 🗂️ SIMS Project Organization Script
echo ===============================================
echo.

cd /d "d:\PMC\sims_project-1"

echo 📁 Creating organizational folders...
if not exist "docs" mkdir docs
if not exist "tests" mkdir tests
if not exist "scripts" mkdir scripts
if not exist "deployment" mkdir deployment
if not exist "utils" mkdir utils
echo ✅ Folders created!
echo.

echo 📚 Moving documentation files...
for %%f in (*LOGIN*.md *ADMIN*.md *AUTH*.md *HOME*.md *LOGOUT*.md *MIGRATION*.md *NGINX*.md *SERVER*.md *SYSTEM*.md *THEME*.md *PROJECT*.md README.md TROUBLESHOOTING.md) do (
    if exist "%%f" (
        move "%%f" docs\ >nul 2>&1
        echo   Moved: %%f
    )
)
if exist "File Tree" (
    move "File Tree" docs\ >nul 2>&1
    echo   Moved: File Tree
)
echo ✅ Documentation organized!
echo.

echo 🧪 Moving test files...
for %%f in (test_*.py verify_*.py validate_*.py diagnose_*.py quick_*.py simple_*.py final_*.py django_verification.py login_system_verification.py run_verification.py url_test.py system_health_check.py) do (
    if exist "%%f" (
        move "%%f" tests\ >nul 2>&1
        echo   Moved: %%f
    )
)
echo ✅ Tests organized!
echo.

echo 🔧 Moving script files...
for %%f in (*.ps1 *.bat) do (
    if exist "%%f" (
        move "%%f" scripts\ >nul 2>&1
        echo   Moved: %%f
    )
)
echo ✅ Scripts organized!
echo.

echo 🚀 Moving deployment files...
for %%f in (*.conf *.service *.sh gunicorn.conf.py server_config.env deployment_fix.py) do (
    if exist "%%f" (
        move "%%f" deployment\ >nul 2>&1
        echo   Moved: %%f
    )
)
echo ✅ Deployment files organized!
echo.

echo 🛠️ Moving utility files...
for %%f in (create_*.py) do (
    if exist "%%f" (
        move "%%f" utils\ >nul 2>&1
        echo   Moved: %%f
    )
)
echo ✅ Utilities organized!
echo.

echo ===============================================
echo 🎉 SIMS Project Organization Complete!
echo ===============================================
echo.
echo 📂 Your new structure:
echo ├── 📁 docs/         (Documentation)
echo ├── 📁 tests/        (Tests ^& Verification)
echo ├── 📁 scripts/      (Utility Scripts)
echo ├── 📁 deployment/   (Deployment Configs)
echo ├── 📁 utils/        (Admin Utilities)
echo ├── 📁 sims/         (Django App)
echo ├── 📁 templates/    (Django Templates)
echo ├── 📁 static/       (Static Files)
echo └── 📄 manage.py     (Django Management)
echo.
echo Your SIMS project is now professionally organized! 🎊
echo.
pause
