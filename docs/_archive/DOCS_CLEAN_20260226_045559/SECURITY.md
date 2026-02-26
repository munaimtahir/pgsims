# Security Best Practices

Security guidelines and configurations for SIMS.

## Security Checklist

### Before Deployment

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain(s)
- [ ] Enable SSL/HTTPS (`SECURE_SSL_REDIRECT=True`)
- [ ] Set secure cookie flags (`SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`)
- [ ] Configure HSTS (`SECURE_HSTS_SECONDS=31536000`)
- [ ] Use strong database password
- [ ] Use environment variables for all secrets
- [ ] Enable database connection encryption
- [ ] Configure firewall rules
- [ ] Set up regular database backups
- [ ] Review user permissions and roles
- [ ] Enable audit logging
- [ ] Configure rate limiting
- [ ] Set up monitoring and alerting

## Django Security Settings

### SECRET_KEY

**Critical**: Never commit SECRET_KEY to version control.

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Store in environment variable:
```env
SECRET_KEY=your-randomly-generated-50-character-secret-key
```

### Debug Mode

**Never** run with `DEBUG=True` in production:
```env
DEBUG=False
```

Debug mode can leak sensitive information about your application structure.

### Allowed Hosts

Restrict which hosts can serve your application:
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com
```

## SSL/HTTPS Configuration

### Force HTTPS Redirect

```env
SECURE_SSL_REDIRECT=True
```

### HSTS (HTTP Strict Transport Security)

```env
SECURE_HSTS_SECONDS=31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

**Note**: Only enable HSTS preload after testing, as it's difficult to reverse.

### Secure Cookies

```env
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Additional Security Headers

Already configured in settings.py:
- `SECURE_BROWSER_XSS_FILTER=True`
- `SECURE_CONTENT_TYPE_NOSNIFF=True`
- `X_FRAME_OPTIONS="DENY"`
- `SECURE_REFERRER_POLICY="same-origin"`

## Password Security

### Password Validators

Django enforces the following password policies:
1. Must not be similar to user attributes
2. Minimum length of 8 characters
3. Cannot be a commonly used password
4. Cannot be entirely numeric

Configured in `settings.py`:
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### Password Storage

Passwords are hashed using Django's default PBKDF2 algorithm with SHA256.

## API Security

### Authentication

All API endpoints require authentication by default:
```python
'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated']
```

### Throttling

Rate limiting to prevent abuse:

```env
THROTTLE_ANON_RATE=100/hour      # Anonymous users
THROTTLE_USER_RATE=1000/hour     # Authenticated users
THROTTLE_SEARCH_RATE=30/min      # Search endpoints
```

### CORS (Cross-Origin Resource Sharing)

If you have a separate frontend:
```env
CORS_ALLOWED_ORIGINS=https://yourfrontend.com,https://app.yourfrontend.com
CORS_ALLOW_CREDENTIALS=True
```

## Database Security

### Connection Security

Use SSL/TLS for database connections in production:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... other settings ...
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}
```

### Database Credentials

Store in environment variables:
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
```

### Regular Backups

```bash
# Automated daily backup
0 2 * * * pg_dump sims_db > /backups/sims_$(date +\%Y\%m\%d).sql
```

## File Upload Security

### Size Limits

Configured in `settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

### Allowed Extensions

Restrict file types:
```python
ALLOWED_UPLOAD_EXTENSIONS = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.xlsx', '.csv']
```

### File Permissions

```python
FILE_UPLOAD_PERMISSIONS = 0o644
```

## Content Security Policy (CSP)

Basic CSP configured. For production, tighten as needed:

```env
CSP_DEFAULT_SRC='self'
CSP_SCRIPT_SRC='self' 'unsafe-inline'  # Remove unsafe-inline if possible
CSP_STYLE_SRC='self' 'unsafe-inline'   # Remove unsafe-inline if possible
CSP_IMG_SRC='self' data: https:
CSP_FONT_SRC='self' data:
```

**Best Practice**: Eliminate `'unsafe-inline'` by using nonces or hashes.

## Session Security

### Session Configuration

```python
SESSION_COOKIE_AGE = 28800  # 8 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
```

### Session Storage

For production, use Redis for sessions:
```env
SESSION_ENGINE=django.contrib.sessions.backends.cache
REDIS_URL=redis://redis:6379/0
```

## Audit Logging

All security-sensitive actions are logged:
- User login/logout
- Password changes
- Permission changes
- Data modifications
- Failed authentication attempts

Review logs regularly:
```bash
tail -f logs/sims_error.log
```

## Monitoring & Alerting

### Health Checks

Monitor application health:
```bash
curl http://yourapp.com/healthz/
```

### Error Tracking

Configure Sentry for error tracking:
```env
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### Failed Login Monitoring

Monitor for brute force attempts:
```bash
grep "Invalid password" logs/sims_error.log | wc -l
```

## Dependency Security

### Regular Updates

```bash
# Check for security updates
pip list --outdated

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Vulnerability Scanning

```bash
# Install safety
pip install safety

# Check for known vulnerabilities
safety check
```

## Docker Security

### Non-Root User

Dockerfile runs as non-root user:
```dockerfile
USER sims
```

### Image Scanning

Scan Docker images for vulnerabilities:
```bash
docker scan sims_web:latest
```

### Secrets Management

Never bake secrets into images:
```bash
# Use environment variables or secrets management
docker-compose run -e SECRET_KEY=$SECRET_KEY web
```

## Nginx Security

### Security Headers

Add to nginx.conf (already configured):
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

### Rate Limiting

Add to nginx.conf:
```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

location /users/login/ {
    limit_req zone=login burst=5;
}
```

## Incident Response

### Compromised Secret Key

1. Generate new SECRET_KEY immediately
2. Update environment variable
3. Restart application
4. Invalidate all sessions
5. Force password reset for all users
6. Review audit logs
7. Assess data exposure

### Database Breach

1. Isolate affected systems
2. Change all database credentials
3. Review audit logs
4. Notify affected users
5. Implement additional monitoring
6. Review and strengthen security measures

## Compliance

### HIPAA (for medical data)

- Enable audit logging for all data access
- Implement access controls based on roles
- Encrypt data at rest and in transit
- Regular security audits
- Incident response procedures
- Business associate agreements

### GDPR

- User consent management
- Data export capabilities
- Data deletion procedures
- Privacy policy
- Data processing agreements

## Security Contacts

Report security issues to: security@yourdomain.com

## Additional Resources

- [Django Security Docs](https://docs.djangoproject.com/en/4.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
