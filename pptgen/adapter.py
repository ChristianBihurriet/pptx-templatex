"""Convert the teaching JSON into the original engine configuration."""

import re

from .errors import ContentError
from .metadata import RESERVED
from .themes import Theme

CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\ud800-\udfff\ufffe\uffff]")
IMAGE_MARKER = re.compile(r"\{\{\s*img:[\w.\-\[\]]+\s*\}\}")


def _text(value, where, required=False):
    if not isinstance(value, str):
        raise ContentError(f"{where}: debe ser texto.")
    if required and not value.strip():
        raise ContentError(f"{where}: es obligatorio y no puede estar vacío.")
    if CONTROL.search(value):
        raise ContentError(
            f"{where}: contiene caracteres de control o XML no admitidos; usa saltos de línea y tabuladores."
        )
    if IMAGE_MARKER.search(value):
        raise ContentError(f"{where}: la sintaxis '{{{{ img:clave }}}}' está reservada por el motor para imágenes.")
    if RESERVED in value:
        raise ContentError(f"{where}: el identificador {RESERVED} está reservado para metadatos internos.")
    return value


def adapt_content(content: dict, theme: Theme) -> dict:
    """Validate all data before returning a src_page/replace_texts configuration."""
    if not isinstance(content, dict):
        raise ContentError("El documento debe ser un objeto JSON.")
    unknown = content.keys() - {"titulo", "modulo", "curso", "diapositivas"}
    if unknown:
        raise ContentError(f"Documento: campos desconocidos: {', '.join(sorted(unknown))}.")
    title = _text(content.get("titulo"), "Documento, campo 'titulo'", required=True)
    metadata = {"titulo_clase": title}
    for key in ("modulo", "curso"):
        metadata[key] = _text(content.get(key, ""), f"Documento, campo '{key}'")
    slides = content.get("diapositivas")
    if not isinstance(slides, list) or not slides:
        raise ContentError("Documento, campo 'diapositivas': debe ser una lista no vacía.")
    result = []
    for index, slide in enumerate(slides, start=1):
        where = f"Diapositiva {index}"
        if not isinstance(slide, dict):
            raise ContentError(f"{where}: debe ser un objeto.")
        kind = slide.get("tipo")
        if not isinstance(kind, str) or kind not in theme.types:
            raise ContentError(
                f"{where}, campo 'tipo': {kind!r} desconocido. Disponibles: {', '.join(theme.types)}."
            )
        spec = theme.types[kind]
        unknown = slide.keys() - ({"tipo"} | spec["campos"].keys())
        if unknown:
            raise ContentError(f"{where} ({kind}): campos desconocidos: {', '.join(sorted(unknown))}.")
        replacements = dict(metadata)
        for field, rule in spec["campos"].items():
            location = f"{where} ({kind}), campo '{field}'"
            required = rule.get("obligatorio", False)
            if required and field not in slide:
                raise ContentError(f"{location}: es obligatorio.")
            value = _text(slide.get(field, ""), location, required)
            if len(value) > rule.get("max_caracteres", float("inf")):
                raise ContentError(f"{location}: supera {rule['max_caracteres']} caracteres; divide el contenido.")
            if len(value.split("\n")) > rule.get("max_lineas", float("inf")):
                raise ContentError(f"{location}: supera {rule['max_lineas']} líneas; divide el contenido.")
            replacements[rule["marcador"]] = value
        result.append({"src_page": spec["pagina"], "replace_texts": replacements})
    return {"slides": result}
