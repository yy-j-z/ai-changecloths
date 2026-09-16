$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root '.venv/Scripts/python.exe'

if (-not (Test-Path $python)) {
    throw 'Missing .venv. Run scripts/setup.ps1 first.'
}

Push-Location $root
try {
    npm run check:web
    & $python -m ruff check server ai-service
    & $python -m ruff format --check server ai-service

    Push-Location 'server'
    try { & $python -m pytest -q } finally { Pop-Location }

    Push-Location 'ai-service'
    try { & $python -m pytest -q } finally { Pop-Location }
} finally {
    Pop-Location
}

