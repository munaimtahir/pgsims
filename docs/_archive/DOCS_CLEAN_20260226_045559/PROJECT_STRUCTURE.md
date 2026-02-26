# SIMS Project Structure

This document describes the organized folder structure of the SIMS (Postgraduate Medical Training System) project.

## 📁 Project Structure

```
sims_project-1/
├── 📂 sims/                    # Main Django application
├── 📂 sims_project/           # Django project settings
├── 📂 templates/              # Django templates
├── 📂 static/                 # Static files (CSS, JS, images)
├── 📂 staticfiles/           # Collected static files for production
├── 📂 logs/                  # Application logs
├── 📂 docs/                  # 📚 Documentation files
│   ├── ADMIN_*.md
│   ├── AUTHENTICATION_*.md
│   ├── HOMEPAGE_*.md
│   ├── LOGIN_*.md
│   ├── LOGOUT_*.md
│   ├── MIGRATION_*.md
│   ├── NGINX_*.md
│   ├── PROJECT_SUMMARY.md
│   ├── README.md
│   ├── SERVER_*.md
│   ├── SYSTEM_*.md
│   ├── THEME_*.md
│   └── TROUBLESHOOTING.md
├── 📂 tests/                 # 🧪 Test and verification scripts
│   ├── test_*.py
│   ├── verify_*.py
│   ├── validate_*.py
│   ├── diagnose_*.py
│   ├── quick_*.py
│   ├── simple_*.py
│   ├── final_*.py
│   ├── django_verification.py
│   ├── login_system_verification.py
│   ├── run_verification.py
│   ├── system_health_check.py
│   └── url_test.py
├── 📂 scripts/               # 🔧 Utility scripts
│   ├── *.bat                 # Batch files
│   ├── *.ps1                 # PowerShell scripts
│   ├── start_django.ps1
│   ├── start_server.bat
│   ├── comprehensive_test.ps1
│   └── server_diagnostic_helper.ps1
├── 📂 deployment/            # 🚀 Deployment configuration
│   ├── *.conf               # Apache/Nginx configs
│   ├── *.service            # Systemd service files
│   ├── *.sh                 # Shell deployment scripts
│   ├── gunicorn.conf.py
│   ├── server_config.env
│   └── deployment_fix.py
├── 📂 utils/                 # 🛠️ Utility tools
│   ├── create_admin.py
│   ├── create_superuser.py
│   └── create_superuser.bat
├── 📂 .git/                  # Git repository
├── 📂 .github/               # GitHub configuration
├── 📂 .vscode/               # VS Code settings
├── 📂 .pytest_cache/         # Pytest cache
├── 📂 __pycache__/           # Python cache
├── 📄 manage.py              # Django management script
├── 📄 db.sqlite3             # SQLite database
├── 📄 requirements.txt       # Python dependencies
├── 📄 pytest.ini            # Pytest configuration
└── 📄 File Tree             # Project structure reference
```

## 📋 Folder Descriptions

### 🏠 Root Level Files
- **manage.py** - Django's command-line utility
- **db.sqlite3** - SQLite database file
- **requirements.txt** - Python package dependencies
- **pytest.ini** - Test configuration

### 📚 docs/
Contains all project documentation including:
- Completion reports for various features
- System deployment guides
- API documentation
- Troubleshooting guides

### 🧪 tests/
All testing and verification scripts:
- Unit tests (`test_*.py`)
- System verification (`verify_*.py`)
- Diagnostic tools (`diagnose_*.py`)
- Quick tests (`quick_*.py`)

### 🔧 scripts/
Utility scripts for development and maintenance:
- PowerShell scripts (`.ps1`)
- Batch files (`.bat`)
- Development helpers

### 🚀 deployment/
Production deployment configuration:
- Web server configs (Apache, Nginx)
- Service definitions
- Deployment automation scripts
- Environment configurations

### 🛠️ utils/
Administrative and utility tools:
- User creation scripts
- Database management tools
- System setup helpers

## 🎯 Benefits of This Structure

1. **🔍 Easy Navigation** - Files are logically grouped by purpose
2. **👥 Team Collaboration** - Clear separation of concerns
3. **🔧 Maintenance** - Easier to find and update specific components
4. **📦 Deployment** - Deployment files are centralized
5. **🧪 Testing** - All test files in one location
6. **📖 Documentation** - Comprehensive docs in dedicated folder

## 🚀 Usage Examples

### Running Tests
```powershell
cd tests/
python test_django.py
python verify_system.py
```

### Deployment
```powershell
cd deployment/
# Copy configuration files to server
# Run deployment scripts
```

### Development Scripts
```powershell
cd scripts/
./start_django.ps1
./comprehensive_test.ps1
```

### Utilities
```powershell
cd utils/
python create_admin.py
python create_superuser.py
```

This organized structure makes the SIMS project more maintainable and professional! 🎉
