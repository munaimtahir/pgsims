# Localhost Deployment Setup Summary

This document provides a quick summary of the localhost deployment setup that has been added to SIMS.

## What Has Been Added

### Configuration Files

1. **`.env.localhost`** - Localhost environment template (copy to `.env` for use)
2. **`.env.vps`** - VPS environment template (copy to `.env` for use)
3. **`.env.example`** - Updated with deployment options
4. **`deployment/server_config.localhost.env`** - Localhost server configuration template

### Docker Configuration

1. **`docker-compose.localhost.yml`** - Docker Compose configuration for localhost
   - Uses port 8000 instead of 81
   - Optional services (PostgreSQL, Redis, Celery) via profiles
   - Simplified for local development

2. **`deployment/nginx.localhost.conf`** - Nginx configuration for localhost
   - Listens on port 8000
   - Server name: localhost

### Django Settings

- **`sims_project/settings.py`** - Updated to support both localhost and VPS
  - Enhanced ALLOWED_HOSTS parsing
  - Improved CORS configuration with localhost defaults
  - Better environment detection

### Frontend Configuration

1. **`frontend/lib/api/client.ts`** - Auto-detects environment
   - Checks window.location to determine localhost vs VPS
   - Automatically selects correct API URL
   - Falls back to environment variable if set

2. **Frontend .env files** (templates, copy to `.env.local`):
   - `frontend/.env.localhost` - Localhost API URL
   - `frontend/.env.vps` - VPS API URL

### Deployment Scripts

1. **`deployment/deploy_localhost.sh`** - Localhost deployment script (Linux/Mac)
2. **`deployment/deploy_localhost.ps1`** - Localhost deployment script (Windows)
3. **`deployment/switch_to_localhost.sh`** - Switch to localhost configuration
4. **`deployment/switch_to_vps.sh`** - Switch to VPS configuration

### Windows Setup Scripts

1. **`scripts/setup_localhost_windows.ps1`** - PowerShell setup script
   - Checks all prerequisites
   - Creates virtual environment
   - Installs dependencies
   - Sets up configuration files

2. **`scripts/setup_localhost_windows.bat`** - Batch file setup script
   - Alternative to PowerShell script
   - Same functionality

### Documentation

1. **`LOCALHOST_DEPLOYMENT_GUIDE.md`** - Complete localhost deployment guide
2. **`LOCALHOST_PREREQUISITES_WINDOWS.md`** - Prerequisites installation guide
3. **`DEPLOYMENT_ENVIRONMENTS.md`** - Comparison and switching guide
4. **`README.md`** - Updated with localhost deployment section

## Quick Start

### For Windows Users

1. **Install prerequisites** (see LOCALHOST_PREREQUISITES_WINDOWS.md)

2. **Run setup script:**
   ```powershell
   .\scripts\setup_localhost_windows.ps1
   ```

3. **Deploy:**
   ```powershell
   .\deployment\deploy_localhost.ps1
   ```

4. **Access:** http://localhost:8000/

### For Linux/Mac Users

1. **Make scripts executable:**
   ```bash
   chmod +x deployment/*.sh
   chmod +x scripts/*.sh
   ```

2. **Run setup:**
   ```bash
   ./scripts/setup_localhost_windows.ps1  # Or adapt for your system
   ```

3. **Deploy:**
   ```bash
   ./deployment/deploy_localhost.sh
   ```

## File Structure

```
sims/
├── .env.localhost              # Localhost config template
├── .env.vps                    # VPS config template
├── .env.example                # Updated example
├── docker-compose.localhost.yml # Localhost Docker Compose
├── deployment/
│   ├── deploy_localhost.sh     # Localhost deployment (Linux/Mac)
│   ├── deploy_localhost.ps1    # Localhost deployment (Windows)
│   ├── switch_to_localhost.sh  # Switch to localhost
│   ├── switch_to_vps.sh        # Switch to VPS
│   ├── nginx.localhost.conf    # Localhost Nginx config
│   └── server_config.localhost.env
├── frontend/
│   ├── .env.localhost          # Localhost frontend config
│   ├── .env.vps                # VPS frontend config
│   └── lib/api/client.ts       # Updated with auto-detection
├── scripts/
│   ├── setup_localhost_windows.ps1
│   └── setup_localhost_windows.bat
├── sims_project/
│   └── settings.py             # Updated for both environments
├── LOCALHOST_DEPLOYMENT_GUIDE.md
├── LOCALHOST_PREREQUISITES_WINDOWS.md
├── DEPLOYMENT_ENVIRONMENTS.md
└── README.md                   # Updated
```

## Key Features

1. **Dual Environment Support** - Easy switching between localhost and VPS
2. **Auto-Detection** - Frontend automatically detects environment
3. **Windows Optimized** - PowerShell and batch scripts for Windows
4. **Docker Support** - Optional Docker deployment for localhost
5. **Flexible Setup** - SQLite by default, PostgreSQL optional
6. **Comprehensive Docs** - Detailed guides for all scenarios

## Environment Differences

| Setting | Localhost | VPS |
|---------|-----------|-----|
| Port | 8000 | 81 |
| DEBUG | True | False |
| Database | SQLite (default) | PostgreSQL (Docker) |
| ALLOWED_HOSTS | localhost,127.0.0.1 | 139.162.9.224,... |
| URL | http://localhost:8000 | http://139.162.9.224:81 |

## Next Steps

1. Review the [LOCALHOST_DEPLOYMENT_GUIDE.md](LOCALHOST_DEPLOYMENT_GUIDE.md)
2. Check [LOCALHOST_PREREQUISITES_WINDOWS.md](LOCALHOST_PREREQUISITES_WINDOWS.md) for prerequisites
3. Read [DEPLOYMENT_ENVIRONMENTS.md](DEPLOYMENT_ENVIRONMENTS.md) to understand differences
4. Start developing on localhost!

## Notes

- `.env` files are in `.gitignore` - you'll need to create them from templates
- Frontend `.env.local` files are also in `.gitignore`
- Shell scripts need execute permissions on Linux/Mac: `chmod +x *.sh`
- Docker Desktop must be running for Docker deployments
- SQLite is the default database for localhost (no setup needed)

## Support

For issues:
1. Check the troubleshooting sections in the guides
2. Review the documentation files
3. Check that all prerequisites are installed
4. Verify environment files are correctly configured

