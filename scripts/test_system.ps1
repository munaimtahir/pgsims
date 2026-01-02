# PowerShell script to test SIMS system components
Write-Host "SIMS System Verification - PowerShell Edition" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Test 1: Check if server is running
Write-Host "`nTesting server accessibility..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Server is running and accessible" -ForegroundColor Green
    } else {
        Write-Host "❌ Server returned status code: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Server is not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Check Django admin
Write-Host "`nTesting Django admin..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/admin/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Django admin is accessible" -ForegroundColor Green
    } else {
        Write-Host "❌ Django admin returned status code: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Django admin is not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Check user dashboard
Write-Host "`nTesting user dashboard..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/users/dashboard/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ User dashboard is accessible" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ User dashboard returned status code: $($response.StatusCode) (might require login)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ℹ️ User dashboard requires authentication: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test 4: Check login page
Write-Host "`nTesting login page..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/accounts/login/" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Login page is accessible" -ForegroundColor Green
    } else {
        Write-Host "❌ Login page returned status code: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Login page is not accessible: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Check static files
Write-Host "`nTesting static files..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/static/" -TimeoutSec 10 -UseBasicParsing
    Write-Host "ℹ️ Static files directory status: $($response.StatusCode)" -ForegroundColor Yellow
} catch {
    Write-Host "ℹ️ Static files handling: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test 6: Check file existence
Write-Host "`nChecking critical files..." -ForegroundColor Yellow

$criticalFiles = @(
    "manage.py",
    "db.sqlite3",
    "sims_project\settings.py",
    "templates\base\base.html",
    "templates\registration\login.html",
    "templates\users\admin_dashboard.html"
)

foreach ($file in $criticalFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
    }
}

Write-Host "`n=================================================" -ForegroundColor Green
Write-Host "System verification complete!" -ForegroundColor Green
Write-Host "Server should be accessible at: http://127.0.0.1:8000" -ForegroundColor Cyan
