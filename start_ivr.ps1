param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $root "frontend"
$venvPython = Join-Path $root "venv\Scripts\python.exe"
$requirements = Join-Path $root "backend\requirements.txt"

if (-not (Test-Path $venvPython)) {
    Write-Host "Virtual environment python executable not found:" -ForegroundColor Red
    Write-Host "  $venvPython" -ForegroundColor Yellow
    Write-Host "Create the venv first, then run this script again." -ForegroundColor Yellow
    exit 1
}

Set-Location $root

if (-not $SkipInstall) {
    Write-Host "Installing/updating backend dependencies..." -ForegroundColor Cyan
    & $venvPython -m pip install -r $requirements
}

$escapedRoot = $root.Replace("'", "''")
$escapedFrontendDir = $frontendDir.Replace("'", "''")
$escapedPython = $venvPython.Replace("'", "''")

$backendCommand = "Set-Location '$escapedRoot'; & '$escapedPython' -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"
$frontendCommand = "Set-Location '$escapedFrontendDir'; & '$escapedPython' -m http.server 5500"

Write-Host "Starting backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand | Out-Null

Write-Host "Starting frontend on http://127.0.0.1:5500 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand | Out-Null

Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5500"

Write-Host "IVR app launched." -ForegroundColor Green
Write-Host "Tip: run .\start_ivr.ps1 -SkipInstall for faster subsequent starts." -ForegroundColor DarkCyan
