"""Public API for the vector2png package."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .converters.ai import AIConverter
from .converters.dxf import DXFConverter
from .options import AIOptions, DXFOptions

__all__ = [
    "AIConverter",
    "DXFConverter",
    "AIOptions",
    "DXFOptions",
    "ai_to_png",
    "dxf_to_png",
    "__version__",
]

__version__ = "0.1.0"


def ai_to_png(
    source: str | Path,
    target: str | Path | None = None,
    options: Optional[AIOptions] = None,
) -> Path:
    """Convert an AI file to PNG using default converter settings."""
    return AIConverter().convert(source, target=target, options=options)


def dxf_to_png(
    source: str | Path,
    target: str | Path | None = None,
    options: Optional[DXFOptions] = None,
) -> Path:
    """Convert a DXF file to PNG using default converter settings."""
    return DXFConverter().convert(source, target=target, options=options)

