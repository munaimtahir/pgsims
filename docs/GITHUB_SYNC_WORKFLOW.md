# GitHub Sync Workflow

## Repository Structure

The SIMS project uses a two-location setup:

1. **Development/Workspace**: `/root/sims` - Primary development location
2. **Production/Deployment**: `/opt/sims_project` - Production deployment location

Both locations are connected to the same GitHub repository: `https://github.com/munaimtahir/sims.git`

## Standard Workflow

### Development (in `/root/sims`)

1. **Make your changes:**
   ```bash
   cd /root/sims
   # Edit files, make changes, etc.
   ```

2. **Commit changes:**
   ```bash
   cd /root/sims
   git add .
   git commit -m "Description of changes"
   ```

3. **Push to GitHub:**
   ```bash
   git push origin main
   ```

### Deployment Sync (in `/opt/sims_project`)

1. **Pull latest changes from GitHub:**
   ```bash
   cd /opt/sims_project
   git pull origin main
   ```

2. **If using Docker:**
   ```bash
   cd /opt/sims_project
   docker compose down
   docker compose up -d --build
   ```

3. **If using traditional deployment:**
   ```bash
   cd /opt/sims_project
   sudo systemctl restart sims
   ```

## Quick Sync Script

You can use this script to quickly sync changes:

```bash
#!/bin/bash
# Quick sync script
cd /root/sims
git add .
git commit -m "Sync changes"
git push origin main

cd /opt/sims_project
git pull origin main
echo "✅ Sync complete!"
```

## Important Notes

- ⚠️ **Always develop in `/root/sims`** - This is your workspace
- ⚠️ **Always deploy from `/opt/sims_project`** - This is the production location
- ✅ **Both locations sync via GitHub** - Push from workspace, pull in production
- ✅ **All deployment scripts use `/opt/sims_project`** - Don't change this

## Verification

After syncing, verify the deployment:

```bash
# Check that production has latest code
cd /opt/sims_project
git log -1

# Verify paths are correct
cd /opt/sims_project/deployment
./verify_path_consistency.sh
```

## Troubleshooting

### If changes don't appear in production:

1. Check that you pushed from `/root/sims`:
   ```bash
   cd /root/sims
   git log -1
   ```

2. Check GitHub has the latest commit:
   ```bash
   # Visit: https://github.com/munaimtahir/sims/commits/main
   ```

3. Pull in production:
   ```bash
   cd /opt/sims_project
   git fetch origin
   git pull origin main
   ```

### If there are merge conflicts:

```bash
cd /opt/sims_project
git stash
git pull origin main
# Resolve conflicts if any
git stash pop
```

## Best Practices

1. **Commit frequently** - Small, logical commits are easier to manage
2. **Test before pushing** - Test changes in `/root/sims` before pushing
3. **Pull before making changes** - Always pull latest in production before deploying
4. **Use descriptive commit messages** - Makes it easier to track changes
5. **Verify after sync** - Always verify deployment after syncing
