"""One-time bridge for old themes; never a runtime source of contracts.

Reads a legacy tema.json and lesson examples, writes a NEW annotated PPTX.
Then remove tipos from tema.json (or remove the file for plantilla.pptx).
"""

import argparse
from pathlib import Path

from pptx import Presentation

from pptgen.errors import ContentError
from pptgen.json_io import read_json
from pptgen.metadata import format_notes, split_notes
from pptgen.themes import load_template


def migrate(directory, examples, destination):
    directory, destination = Path(directory), Path(destination)
    config = read_json(directory / "tema.json")
    presentation = Presentation(str(directory / config["plantilla"]))
    samples = read_json(examples)["diapositivas"]
    purposes = {
        "portada": "Presentar el tema y orientar al alumnado al comienzo de la clase.",
        "pregunta": "Plantear un problema cercano para construir intuición antes de la teoría.",
        "definicion": "Explicar un concepto y relacionarlo con un problema o ejemplo práctico.",
        "codigo": "Mostrar código legible y explicar su comportamiento sin ejecutarlo automáticamente.",
    }
    for kind, spec in config["tipos"].items():
        slide = presentation.slides[spec["pagina"] - 1]
        frame = slide.notes_slide.notes_text_frame
        if frame is None:
            raise ContentError(f"Tipo '{kind}': falta el cuerpo de notas.")
        previous, human = split_notes(frame.text)
        if previous:
            raise ContentError(f"Tipo '{kind}': ya tiene metadatos; no se sobrescriben.")
        sample = next((s for s in samples if s.get("tipo") == kind), None)
        if sample is None:
            raise ContentError(f"Falta un ejemplo para '{kind}'.")
        contract = {
            "metadatos_version": 1, "contrato_version": 1, "tipo": kind,
            "proposito": purposes.get(kind, f"Apoyar la explicación docente mediante {kind}."),
            "campos": {name: {**rule, "tipo_dato": "string", "descripcion": f"Texto del campo {name}."}
                       for name, rule in spec["campos"].items()},
            "ejemplo": sample,
            "restricciones": ["Texto literal; sin Markdown.", "Diseño fijo; revisar el ajuste visual en PowerPoint."],
        }
        frame.text = format_notes(contract, human)
    if destination.exists():
        raise ContentError(f"El archivo '{destination}' ya existe.")
    presentation.save(str(destination))
    migrated = load_template(destination, directory.name)
    if migrated.types != config["tipos"]:
        raise ContentError("La migración no conserva exactamente los contratos originales.")
    return migrated


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directorio", type=Path)
    parser.add_argument("ejemplos", type=Path)
    parser.add_argument("destino", type=Path)
    args = parser.parse_args()
    theme = migrate(args.directorio, args.ejemplos, args.destino)
    print(f"Migrados {len(theme.types)} tipos sin cambiar sus contratos: {args.destino}")
