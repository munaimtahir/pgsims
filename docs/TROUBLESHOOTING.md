# SIMS System Troubleshooting Guide

## Quick Start Commands

### Start the Django Server
```bash
cd d:\PMC\sims_project
python manage.py runserver 127.0.0.1:8000
```

### Create Admin User (if needed)
```bash
cd d:\PMC\sims_project
python create_admin.py
```

### Run System Verification
```bash
cd d:\PMC\sims_project
python verify_django.py
```

### Run Comprehensive Tests
```powershell
cd d:\PMC\sims_project
.\comprehensive_test.ps1
```

## Common Issues and Solutions

### 1. Server Won't Start
**Symptoms**: Django server fails to start or shows errors
**Solutions**:
- Check if port 8000 is already in use: `netstat -an | findstr :8000`
- Apply migrations: `python manage.py migrate`
- Check for Python syntax errors in recent changes

### 2. Template Not Found Errors
**Symptoms**: TemplateDoesNotExist errors
**Solutions**:
- Verify template files exist in correct directories
- Check TEMPLATES setting in settings.py
- Ensure template inheritance is correct

### 3. Database Connection Issues
**Symptoms**: Database errors or migration issues
**Solutions**:
- Delete db.sqlite3 and run: `python manage.py migrate`
- Check database permissions
- Verify DATABASES setting in settings.py

### 4. Admin Login Issues
**Symptoms**: Cannot login to admin or user accounts
**Solutions**:
- Reset admin password: `python create_admin.py`
- Check if user exists: `python manage.py shell`
- Verify authentication backends in settings

### 5. Static Files Not Loading
**Symptoms**: CSS/JS not loading, styling broken
**Solutions**:
- Run: `python manage.py collectstatic`
- Check STATIC_URL and STATICFILES_DIRS settings
- Verify static files exist in correct directories

### 6. Permission Denied Errors
**Symptoms**: 403 Forbidden or permission errors
**Solutions**:
- Check user roles and permissions
- Verify login_required decorators
- Check Django permissions system

## Testing Checklist

### Basic Functionality
- [ ] Server starts without errors
- [ ] Admin login works (admin/admin123)
- [ ] Dashboard loads for each role
- [ ] User profile pages work
- [ ] Analytics pages display correctly

### Authentication
- [ ] Login page loads
- [ ] Logout functionality works
- [ ] Password reset works
- [ ] Password change works
- [ ] Role-based access control

### Dashboard Features
- [ ] Admin dashboard shows system stats
- [ ] Supervisor dashboard shows trainee info
- [ ] Postgraduate dashboard shows personal progress
- [ ] Analytics charts display correctly
- [ ] Navigation between sections works

### Data Management
- [ ] User creation and editing
- [ ] Profile updates save correctly
- [ ] Logbook entries can be created
- [ ] Case management works
- [ ] Certificate tracking functions

## Development Commands

### Database Management
```bash
# Apply migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Show migration status
python manage.py showmigrations

# Reset database (WARNING: deletes all data)
del db.sqlite3
python manage.py migrate
python create_admin.py
```

### User Management
```bash
# Create superuser interactively
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Change user password in shell
python manage.py changepassword username
```

### System Information
```bash
# Check Django version
python -c "import django; print(django.get_version())"

# Check installed packages
pip list

# Run system checks
python manage.py check
```

## Log Files

### Server Logs
- Django development server outputs to console
- Check console for error messages
- Look for 404, 500, or other HTTP errors

### Application Logs
- Custom logs in `logs/sims.log` (if configured)
- Django admin logs in database
- Check browser developer tools for JavaScript errors

## Performance Optimization

### Database
- Monitor query count in debug mode
- Use select_related() for foreign keys
- Consider database indexing for production

### Templates
- Minimize template inheritance depth
- Use template fragment caching where appropriate
- Optimize image sizes and formats

### Static Files
- Compress CSS and JavaScript for production
- Use CDN for Bootstrap and other libraries
- Enable gzip compression on server

## Security Considerations

### Production Deployment
- Set DEBUG = False in production
- Use environment variables for secrets
- Configure ALLOWED_HOSTS properly
- Use HTTPS in production
- Regular security updates

### User Management
- Enforce strong password policies
- Regular user account audits
- Monitor login attempts
- Implement session timeouts

## Contact Information

For technical support or questions:
- Check this troubleshooting guide first
- Review Django documentation
- Contact system administrator

Last Updated: May 30, 2025
