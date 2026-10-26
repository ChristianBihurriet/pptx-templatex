"""Spanish CLI for local lesson generation."""

import argparse
import sys
from pathlib import Path

from pptx_templatex import TemplateError

from .adapter import adapt_content
from .catalog import write_catalog
from .errors import ContentError
from .generator import generate
from .json_io import read_json
from .themes import available_themes, load_theme


def main(argv=None):
    parser = argparse.ArgumentParser(description="Genera presentaciones docentes localmente desde JSON.")
    parser.add_argument("contenido", nargs="?", type=Path, help="Archivo JSON de contenido")
    parser.add_argument("--tema", default="dam_oscuro", help="Tema visual (por defecto: dam_oscuro)")
    parser.add_argument("--nombre", help="Nombre del PPTX sin extensión (por defecto: nombre del JSON)")
    parser.add_argument("--salida", type=Path, default=Path("salida"), help="Directorio de destino")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--validar", action="store_true", help="Valida contenido y tema sin crear archivos")
    actions.add_argument("--listar-temas", action="store_true", help="Lista los temas disponibles")
    actions.add_argument("--listar-tipos", action="store_true", help="Lista los tipos del tema seleccionado")
    actions.add_argument(
        "--documentar-tipos", action="store_true", help="Genera catálogos Markdown y JSON desde el PPTX"
    )
    args = parser.parse_args(argv)
    try:
        if args.listar_temas:
            print("\n".join(available_themes()) or "No hay temas disponibles.")
            return 0
        theme = load_theme(args.tema)
        if args.documentar_tipos:
            for path in write_catalog(theme, args.salida):
                print(f"Catálogo generado: {path}")
            return 0
        if args.listar_tipos:
            for kind, spec in theme.types.items():
                fields = ", ".join(f"{f}{'*' if r.get('obligatorio') else ''}" for f, r in spec["campos"].items())
                print(f"{kind}: {fields}")
            print("* Campo obligatorio; los demás son opcionales.")
            return 0
        if args.contenido is None:
            parser.error("debes indicar el archivo JSON de contenido")
        content = read_json(args.contenido)
        if args.validar:
            config = adapt_content(content, theme)
            print(f"JSON válido: {len(config['slides'])} diapositivas compatibles con '{theme.name}'.")
        else:
            name = args.nombre if args.nombre is not None else args.contenido.stem
            output = generate(content, theme, name, args.salida)
            print(f"Presentación creada: {output}")
        return 0
    except (ContentError, TemplateError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
