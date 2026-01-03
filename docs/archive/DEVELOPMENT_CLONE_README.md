# Development Clone - /root/sims

## Important Note

This directory (`/root/sims`) is a **development/testing clone** of the SIMS repository.

## Production Deployment Location

**The official production deployment location is: `/opt/sims_project`**

All deployment scripts, systemd services, Docker configurations, and production documentation reference `/opt/sims_project` as the standard location.

## Purpose of This Directory

This clone can be used for:
- Local development and testing
- Experimentation with new features
- Quick testing before pushing to production

## Workflow

1. **Make changes in this directory** (`/root/sims`)
2. **Test your changes locally**
3. **Commit and push to GitHub:**
   ```bash
   cd /root/sims
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```
4. **Pull changes in production directory:**
   ```bash
   cd /opt/sims_project
   git pull origin main
   ```

## Important Reminders

- ⚠️ **DO NOT** run deployment scripts from this directory
- ⚠️ **DO NOT** configure systemd services to use this directory
- ⚠️ **DO NOT** use this directory for production deployments
- ✅ **DO** use this directory for development and testing
- ✅ **DO** sync changes to `/opt/sims_project` via GitHub

## Syncing with Production

After making changes and pushing to GitHub:

```bash
# In production directory
cd /opt/sims_project
git pull origin main

# If using Docker
cd /opt/sims_project
docker compose down
docker compose up -d --build

# If using traditional deployment
cd /opt/sims_project
sudo systemctl restart sims
```

## Questions?

Refer to the main deployment documentation in `/opt/sims_project/deployment/DEPLOYMENT_README.md`
