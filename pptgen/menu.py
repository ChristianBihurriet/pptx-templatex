"""Dependency-free interactive menu for the normal teaching workflow."""

from collections.abc import Callable
from pathlib import Path

from pptx_templatex import TemplateError

from .adapter import adapt_content
from .catalog import write_catalog
from .discovery import ContentInfo, discover_contents, find_content_root
from .errors import ContentError
from .generator import generate
from .json_io import read_json
from .system import open_path
from .themes import available_themes, load_theme

Reader = Callable[[str], str]
Writer = Callable[[str], None]


class MenuExit(Exception):
    pass


def _read(reader: Reader, prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    try:
        value = reader(f"{prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt) as exc:
        raise MenuExit from exc
    return value or (default or "")


def _yes(reader: Reader, prompt: str) -> bool:
    return _read(reader, f"{prompt} [s/N]").casefold() in {"s", "si", "sí", "y", "yes"}


def _show_contents(entries: list[ContentInfo], write: Writer, allow_all: bool, controls: bool = True) -> None:
    write("\nContenidos disponibles:\n")
    for index, entry in enumerate(entries, 1):
        group = entry.relative.parent.as_posix() if entry.relative.parent != Path(".") else "general"
        status = " · JSON ilegible" if entry.error else f" · {entry.slide_count} diapositivas"
        write(f"  {index}. [{group}] {entry.title}")
        write(f"     {entry.relative.as_posix()}{status}")
    if controls:
        if allow_all:
            write("\n  A. Todos los contenidos")
        write("  R. Recargar listado")
        write("  0. Volver")


def _select_contents(reader: Reader, write: Writer, allow_all: bool = True) -> list[ContentInfo] | None:
    while True:
        entries = discover_contents()
        if not entries:
            write("\nNo se encontraron archivos JSON dentro de 'contenidos/'.")
            return None
        _show_contents(entries, write, allow_all)
        choice = _read(reader, "Opción").casefold()
        if choice == "0":
            return None
        if choice == "r":
            continue
        if allow_all and choice == "a":
            return entries
        if choice.isdigit() and 1 <= int(choice) <= len(entries):
            return [entries[int(choice) - 1]]
        write("Opción no válida.")


def _select_theme(reader: Reader, write: Writer):
    names = available_themes()
    if not names:
        raise ContentError("No hay temas disponibles.")
    write("\nTemas disponibles:")
    for index, name in enumerate(names, 1):
        write(f"  {index}. {name}")
    default = "dam_oscuro" if "dam_oscuro" in names else names[0]
    choice = _read(reader, "Tema (número o nombre)", default)
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        choice = names[int(choice) - 1]
    if choice not in names:
        raise ContentError(f"Tema '{choice}' inexistente.")
    return load_theme(choice)


def _validate(reader: Reader, write: Writer) -> None:
    selected = _select_contents(reader, write)
    if not selected:
        return
    theme = _select_theme(reader, write)
    valid = 0
    errors = []
    write("")
    for entry in selected:
        try:
            content = read_json(entry.path)
            config = adapt_content(content, theme)
            valid += 1
            write(f"✓ {entry.relative.as_posix()}: {len(config['slides'])} diapositivas")
        except (ContentError, TemplateError, OSError) as exc:
            errors.append((entry, exc))
            write(f"✗ {entry.relative.as_posix()}: {exc}")
    write(f"\nResultado: {valid} válidos y {len(errors)} con errores.")


def _generate(reader: Reader, write: Writer) -> None:
    selected = _select_contents(reader, write)
    if not selected:
        return
    theme = _select_theme(reader, write)
    output_dir = Path(_read(reader, "Directorio de salida", "salida"))
    batch = len(selected) > 1
    if batch and not _yes(reader, f"Se intentarán generar {len(selected)} presentaciones. ¿Continuar?"):
        write("Operación cancelada.")
        return
    explicit_name = None if batch else _read(reader, "Nombre del PPTX", selected[0].path.stem)
    generated = []
    errors = []
    write("")
    for entry in selected:
        try:
            name = entry.path.stem if batch else explicit_name
            output = generate(read_json(entry.path), theme, name, output_dir)
            generated.append(output)
            write(f"✓ Presentación creada: {output}")
        except (ContentError, TemplateError, OSError) as exc:
            errors.append((entry, exc))
            write(f"✗ {entry.relative.as_posix()}: {exc}")
    write(f"\nResultado: {len(generated)} generadas y {len(errors)} con errores.")
    if len(generated) == 1 and _yes(reader, "¿Abrir la presentación?"):
        open_path(generated[0])
    elif len(generated) > 1 and _yes(reader, "¿Abrir la carpeta de salida?"):
        open_path(output_dir)


def _inspect_contents(reader: Reader, write: Writer) -> None:
    entries = discover_contents()
    if not entries:
        write("No se encontraron contenidos.")
        return
    _show_contents(entries, write, allow_all=False, controls=False)
    _read(reader, "Pulsa Intro para volver")


def _show_types(theme, write: Writer) -> None:
    write(f"\nTipos del tema '{theme.name}':")
    for index, (kind, spec) in enumerate(theme.types.items(), 1):
        fields = ", ".join(f"{name}{'*' if rule.get('obligatorio') else ''}" for name, rule in spec["campos"].items())
        write(f"  {index}. {kind}: {fields}")
    write("* Campo obligatorio; los demás son opcionales.")


def _themes_menu(reader: Reader, write: Writer) -> None:
    while True:
        write(
            "\nGESTIONAR TEMAS Y DOCUMENTACIÓN\n\n"
            "1. Listar temas\n"
            "2. Consultar tipos y campos\n"
            "3. Regenerar documentación de un tema\n"
            "4. Validar una plantilla\n"
            "0. Volver"
        )
        choice = _read(reader, "Opción")
        if choice == "0":
            return
        if choice == "1":
            names = available_themes()
            write("\n" + ("\n".join(f"- {name}" for name in names) or "No hay temas disponibles."))
        elif choice == "2":
            _show_types(_select_theme(reader, write), write)
        elif choice == "3":
            theme = _select_theme(reader, write)
            output_dir = Path(_read(reader, "Directorio de documentación", "prompts"))
            targets = [output_dir / f"tipos_{theme.name}.md", output_dir / f"tipos_{theme.name}.json"]
            existing = [path for path in targets if path.exists()]
            if existing and not _yes(reader, "La documentación existente será reemplazada. ¿Continuar?"):
                write("Operación cancelada.")
                continue
            for path in write_catalog(theme, output_dir):
                write(f"✓ Catálogo generado: {path}")
        elif choice == "4":
            theme = _select_theme(reader, write)
            write(f"✓ Plantilla válida: {theme.template} ({len(theme.types)} tipos)")
        else:
            write("Opción no válida.")


def run_menu(reader: Reader = input, write: Writer = print) -> int:
    """Run until the user exits; errors return to the main menu."""
    try:
        while True:
            write(
                "\nPPTGEN — Presentaciones docentes\n\n"
                "1. Generar presentaciones\n"
                "2. Validar contenidos\n"
                "3. Consultar contenidos\n"
                "4. Gestionar temas y documentación\n"
                "5. Abrir carpeta de salida\n"
                "0. Salir"
            )
            choice = _read(reader, "Opción")
            try:
                if choice == "0":
                    write("\nHasta pronto.")
                    return 0
                if choice == "1":
                    _generate(reader, write)
                elif choice == "2":
                    _validate(reader, write)
                elif choice == "3":
                    _inspect_contents(reader, write)
                elif choice == "4":
                    _themes_menu(reader, write)
                elif choice == "5":
                    root = find_content_root()
                    base = root.parent if root is not None else Path.cwd()
                    open_path(base / "salida")
                else:
                    write("Opción no válida.")
            except (ContentError, TemplateError, OSError) as exc:
                write(f"Error: {exc}")
    except MenuExit:
        write("\nHasta pronto.")
        return 0
