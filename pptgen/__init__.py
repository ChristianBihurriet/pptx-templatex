"""Local teaching-content adapter for pptx-templatex."""

from .adapter import adapt_content
from .generator import generate
from .themes import load_theme

__all__ = ["adapt_content", "generate", "load_theme"]
