#!/bin/bash
# SIMS Nginx 403 Forbidden Error Diagnostic Script for 172.236.152.35
# Run this script on your server to diagnose the 403 error

echo "🔍 SIMS Server Diagnostic - 403 Forbidden Error"
echo "=========================================================="
echo "Server: 172.236.152.35"
echo "Date: $(date)"
echo "User: $(whoami)"
echo ""

# 1. Check service status
echo "1. 📊 SERVICE STATUS CHECK"
echo "----------------------------------------"
echo "Nginx Status:"
sudo systemctl status nginx --no-pager
echo ""
echo "SIMS Service Status:"
sudo systemctl status sims --no-pager
echo ""
echo "Gunicorn Processes:"
ps aux | grep gunicorn
echo ""

# 2. Check file permissions and ownership
echo "2. 📁 FILE PERMISSIONS CHECK"
echo "----------------------------------------"
echo "Project directory ownership:"
ls -la /opt/ | grep sims_project
echo ""
echo "Project directory contents:"
ls -la /opt/sims_project/
echo ""
echo "Static files directory:"
ls -la /opt/sims_project/ | grep static
echo ""

# 3. Check Nginx configuration
echo "3. ⚙️  NGINX CONFIGURATION CHECK"
echo "----------------------------------------"
echo "Nginx config test:"
sudo nginx -t
echo ""
echo "Sites enabled:"
ls -la /etc/nginx/sites-enabled/
echo ""
echo "SIMS config content (first 20 lines):"
sudo head -20 /etc/nginx/sites-available/sims 2>/dev/null || echo "Config file not found"
echo ""

# 4. Check network and ports
echo "4. 🌐 NETWORK & PORTS CHECK"
echo "----------------------------------------"
echo "Port 80 status:"
ss -tulpn | grep :80
echo ""
echo "Server listening status:"
ss -tulpn | grep :80
echo ""

# 5. Check logs for errors
echo "5. 📋 LOG FILES CHECK"
echo "----------------------------------------"
echo "Last 10 lines of Nginx error log:"
sudo tail -10 /var/log/nginx/error.log 2>/dev/null || echo "No nginx error log"
echo ""
echo "Last 10 lines of SIMS error log:"
sudo tail -10 /var/log/nginx/sims_error.log 2>/dev/null || echo "No sims error log"
echo ""
echo "Last 10 lines of SIMS service log:"
sudo journalctl -u sims -n 10 --no-pager 2>/dev/null || echo "No sims service log"
echo ""

# 6. Check Django setup
echo "6. 🐍 DJANGO SETUP CHECK"
echo "----------------------------------------"
cd /opt/sims_project
echo "Current directory: $(pwd)"
echo "Django manage.py check:"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    python manage.py check 2>&1 || echo "Django check failed"
else
    echo "Virtual environment not found"
fi
echo ""

# 7. Check socket file
echo "7. 🔌 SOCKET FILE CHECK"
echo "----------------------------------------"
echo "Looking for Gunicorn socket:"
ls -la /opt/sims_project/ | grep sock
ls -la /opt/sims_project/*.sock 2>/dev/null || echo "No socket file found"
echo ""

# 8. Check firewall
echo "8. 🛡️  FIREWALL CHECK"
echo "----------------------------------------"
echo "UFW status:"
sudo ufw status 2>/dev/null || echo "UFW not available"
echo ""
echo "iptables rules (HTTP):"
sudo iptables -L | grep -i http 2>/dev/null || echo "No HTTP rules found"
echo ""

# 9. Quick fix suggestions
echo "9. 🔧 QUICK FIX SUGGESTIONS"
echo "----------------------------------------"
echo "To fix common 403 issues, try these commands:"
echo "sudo chown -R www-data:www-data /opt/sims_project"
echo "sudo chmod -R 755 /opt/sims_project"
echo "sudo systemctl restart sims"
echo "sudo systemctl restart nginx"
echo ""

echo "=========================================================="
echo "🎯 DIAGNOSTIC COMPLETE"
echo "Share this output for analysis and solutions!"
echo "=========================================================="
