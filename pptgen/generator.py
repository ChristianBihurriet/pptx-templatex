"""Generate editable PowerPoint files locally with the original engine."""

import hashlib
import re
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from pptx_templatex import TemplateEngine

from .adapter import adapt_content
from .errors import ContentError
from .notes import restore_notes, sanitize_template, verify_clean_output
from .themes import Theme, load_template


def generate(content: dict, theme: Theme, name: str, output_dir="salida") -> Path:
    # Reload, so a previously loaded Theme cannot supply stale rules or page numbers.
    current = load_template(theme.template, theme.name)
    config = adapt_content(content, current)
    # Portable filenames: never interpret a title as a path or silently rename it.
    if (
        not isinstance(name, str) or not name.strip() or len(name) > 150
        or re.search(r'[<>:"/\\|?*\x00-\x1f]', name) or name.endswith((".", " "))
        or name.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL"}
        or re.fullmatch(r"(?:COM|LPT)[1-9](?:\..*)?", name, re.IGNORECASE)
    ):
        raise ContentError(
            "Nombre de presentación no válido: usa un nombre de archivo sin rutas (máximo 150 caracteres)."
        )
    destination = Path(output_dir) / f"{name}.pptx"
    if destination.exists():
        raise ContentError(f"El archivo '{destination}' ya existe. Elige otro --nombre o --salida.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".pptgen-", dir=destination.parent) as workspace:
        source = Path(workspace) / "source.pptx"
        sanitized = Path(workspace) / "sanitized.pptx"
        result = Path(workspace) / "result.pptx"
        shutil.copyfile(current.template, source)
        if hashlib.sha256(source.read_bytes()).hexdigest() != current.source_sha256:
            raise ContentError("La plantilla cambió durante la generación; vuelve a intentarlo.")
        human = sanitize_template(source, sanitized)
        TemplateEngine(sanitized, render_rich_text=False).process(config, result)
        restore_notes(result, config, human)
        verify_clean_output(result)
        # Publish only a verified package, without overwriting even in a race.
        try:
            with destination.open("xb") as stream:
                try:
                    with result.open("rb") as checked:
                        shutil.copyfileobj(checked, stream)
                except OSError:
                    stream.close()
                    destination.unlink()
                    raise
        except FileExistsError as exc:
            raise ContentError(f"El archivo '{destination}' ya existe.") from exc
    return destination
