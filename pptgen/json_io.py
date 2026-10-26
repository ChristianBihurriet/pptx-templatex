"""Read JSON without silently accepting duplicate keys or nonstandard values."""

import json
from pathlib import Path

from .errors import ContentError


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContentError(f"Clave JSON duplicada: '{key}'.")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ContentError(f"Constante JSON no válida: {value}.")


def parse_json(text: str, where="JSON"):
    try:
        return json.loads(text, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
    except (ContentError, json.JSONDecodeError) as exc:
        raise ContentError(f"{where}: {exc}") from exc


def read_json(path: Path):
    try:
        return parse_json(Path(path).read_text(encoding="utf-8-sig"), f"JSON '{path}'")
    except (OSError, UnicodeError) as exc:
        raise ContentError(f"No se puede leer JSON '{path}': {exc}") from exc
