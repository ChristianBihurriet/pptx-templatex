$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectDir

if (Test-Path ".venv/bin/python") {
    throw ".venv pertenece a Linux. Elimínalo o utiliza otro clon."
}

py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -e ".[dev,svg]"
& .\.venv\Scripts\pptgen.exe --listar-temas
& .\.venv\Scripts\python.exe -m pytest -q

Write-Host "Entorno Windows preparado. Actívalo con: .\.venv\Scripts\Activate.ps1"
