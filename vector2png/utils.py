"""Helper utilities shared across converters."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Callable

from .exceptions import DependencyMissingError


def ensure_input_path(path: str | Path) -> Path:
    """Return a resolved path and ensure it exists."""
    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Input file not found: {resolved}")
    return resolved


def ensure_output_path(source: Path, target: str | Path | None) -> Path:
    """Derive the output path; default to source stem if not provided."""
    if target is None:
        output = source.with_suffix(".png")
    else:
        output = Path(target).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def optional_import(module: str, package: str | None = None, hint: str | None = None) -> Any:
    """Try importing a module and raise a descriptive error when missing."""
    try:
        return importlib.import_module(module)
    except ImportError as exc:  # pragma: no cover - simple helper
        pkg_name = package or module
        raise DependencyMissingError(pkg_name, hint) from exc


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp ``value`` to the inclusive ``[minimum, maximum]`` range."""
    return max(minimum, min(value, maximum))


def lazy_property(factory: Callable[[], Any]) -> property:
    """Return a cached property created from *factory*."""

    attr_name = f"_{factory.__name__}_cached"

    def getter(self: Any) -> Any:
        if not hasattr(self, attr_name):
            setattr(self, attr_name, factory(self))
        return getattr(self, attr_name)

    return property(getter)
