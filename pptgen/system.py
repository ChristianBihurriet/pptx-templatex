"""Small cross-platform integrations used by the interactive CLI."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .errors import ContentError


def open_path(path: Path) -> None:
    target = Path(path).resolve()
    if not target.exists():
        raise ContentError(f"No existe '{target}'.")
    if sys.platform == "win32":
        os.startfile(target)  # type: ignore[attr-defined]
        return
    command = "open" if sys.platform == "darwin" else "xdg-open"
    executable = shutil.which(command)
    if executable is None:
        raise ContentError(f"No se encontró el comando '{command}' para abrir '{target}'.")
    try:
        subprocess.Popen([executable, str(target)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError as exc:
        raise ContentError(f"No se pudo abrir '{target}': {exc}") from exc
