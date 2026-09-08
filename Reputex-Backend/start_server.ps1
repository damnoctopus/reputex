$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $ScriptDir

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    . ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Host "Warning: .venv not found. Make sure you have created the virtual environment." -ForegroundColor Yellow
}

Write-Host "Starting FastAPI server..." -ForegroundColor Cyan
python -m uvicorn app.main:app --reload
