# SIMS Server 403 Diagnostic Helper Script
# This script helps you run diagnostics on your remote server

param(
    [string]$ServerUser = "user",
    [string]$ServerIP = "172.236.152.35"
)

Write-Host "🔍 SIMS Server 403 Forbidden Diagnostic Helper" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if SSH is available
try {
    ssh -V | Out-Null
    Write-Host "✅ SSH client is available" -ForegroundColor Green
} catch {
    Write-Host "❌ SSH client not found. Please install OpenSSH or use PuTTY." -ForegroundColor Red
    exit 1
}

Write-Host "Server: $ServerIP" -ForegroundColor Yellow
Write-Host "User: $ServerUser" -ForegroundColor Yellow
Write-Host ""

Write-Host "📋 Available Actions:" -ForegroundColor Cyan
Write-Host "1. Upload diagnostic script to server"
Write-Host "2. Run diagnostic script on server"
Write-Host "3. Check basic server connectivity"
Write-Host "4. Download server logs for analysis"
Write-Host "5. Run quick fixes on server"
Write-Host ""

$choice = Read-Host "Select an action (1-5)"

switch ($choice) {
    "1" {
        Write-Host "📤 Uploading diagnostic script..." -ForegroundColor Yellow
        if (Test-Path "diagnose_nginx_403.sh") {
            try {
                scp diagnose_nginx_403.sh "${ServerUser}@${ServerIP}:~/"
                Write-Host "✅ Diagnostic script uploaded successfully!" -ForegroundColor Green
                Write-Host "Next step: SSH to your server and run: chmod +x ~/diagnose_nginx_403.sh && ./diagnose_nginx_403.sh"
            } catch {
                Write-Host "❌ Failed to upload script. Check your SSH connection." -ForegroundColor Red
            }
        } else {
            Write-Host "❌ diagnose_nginx_403.sh not found in current directory" -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host "🔍 Running diagnostic script on server..." -ForegroundColor Yellow
        Write-Host "You'll need to enter your SSH password/key" -ForegroundColor Cyan
        ssh "${ServerUser}@${ServerIP}" "chmod +x ~/diagnose_nginx_403.sh && ./diagnose_nginx_403.sh"
    }
    
    "3" {
        Write-Host "🌐 Testing server connectivity..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "SSH Connection Test:" -ForegroundColor Cyan
        ssh "${ServerUser}@${ServerIP}" "echo 'SSH connection successful'; uname -a"
        Write-Host ""
        Write-Host "HTTP Connection Test:" -ForegroundColor Cyan
        try {
            $response = Invoke-WebRequest -Uri "http://$ServerIP" -TimeoutSec 10 -ErrorAction Stop
            Write-Host "✅ HTTP connection successful - Status: $($response.StatusCode)" -ForegroundColor Green
        } catch {
            Write-Host "❌ HTTP connection failed: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    "4" {
        Write-Host "📥 Downloading server logs..." -ForegroundColor Yellow
        $logDir = "server_logs_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        
        Write-Host "Downloading Nginx logs..." -ForegroundColor Cyan
        scp "${ServerUser}@${ServerIP}:/var/log/nginx/error.log" "$logDir/nginx_error.log" 2>$null
        scp "${ServerUser}@${ServerIP}:/var/log/nginx/access.log" "$logDir/nginx_access.log" 2>$null
        scp "${ServerUser}@${ServerIP}:/var/log/nginx/sims_error.log" "$logDir/sims_error.log" 2>$null
        
        Write-Host "✅ Logs downloaded to: $logDir" -ForegroundColor Green
    }
    
    "5" {
        Write-Host "🔧 Running quick fixes on server..." -ForegroundColor Yellow
        Write-Host "This will fix common permission issues" -ForegroundColor Cyan
        
        $commands = @(
            "sudo chown -R www-data:www-data /opt/sims_project",
            "sudo chmod -R 755 /opt/sims_project",
            "sudo systemctl restart sims",
            "sudo systemctl restart nginx",
            "sudo systemctl status nginx --no-pager",
            "sudo systemctl status sims --no-pager"
        )
        
        foreach ($cmd in $commands) {
            Write-Host "Running: $cmd" -ForegroundColor Yellow
            ssh "${ServerUser}@${ServerIP}" $cmd
            Write-Host ""
        }
        
        Write-Host "✅ Quick fixes applied. Try accessing http://$ServerIP again" -ForegroundColor Green
    }
    
    default {
        Write-Host "❌ Invalid choice. Please select 1-5." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📞 Manual SSH Commands:" -ForegroundColor Cyan
Write-Host "ssh ${ServerUser}@${ServerIP}" -ForegroundColor Yellow
Write-Host "Or use your preferred SSH client to connect to $ServerIP" -ForegroundColor Gray
