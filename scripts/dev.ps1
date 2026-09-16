$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv/Scripts/python.exe'

if (-not (Test-Path $python)) {
    throw 'Missing .venv. Run scripts/setup.ps1 first.'
}

Start-Process powershell -WindowStyle Normal -ArgumentList '-NoExit', '-Command', "Set-Location '$root/server'; & '$python' -m uvicorn app.main:app --reload --port 8000"
Start-Process powershell -WindowStyle Normal -ArgumentList '-NoExit', '-Command', "Set-Location '$root/ai-service'; & '$python' -m uvicorn app.main:app --reload --port 8001"
Start-Process powershell -WindowStyle Normal -ArgumentList '-NoExit', '-Command', "Set-Location '$root'; npm run dev:web"

