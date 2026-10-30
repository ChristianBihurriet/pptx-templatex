#!/usr/bin/env sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_dir"

if [ -f .venv/Scripts/python.exe ]; then
    echo "Error: .venv pertenece a Windows. Elimínalo o utiliza otro clon." >&2
    exit 1
fi

python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev,svg]"
.venv/bin/pptgen --listar-temas
.venv/bin/python -m pytest -q

echo "Entorno Ubuntu preparado. Actívalo con: source .venv/bin/activate"
