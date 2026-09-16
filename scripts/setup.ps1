$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$venv = Join-Path $root '.venv'
$python = Join-Path $venv 'Scripts/python.exe'
$env:UV_CACHE_DIR = Join-Path $root '.uv-cache'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $root '.uv-python'

if (-not (Test-Path $python)) {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        & uv venv --python 3.11 $venv
        if ($LASTEXITCODE -ne 0) { throw 'uv failed to create the Python environment.' }
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3.11 -m venv $venv
        if ($LASTEXITCODE -ne 0) { throw 'py failed to create the Python environment.' }
    } else {
        $version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ($version -ne '3.11') {
            throw "Python 3.11 is required; found Python $version. Install Python 3.11 or uv."
        }
        & python -m venv $venv
        if ($LASTEXITCODE -ne 0) { throw 'python failed to create the Python environment.' }
    }
}

$venvVersion = & $python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($venvVersion -ne '3.11') {
    throw "The existing .venv uses Python $venvVersion. Remove it and rerun setup with Python 3.11."
}

& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $root 'requirements-dev.txt')
& $python -m pip install -r (Join-Path $root 'server/requirements.txt')
& $python -m pip install -r (Join-Path $root 'ai-service/requirements.txt')

Push-Location $root
try {
    npm install
} finally {
    Pop-Location
}

Write-Host 'Environment ready. Run scripts/check.ps1 to verify it.'
