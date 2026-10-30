"""Spanish CLI for local lesson generation."""

import argparse
import sys
from pathlib import Path

from pptx_templatex import TemplateError

from .adapter import adapt_content
from .catalog import write_catalog
from .discovery import discover_contents
from .errors import ContentError
from .generator import generate
from .json_io import read_json
from .menu import run_menu
from .themes import available_themes, load_theme


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        return run_menu()
    parser = argparse.ArgumentParser(description="Genera presentaciones docentes localmente desde JSON.")
    parser.add_argument("contenido", nargs="?", type=Path, help="Archivo JSON de contenido")
    parser.add_argument("--tema", default="dam_oscuro", help="Tema visual (por defecto: dam_oscuro)")
    parser.add_argument("--nombre", help="Nombre del PPTX sin extensión (por defecto: nombre del JSON)")
    parser.add_argument("--salida", type=Path, default=Path("salida"), help="Directorio de destino")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--validar", action="store_true", help="Valida contenido y tema sin crear archivos")
    actions.add_argument("--listar-temas", action="store_true", help="Lista los temas disponibles")
    actions.add_argument("--listar-tipos", action="store_true", help="Lista los tipos del tema seleccionado")
    actions.add_argument("--validar-todos", action="store_true", help="Valida todos los JSON de contenidos/")
    actions.add_argument("--generar-todos", action="store_true", help="Genera todos los JSON válidos de contenidos/")
    actions.add_argument(
        "--documentar-tipos", action="store_true", help="Genera catálogos Markdown y JSON desde el PPTX"
    )
    args = parser.parse_args(arguments)
    if (args.validar_todos or args.generar_todos) and args.contenido is not None:
        parser.error("no combines un contenido concreto con una operación sobre todos los contenidos")
    if args.generar_todos and args.nombre is not None:
        parser.error("--nombre no se puede usar con --generar-todos")
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
        if args.validar_todos or args.generar_todos:
            entries = discover_contents()
            if not entries:
                raise ContentError("No se encontraron archivos JSON dentro de 'contenidos/'.")
            successes = 0
            failures = 0
            for entry in entries:
                try:
                    content = read_json(entry.path)
                    if args.validar_todos:
                        config = adapt_content(content, theme)
                        print(f"VÁLIDO {entry.relative.as_posix()}: {len(config['slides'])} diapositivas")
                    else:
                        output = generate(content, theme, entry.path.stem, args.salida)
                        print(f"GENERADO {entry.relative.as_posix()}: {output}")
                    successes += 1
                except (ContentError, TemplateError, OSError) as exc:
                    failures += 1
                    print(f"ERROR {entry.relative.as_posix()}: {exc}", file=sys.stderr)
            action = "válidos" if args.validar_todos else "generados"
            print(f"Resultado: {successes} {action} y {failures} con errores.")
            return 1 if failures else 0
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
