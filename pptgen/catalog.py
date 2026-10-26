"""Derived documentation: contracts are always read from the selected PPTX."""

import json
from pathlib import Path


def catalog_data(theme):
    return {"catalogo_version": 1, "tema": theme.name, "origen_sha256": theme.source_sha256,
            "tipos": theme.contracts}


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def catalog_markdown(theme):
    lines = [f"# Tipos docentes: {theme.name}", "", "Generado desde las notas del PPTX; no editar a mano.",
             "", f"Origen SHA-256: `{theme.source_sha256}`", "",
             "## Contrato común", "",
             "Devuelve solo JSON UTF-8. Raíz: `titulo` (texto no vacío), `diapositivas` (lista no vacía); "
             "`modulo` y `curso` son textos opcionales. No se admiten otras claves.", "",
             "Cada diapositiva contiene `tipo` y los campos siguientes. Todos son cadenas, nunca null, objetos "
             "ni listas. Los obligatorios no pueden quedar vacíos. Un opcional omitido equivale a texto vacío.", "",
             "Texto literal: sin Markdown ni HTML; no se ejecuta código. Usa \\n para saltos y espacios para "
             "indentar. No uses controles salvo \\n y \\t, ni la sintaxis reservada {{ img:clave }} ni "
             "PPTGEN_METADATA. No uses claves duplicadas, NaN o Infinity.", "",
             "Los máximos son bloqueantes; cuentan caracteres Unicode y líneas separadas por \\n, "
             "no líneas visuales. Divide el contenido si excede un máximo. "
             "No hay truncado ni paginación automática.", ""]
    for kind, spec in theme.contracts.items():
        lines += [f"## {kind}", "", spec["proposito"], "",
                  f"Versión del contrato: {spec['contrato_version']}. Metadatos: {spec['metadatos_version']}.", "",
                  "| Campo | Tipo | Obligatorio | Caracteres máx. | Líneas máx. | Descripción |",
                  "| --- | --- | --- | --- | --- | --- |"]
        for name, rule in spec["campos"].items():
            values = [name, rule["tipo_dato"], "sí" if rule.get("obligatorio", False) else "no",
                      rule.get("max_caracteres", "sin máximo"), rule.get("max_lineas", "sin máximo"),
                      rule.get("descripcion", "")]
            lines.append("| " + " | ".join(_cell(v) for v in values) + " |")
        example = {"titulo": "Ejemplo de clase", "diapositivas": [spec["ejemplo"]]}
        lines += ["", "Ejemplo válido completo:", "", "```json",
                  json.dumps(example, ensure_ascii=False, indent=2), "```", "",
                  "Capacidades: campos de texto en un diseño fijo; "
                  "sin listas, imágenes variables ni diagramas automáticos."]
        lines += ["", *[f"- {r}" for r in spec.get("restricciones", [])], ""]
    return "\n".join(lines)


def write_catalog(theme, output_dir):
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    markdown = directory / f"tipos_{theme.name}.md"
    data = directory / f"tipos_{theme.name}.json"
    markdown.write_text(catalog_markdown(theme), encoding="utf-8")
    data.write_text(json.dumps(catalog_data(theme), ensure_ascii=False, indent=2), encoding="utf-8")
    return markdown, data
