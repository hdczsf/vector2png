"""Dataclasses describing converter options."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


RgbColor = Tuple[int, int, int]


@dataclass(slots=True)
class AIOptions:
    """Options that control AI to PNG conversion."""

    dpi: int = 300
    transparent: bool = False
    background_color: Optional[RgbColor] = None
    prefer_method: str = "auto"
    fallback: bool = True
    timeout: int = 30


@dataclass(slots=True)
class DXFOptions:
    """Options that control DXF to PNG conversion."""

    dpi: int = 300
    page_width: float = 0
    page_height: float = 0
    margins: float = 20
    scale: float = 1.0
    max_width: Optional[float] = None
    max_height: Optional[float] = None
    background: str = "white"
    color_policy: str = "color"
    lineweight_scaling: float = 1.0
    layout_name: Optional[str] = None
    pdsize: Optional[float] = None
    normalize_relative_size: bool = False


__all__ = ["AIOptions", "DXFOptions", "RgbColor"]
