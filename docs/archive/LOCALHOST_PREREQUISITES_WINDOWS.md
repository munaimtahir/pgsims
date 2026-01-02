# SIMS Localhost Prerequisites for Windows

This guide lists all prerequisites needed to run SIMS on your Windows localhost machine.

## Required Prerequisites

### 1. Python 3.11 or Higher

**Download:** https://www.python.org/downloads/

**Installation Steps:**
1. Download the latest Python 3.11+ installer
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation
4. Complete the installation

**Verify Installation:**
```powershell
python --version
# Should show: Python 3.11.x or higher
```

### 2. pip (Python Package Manager)

pip usually comes with Python. If not installed:

```powershell
python -m ensurepip --upgrade
```

**Verify Installation:**
```powershell
pip --version
```

### 3. Node.js 18 or Higher

**Download:** https://nodejs.org/

**Installation Steps:**
1. Download the LTS (Long Term Support) version
2. Run the installer
3. Follow the installation wizard
4. Restart your terminal after installation

**Verify Installation:**
```powershell
node --version
# Should show: v18.x.x or higher

npm --version
# Should show: 9.x.x or higher
```

### 4. Docker Desktop for Windows

**Download:** https://www.docker.com/products/docker-desktop/

**Installation Steps:**
1. Download Docker Desktop for Windows
2. Run the installer
3. Follow the installation wizard
4. Restart your computer if prompted
5. Start Docker Desktop from the Start menu
6. Wait for Docker Desktop to fully start (whale icon in system tray)

**Verify Installation:**
```powershell
docker --version
docker compose version
```

**Note:** Docker Desktop must be running for Docker commands to work.

### 5. Git (Optional but Recommended)

**Download:** https://git-scm.com/download/win

**Installation Steps:**
1. Download Git for Windows
2. Run the installer
3. Use default options (recommended)
4. Complete the installation

**Verify Installation:**
```powershell
git --version
```

## Optional Prerequisites

### PostgreSQL (Optional)

For localhost, you can use SQLite (default) or PostgreSQL.

**If using PostgreSQL:**
- **Download:** https://www.postgresql.org/download/windows/
- Or use PostgreSQL in Docker (recommended)

### Redis (Optional)

For Celery and caching, Redis is recommended but optional for basic localhost setup.

**Options:**
1. Use Docker to run Redis (recommended)
2. Install Redis for Windows: https://github.com/microsoftarchive/redis/releases
3. Use Redis in Docker Compose (included in docker-compose.localhost.yml)

## Quick Setup Script

Use the provided setup script to check prerequisites and set up the environment:

**PowerShell:**
```powershell
.\scripts\setup_localhost_windows.ps1
```

**Command Prompt (Batch):**
```cmd
scripts\setup_localhost_windows.bat
```

## Manual Setup Steps

If you prefer to set up manually:

1. **Clone the repository:**
   ```powershell
   git clone <repository-url>
   cd sims
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```powershell
   pip install --upgrade pip wheel
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```powershell
   Copy-Item .env.localhost .env
   # Edit .env with your settings if needed
   ```

5. **Install frontend dependencies:**
   ```powershell
   cd frontend
   npm install
   Copy-Item .env.localhost .env.local
   cd ..
   ```

6. **Run migrations:**
   ```powershell
   python manage.py migrate
   ```

7. **Create superuser:**
   ```powershell
   python manage.py createsuperuser
   ```

8. **Start development server:**
   ```powershell
   python manage.py runserver
   ```

## Troubleshooting

### Python Not Found

- Make sure Python is added to PATH
- Restart your terminal after installation
- Try using `py` instead of `python` on Windows

### Docker Not Running

- Start Docker Desktop from the Start menu
- Wait for Docker to fully start (check system tray icon)
- Restart Docker Desktop if needed

### Port Already in Use

If port 8000 is already in use:
- Stop the process using port 8000
- Or change the port in `.env` file and runserver command

### Permission Errors

- Run PowerShell/Command Prompt as Administrator if needed
- Check file/folder permissions
- Make sure you're in the correct directory

## Next Steps

After installing prerequisites:

1. Run the setup script: `.\scripts\setup_localhost_windows.ps1`
2. Follow the [Localhost Deployment Guide](LOCALHOST_DEPLOYMENT_GUIDE.md)
3. Start developing!

