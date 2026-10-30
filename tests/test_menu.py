"""Interactive menu and automatic content discovery."""

import json

from pptx import Presentation

from pptgen.cli import main
from pptgen.discovery import discover_contents
from pptgen.menu import run_menu


def lesson(title="Clase"):
    return {
        "titulo": title,
        "modulo": "Programación",
        "curso": "1DAM",
        "diapositivas": [{"tipo": "portada", "titulo": title}],
    }


def reader(*answers):
    values = iter(answers)
    return lambda _prompt: next(values)


def test_discovery_is_recursive_and_keeps_invalid_json_visible(tmp_path):
    root = tmp_path / "contenidos"
    (root / "programacion").mkdir(parents=True)
    (root / "bd").mkdir()
    (root / "programacion/clase.json").write_text(json.dumps(lesson("Colecciones")), encoding="utf-8")
    (root / "bd/roto.json").write_text("{", encoding="utf-8")

    entries = discover_contents(root)

    assert [entry.relative.as_posix() for entry in entries] == ["bd/roto.json", "programacion/clase.json"]
    assert entries[0].error
    assert entries[1].title == "Colecciones"
    assert entries[1].slide_count == 1


def test_interactive_menu_validates_all_contents(tmp_path, monkeypatch):
    root = tmp_path / "contenidos/programacion"
    root.mkdir(parents=True)
    (root / "uno.json").write_text(json.dumps(lesson("Uno")), encoding="utf-8")
    (root / "dos.json").write_text(json.dumps(lesson("Dos")), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    output = []

    assert run_menu(reader("2", "a", "", "0"), output.append) == 0

    text = "\n".join(output)
    assert "uno.json: 1 diapositivas" in text
    assert "dos.json: 1 diapositivas" in text
    assert "Resultado: 2 válidos y 0 con errores" in text
    assert text.endswith("Hasta pronto.")


def test_interactive_menu_generates_selected_content(tmp_path, monkeypatch):
    root = tmp_path / "contenidos/programacion"
    root.mkdir(parents=True)
    (root / "clase.json").write_text(json.dumps(lesson("Colecciones")), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    output = []

    answers = reader("1", "1", "", "salida", "Colecciones Java", "n", "0")
    assert run_menu(answers, output.append) == 0

    result = tmp_path / "salida/Colecciones Java.pptx"
    assert result.is_file()
    assert len(Presentation(result).slides) == 1
    assert "Presentación creada" in "\n".join(output)


def test_interactive_menu_regenerates_theme_documentation(tmp_path, monkeypatch):
    (tmp_path / "contenidos").mkdir()
    monkeypatch.chdir(tmp_path)
    output = []

    answers = reader("4", "3", "", "prompts", "0", "0")
    assert run_menu(answers, output.append) == 0

    assert (tmp_path / "prompts/tipos_dam_oscuro.md").is_file()
    assert (tmp_path / "prompts/tipos_dam_oscuro.json").is_file()


def test_direct_batch_validation_and_empty_arguments_open_menu(tmp_path, monkeypatch):
    root = tmp_path / "contenidos/programacion"
    root.mkdir(parents=True)
    (root / "clase.json").write_text(json.dumps(lesson()), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert main(["--validar-todos"]) == 0
    monkeypatch.setattr("pptgen.cli.run_menu", lambda: 27)
    assert main([]) == 27


def test_direct_batch_generation_uses_each_json_name(tmp_path, monkeypatch):
    root = tmp_path / "contenidos/programacion"
    root.mkdir(parents=True)
    (root / "uno.json").write_text(json.dumps(lesson("Uno")), encoding="utf-8")
    (root / "dos.json").write_text(json.dumps(lesson("Dos")), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert main(["--generar-todos", "--salida", "presentaciones"]) == 0
    assert (tmp_path / "presentaciones/uno.pptx").is_file()
    assert (tmp_path / "presentaciones/dos.pptx").is_file()
