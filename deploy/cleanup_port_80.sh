#!/bin/bash
# Port 80 Cleanup Script for SIMS Deployment on 172.236.152.35
# This script safely handles existing web services on port 80

echo "🔧 Port 80 Cleanup for SIMS Deployment"
echo "======================================="

echo "1. 🔍 Checking what's using port 80..."
echo "Services listening on port 80:"
ss -tulpn | grep :80

echo ""
echo "2. 🔍 Checking running web servers..."

# Check for Apache
if systemctl is-active --quiet apache2; then
    echo "📋 Apache2 is running"
    echo "   Status: $(systemctl is-active apache2)"
elif systemctl is-enabled --quiet apache2 2>/dev/null; then
    echo "📋 Apache2 is installed but not running"
else
    echo "✅ Apache2 not found"
fi

# Check for Nginx
if systemctl is-active --quiet nginx; then
    echo "📋 Nginx is running"
    echo "   Status: $(systemctl is-active nginx)"
elif systemctl is-enabled --quiet nginx 2>/dev/null; then
    echo "📋 Nginx is installed but not running"
else
    echo "✅ Nginx not found"
fi

# Check for other common services
echo ""
echo "3. 🔍 Checking for other services..."
if pgrep -f "httpd\|lighttpd\|caddy" > /dev/null; then
    echo "📋 Other web server processes found:"
    pgrep -fl "httpd\|lighttpd\|caddy"
else
    echo "✅ No other common web servers found"
fi

echo ""
echo "4. 🛠️  Recommended actions:"
echo "============================================="

# Provide specific recommendations
if systemctl is-active --quiet apache2; then
    echo "🔧 Apache2 is running. To proceed with SIMS deployment:"
    echo "   sudo systemctl stop apache2"
    echo "   sudo systemctl disable apache2  # (optional, prevents auto-start)"
    echo ""
elif systemctl is-active --quiet nginx; then
    echo "🔧 Nginx is already running. The SIMS deployment will:"
    echo "   ✅ Configure Nginx for SIMS"
    echo "   ✅ Replace the default site configuration"
    echo "   ✅ This is expected and should work fine"
    echo ""
else
    echo "🤔 Unknown service using port 80. Check the process list above."
    echo "   You may need to stop the conflicting service manually."
fi

echo "5. 🚀 Next steps:"
echo "============================================="
echo "Option A - Quick cleanup and deploy:"
echo "   sudo systemctl stop apache2 2>/dev/null || true"
echo "   sudo systemctl stop nginx 2>/dev/null || true"
echo "   ./deploy_server.sh"
echo ""
echo "Option B - Just deploy (if Nginx is the service using port 80):"
echo "   ./deploy_server.sh"
echo ""
echo "The deployment script will handle Nginx configuration automatically."
echo "============================================="
