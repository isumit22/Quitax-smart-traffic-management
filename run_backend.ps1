@echo off
Write-Host "Activating virtual environment and starting backend..."
if (Test-Path -Path .venv\Scripts\Activate.ps1) {
    . .venv\Scripts\Activate.ps1
}
python backend\app.py