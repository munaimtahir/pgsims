# Smoke Test and Migration Checklist

This document provides a comprehensive checklist for testing SIMS deployment and verifying that all critical functionality works correctly.

## Pre-Deployment Checklist

### Environment Configuration
- [ ] `SECRET_KEY` is set and is at least 50 characters long
- [ ] `DEBUG` is set to `False` for production
- [ ] `ALLOWED_HOSTS` includes your domain name
- [ ] `DB_PASSWORD` is strong and secure
- [ ] `CSRF_TRUSTED_ORIGINS` includes your domain with `https://`
- [ ] `SESSION_COOKIE_SECURE` is set to `True`
- [ ] `CSRF_COOKIE_SECURE` is set to `True`

### SSL/HTTPS Configuration
- [ ] Domain DNS points to correct server IP
- [ ] Traefik/Coolify is configured for the domain
- [ ] SSL certificate is generated (Let's Encrypt)
- [ ] HTTPS is enforced (HTTP redirects to HTTPS)

### Docker Configuration
- [ ] No port 80 or 443 bindings in compose files
- [ ] Port 8000 is exposed internally only
- [ ] All services are in the same Docker network
- [ ] Volume mounts are configured for persistence

## Deployment Verification

### 1. Container Health Checks

Verify all containers are running:

```bash
# For docker-compose deployment
docker-compose -f docker-compose.coolify.yml ps

# Expected: All services should be "Up (healthy)"
```

Check individual service health:

```bash
# Database
docker-compose -f docker-compose.coolify.yml exec db pg_isready -U sims_user

# Redis
docker-compose -f docker-compose.coolify.yml exec redis redis-cli ping

# Web application
docker-compose -f docker-compose.coolify.yml exec web curl -f http://localhost:8000/healthz/
```

**Expected Results:**
- PostgreSQL: `ready`
- Redis: `PONG`
- Web: HTTP 200 with JSON response

### 2. Application Health Endpoint

```bash
curl -v https://yourdomain.com/healthz/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "cache": "ok",
    "celery": "ok"
  }
}
```

**Verification Points:**
- [ ] HTTP status is 200
- [ ] Response is valid JSON
- [ ] All checks show "ok" status
- [ ] Response time is < 2 seconds

### 3. HTTPS/SSL Verification

```bash
curl -I https://yourdomain.com
```

**Expected Response Headers:**
- [ ] `HTTP/2 200` or `HTTP/1.1 200`
- [ ] `Strict-Transport-Security` header present
- [ ] No SSL certificate errors
- [ ] Valid certificate chain

Test SSL quality:
```bash
# Check SSL/TLS protocol version
curl -vI https://yourdomain.com 2>&1 | grep -E "SSL|TLS|cipher"

# Or use openssl for detailed info
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com < /dev/null 2>&1 | grep -E "Protocol|Cipher"
```

**Verification Points:**
- [ ] TLS 1.2 or TLS 1.3 is used
- [ ] Strong cipher suites
- [ ] Valid certificate (not self-signed in production)
- [ ] Certificate not expired

### 4. Reverse Proxy Headers

Check that Django correctly detects HTTPS:

```bash
# Access any page and check X-Forwarded-Proto in logs
docker-compose -f docker-compose.coolify.yml logs web | grep "X-Forwarded-Proto"
```

**Verification Points:**
- [ ] `X-Forwarded-Proto: https` is present in requests
- [ ] Django `request.is_secure()` returns `True`
- [ ] No redirect loops occur
- [ ] Cookies have `Secure` flag set

### 5. Static Files

Test static file serving with WhiteNoise:

```bash
# CSS
curl -I https://yourdomain.com/static/css/style.css

# JavaScript
curl -I https://yourdomain.com/static/js/main.js

# Admin static files
curl -I https://yourdomain.com/static/admin/css/base.css
```

**Expected Response Headers:**
- [ ] HTTP status is 200
- [ ] `Content-Type` is correct (text/css, application/javascript)
- [ ] `Cache-Control` header is present
- [ ] `ETag` header is present (WhiteNoise feature)
- [ ] Files are compressed (check `Content-Encoding: gzip`)

**Verification Points:**
- [ ] CSS loads correctly in browser
- [ ] JavaScript loads correctly
- [ ] No 404 errors for static files
- [ ] Static files have long cache times (check browser dev tools)

### 6. Media Files

Test media file uploads and access:

```bash
# Upload a file through admin or application
# Then test access:
curl -I https://yourdomain.com/media/uploads/test-file.jpg
```

**Verification Points:**
- [ ] Files can be uploaded
- [ ] Uploaded files are accessible
- [ ] Correct content-type headers
- [ ] Appropriate cache headers

## Functional Testing

### 7. Django Admin Access

1. Visit `https://yourdomain.com/admin/`

**Verification Points:**
- [ ] Admin login page loads
- [ ] CSS/styling is applied correctly
- [ ] Can log in with superuser credentials
- [ ] Dashboard loads successfully
- [ ] Can view model lists
- [ ] Can create/edit/delete records
- [ ] No JavaScript errors in console

### 8. User Authentication

Test user flows:

**Login:**
- [ ] Visit login page
- [ ] Submit valid credentials
- [ ] Redirected to dashboard
- [ ] Session persists across page loads

**Logout:**
- [ ] Click logout
- [ ] Session is cleared
- [ ] Redirected to login page
- [ ] Cannot access protected pages

**Password Reset:**
- [ ] Request password reset
- [ ] Email is sent (check logs if using console backend)
- [ ] Reset link works
- [ ] Can set new password

### 9. Database Operations

```bash
# Connect to database
docker-compose -f docker-compose.coolify.yml exec db psql -U sims_user -d sims_db
```

**Run test queries:**
```sql
-- Check tables exist
\dt

-- Check users
SELECT COUNT(*) FROM auth_user;

-- Check recent activity
SELECT COUNT(*) FROM django_session WHERE expire_date > NOW();

-- Exit
\q
```

**Verification Points:**
- [ ] All expected tables exist
- [ ] Migrations are applied
- [ ] Can query tables
- [ ] Data is persisted across restarts

### 10. Redis Cache

```bash
# Connect to Redis
docker-compose -f docker-compose.coolify.yml exec redis redis-cli

# Test cache operations
PING
KEYS *
INFO stats
```

**Verification Points:**
- [ ] Redis is responding
- [ ] Cache keys are being created
- [ ] Session data is stored in Redis
- [ ] No connection errors in logs

### 11. Celery Workers

Check Celery worker status:

```bash
# View worker logs
docker-compose -f docker-compose.coolify.yml logs worker

# Check worker is processing tasks
docker-compose -f docker-compose.coolify.yml exec worker celery -A sims_project inspect active
```

**Verification Points:**
- [ ] Worker is running
- [ ] Worker is connected to Redis
- [ ] Tasks are being processed
- [ ] No error messages in logs

Test a simple task:
```bash
docker-compose -f docker-compose.coolify.yml exec web python manage.py shell
```

```python
from sims.notifications.tasks import send_test_notification
result = send_test_notification.delay()
print(result.get(timeout=10))
exit()
```

**Verification Points:**
- [ ] Task is sent to queue
- [ ] Worker picks up task
- [ ] Task completes successfully
- [ ] Result is returned

### 12. API Endpoints

Test API functionality:

```bash
# Get JWT token
curl -X POST https://yourdomain.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"yourpassword"}'

# Use token to access protected endpoint
curl -X GET https://yourdomain.com/api/users/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Verification Points:**
- [ ] Can obtain JWT token
- [ ] Token authentication works
- [ ] API endpoints return correct data
- [ ] Proper error responses (401, 403, etc.)
- [ ] CORS headers are correct (if needed)

### 13. Form Submissions

Test forms on the application:

**CSRF Protection:**
- [ ] Forms include CSRF token
- [ ] Form submissions succeed
- [ ] Invalid CSRF tokens are rejected

**File Uploads:**
- [ ] Can upload files
- [ ] Files are saved to media folder
- [ ] File size limits are enforced
- [ ] Allowed file types are validated

**Data Validation:**
- [ ] Required fields are enforced
- [ ] Invalid data shows error messages
- [ ] Valid data is saved correctly

## Performance Testing

### 14. Response Times

```bash
# Test page load times
time curl -s https://yourdomain.com/ > /dev/null

# Test health endpoint
time curl -s https://yourdomain.com/healthz/ > /dev/null
```

**Acceptable Response Times:**
- [ ] Homepage: < 2 seconds
- [ ] Health check: < 1 second
- [ ] API endpoints: < 1 second
- [ ] Admin pages: < 3 seconds

### 15. Concurrent Requests

Test with Apache Bench or similar:

```bash
# Install if needed: apt-get install apache2-utils

# Test 100 requests, 10 concurrent
ab -n 100 -c 10 https://yourdomain.com/healthz/
```

**Verification Points:**
- [ ] No failed requests
- [ ] Consistent response times
- [ ] No 500 errors
- [ ] No connection timeouts

### 16. Resource Usage

```bash
# Check Docker stats
docker stats --no-stream
```

**Expected Resource Usage (approximate):**
- [ ] Web container: 100-500MB RAM
- [ ] PostgreSQL: 50-200MB RAM
- [ ] Redis: 10-50MB RAM
- [ ] Worker: 100-300MB RAM
- [ ] Total CPU usage: < 50% under normal load

## Security Testing

### 17. Security Headers

```bash
curl -I https://yourdomain.com
```

**Required Headers:**
- [ ] `Strict-Transport-Security` (HSTS)
- [ ] `X-Frame-Options: DENY`
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `Referrer-Policy: same-origin`
- [ ] `X-XSS-Protection: 1; mode=block`

### 18. Admin Access

**Security Checks:**
- [ ] Admin URL is not exposed to public
- [ ] Strong password is enforced
- [ ] Rate limiting is active
- [ ] Failed login attempts are logged
- [ ] Admin can only be accessed via HTTPS

### 19. Database Security

**Verification Points:**
- [ ] Database is not accessible from internet
- [ ] Database password is strong
- [ ] Database user has minimal required permissions
- [ ] Database backups are encrypted

### 20. Secrets Management

**Verification Points:**
- [ ] `SECRET_KEY` is not exposed in logs
- [ ] `DB_PASSWORD` is not exposed in logs
- [ ] `.env` file is not in git repository
- [ ] Environment variables are used (not hardcoded)
- [ ] No secrets in error messages

## Post-Deployment Checklist

### Monitoring Setup
- [ ] Set up log aggregation
- [ ] Configure error alerting
- [ ] Set up uptime monitoring
- [ ] Configure health check alerts
- [ ] Set up performance monitoring

### Backup Strategy
- [ ] Database backup script is configured
- [ ] Backups are automated (cron job)
- [ ] Backup restoration is tested
- [ ] Media files are backed up
- [ ] Backups are stored off-site

### Documentation
- [ ] Deployment process is documented
- [ ] Environment variables are documented
- [ ] Runbook for common issues exists
- [ ] Contact information for support is available
- [ ] Change log is maintained

## Regression Testing

After updates or changes, re-run these key tests:

1. [ ] Health endpoint returns 200
2. [ ] Admin login works
3. [ ] Static files load correctly
4. [ ] Database queries work
5. [ ] Celery tasks process
6. [ ] No new security vulnerabilities
7. [ ] Performance is acceptable

## Known Issues / Limitations

Document any known issues specific to your deployment:

```
Example:
- [ ] Issue: Large file uploads timeout after 60 seconds
      Workaround: Increase Traefik timeouts or gunicorn worker timeout (--timeout flag)
      
- [ ] Issue: Celery tasks fail during database maintenance
      Workaround: Stop worker during maintenance windows
```

## Sign-Off

Deployment tested and verified by: ________________

Date: ________________

Environment: ☐ Staging  ☐ Production

All critical tests passed: ☐ Yes  ☐ No (see notes below)

Notes:
```
[Add any deployment notes, issues, or observations here]
```

---

## Quick Smoke Test (1 minute)

For quick verification after deployment:

```bash
# 1. Health check
curl https://yourdomain.com/healthz/ | jq .

# 2. SSL check
curl -I https://yourdomain.com | grep "HTTP\|Strict-Transport"

# 3. Admin access
curl -I https://yourdomain.com/admin/

# 4. Static files
curl -I https://yourdomain.com/static/admin/css/base.css

# 5. Container health
docker ps --filter "name=sims" --format "{{.Names}}: {{.Status}}"
```

All checks should pass within 1 minute. If any fail, investigate immediately.
