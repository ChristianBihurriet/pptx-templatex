"""Discover lesson JSON files without maintaining a separate registry."""

from dataclasses import dataclass
from pathlib import Path

from .errors import ContentError
from .json_io import read_json


@dataclass(frozen=True)
class ContentInfo:
    path: Path
    relative: Path
    title: str
    module: str
    course: str
    slide_count: int
    error: str = ""


def find_content_root(start: Path | None = None) -> Path | None:
    """Prefer the current project, then the editable source checkout."""
    candidates = [Path(start or Path.cwd()) / "contenidos", Path(__file__).resolve().parents[1] / "contenidos"]
    seen = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen and resolved.is_dir():
            return resolved
        seen.add(resolved)
    return None


def discover_contents(root: Path | None = None) -> list[ContentInfo]:
    directory = Path(root).resolve() if root is not None else find_content_root()
    if directory is None or not directory.is_dir():
        return []
    entries = []
    for path in sorted(directory.rglob("*.json"), key=lambda item: str(item).casefold()):
        relative = path.relative_to(directory)
        try:
            content = read_json(path)
            if not isinstance(content, dict):
                raise ContentError("la raíz debe ser un objeto")
            slides = content.get("diapositivas", [])
            entries.append(
                ContentInfo(
                    path=path,
                    relative=relative,
                    title=str(content.get("titulo") or path.stem),
                    module=str(content.get("modulo") or ""),
                    course=str(content.get("curso") or ""),
                    slide_count=len(slides) if isinstance(slides, list) else 0,
                )
            )
        except ContentError as exc:
            entries.append(ContentInfo(path, relative, path.stem, "", "", 0, str(exc)))
    return entries
