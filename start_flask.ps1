$ErrorActionPreference = 'Stop'

Set-Location $PSScriptRoot

$pythonExe = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $pythonExe)) {
    throw "Python da virtualenv não encontrado em $pythonExe"
}

$oldProcesses = Get-CimInstance Win32_Process |
    Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'FinanceTrack' -and $_.CommandLine -match 'app\.py' }

foreach ($process in $oldProcesses) {
    Stop-Process -Id $process.ProcessId -Force
}

$env:FLASK_DEBUG = 'true'
& $pythonExe app.py
