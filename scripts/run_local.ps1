$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

Write-Host "Bypassing execution policy for this PowerShell process..."
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

& "$repoRoot\.venv\Scripts\Activate.ps1"
python -m pip install -e ".[dev]"
python scripts/build_recommender.py

function Get-FreePort {
    param(
        [int]$StartPort = 8001,
        [int]$Limit = 100
    )

    $port = $StartPort
    for ($i = 0; $i -lt $Limit; $i++) {
        $inUse = $false
        try {
            $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $port)
            $listener.Start()
            $listener.Stop()
        }
        catch {
            $inUse = $true
        }

        if (-not $inUse) {
            return $port
        }

        $port++
    }

    throw "No free port found in the requested range."
}

$apiPort = Get-FreePort -StartPort 8001
$uiPort = Get-FreePort -StartPort 8501

Write-Host "Starting API on http://127.0.0.1:$apiPort"
Write-Host "Starting Streamlit UI on http://127.0.0.1:$uiPort"

$apiProcess = Start-Process powershell -ArgumentList "-NoExit","-Command","Set-Location '$repoRoot'; & '$repoRoot\.venv\Scripts\Activate.ps1'; python -m uvicorn netflix_recommender.api.main:app --host 127.0.0.1 --port $apiPort" -PassThru
$uiProcess = Start-Process powershell -ArgumentList "-NoExit","-Command","Set-Location '$repoRoot'; & '$repoRoot\.venv\Scripts\Activate.ps1'; python -m streamlit run app/streamlit_app.py --server.port $uiPort --server.headless true" -PassThru

Write-Host "API PID: $($apiProcess.Id)"
Write-Host "UI PID: $($uiProcess.Id)"
Write-Host "Use Ctrl+C in each terminal window to stop the services."
