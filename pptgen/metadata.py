"""Versioned contracts stored in presenter notes. No external type registry."""

import json
import re

from .errors import ContentError
from .json_io import parse_json

BEGIN = "[[PPTGEN_METADATA_JSON_V1]]"
END = "[[/PPTGEN_METADATA_JSON_V1]]"
RESERVED = "PPTGEN_METADATA"
IDENTIFIER = re.compile(r"[a-z][a-z0-9_]*\Z")
GLOBAL_MARKERS = {"titulo_clase", "modulo", "curso"}
MARKER = re.compile(r"\{\{\s*([a-z][a-z0-9_]*)\s*\}\}")


def keys(value, allowed, required, where):
    if not isinstance(value, dict):
        raise ContentError(f"{where}: debe ser un objeto.")
    if value.keys() - allowed:
        raise ContentError(f"{where}: campos desconocidos: {', '.join(sorted(value.keys() - allowed))}.")
    if required - value.keys():
        raise ContentError(f"{where}: faltan campos: {', '.join(sorted(required - value.keys()))}.")


def identifier(value, where):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ContentError(f"{where}: identificador no válido; usa [a-z][a-z0-9_]*.")


def description(value, where):
    if not isinstance(value, str) or not value.strip():
        raise ContentError(f"{where}: debe ser texto no vacío.")


def split_notes(text, where="Notas"):
    """Read exactly one recognized block, leaving human text outside untouched."""
    if RESERVED not in text:
        return None, text
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
        raise ContentError(f"{where}: bloque de metadatos incompleto, duplicado o versión de delimitador no admitida.")
    before, rest = text.split(BEGIN)
    payload, after = rest.split(END)
    if RESERVED in before + after:
        raise ContentError(f"{where}: delimitadores de metadatos desconocidos o duplicados.")
    contract = parse_json(payload, where)
    if not isinstance(contract, dict):
        raise ContentError(f"{where}: los metadatos deben ser un objeto JSON.")
    return contract, (before.rstrip() + "\n" + after.lstrip()).strip()


def format_notes(contract, human=""):
    prefix = human.rstrip() + "\n\n" if human.strip() else ""
    return prefix + BEGIN + "\n" + json.dumps(contract, ensure_ascii=False, indent=2) + "\n" + END


def text_frames(shapes):
    for shape in shapes:
        if getattr(shape, "has_text_frame", False):
            yield shape.text_frame
        if getattr(shape, "has_table", False):
            for row in shape.table.rows:
                for cell in row.cells:
                    yield cell.text_frame


def slide_markers(slide, where):
    found = set()
    for shape in slide.shapes:
        if hasattr(shape, "shapes"):
            raise ContentError(f"{where}: desagrupa las formas de la diapositiva.")
    for frame in text_frames(slide.shapes):
        for paragraph in frame.paragraphs:
            text = paragraph.text
            found.update(MARKER.findall(text))
            residue = MARKER.sub("", text)
            if "{{" in residue or "}}" in residue:
                raise ContentError(f"{where}: marcador mal formado o no admitido: {text!r}.")
            if RESERVED in text:
                raise ContentError(f"{where}: los metadatos deben estar en notas, no en el contenido visible.")
    return found


def validate_contract(contract, where):
    required = {"metadatos_version", "contrato_version", "tipo", "proposito", "campos", "ejemplo"}
    keys(contract, required | {"restricciones"}, required, where)
    if type(contract["metadatos_version"]) is not int or contract["metadatos_version"] != 1:
        raise ContentError(f"{where}: metadatos_version debe ser 1.")
    if type(contract["contrato_version"]) is not int or contract["contrato_version"] < 1:
        raise ContentError(f"{where}: contrato_version debe ser un entero positivo.")
    identifier(contract["tipo"], f"{where}, tipo")
    description(contract["proposito"], f"{where}, proposito")
    restrictions = contract.get("restricciones", [])
    if not isinstance(restrictions, list) or any(not isinstance(r, str) or not r.strip() for r in restrictions):
        raise ContentError(f"{where}: restricciones debe ser una lista de textos no vacíos.")
    fields = contract["campos"]
    if not isinstance(fields, dict) or not fields:
        raise ContentError(f"{where}: campos debe ser un objeto no vacío.")
    markers = set(GLOBAL_MARKERS)
    for field, rule in fields.items():
        location = f"{where}, campo '{field}'"
        identifier(field, location)
        if field == "tipo":
            raise ContentError(f"{location}: nombre reservado.")
        keys(rule, {"marcador", "tipo_dato", "obligatorio", "max_caracteres", "max_lineas", "descripcion"},
             {"marcador", "tipo_dato"}, location)
        identifier(rule["marcador"], f"{location}, marcador")
        if rule["marcador"] in markers:
            raise ContentError(f"{location}: marcador duplicado o reservado.")
        markers.add(rule["marcador"])
        if rule["tipo_dato"] != "string":
            raise ContentError(f"{location}: tipo_dato solo admite string.")
        if type(rule.get("obligatorio", False)) is not bool:
            raise ContentError(f"{location}: obligatorio debe ser booleano.")
        for limit in ("max_caracteres", "max_lineas"):
            if limit in rule and (type(rule[limit]) is not int or rule[limit] <= 0):
                raise ContentError(f"{location}: {limit} debe ser un entero positivo.")
        if "descripcion" in rule:
            description(rule["descripcion"], f"{location}, descripcion")
    if not isinstance(contract["ejemplo"], dict) or contract["ejemplo"].get("tipo") != contract["tipo"]:
        raise ContentError(f"{where}: ejemplo debe ser una diapositiva del mismo tipo.")


def extract_contracts(presentation, name):
    contracts = {}
    for page, slide in enumerate(presentation.slides, start=1):
        where = f"Tema '{name}', página {page}"
        contract = None
        if slide.has_notes_slide:
            frame = slide.notes_slide.notes_text_frame
            if frame is None:
                raise ContentError(f"{where}: notas sin marcador de cuerpo; restaura el cuerpo de notas en PowerPoint.")
            contract, _ = split_notes(frame.text, where)
        found = slide_markers(slide, where)
        if contract is None:
            if found:
                raise ContentError(f"{where}: hay marcadores sin contrato en las notas.")
            continue
        validate_contract(contract, where)
        kind = contract["tipo"]
        where += f", tipo '{kind}'"
        if kind in contracts:
            raise ContentError(f"{where}: tipo duplicado; cada tipo debe identificar una única página.")
        declared = {r["marcador"] for r in contract["campos"].values()}
        missing, unknown = declared - found, found - declared - GLOBAL_MARKERS
        if missing or unknown:
            raise ContentError(f"{where}: marcadores ausentes {sorted(missing)}; desconocidos {sorted(unknown)}.")
        contracts[kind] = {**contract, "pagina": page}
    if not contracts:
        raise ContentError(f"Tema '{name}': no contiene tipos documentados en notas.")
    return contracts
