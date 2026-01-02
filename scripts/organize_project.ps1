# SIMS Project Organization Script
Write-Host "🗂️ Organizing SIMS Project Structure..." -ForegroundColor Green

$projectRoot = "d:\PMC\sims_project-1"
$folders = @{
    'docs' = @('*.md', 'File Tree')
    'tests' = @('test_*.py', 'verify_*.py', 'validate_*.py', 'diagnose_*.py', 'quick_*.py', 'simple_*.py', 'final_*.py', 'django_verification.py', 'login_system_verification.py', 'run_verification.py', 'url_test.py', 'system_health_check.py')
    'scripts' = @('*.ps1', '*.bat')
    'deployment' = @('*.conf', '*.service', '*.sh', 'gunicorn.conf.py', 'server_config.env', 'deployment_fix.py')
    'utils' = @('create_*.py')
}

# Create folders if they don't exist
foreach ($folderName in $folders.Keys) {
    $folderPath = Join-Path $projectRoot $folderName
    if (!(Test-Path $folderPath)) {
        New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
        Write-Host "✅ Created folder: $folderName" -ForegroundColor Yellow
    }
}

# Move files to appropriate folders
foreach ($folderName in $folders.Keys) {
    $folderPath = Join-Path $projectRoot $folderName
    $patterns = $folders[$folderName]
    
    foreach ($pattern in $patterns) {
        $files = Get-ChildItem -Path $projectRoot -Name $pattern -File 2>$null
        foreach ($file in $files) {
            $sourcePath = Join-Path $projectRoot $file
            $destPath = Join-Path $folderPath $file
            
            if (Test-Path $sourcePath) {
                try {
                    Move-Item $sourcePath $destPath -Force
                    Write-Host "📁 Moved $file → $folderName/" -ForegroundColor Cyan
                } catch {
                    Write-Host "❌ Failed to move $file : $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        }
    }
}

Write-Host "🎉 Project organization complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📂 New Project Structure:" -ForegroundColor Yellow
Write-Host "├── 📁 docs/         (Documentation)" -ForegroundColor White
Write-Host "├── 📁 tests/        (Tests & Verification)" -ForegroundColor White
Write-Host "├── 📁 scripts/      (Utility Scripts)" -ForegroundColor White
Write-Host "├── 📁 deployment/   (Deployment Configs)" -ForegroundColor White
Write-Host "├── 📁 utils/        (Admin Utilities)" -ForegroundColor White
Write-Host "├── 📁 sims/         (Django App)" -ForegroundColor White
Write-Host "├── 📁 templates/    (Django Templates)" -ForegroundColor White
Write-Host "├── 📁 static/       (Static Files)" -ForegroundColor White
Write-Host "└── 📄 manage.py     (Django Management)" -ForegroundColor White
